from __future__ import annotations

from pathlib import Path

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
]


def verify(token_file: str = "token.json") -> None:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    token = Path(token_file).expanduser().resolve()
    if not token.exists():
        raise SystemExit(f"Token not found: {token}")

    credentials = Credentials.from_authorized_user_file(str(token), SCOPES)
    youtube = build("youtube", "v3", credentials=credentials)
    response = youtube.channels().list(part="snippet,statistics", mine=True).execute()
    channels = response.get("items", [])

    if not channels:
        raise SystemExit("OAuth succeeded, but no YouTube channel was returned for this account.")

    channel = channels[0]
    snippet = channel["snippet"]
    statistics = channel.get("statistics", {})
    print("YouTube API connection: OK")
    print(f"Channel name: {snippet.get('title')}")
    print(f"Channel ID: {channel.get('id')}")
    print(f"Subscribers: {statistics.get('subscriberCount', 'hidden')}")
    print(f"Videos: {statistics.get('videoCount', '0')}")


if __name__ == "__main__":
    verify()
