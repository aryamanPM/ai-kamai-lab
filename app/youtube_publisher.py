"""YouTube publishing helpers. Publishing is explicit; no automatic upload is triggered by import."""
from __future__ import annotations

from pathlib import Path
from typing import Optional


def build_youtube_service(token_file: str = "token.json"):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    credentials = Credentials.from_authorized_user_file(
        str(Path(token_file).expanduser().resolve())
    )
    return build("youtube", "v3", credentials=credentials)


def upload_video(
    video_file: str,
    title: str,
    description: str,
    privacy_status: str = "private",
    category_id: str = "28",
    token_file: str = "token.json",
) -> str:
    """Upload a video and return its YouTube video ID.

    Default privacy is private to prevent accidental public publishing.
    """
    from googleapiclient.http import MediaFileUpload

    if privacy_status not in {"private", "unlisted", "public"}:
        raise ValueError("privacy_status must be private, unlisted, or public")

    service = build_youtube_service(token_file)
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category_id,
        },
        "status": {"privacyStatus": privacy_status},
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = service.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        _, response = request.next_chunk()

    return response["id"]
