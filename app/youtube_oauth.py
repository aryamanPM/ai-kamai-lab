"""Local one-time OAuth bootstrap for the AI Kamai Lab YouTube channel.

Never commit the downloaded Google OAuth client JSON or generated token file.
"""
from __future__ import annotations

import argparse
from pathlib import Path

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


def authorize(client_secret_file: str, token_file: str = "token.json") -> None:
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError as exc:
        raise SystemExit(
            "Install dependencies first: pip install -r requirements.txt"
        ) from exc

    client = Path(client_secret_file).expanduser().resolve()
    if not client.exists():
        raise SystemExit(f"OAuth client JSON not found: {client}")

    flow = InstalledAppFlow.from_client_secrets_file(str(client), SCOPES)
    credentials = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    Path(token_file).expanduser().write_text(credentials.to_json(), encoding="utf-8")
    print(f"OAuth complete. Token saved locally to {Path(token_file).resolve()}")
    print("Do not commit or upload this token file.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("client_secret_file")
    parser.add_argument("--token-file", default="token.json")
    args = parser.parse_args()
    authorize(args.client_secret_file, args.token_file)
