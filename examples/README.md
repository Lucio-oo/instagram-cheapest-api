# Instagram Cheapest API - Code Examples

Copy-paste, runnable code examples for the [Instagram Cheapest API](https://rapidapi.com/liucccccccccccc/api/instagram-cheapest) on RapidAPI.

## Prerequisites

1. **Get your API key** from [RapidAPI](https://rapidapi.com/liucccccccccccc/api/instagram-cheapest)
   - Sign up / log in to RapidAPI
   - Subscribe to a plan (free tier: 30 requests/month)
   - Copy your API key from the dashboard

2. **Set the environment variable**:
   ```bash
   export RAPIDAPI_KEY='your-api-key-here'
   ```

## Available Endpoints

All endpoints are `GET` requests. The API returns real-time, uncached JSON.

| # | Endpoint | Description | Required Parameter |
|---|----------|-------------|-------------------|
| 1 | `userinfo` | Get user profile by username | `username` (path param) |
| 2 | `userinfo_by_user_id` | Get user profile by numeric ID | `user_id` (query param) |
| 3 | `username_by_uid` | Get username for a numeric UID | `uid` (query param) |
| 4 | `user_media` | Get user's media posts | `user_id` (query param) |
| 5 | `user_reels` | Get user's Reels | `user_id` (query param) |
| 6 | `user_tag_media` | Get media user is tagged in | `user_id` (query param) |
| 7 | `media_by_code2` | Get single media item by shortcode | `code` (query param) |
| 8 | `media_comments` | Get comments for a media shortcode | `code` (query param) |
| 9 | `reels_audio` | Get Reels using a specific audio track | `audio_id` (query param) |

**Optional parameter**: `fields` — reduce bandwidth by requesting only specific JSON fields (e.g., `fields=username,full_name,follower_count`).

## Examples by Language

### Bash / curl

```bash
chmod +x curl.sh
export RAPIDAPI_KEY='your-api-key-here'
./curl.sh
```

The script demonstrates all 9 endpoints plus a `fields` example.

### Python

**Requirements**: Python 3.7+, `requests` library

```bash
pip install requests
export RAPIDAPI_KEY='your-api-key-here'
python python_quickstart.py
```

Provides a clean `InstagramCheapest` client class with methods for all endpoints.

### Node.js

**Requirements**: Node.js 18+ (uses built-in `fetch`)

```bash
export RAPIDAPI_KEY='your-api-key-here'
node node_quickstart.js
```

ES6 class-based client with async/await.

### PHP

**Requirements**: PHP 7.4+ with cURL extension

```bash
export RAPIDAPI_KEY='your-api-key-here'
php php_quickstart.php
```

Object-oriented client using cURL.

### Go

**Requirements**: Go 1.18+

```bash
export RAPIDAPI_KEY='your-api-key-here'
go run go_quickstart.go
```

Idiomatic Go client with proper error handling.

## API Details

- **Base URL**: `https://instagram-cheapest.p.rapidapi.com/api/v1/instagram`
- **Authentication**: Include these headers on every request:
  - `x-rapidapi-key: YOUR_API_KEY`
  - `x-rapidapi-host: instagram-cheapest.p.rapidapi.com`
- **Method**: All endpoints use `GET`
- **Response format**: Raw JSON (real-time, no cache)

## Pricing

From **$0.10 per 1,000 requests** on the Mega tier. Free tier includes 30 requests/month.

See full pricing at: https://rapidapi.com/liucccccccccccc/api/instagram-cheapest/pricing

## Bandwidth Optimization

Use the `fields` parameter to request only the data you need:

```bash
# Full response (all fields)
curl "https://instagram-cheapest.p.rapidapi.com/api/v1/instagram/user/nike" \
  -H "x-rapidapi-key: YOUR_KEY" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"

# Slim response (specific fields only)
curl "https://instagram-cheapest.p.rapidapi.com/api/v1/instagram/user/nike?fields=username,full_name,follower_count" \
  -H "x-rapidapi-key: YOUR_KEY" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
```

This reduces response size and bandwidth costs (10 GB/month included, then $0.001/MB).

## Support

- **API Documentation**: https://rapidapi.com/liucccccccccccc/api/instagram-cheapest
- **RapidAPI Support**: https://rapidapi.com/support

## Legal

This API returns public Instagram data only. Users are responsible for compliance with Instagram's terms of service and applicable privacy laws (GDPR, CCPA). Not affiliated with or endorsed by Meta or Instagram.
