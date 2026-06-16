#!/usr/bin/env python3
"""Download public Instagram photos & videos via the Instagram Cheapest API.

Setup:
    pip install requests
    export RAPIDAPI_KEY='your-key'      # from https://rapidapi.com/liucccccccccccc/api/instagram-cheapest

Usage:
    python3 download_media.py Cabc123XYz                 # one post / Reel by shortcode
    python3 download_media.py @nike                      # a whole profile
    python3 download_media.py @nike --pages 5            # more pages of the profile
    python3 download_media.py https://www.instagram.com/p/Cabc123XYz/   # a pasted URL works too

Files are saved into ./downloads/. Note: Instagram CDN links are signed and
expire quickly, so this fetches the JSON and downloads immediately.
"""
import os
import sys
import json
import time
import argparse
import requests

HOST = "instagram-cheapest.p.rapidapi.com"
BASE_URL = f"https://{HOST}/api/v1/instagram"
API_KEY = os.environ.get("RAPIDAPI_KEY", "")
HEADERS = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}


def get(path, params=None):
    """GET against the API (returns raw Instagram JSON)."""
    resp = requests.get(f"{BASE_URL}/{path}", headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def find_media(node, found=None):
    """Recursively collect best-resolution image/video URLs from the JSON.

    Handles single photos, videos/Reels, and carousels alike. If Instagram ever
    changes its response shape, print the JSON and verify these keys.
    """
    if found is None:
        found = []
    if isinstance(node, dict):
        videos = node.get("video_versions")
        if isinstance(videos, list) and videos:
            best = max(videos, key=lambda v: v.get("width", 0) or 0)
            if best.get("url"):
                found.append({"type": "video", "url": best["url"]})
        iv = node.get("image_versions2")
        if isinstance(iv, dict):
            candidates = iv.get("candidates") or []
            # Skip the poster image that videos also carry.
            if candidates and not (isinstance(videos, list) and videos):
                best = max(candidates, key=lambda c: c.get("width", 0) or 0)
                if best.get("url"):
                    found.append({"type": "photo", "url": best["url"]})
        for value in node.values():
            find_media(value, found)
    elif isinstance(node, list):
        for item in node:
            find_media(item, found)
    return found


def download_media(media, out_dir="downloads", prefix="ig"):
    """Stream each CDN URL to disk. No API key needed — these are public CDN links."""
    os.makedirs(out_dir, exist_ok=True)
    saved = []
    for i, m in enumerate(media):
        ext = "mp4" if m["type"] == "video" else "jpg"
        path = os.path.join(out_dir, f"{prefix}_{i}.{ext}")
        with requests.get(m["url"], timeout=60, stream=True) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"  saved {path}")
        saved.append(path)
    return saved


def download_post(code):
    print(f"Fetching post {code} ...")
    post = get("media_by_code2", params={"code": code})
    media = find_media(post)
    print(f"Found {len(media)} media file(s)")
    return download_media(media, prefix=code)


def download_profile(username, max_pages=3):
    profile = get(f"user/{username}")
    user_id = profile.get("id") or profile.get("pk")
    if not user_id:
        print("Could not find user_id. Raw profile (first 1 KB):")
        print(json.dumps(profile, indent=2)[:1000])
        return []
    print(f"{username} -> user_id {user_id}")
    saved, next_max_id, page = [], None, 0
    while page < max_pages:
        params = {"user_id": user_id}
        if next_max_id:
            params["next_max_id"] = next_max_id
        resp = get("user_media", params=params)
        media = find_media(resp)
        print(f"Page {page + 1}: {len(media)} media file(s)")
        saved += download_media(media, out_dir=f"downloads/{username}",
                                prefix=f"{username}_p{page}")
        if not resp.get("more_available"):
            break
        next_max_id = resp.get("next_max_id")
        if not next_max_id:
            break
        page += 1
        time.sleep(1)  # stay under the free tier's ~1 req/sec
    return saved


def parse_target(target):
    """Return ('post', shortcode) or ('profile', username) from any input."""
    t = target.strip().rstrip("/")
    if "instagram.com" in t:
        parts = [p for p in t.split("/") if p]
        for kw in ("p", "reel", "reels", "tv"):
            if kw in parts:
                return "post", parts[parts.index(kw) + 1]
        return "profile", parts[-1].lstrip("@")
    if t.startswith("@"):
        return "profile", t[1:]
    return "post", t


def main():
    parser = argparse.ArgumentParser(description="Download public Instagram media.")
    parser.add_argument("target", help="a shortcode, @username, or full instagram.com URL")
    parser.add_argument("--pages", type=int, default=3,
                        help="max pages when downloading a profile (default 3)")
    args = parser.parse_args()

    if not API_KEY:
        sys.exit("Set RAPIDAPI_KEY first:  export RAPIDAPI_KEY='your-key'")

    kind, value = parse_target(args.target)
    if kind == "profile":
        download_profile(value, max_pages=args.pages)
    else:
        download_post(value)


if __name__ == "__main__":
    main()
