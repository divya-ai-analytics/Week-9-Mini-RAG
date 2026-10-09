# MP2 Reflection — complete after running the project

**Corpus used:** Ten original research-summary text documents based on my three papers about social-media depression and suicide-risk text analysis. The guidelines allow replacing Sherlock Holmes with our own text corpus. This is document retrieval research, not a clinical tool.

## What worked

**To fill in after I actually test the program:** Which source match succeeded? Give the question and the relevant filename/part. The design uses around 500-character chunks and retains the document filename and part in each Qdrant payload.

## What didn't work

**To fill in after testing:** Record an actual problem. For example, *only if observed*, note that a question retrieved the wrong section or that a sentence was split between chunks. Explain what you inspected or corrected.

## What I'd change

With more time, I would experiment with paragraph-aware chunking and compare retrieval source matches against the current 500-character overlapping chunks. I would keep the same golden questions for a fair comparison.

## One surprise

**To fill in after testing:** Record something genuinely surprising from your own execution: a retrieval match, an unexpected answer, a latency, or a model limitation. Do not invent a result.

## Validation output

Run `python mp2_rag.py validate` after ingesting, then paste the full real terminal output here or save it to `mp2_validation.txt`. The included `mp2_validation.txt` is a placeholder, not a claimed test result.
