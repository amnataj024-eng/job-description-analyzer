# Job Description Analyzer (LangGraph)

Turns a job description into a structured hiring report using a 4-node LangGraph workflow.

## Workflow
User input -> validation -> Node 1 `extract_info` -> Node 2 `classify_job` -> Node 3 `rank_top_skills` -> Node 4 `generate_report` -> report

Shared state (`state.py`) carries the data between nodes; Pydantic models (`schemas.py`) define each node's output.

## Setup (Windows, VS Code terminal)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```
Open `.env` and paste your API key (Gemini or Groq, set `LLM_PROVIDER`).

## Run
```
streamlit run app.py          # web UI
python main.py sample_jd.txt  # command line
```

## Features
- 4 LangGraph nodes with state passing and early stop on errors
- Empty / too short / junk input handled with a friendly message
- Skills shown as tags, top 3 skills highlighted
- Export report as `hiring_report.json`

## Files
| File | Purpose |
|---|---|
| `app.py` | Streamlit UI |
| `graph.py` | LangGraph workflow + `run_analysis()` |
| `nodes.py` | The 4 nodes |
| `schemas.py` | Pydantic models |
| `state.py` | Shared graph state |
| `llm.py` | Gemini / Groq switch |
| `validation.py` | Input checks |
