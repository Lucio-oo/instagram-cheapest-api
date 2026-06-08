#!/usr/bin/env bash
set -euo pipefail

# Instagram Cheapest API — curl examples
# Get your API key: https://rapidapi.com/liucccccccccccc/api/instagram-cheapest

if [ -z "${RAPIDAPI_KEY:-}" ]; then
  echo "Error: RAPIDAPI_KEY environment variable is not set"
  echo "Usage: export RAPIDAPI_KEY='your-key-here' && bash curl.sh"
  exit 1
fi

BASE_URL="https://instagram-cheapest.p.rapidapi.com/api/v1/instagram"

# 1. Get user profile by username
echo "=== 1. userinfo (by username) ==="
curl -X GET "${BASE_URL}/user/nike" \
  -H "x-rapidapi-key: ${RAPIDAPI_KEY}" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
echo -e "\n"

# 2. Get user profile by user ID
echo "=== 2. userinfo_by_user_id ==="
curl -X GET "${BASE_URL}/user_by_user_id?user_id=25025320" \
  -H "x-rapidapi-key: ${RAPIDAPI_KEY}" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
echo -e "\n"

# 3. Get username by UID
echo "=== 3. username_by_uid ==="
curl -X GET "${BASE_URL}/username_by_uid?uid=25025320" \
  -H "x-rapidapi-key: ${RAPIDAPI_KEY}" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
echo -e "\n"

# 4. Get user's media posts
echo "=== 4. user_media ==="
curl -X GET "${BASE_URL}/user_media?user_id=25025320" \
  -H "x-rapidapi-key: ${RAPIDAPI_KEY}" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
echo -e "\n"

# 5. Get user's Reels
echo "=== 5. user_reels ==="
curl -X GET "${BASE_URL}/user_reels?user_id=25025320" \
  -H "x-rapidapi-key: ${RAPIDAPI_KEY}" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
echo -e "\n"

# 6. Get media user is tagged in
echo "=== 6. user_tag_media ==="
curl -X GET "${BASE_URL}/user_tag_media?user_id=25025320" \
  -H "x-rapidapi-key: ${RAPIDAPI_KEY}" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
echo -e "\n"

# 7. Get media by shortcode
echo "=== 7. media_by_code2 ==="
curl -X GET "${BASE_URL}/media_by_code2?code=C1234567890" \
  -H "x-rapidapi-key: ${RAPIDAPI_KEY}" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
echo -e "\n"

# 8. Get media comments
echo "=== 8. media_comments ==="
curl -X GET "${BASE_URL}/media_comments?code=C1234567890" \
  -H "x-rapidapi-key: ${RAPIDAPI_KEY}" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
echo -e "\n"

# 9. Get Reels by audio ID
echo "=== 9. reels_audio ==="
curl -X GET "${BASE_URL}/reels_audio?audio_id=1234567890123456789" \
  -H "x-rapidapi-key: ${RAPIDAPI_KEY}" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
echo -e "\n"

# Example: using 'fields' parameter to reduce bandwidth
echo "=== Example: fields parameter to reduce response size ==="
curl -X GET "${BASE_URL}/user/nike?fields=username,full_name,follower_count" \
  -H "x-rapidapi-key: ${RAPIDAPI_KEY}" \
  -H "x-rapidapi-host: instagram-cheapest.p.rapidapi.com"
echo -e "\n"
