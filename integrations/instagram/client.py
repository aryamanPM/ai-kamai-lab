from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class InstagramConfig:
    access_token: str
    user_id: str
    api_version: str

    @classmethod
    def from_env(cls) -> "InstagramConfig":
        values = {
            "access_token": os.getenv("INSTAGRAM_ACCESS_TOKEN", ""),
            "user_id": os.getenv("INSTAGRAM_USER_ID", ""),
            "api_version": os.getenv("INSTAGRAM_API_VERSION", ""),
        }
        missing = [key for key, value in values.items() if not value]
        if missing:
            raise RuntimeError(f"Missing Instagram configuration: {', '.join(missing)}")
        return cls(**values)


class InstagramPublisher:
    """Safe API boundary. Network calls are added only after Meta credentials are configured."""

    def __init__(self, config: InstagramConfig | None = None) -> None:
        self.config = config or InstagramConfig.from_env()

    def status(self) -> dict:
        return {"configured": True, "user_id": self.config.user_id, "api_version": self.config.api_version}

    def publish(self, media_url: str, caption: str) -> dict:
        if not media_url.startswith(("https://", "http://")):
            raise ValueError("media_url must be an HTTP(S) URL")
        if not caption.strip():
            raise ValueError("caption cannot be empty")
        raise NotImplementedError("Enable the supported Meta publishing flow after credentials are configured.")
