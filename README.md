# Desk Notes Search

Rank supplied personal-note excerpts using deterministic lexical relevance scores.

Uses Python 3.10+ and its standard library only. No package installation, virtual
environment, external service, or network access is required.

## Run

```console
python -m retrieval_tool --help
python -m retrieval_tool examples/sample.json
python -m retrieval_tool --check-fixtures fixtures/cases.jsonl
python generate_fixtures.py --count 20
python -m unittest discover -s tests -v
```

Run from this directory. The optional path defaults to `-`, which reads JSON from
stdin. Output is JSON or a fixture-check summary. Exit codes are 0 success,
1 file failure, and 2 invalid input. Examples and fixtures contain generated data.

Requires query, notes [{id,text}] (up to 200), and limit (1–50). ASCII letters/digits are lowercased into unique term sets. Score is the sum of 1/(document_frequency+1) for matching query terms divided by document unique-term count, rounded to six decimals. Zero matches are omitted and ties sort by ID. This is a documented custom lexical fallback, not embeddings, semantic search, or an LLM.

## Learning focus

User-directed personal AI/LLM/agent exploration. This is an independent concept exercise based on the modeled
roadmap. It makes no claim to be employer-owned or period-authentic production code.

## Structure

- `retrieval_tool/core.py`: validated parsing, storage, or state transitions.
- `retrieval_tool/cli.py`: JSON command interface.
- `retrieval_tool/generate_fixtures.py`: original deterministic validation cases.
- `retrieval_tool/fixture_check.py`: expected-output/error checks.
- `fixtures/cases.jsonl`: 294 generated cases, with explicit descriptions.
- `tests/`: independently selected boundaries and the complete corpus check.

Branches `feature/core`, `feature/cli`, `data/fixtures`, and `docs/usage` retain
snapshots; `main` contains the complete tool. Dates and provenance are also recorded
in TIMELINE.json. Many data cases share a scenario; they are not separate features.

Keep changes focused, use actual dates for new work, and add a regression test
for changed behavior. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
