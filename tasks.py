#!/usr/bin/env python3
import argparse
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT / "frontend"
DEFAULT_DATA = ROOT / "Database" / "data" / "database.json"


def choose_backend_python_command() -> list[str]:
    if shutil.which("uv"):
        return ["uv", "run", "python"]
    return [sys.executable]


def start_backend(args: argparse.Namespace) -> subprocess.Popen[bytes]:
    command = choose_backend_python_command() + [
        str(ROOT / "Database" / "slide_server.py"),
        "--data",
        str(args.data),
        "--host",
        args.backend_host,
        "--port",
        str(args.backend_port),
    ]
    return subprocess.Popen(command, cwd=ROOT)


def start_frontend(args: argparse.Namespace) -> subprocess.Popen[bytes]:
    env = os.environ.copy()
    env["VITE_API_URL"] = args.api_url or f"http://{args.backend_host}:{args.backend_port}"
    command = ["npm", "run", "dev", "--", "--host", args.frontend_host, "--port", str(args.frontend_port)]
    return subprocess.Popen(command, cwd=FRONTEND_DIR, env=env)


def run_backend(args: argparse.Namespace) -> int:
    process = start_backend(args)
    return process.wait()


def run_frontend(args: argparse.Namespace) -> int:
    process = start_frontend(args)
    return process.wait()


def terminate_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def run_dev(args: argparse.Namespace) -> int:
    backend = start_backend(args)
    frontend = start_frontend(args)
    processes = [backend, frontend]

    def shutdown(_signum: int, _frame) -> None:
        for process in processes:
            terminate_process(process)
        raise SystemExit(130)

    previous_sigint = signal.signal(signal.SIGINT, shutdown)
    previous_sigterm = signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            for process in processes:
                return_code = process.poll()
                if return_code is not None:
                    for other in processes:
                        if other is not process:
                            terminate_process(other)
                    return return_code
            time.sleep(0.5)
    finally:
        signal.signal(signal.SIGINT, previous_sigint)
        signal.signal(signal.SIGTERM, previous_sigterm)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Development tasks for the AI Slides project.")
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA,
        help="Path to the backend JSON database file.",
    )
    parser.add_argument("--backend-host", default="127.0.0.1", help="Host for the slide server.")
    parser.add_argument("--backend-port", type=int, default=8000, help="Port for the slide server.")
    parser.add_argument("--frontend-host", default="127.0.0.1", help="Host for the Vite dev server.")
    parser.add_argument("--frontend-port", type=int, default=5173, help="Port for the Vite dev server.")
    parser.add_argument(
        "--api-url",
        default=None,
        help="Override the frontend API URL. Defaults to the backend host/port.",
    )

    subparsers = parser.add_subparsers(dest="task", required=True)
    subparsers.add_parser("backend", help="Start only the FastAPI slide server.")
    subparsers.add_parser("frontend", help="Start only the Vite frontend.")
    subparsers.add_parser("dev", help="Start both backend and frontend.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.task == "backend":
        return run_backend(args)
    if args.task == "frontend":
        return run_frontend(args)
    if args.task == "dev":
        return run_dev(args)

    parser.error(f"Unknown task: {args.task}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
