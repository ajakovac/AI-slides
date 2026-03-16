# AI Slides

This project builds a slide-style knowledge base from Markdown files, serves the generated database through a FastAPI backend, and displays it in a React frontend.

## Project Structure

- `Markdowns/`: source material written in Markdown
- `Database/sources.txt`: list of Markdown files to import into the database
- `Database/add_source.py`: builds or updates the JSON database from the source files
- `Database/data/database.json`: generated content database used by the server
- `Database/slide_server.py`: FastAPI slide server
- `frontend/`: Vite + React frontend
- `Images/`: images referenced from the Markdown files

## Installation

### Python backend

This repository uses Python `3.12+` and the dependencies listed in `pyproject.toml`.

If you use `uv`:

```bash
uv sync
```

If you prefer a standard virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Frontend

Install the frontend dependencies:

```bash
cd frontend
npm install
```

## Using the source list

The source list file is `Database/sources.txt`.

It contains the Markdown files that should be loaded from `Markdowns/`. Add one file name per line, for example:

```txt
content_of_the_AI_course.md
attention-and-transformers.md
reasoning.md
```

Notes:

- Use file names relative to `Markdowns/`.
- Blank lines are ignored.
- Lines starting with `#` are ignored.
- The file name is `sources.txt`, not `source.txt`.

## Building or Refreshing the Database

From the repository root, run:

```bash
uv run python Database/add_source.py --startnew --files Database/sources.txt --database Database/data/database.json
```

If you are using a virtual environment instead of `uv`, run:

```bash
python Database/add_source.py --startnew --files Database/sources.txt --database Database/data/database.json
```

What this does:

- reads the Markdown files listed in `Database/sources.txt`
- loads them from `Markdowns/`
- writes the generated result to `Database/data/database.json`

If you only want to update existing content without forcing a fresh database, remove `--startnew`.

## Starting the Slide Server

Start the FastAPI backend from the repository root:

```bash
uv run python Database/slide_server.py --data Database/data/database.json --host 127.0.0.1 --port 8000
```

Without `uv`:

```bash
python Database/slide_server.py --data Database/data/database.json --host 127.0.0.1 --port 8000
```

The backend will then be available at:

```txt
http://127.0.0.1:8000
```

The server watches the JSON file and hot-reloads when `Database/data/database.json` changes.

## Starting the Frontend

The frontend expects the backend to be running on port `8000`.

From the `frontend/` directory:

```bash
VITE_API_URL=http://127.0.0.1:8000 npm run dev
```

Vite will print the local frontend URL, typically:

```txt
http://127.0.0.1:5173
```

## Typical Local Workflow

1. Install Python and frontend dependencies.
2. Update `Database/sources.txt` with the Markdown files you want to include.
3. Rebuild the database:

```bash
uv run python Database/add_source.py --startnew --files Database/sources.txt --database Database/data/database.json
```

4. Start the backend:

```bash
uv run python Database/slide_server.py --data Database/data/database.json --host 127.0.0.1 --port 8000
```

5. In a second terminal, start the frontend:

```bash
cd frontend
VITE_API_URL=http://127.0.0.1:8000 npm run dev
```

## Troubleshooting

- If the frontend is empty, first check that `Database/data/database.json` exists and the backend is running.
- If content is missing, verify that the Markdown file is listed in `Database/sources.txt`.
- If image loading fails, keep the backend on `http://localhost:8000` or `http://127.0.0.1:8000`, because image requests are currently hardcoded to port `8000` in the frontend.
