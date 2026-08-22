from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List


class TaskStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


@dataclass
class Task:
    name: str
    agent: str
    priority: int = 50
    retries: int = 0
    max_retries: int = 2
    status: TaskStatus = TaskStatus.QUEUED
    output: str | None = None
    error: str | None = None


@dataclass
class Agent:
    name: str
    handler: Callable[[Task], str]


class Orchestrator:
    """Small dependency-free task orchestrator for the AI Kamai Lab MVP."""

    def __init__(self) -> None:
        self.agents: Dict[str, Agent] = {}
        self.queue: List[Task] = []

    def register(self, agent: Agent) -> None:
        self.agents[agent.name] = agent

    def submit(self, task: Task) -> None:
        if task.agent not in self.agents:
            raise ValueError(f"Unknown agent: {task.agent}")
        self.queue.append(task)
        self.queue.sort(key=lambda item: item.priority, reverse=True)

    def run_next(self) -> Task | None:
        if not self.queue:
            return None
        task = self.queue.pop(0)
        agent = self.agents[task.agent]
        task.status = TaskStatus.RUNNING
        try:
            task.output = agent.handler(task)
            task.status = TaskStatus.DONE
        except Exception as exc:  # noqa: BLE001
            task.error = str(exc)
            task.retries += 1
            if task.retries <= task.max_retries:
                task.status = TaskStatus.QUEUED
                self.submit(task)
            else:
                task.status = TaskStatus.FAILED
        return task

    def run_all(self) -> list[Task]:
        completed: list[Task] = []
        while self.queue:
            task = self.run_next()
            if task is not None:
                completed.append(task)
        return completed
