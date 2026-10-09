"""Week 9 Mini-RAG: ask questions about my 10 research summary documents.

Built using the required OpenAI and Qdrant libraries, without RAG frameworks.
Commands: python mp2_rag.py ingest | ask | validate
"""
import json
import os
import sys
import time
from pathlib import Path
from uuid import uuid4

from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_BASE_URL"]
)
from qdrant_client import QdrantClient, models
BASE = Path(__file__).parent
CORPUS_DIR = BASE / "corpus"
DATA_DIR = BASE / "data"
COLLECTION = "mp2_mental_health_research"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
DIMENSIONS = 1536
CHUNK_SIZE = 500
OVERLAP = 80

# Clients are created only when needed, making simple local tests possible.
def openai_client():
    return OpenAI()


def qdrant_client():
    return QdrantClient(url=os.environ["QDRANT_URL"],
                        api_key=os.environ.get("QDRANT_API_KEY") or None)


# 1. Read the .txt documents and keep their original filenames.
def load_corpus(folder):
    documents = []
    for file in sorted(Path(folder).glob("*.txt")):
        text = file.read_text(encoding="utf-8").strip()
        if text:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            # Each file starts with DOCUMENT xx / 10, then the topic title.
            title = lines[1] if len(lines) > 1 else lines[0]
            documents.append({"source": file.name, "title": title, "text": text})
    return documents


# 2. Split text into ~500-character chunks with 80-character overlap.
def chunk_document(doc):
    text = doc["text"]
    result = []
    start = 0
    part = 1
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        # Try to end at a space rather than the middle of a word.
        if end < len(text):
            space = text.rfind(" ", start + CHUNK_SIZE // 2, end)
            if space > start:
                end = space + 1
        content = text[start:end].strip()
        if content:
            result.append({"source": doc["source"], "title": doc["title"],
                           "section": "Part " + str(part), "text": content})
            part += 1
        if end == len(text):
            break
        start = max(start + 1, end - OVERLAP)
    return result


# 3. Create vector representations using OpenAI in small batches.
def embed_texts(texts):
    if not texts:
        return []
    client = openai_client()
    vectors = []
    for i in range(0, len(texts), 32):
        batch = texts[i:i + 32]
        reply = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        vectors.extend([item.embedding for item in sorted(reply.data, key=lambda x: x.index)])
    return vectors


# 4. Reset Qdrant collection when ingesting a new corpus.
def setup_collection():
    db = qdrant_client()
    if db.collection_exists(COLLECTION):
        db.delete_collection(COLLECTION)
    db.create_collection(collection_name=COLLECTION,
                         vectors_config=models.VectorParams(size=DIMENSIONS,
                                                             distance=models.Distance.COSINE))


# 5. Store chunks along with their filenames and section numbers.
def ingest_chunks(chunks):
    db = qdrant_client()
    for start in range(0, len(chunks), 32):
        group = chunks[start:start + 32]
        vectors = embed_texts([c["text"] for c in group])
        points = [models.PointStruct(id=str(uuid4()), vector=vector, payload=chunk)
                  for chunk, vector in zip(group, vectors)]
        db.upsert(collection_name=COLLECTION, points=points, wait=True)


# 6. Search Qdrant for relevant passages.
def retrieve(question, k=3):
    db = qdrant_client()
    vector = embed_texts([question])[0]
    found = db.query_points(collection_name=COLLECTION,
                            query=vector, limit=k, with_payload=True).points
    return [dict(point.payload, score=point.score) for point in found]


SYSTEM_PROMPT = ("Answer only from the supplied research-document excerpts. "
                 "Do not make up facts or claim that text classification is a medical diagnosis. "
                 "If the evidence is missing, say you cannot find it. "
                 "Cite the document title and part in the answer, e.g. "
                 "[Source: Document Title — Part 2].")


# 7. Build grounded answer with source citations.
def answer(question, k=3):
    began = time.time()
    passages = retrieve(question, k=k)
    context = "\n\n".join(
        "[Source: " + p["title"] + " — " + p["section"] + "]\n" + p["text"]
        for p in passages)
    user_prompt = "Evidence:\n" + context + "\n\nQuestion: " + question
    response = openai_client().chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": user_prompt}],
        temperature=0)
    return {"question": question,
            "answer": response.choices[0].message.content or "",
            "citations": [{"source": p["source"], "title": p["title"],
                           "section": p["section"], "score": p["score"]}
                          for p in passages],
            "latency_ms": round((time.time() - began) * 1000)}


def validate_against(file):
    questions = [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()
                 if line.strip()]
    hits = 0
    print("\nValidating", len(questions), "questions from", file.name)
    for item in questions:
        result = answer(item["question"])
        sources = {p["source"] for p in result["citations"]}
        match = item["expected_source"] in sources
        hits += int(match)
        facts = sum(f.lower() in result["answer"].lower()
                    for f in item.get("expected_facts", []))
        print(("PASS" if match else "CHECK"), item["id"])
        print(" Question:", item["question"])
        print(" Answer:", result["answer"])
        print(" Retrieved sources:", ", ".join(sorted(sources)))
        print(" Expected source:", item["expected_source"])
        print(" Expected phrases:", facts, "/", len(item.get("expected_facts", [])))
        print(" Time:", result["latency_ms"], "ms\n")
    print("Source-match:", str(hits) + "/" + str(len(questions)))
    return hits


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("ingest", "ask", "validate"):
        print("Usage: python mp2_rag.py [ingest|ask|validate]")
        return
    action = sys.argv[1]
    if action == "ingest":
        docs = load_corpus(CORPUS_DIR)
        if not docs:
            print("No text files found in corpus/")
            return
        chunks = []
        for doc in docs:
            pieces = chunk_document(doc)
            print(doc["source"], "->", len(pieces), "chunks")
            chunks.extend(pieces)
        setup_collection()
        ingest_chunks(chunks)
        print("Ingested", len(chunks), "chunks from", len(docs), "documents")
    elif action == "ask":
        print("Ask about the social media mental-health research papers.")
        while True:
            try:
                question = input("Question (blank to finish): ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not question:
                break
            result = answer(question)
            print("\n" + result["answer"])
            print("Retrieved:", ", ".join(c["source"] for c in result["citations"]))
    else:
        validate_against(DATA_DIR / "predefined_questions.jsonl")
        validate_against(DATA_DIR / "learner_questions.jsonl")


if __name__ == "__main__":
    main()
