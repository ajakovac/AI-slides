import json
import argparse
import asyncio
import os
import time
from contextlib import asynccontextmanager
from typing import Any, Dict
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

import uvicorn
from fastapi.middleware.cors import CORSMiddleware


data_store: Dict[str, Any] = {}
system_store: Dict[str, Any] = {}
layout_store: Dict[str, Any] = {}
_data_lock = asyncio.Lock()

DATA_FILE = "data/database.json"
SYSTEM_FILE = "data/database_system.json"
LAYOUT_FILE = "data/database_layout.json"
POLL_SECONDS = 1.0

async def load_data() -> None:
    # Load main content data
    main_data = {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            main_data = json.load(f)
    except FileNotFoundError:
        print(f"Warning: {DATA_FILE} not found")
    except json.JSONDecodeError as e:
        print(f"Error loading {DATA_FILE}: {e}")

    # Load system data
    system_data = {}
    try:
        with open(SYSTEM_FILE, "r", encoding="utf-8") as f:
            system_data = json.load(f)
    except FileNotFoundError:
        print(f"Warning: {SYSTEM_FILE} not found")
    except json.JSONDecodeError as e:
        print(f"Error loading {SYSTEM_FILE}: {e}")

    # Load layout data
    layout_data = {}
    try:
        with open(LAYOUT_FILE, "r", encoding="utf-8") as f:
            layout_data = json.load(f)
    except FileNotFoundError:
        print(f"Warning: {LAYOUT_FILE} not found")
    except json.JSONDecodeError as e:
        print(f"Error loading {LAYOUT_FILE}: {e}")

    async with _data_lock:
        data_store.clear()
        data_store.update(main_data)
        system_store.clear()
        system_store.update(system_data)
        layout_store.clear()
        layout_store.update(layout_data)


async def hot_reload_loop(poll_seconds: float):
    last_mtimes = {}
    files_to_watch = [DATA_FILE, SYSTEM_FILE, LAYOUT_FILE]

    while True:
        try:
            changed = False
            for filename in files_to_watch:
                try:
                    mtime = os.path.getmtime(filename)
                    if filename not in last_mtimes:
                        last_mtimes[filename] = mtime
                    elif mtime != last_mtimes[filename]:
                        changed = True
                        last_mtimes[filename] = mtime
                except FileNotFoundError:
                    continue
            
            if changed:
                await load_data()
                print(f"[hot-reload] Reloaded at {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"[hot-reload] Error: {e}")

        await asyncio.sleep(poll_seconds)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup phase
    await load_data()
    task = asyncio.create_task(hot_reload_loop(POLL_SECONDS))

    yield  # App runs here

    # Shutdown phase
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev; in prod: set your real origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/item/{key}")
async def get_item(key: str):
    async with _data_lock:
        if key in data_store:
            return data_store[key]
        elif key in layout_store:
            return layout_store[key]
        else:
            raise HTTPException(status_code=404, detail="Key not found")

@app.get("/keys")
async def get_keys():
    async with _data_lock:
        return list(data_store.keys())

@app.get("/system")
async def get_system():
    async with _data_lock:
        return system_store

@app.get("/layout")
async def get_layout():
    async with _data_lock:
        return layout_store

# Directory where images live (relative to this file)
IMAGES_DIR = (Path(__file__).resolve().parent / "../Images").resolve()

@app.get("/image/{image_name}")
def get_image(image_name: str):
    # Basic path safety: forbid slashes/backslashes and ".."
    if "/" in image_name or "\\" in image_name or ".." in image_name:
        raise HTTPException(status_code=400, detail="Invalid image name")

    path = (IMAGES_DIR / image_name).resolve()

    # Ensure the resolved path is still inside IMAGES_DIR (prevents traversal)
    try:
        path.relative_to(IMAGES_DIR)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid image path")

    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")

    # FileResponse will set Content-Type based on filename extension
    return FileResponse(path)


@app.get("/image_show/{key}")
async def get_image(key: str):
    async with _data_lock:
        directory = Path("../Images")
        matching_files = list(directory.glob(f"{key}.*"))
        if not matching_files:
            raise HTTPException(status_code=404, detail="Image not found")
        if len(matching_files) > 1:
            raise HTTPException(status_code=500, detail="Multiple images found for key")
        return FileResponse(
            matching_files[0],
            media_type=None,  # let it infer (image/png, image/jpeg, etc.)
            filename=matching_files[0].name,
            headers={
                "Content-Disposition": f'inline; filename="{matching_files[0].name}"'
            }
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FastAPI dict server with hot reload")
    parser.add_argument("--data", type=str, default="data/database.json", help="Path to the JSON data file")
    parser.add_argument("--poll", type=float, default=1.0)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()

    DATA_FILE = args.data
    SYSTEM_FILE = args.data.replace('.json', '_system.json')
    LAYOUT_FILE = args.data.replace('.json', '_layout.json')
    POLL_SECONDS = args.poll

    uvicorn.run(app, host=args.host, port=args.port)
