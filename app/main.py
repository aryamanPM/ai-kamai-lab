from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state"
STATE_DIR.mkdir(exist_ok=True)
STATE_FILE = STATE_DIR / "tasks.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("ai-kamai-lab")


@dataclass
class Task:
    id: str
    agent: str
    action: str
    priority: int = 50
    status: str = "queued"
    retries: int = 0
    max_retries: int = 3
    output: dict | None = None
    error: str | None = None
    created_at: str = ""
    updated_at: str = ""


class TaskStore:
    def __init__(self, path: Path = STATE_FILE):
        self.path = path
        self.tasks: dict[str, Task] = {}
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            return
        raw = json.loads(self.path.read_text())
        self.tasks = {k: Task(**v) for k, v in raw.items()}

    def save(self) -> None:
        self.path.write_text(json.dumps({k: asdict(v) for k, v in self.tasks.items()}, indent=2))

    def add(self, task: Task) -> None:
        now = datetime.now(timezone.utc).isoformat()
        task.created_at = task.created_at or now
        task.updated_at = now
        self.tasks[task.id] = task
        self.save()


class AgentRegistry:
    def __init__(self):
        self.handlers: dict[str, Callable[[Task], dict]] = {}

    def register(self, name: str, handler: Callable[[Task], dict]) -> None:
        self.handlers[name] = handler

    def run(self, task: Task) -> dict:
        if task.agent not in self.handlers:
            raise RuntimeError(f"No handler registered for agent: {task.agent}")
        return self.handlers[task.agent](task)


def manager(task: Task) -> dict:
    return {"decision": "route", "next": task.action}


def researcher(task: Task) -> dict:
    return {"status": "research_adapter_ready", "action": task.action}


def strategist(task: Task) -> dict:
    return {"status": "strategy_adapter_ready", "action": task.action}


def copywriter(task: Task) -> dict:
    return {"status": "copy_adapter_ready", "action": task.action}


def qa(task: Task) -> dict:
    return {"approved": False, "reason": "Production QA requires generated media/content input."}


def build_registry() -> AgentRegistry:
    registry = AgentRegistry()
    for name, fn in {
        "manager": manager,
        "researcher": researcher,
        "strategist": strategist,
        "copywriter": copywriter,
        "qa": qa,
    }.items():
        registry.register(name, fn)
    return registry


def run_once(store: TaskStore, registry: AgentRegistry) -> None:
    queued = sorted(
        (t for t in store.tasks.values() if t.status == "queued"),
        key=lambda t: (-t.priority, t.created_at),
    )
    if not queued:
        log.info("No queued tasks")
        return

    task = queued[0]
    task.status = "running"
    task.updated_at = datetime.now(timezone.utc).isoformat()
    store.save()
    try:
        task.output = registry.run(task)
        task.status = "done"
        task.error = None
        log.info("Task %s completed", task.id)
    except Exception as exc:  # noqa: BLE001
        task.retries += 1
        task.error = str(exc)
        task.status = "queued" if task.retries < task.max_retries else "failed"
        log.exception("Task %s failed", task.id)
    finally:
        task.updated_at = datetime.now(timezone.utc).isoformat()
        store.save()


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Kamai Lab orchestration engine")
    parser.add_argument("--seed", action="store_true", help="seed a safe smoke-test task")
    args = parser.parse_args()

    store = TaskStore()
    registry = build_registry()
    if args.seed and "smoke-test" not in store.tasks:
        store.add(Task(id="smoke-test", agent="manager", action="health_check", priority=100))
    run_once(store, registry)


if __name__ == "__main__":
    main()
