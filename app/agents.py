from .core import Agent, Task


def _result(label: str):
    def handler(task: Task) -> str:
        return f"{label}: {task.name}"
    return handler


def register_default_agents(orchestrator) -> None:
    handlers = {
        "manager": "Orchestration",
        "researcher": "Trend research",
        "strategist": "Content strategy",
        "copywriter": "Script/copy generation",
        "qa": "Quality assurance",
        "analytics": "Performance analysis",
        "learning": "Learning-loop update",
    }
    for name, label in handlers.items():
        orchestrator.register(Agent(name=name, handler=_result(label)))
