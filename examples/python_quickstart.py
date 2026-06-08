"""
Instagram Cheapest API - Python Quickstart

Install: pip install requests
Run:     export RAPIDAPI_KEY='your-key-here' && python python_quickstart.py

Docs: https://rapidapi.com/liucccccccccccc/api/instagram-cheapest
"""

import os
import sys
import json
import requests
from typing import Optional, Dict, Any


class InstagramCheapest:
    """Client for Instagram Cheapest API on RapidAPI."""

    BASE_URL = "https://instagram-cheapest.p.rapidapi.com/api/v1/instagram"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("RAPIDAPI_KEY")
        if not self.api_key:
            raise ValueError(
                "RAPIDAPI_KEY not found. Set it via environment variable or pass to constructor."
            )
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "instagram-cheapest.p.rapidapi.com"
        }
        self.timeout = 30  # seconds

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Internal GET request helper with error handling."""
        url = f"{self.BASE_URL}{path}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}", file=sys.stderr)
            raise

    def userinfo(self, username: str, fields: Optional[str] = None) -> Dict[str, Any]:
        """Get user profile by username."""
        params = {"fields": fields} if fields else None
        return self._get(f"/user/{username}", params=params)

    def userinfo_by_user_id(self, user_id: str, fields: Optional[str] = None) -> Dict[str, Any]:
        """Get user profile by numeric user ID."""
        params = {"user_id": user_id}
        if fields:
            params["fields"] = fields
        return self._get("/user_by_user_id", params=params)

    def username_by_uid(self, uid: str) -> Dict[str, Any]:
        """Get username for a numeric UID."""
        return self._get("/username_by_uid", params={"uid": uid})

    def user_media(self, user_id: str, fields: Optional[str] = None) -> Dict[str, Any]:
        """Get user's media posts."""
        params = {"user_id": user_id}
        if fields:
            params["fields"] = fields
        return self._get("/user_media", params=params)

    def user_reels(self, user_id: str, fields: Optional[str] = None) -> Dict[str, Any]:
        """Get user's Reels."""
        params = {"user_id": user_id}
        if fields:
            params["fields"] = fields
        return self._get("/user_reels", params=params)

    def user_tag_media(self, user_id: str, fields: Optional[str] = None) -> Dict[str, Any]:
        """Get media the user is tagged in."""
        params = {"user_id": user_id}
        if fields:
            params["fields"] = fields
        return self._get("/user_tag_media", params=params)

    def media_by_code2(self, code: str, fields: Optional[str] = None) -> Dict[str, Any]:
        """Get single media item by shortcode."""
        params = {"code": code}
        if fields:
            params["fields"] = fields
        return self._get("/media_by_code2", params=params)

    def media_comments(self, code: str, fields: Optional[str] = None) -> Dict[str, Any]:
        """Get comments for a media shortcode."""
        params = {"code": code}
        if fields:
            params["fields"] = fields
        return self._get("/media_comments", params=params)

    def reels_audio(self, audio_id: str, fields: Optional[str] = None) -> Dict[str, Any]:
        """Get Reels that use a specific audio track."""
        params = {"audio_id": audio_id}
        if fields:
            params["fields"] = fields
        return self._get("/reels_audio", params=params)


if __name__ == "__main__":
    # Initialize client (reads RAPIDAPI_KEY from environment)
    client = InstagramCheapest()

    print("=== Example 1: Get user profile by username ===")
    user = client.userinfo("nike")
    print(json.dumps(user, indent=2))
    print()

    print("=== Example 2: Get user profile with 'fields' parameter (reduced bandwidth) ===")
    # Only request specific fields to minimize response size and bandwidth costs
    user_slim = client.userinfo("nike", fields="username,full_name,follower_count")
    print(json.dumps(user_slim, indent=2))
    print()

    print("=== Example 3: Get username by UID ===")
    username_data = client.username_by_uid("25025320")
    print(json.dumps(username_data, indent=2))
