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
_data_lock = asyncio.Lock()

DATA_FILE = "data.json"
POLL_SECONDS = 1.0


async def load_data(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        new_data = json.load(f)

    if not isinstance(new_data, dict):
        raise ValueError("Top-level JSON must be an object/dict.")

    async with _data_lock:
        data_store.clear()
        data_store.update(new_data)


async def hot_reload_loop(filename: str, poll_seconds: float):
    last_mtime = None

    while True:
        try:
            mtime = os.path.getmtime(filename)
            if last_mtime is None:
                last_mtime = mtime

            if mtime != last_mtime:
                await load_data(filename)
                last_mtime = mtime
                print(f"[hot-reload] Reloaded at {time.strftime('%H:%M:%S')}")
        except json.JSONDecodeError as e:
            print(f"[hot-reload] JSON error: {e}")
        except Exception as e:
            print(f"[hot-reload] Error: {e}")

        await asyncio.sleep(poll_seconds)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup phase
    await load_data(DATA_FILE)
    task = asyncio.create_task(hot_reload_loop(DATA_FILE, POLL_SECONDS))

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
        if key not in data_store:
            raise HTTPException(status_code=404, detail="Key not found")
        return data_store[key]

@app.get("/keys")
async def get_keys():
    async with _data_lock:
        return list(data_store.keys())

@app.get("/image/{key}")
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
    POLL_SECONDS = args.poll

    uvicorn.run(app, host=args.host, port=args.port)
