from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class WorkerCommand:
    name: str
    description: str
    command: tuple[str, ...]


WORKERS: dict[str, WorkerCommand] = {
    "1": WorkerCommand(
        name="notification",
        description="Messaging, notifications, conversations, rendered email delivery",
        command=("uv", "run", "arq", "workers.notification_worker.worker.WorkerSettings"),
    ),
    "2": WorkerCommand(
        name="system",
        description="System maintenance and worker orchestration",
        command=("uv", "run", "arq", "workers.system_worker.worker.WorkerSettings"),
    ),
    "3": WorkerCommand(
        name="translator_formatter",
        description="Future translation and formatting jobs",
        command=("uv", "run", "arq", "workers.translator_formatter_worker.worker.WorkerSettings"),
    ),
}


def print_commands() -> None:
    print()
    print("Available local worker commands:")
    for key, worker in WORKERS.items():
        print(f"  {key}. {worker.name}: {' '.join(worker.command)}")
    print()


def run_worker(worker: WorkerCommand) -> int:
    print()
    print(f"Starting {worker.name} worker")
    print(f"Command: {' '.join(worker.command)}")
    print("Stop with Ctrl+C.")
    print()
    try:
        completed = subprocess.run(worker.command, cwd=PROJECT_ROOT, check=False)
    except KeyboardInterrupt:
        return 130
    return int(completed.returncode)


def choose_worker() -> WorkerCommand | None:
    while True:
        print()
        print("Atlas local worker launcher")
        print(f"Project: {PROJECT_ROOT}")
        print()
        for key, worker in WORKERS.items():
            print(f"{key}. Start {worker.name} worker")
            print(f"   {worker.description}")
        print("4. Show commands")
        print("0. Exit")
        print()

        choice = input("Select: ").strip()
        if choice == "0":
            return None
        if choice == "4":
            print_commands()
            continue
        worker = WORKERS.get(choice)
        if worker:
            return worker
        print(f"Unknown option: {choice}")


def main() -> int:
    if "--list" in sys.argv:
        print_commands()
        return 0

    worker = choose_worker()
    if worker is None:
        return 0
    return run_worker(worker)


if __name__ == "__main__":
    raise SystemExit(main())
