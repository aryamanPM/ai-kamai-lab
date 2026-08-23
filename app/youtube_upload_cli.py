from __future__ import annotations

import argparse
from pathlib import Path

from .youtube_publisher import upload_video


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload one YouTube video.")
    parser.add_argument("video_file")
    parser.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    parser.add_argument("--title", default="AI Kamai Lab — Private Upload Test")
    parser.add_argument("--description", default="Private connectivity test for AI Kamai Lab YouTube automation.")
    parser.add_argument("--token-file", default="token.json")
    args = parser.parse_args()

    video = Path(args.video_file).expanduser().resolve()
    if not video.exists():
        raise SystemExit(f"Video file not found: {video}")

    video_id = upload_video(
        video_file=str(video),
        title=args.title,
        description=args.description,
        privacy_status=args.privacy,
        token_file=args.token_file,
    )
    print(f"Upload successful")
    print(f"Video ID: {video_id}")
    print(f"Privacy: {args.privacy}")


if __name__ == "__main__":
    main()
