# todoreels-py

A small Python service that checks a reel script for **invented figures**.

It is part of TODOreels, a project that creates Instagram reels with AI. The main pipeline runs on LangGraph in TypeScript; this service is the first piece ported to Python.

## Why it exists

An LLM editor scores a script "by eye" and can miss a made-up number, like *"90 out of every 100 people disappeared"* when the research never says that.

This service does an exact check instead: every figure in the script must appear in the facts of the research brief. No LLM is involved, so the result is deterministic and free.

## How it works

- `extract_figures` pulls all numbers out of a text and normalizes them (`10.000` becomes `10000`, `3,5` becomes `3.5`).
- `find_unsupported_figures` returns the figures that are in the script but not in the brief.
- Pydantic models (`ReelScript`, `BriefSchema`) validate the data. They read and write the same camelCase JSON as the TypeScript side.
- FastAPI exposes it as `POST /check-figures`.

Example response for a script that invents a "90":

```json
{ "unsupportedFigures": ["90"] }
```

A request with invalid data (for example `certainty: 0.9` instead of `"high"`) is rejected with a `422` before any code runs.

## Run it

```bash
uv sync
uv run fastapi dev src/todoreels_py/api.py
```

Then open http://127.0.0.1:8000/docs to try the API in the browser.

## Test it

```bash
uv run pytest
```

## Stack

Python 3.13 · uv · FastAPI · Pydantic · pytest
