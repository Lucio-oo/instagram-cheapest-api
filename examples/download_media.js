#!/usr/bin/env node
// Download public Instagram photos & videos via the Instagram Cheapest API.
//
// Setup (Node 18+ — uses built-in fetch):
//   export RAPIDAPI_KEY='your-key'   // from https://rapidapi.com/liucccccccccccc/api/instagram-cheapest
//
// Usage:
//   node download_media.js Cabc123XYz                 // one post / Reel by shortcode
//   node download_media.js @nike                      // a whole profile
//   node download_media.js @nike --pages 5            // more pages of the profile
//   node download_media.js https://www.instagram.com/p/Cabc123XYz/   // a pasted URL works too
//
// Files are saved into ./downloads/. Instagram CDN links are signed and expire
// quickly, so this fetches the JSON and downloads immediately.
import { writeFile, mkdir } from "node:fs/promises";

const HOST = "instagram-cheapest.p.rapidapi.com";
const BASE_URL = `https://${HOST}/api/v1/instagram`;
const API_KEY = process.env.RAPIDAPI_KEY || "";

async function get(path, params = {}) {
  const qs = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/${path}${qs ? "?" + qs : ""}`, {
    headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${path}`);
  return res.json();
}

// Recursively collect best-resolution image/video URLs (handles carousels).
function findMedia(node, found = []) {
  if (Array.isArray(node)) {
    node.forEach((item) => findMedia(item, found));
  } else if (node && typeof node === "object") {
    const videos = node.video_versions;
    if (Array.isArray(videos) && videos.length) {
      const best = videos.reduce((a, b) => ((b.width || 0) > (a.width || 0) ? b : a));
      if (best.url) found.push({ type: "video", url: best.url });
    }
    const cands = node.image_versions2?.candidates;
    if (Array.isArray(cands) && cands.length && !(Array.isArray(videos) && videos.length)) {
      const best = cands.reduce((a, b) => ((b.width || 0) > (a.width || 0) ? b : a));
      if (best.url) found.push({ type: "photo", url: best.url });
    }
    Object.values(node).forEach((v) => findMedia(v, found));
  }
  return found;
}

async function downloadMedia(media, dir = "downloads", prefix = "ig") {
  await mkdir(dir, { recursive: true });
  for (let i = 0; i < media.length; i++) {
    const ext = media[i].type === "video" ? "mp4" : "jpg";
    const res = await fetch(media[i].url); // no API headers — public CDN
    const buf = Buffer.from(await res.arrayBuffer());
    const path = `${dir}/${prefix}_${i}.${ext}`;
    await writeFile(path, buf);
    console.log(`  saved ${path}`);
  }
}

async function downloadPost(code) {
  console.log(`Fetching post ${code} ...`);
  const post = await get("media_by_code2", { code });
  const media = findMedia(post);
  console.log(`Found ${media.length} media file(s)`);
  await downloadMedia(media, "downloads", code);
}

async function downloadProfile(username, maxPages = 3) {
  const profile = await get(`user/${username}`);
  const userId = profile.id || profile.pk;
  if (!userId) {
    console.log("Could not find user_id — inspect the raw profile JSON.");
    return;
  }
  console.log(`${username} -> user_id ${userId}`);
  let nextMaxId = null;
  for (let page = 0; page < maxPages; page++) {
    const params = { user_id: userId };
    if (nextMaxId) params.next_max_id = nextMaxId;
    const resp = await get("user_media", params);
    const media = findMedia(resp);
    console.log(`Page ${page + 1}: ${media.length} media file(s)`);
    await downloadMedia(media, `downloads/${username}`, `${username}_p${page}`);
    if (!resp.more_available) break;
    nextMaxId = resp.next_max_id;
    if (!nextMaxId) break;
    await new Promise((r) => setTimeout(r, 1000)); // ~1 req/sec on the free tier
  }
}

function parseTarget(target) {
  const t = target.trim().replace(/\/+$/, "");
  if (t.includes("instagram.com")) {
    const parts = t.split("/").filter(Boolean);
    for (const kw of ["p", "reel", "reels", "tv"]) {
      const i = parts.indexOf(kw);
      if (i !== -1) return ["post", parts[i + 1]];
    }
    return ["profile", parts[parts.length - 1].replace(/^@/, "")];
  }
  if (t.startsWith("@")) return ["profile", t.slice(1)];
  return ["post", t];
}

const argv = process.argv.slice(2);
if (!API_KEY) {
  console.error("Set RAPIDAPI_KEY first:  export RAPIDAPI_KEY='your-key'");
  process.exit(1);
}
if (!argv.length) {
  console.error("Usage: node download_media.js <shortcode | @username | url> [--pages N]");
  process.exit(1);
}
const pagesIdx = argv.indexOf("--pages");
const maxPages = pagesIdx !== -1 ? parseInt(argv[pagesIdx + 1], 10) : 3;
const target = argv.find((a, i) => !a.startsWith("--") && argv[i - 1] !== "--pages");

const [kind, value] = parseTarget(target);
if (kind === "profile") await downloadProfile(value, maxPages);
else await downloadPost(value);
