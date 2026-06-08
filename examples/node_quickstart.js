/**
 * Instagram Cheapest API - Node.js Quickstart
 *
 * Requirements: Node.js 18+ (uses built-in fetch)
 * Run: export RAPIDAPI_KEY='your-key-here' && node node_quickstart.js
 *
 * Docs: https://rapidapi.com/liucccccccccccc/api/instagram-cheapest
 */

const BASE_URL = 'https://instagram-cheapest.p.rapidapi.com/api/v1/instagram';

class InstagramCheapest {
  constructor(apiKey = null) {
    this.apiKey = apiKey || process.env.RAPIDAPI_KEY;
    if (!this.apiKey) {
      throw new Error('RAPIDAPI_KEY not found. Set it via environment variable or pass to constructor.');
    }
    this.headers = {
      'x-rapidapi-key': this.apiKey,
      'x-rapidapi-host': 'instagram-cheapest.p.rapidapi.com'
    };
  }

  async _get(path, params = {}) {
    const url = new URL(`${BASE_URL}${path}`);
    Object.entries(params).forEach(([key, value]) => {
      if (value !== null && value !== undefined) {
        url.searchParams.append(key, value);
      }
    });

    try {
      const response = await fetch(url.toString(), {
        method: 'GET',
        headers: this.headers
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Request failed:', error.message);
      throw error;
    }
  }

  async userinfo(username, fields = null) {
    const params = fields ? { fields } : {};
    return this._get(`/user/${username}`, params);
  }

  async userinfoByUserId(userId, fields = null) {
    const params = { user_id: userId };
    if (fields) params.fields = fields;
    return this._get('/user_by_user_id', params);
  }

  async usernameByUid(uid) {
    return this._get('/username_by_uid', { uid });
  }

  async userMedia(userId, fields = null) {
    const params = { user_id: userId };
    if (fields) params.fields = fields;
    return this._get('/user_media', params);
  }

  async userReels(userId, fields = null) {
    const params = { user_id: userId };
    if (fields) params.fields = fields;
    return this._get('/user_reels', params);
  }

  async userTagMedia(userId, fields = null) {
    const params = { user_id: userId };
    if (fields) params.fields = fields;
    return this._get('/user_tag_media', params);
  }

  async mediaByCode2(code, fields = null) {
    const params = { code };
    if (fields) params.fields = fields;
    return this._get('/media_by_code2', params);
  }

  async mediaComments(code, fields = null) {
    const params = { code };
    if (fields) params.fields = fields;
    return this._get('/media_comments', params);
  }

  async reelsAudio(audioId, fields = null) {
    const params = { audio_id: audioId };
    if (fields) params.fields = fields;
    return this._get('/reels_audio', params);
  }
}

async function main() {
  // Initialize client (reads RAPIDAPI_KEY from environment)
  const client = new InstagramCheapest();

  console.log('=== Example 1: Get user profile by username ===');
  const user = await client.userinfo('nike');
  console.log(JSON.stringify(user, null, 2));
  console.log();

  console.log('=== Example 2: Get user profile with fields parameter (reduced bandwidth) ===');
  // Only request specific fields to minimize response size and bandwidth costs
  const userSlim = await client.userinfo('nike', 'username,full_name,follower_count');
  console.log(JSON.stringify(userSlim, null, 2));
  console.log();

  console.log('=== Example 3: Get username by UID ===');
  const usernameData = await client.usernameByUid('25025320');
  console.log(JSON.stringify(usernameData, null, 2));
}

// Run the demo
main().catch(error => {
  console.error('Error:', error.message);
  process.exit(1);
});
