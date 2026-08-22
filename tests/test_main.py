import json
import tempfile
from pathlib import Path

from app.main import AgentRegistry, Task, TaskStore, build_registry, run_once


def test_manager_task_runs():
    with tempfile.TemporaryDirectory() as tmp:
        store = TaskStore(Path(tmp) / "tasks.json")
        store.add(Task(id="t1", agent="manager", action="health_check", priority=100))
        run_once(store, build_registry())
        assert store.tasks["t1"].status == "done"
        assert store.tasks["t1"].output["decision"] == "route"


def test_unknown_agent_retries_then_fails():
    with tempfile.TemporaryDirectory() as tmp:
        store = TaskStore(Path(tmp) / "tasks.json")
        store.add(Task(id="t2", agent="missing", action="x", max_retries=1))
        run_once(store, build_registry())
        assert store.tasks["t2"].status == "failed"
        assert store.tasks["t2"].retries == 1


def test_state_is_json_persisted():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "tasks.json"
        store = TaskStore(path)
        store.add(Task(id="t3", agent="manager", action="x"))
        assert json.loads(path.read_text())["t3"]["status"] == "queued"
