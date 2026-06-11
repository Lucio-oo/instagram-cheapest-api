# Instagram Cheapest API

Real-time Instagram data via raw JSON — from **$0.10 per 1,000 requests**.

[![Subscribe on RapidAPI](https://img.shields.io/badge/RapidAPI-Subscribe-2ecc71)](https://rapidapi.com/liucccccccccccc/api/instagram-cheapest)
[![OpenAPI 3.0](https://img.shields.io/badge/OpenAPI-3.0-6BA539)](./landing/openapi.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

Official quickstarts and a deployable landing page for the **Instagram Cheapest** API on RapidAPI.
Fetch public Instagram profiles, posts, Reels, comments, tagged media, and Reels audio as raw, real-time JSON.

**→ Get started (free tier):** https://rapidapi.com/liucccccccccccc/api/instagram-cheapest
**→ Guides, pricing calculator & API comparison:** https://instagram.kolapihub.com

## Quick start

1. Subscribe to the free **Basic** plan on RapidAPI and copy your API key.
2. Export it:
   ```bash
   export RAPIDAPI_KEY='your-rapidapi-key'
   ```
3. Make your first call:
   ```bash
   curl "https://instagram-cheapest.p.rapidapi.com/api/v1/instagram/user/nike" \
     -H "x-rapidapi-key: $RAPIDAPI_KEY" \
     -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
   ```

Python:
```python
import os, requests

BASE = "https://instagram-cheapest.p.rapidapi.com/api/v1/instagram"
headers = {
    "x-rapidapi-key": os.environ["RAPIDAPI_KEY"],
    "x-rapidapi-host": "instagram-cheapest.p.rapidapi.com",
}
resp = requests.get(f"{BASE}/user/nike", headers=headers, timeout=30)
print(resp.json())
```

## Endpoints

All endpoints are `GET` and return raw JSON. Add the optional `fields` query param to request only the keys you need and cut bandwidth.

| Endpoint | Path | Required param |
|----------|------|----------------|
| User profile (by username) | `/api/v1/instagram/user/{username}` | `username` |
| User profile (by ID) | `/api/v1/instagram/user_by_user_id` | `user_id` |
| Username by UID | `/api/v1/instagram/username_by_uid` | `uid` |
| User media / posts | `/api/v1/instagram/user_media` | `user_id` |
| User Reels | `/api/v1/instagram/user_reels` | `user_id` |
| Tagged media | `/api/v1/instagram/user_tag_media` | `user_id` |
| Media by shortcode | `/api/v1/instagram/media_by_code2` | `code` |
| Media comments | `/api/v1/instagram/media_comments` | `code` |
| Reels by audio | `/api/v1/instagram/reels_audio` | `audio_id` |

**Pagination:** list endpoints return ~12 items per page. `user_media` takes a `next_max_id` cursor;
`user_reels`, `user_tag_media`, and `media_comments` take `after`; `reels_audio` takes `max_id`.
Omit the cursor on the first call, then echo back the cursor from the previous response —
full loops in the [pagination guide](https://instagram.kolapihub.com/blog/instagram-api-pagination/)
and parameter-level detail in the [OpenAPI spec](./landing/openapi.yaml).

## Pricing

| Tier | Monthly | Cost per 1,000 requests | Rate limit |
|------|---------|--------------------------|------------|
| Basic | $0 | — (30 requests/mo) | 1 req/sec |
| Pro | $59 | $0.13 | 20 req/min |
| Ultra | $119 | $0.11 | 40 req/min |
| Mega | $249 | $0.10 | 120 req/min |

Paid tiers are a monthly base fee plus per-request overage. See RapidAPI for current billing details.

## Repository contents

- **[`examples/`](./examples/)** — runnable quickstarts in cURL, Python, Node.js, PHP, Go, and Ruby.
- **[`landing/`](./landing/)** — the static site behind [instagram.kolapihub.com](https://instagram.kolapihub.com): landing page, [tutorials](https://instagram.kolapihub.com/blog/), and [API comparison](https://instagram.kolapihub.com/compare/).
- **[`landing/openapi.yaml`](./landing/openapi.yaml)** — OpenAPI 3.0 spec (also served at [instagram.kolapihub.com/openapi.yaml](https://instagram.kolapihub.com/openapi.yaml)) — point your codegen or AI coding assistant at it.
- **[`landing/postman_collection.json`](./landing/postman_collection.json)** — Postman collection; import by URL: `https://instagram.kolapihub.com/postman_collection.json`.

## Run the examples

```bash
export RAPIDAPI_KEY='your-key'
python3 examples/python_quickstart.py
# or:  node examples/node_quickstart.js   |   bash examples/curl.sh   |   ruby examples/ruby_quickstart.rb
```

## Disclaimer

This API returns **public** Instagram data only. You are responsible for complying with Instagram's
Terms of Use and applicable privacy laws (e.g. GDPR/CCPA). Not affiliated with or endorsed by Meta or Instagram.

## License

[MIT](./LICENSE)
