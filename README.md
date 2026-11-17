# AI Engineering Roadmap

A hands-on learning repository for AI engineering. It collects the code, experiments and notes I build while working through the skills needed to ship LLM-powered applications: configuration and secrets handling, calling LLM APIs, testing, and tooling.

## Tech stack

- **Python 3.13+**
- **[uv](https://docs.astral.sh/uv/)**: manages the project, its dependencies and its virtual environment
- **[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)**: loads and validates settings from `.env`
- **[pytest](https://docs.pytest.org/)**: runs the tests
- **[Ruff](https://docs.astral.sh/ruff/)**: lints and formats the code

## Project structure

```
AI-EngineeringRoadMap/
├── src/
│   └── ai_engineeringroadmap/
│       ├── __init__.py          # package entry point (main)
│       ├── config/
│       │   └── setings.py       # Settings class, loaded from .env
│       └── tests/
│           └── test_config.py   # tests for settings validation
├── .env                         # local environment variables (not committed)
├── pyproject.toml               # project metadata and dependencies
└── README.md
```

## Getting started

### 1. Install uv

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install dependencies

```powershell
uv sync
```

This creates `.venv` and installs everything listed in `pyproject.toml`.

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
LLM_API_KEY=your-api-key-here
LLM_BASE_URL=https://api.example.com/v1
LOG_LEVEL=INFO
```

| Variable       | Required | Description                                       |
| -------------- | -------- | ------------------------------------------------- |
| `LLM_API_KEY`  | Yes      | API key for the LLM provider                      |
| `LLM_BASE_URL` | Yes      | Base URL of the LLM API                           |
| `LOG_LEVEL`    | No       | Logging level (`DEBUG`, `INFO`, ...). Default: `INFO` |

> Never commit `.env`. Add it to `.gitignore`.

## Usage

Run the app:

```powershell
uv run ai-engineeringroadmap
```

Run the tests:

```powershell
uv run pytest -v
```

Lint and format:

```powershell
uv run ruff check --fix
uv run ruff format
```

> `uv run` executes commands inside the project's virtual environment, so you don't need to activate `.venv` first.

## Roadmap

- [x] Project setup with uv
- [x] Settings and secrets management with pydantic-settings
- [x] Unit tests with pytest
- [x] Linting and formatting with Ruff
- [ ] Calling LLM APIs (chat completions, streaming)
- [ ] Prompt engineering and structured outputs
- [ ] Embeddings and vector search
- [ ] Retrieval-augmented generation (RAG)
- [ ] Tool use and agents
- [ ] Evaluation and observability
- [ ] Deployment
