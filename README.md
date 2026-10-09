# IIT Madras Week 9 — Mini-RAG: Ask My Research Documents

This is a small, beginner-friendly RAG assignment adapted from the Week 9 starter. It uses **10 text documents based on three research papers**, instead of Sherlock Holmes. The course handout specifically allows a personal `.txt` corpus with replacement questions.

## Project folders
- `mp2_rag.py`: the seven RAG steps (loading, chunking, embedding, setting up Qdrant, ingesting, retrieval, answering) and basic commands.
- `corpus/`: 10 research summary files (.txt).
- `data/predefined_questions.jsonl`: **2 replacement** predefined-style questions. The original Sherlock-specific questions are inapplicable to the research documents.
- `data/learner_questions.jsonl`: **3 questions** at easy, medium, and hard levels.
- `data/optional_golden_set_10.json`: additional reference questions, not required by MP2.
- `mp2_reflection.md`: four required sections, with personal test observations still to complete.
- `mp2_validation.txt`: placeholder pending actual live testing.

## Requirements
Python 3.10 or later, OpenAI API key (billing enabled), and a Qdrant Cloud collection URL and API key. API calls cost money. Don't commit keys to GitHub.

## Run in terminal (Linux, macOS, Vocareum)
```bash
cd learner
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your real keys, then:
source .env
python mp2_rag.py ingest
python mp2_rag.py ask
python mp2_rag.py validate | tee mp2_validation.txt
```

**If your terminal is already inside `learner/`, do not run `cd learner` again.**

## Windows PowerShell alternative
```powershell
cd learner
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
For PowerShell, do **not** run `source .env`. Instead, set `$env:OPENAI_API_KEY`, `$env:QDRANT_URL`, `$env:QDRANT_API_KEY` in the current shell (or use a `.env` parser and adjust startup code). Then run the same Python commands.

## How it works
1. Read each research file, including its filename and title.
2. Split into ~500 character passages with 80 character overlaps and `Part N` labels.
3. Embed each passage using `text-embedding-3-small` (1536 dimensions).
4. Add passages and filename/part metadata to Qdrant using cosine similarity.
5. For each question, retrieve the top 3 matching passages.
6. Answer using `gpt-4o-mini` and cite the title/part. If facts are missing, say so.
7. `validate` checks whether the expected source filename appeared in retrieved top-3 results and counts basic expected answer phrases. **Source-match is not the same as answer correctness.**

## Before submission
- Run `ingest`, `ask` and `validate` with valid credentials.
- Inspect all five answers and ensure any errors are documented.
- Paste the actual validation output into `mp2_validation.txt` (or the reflection).
- Replace reflection prompts with your own observed findings.
- Add your personal work, make sure you understand the script, and follow your institute's academic-integrity/AI-use rules.
- Create **your own separate GitHub repository**, exclude `.env`, and submit its URL.

## Testing limits
Only offline syntax/data/logic checks can be done without your credentials. No OpenAI answer or Qdrant retrieval is claimed to have been tested against a live cloud service.
