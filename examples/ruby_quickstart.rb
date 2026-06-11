# Instagram Cheapest API - Ruby Quickstart
#
# Requirements: Ruby 2.7+ (standard library only)
# Run:          export RAPIDAPI_KEY='your-key-here' && ruby ruby_quickstart.rb
#
# Docs: https://rapidapi.com/liucccccccccccc/api/instagram-cheapest

require "net/http"
require "json"
require "uri"

# Client for Instagram Cheapest API on RapidAPI.
class InstagramCheapest
  BASE_URL = "https://instagram-cheapest.p.rapidapi.com/api/v1/instagram".freeze

  def initialize(api_key = nil)
    @api_key = api_key || ENV["RAPIDAPI_KEY"]
    if @api_key.nil? || @api_key.empty?
      raise ArgumentError, "RAPIDAPI_KEY not found. Set it via environment variable or pass to constructor."
    end
  end

  # Get user profile by username.
  def userinfo(username, fields: nil)
    get("/user/#{username}", fields ? { fields: fields } : {})
  end

  # Get user profile by numeric user ID.
  def userinfo_by_user_id(user_id, fields: nil)
    get("/user_by_user_id", with_fields({ user_id: user_id }, fields))
  end

  # Get username for a numeric UID.
  def username_by_uid(uid)
    get("/username_by_uid", { uid: uid })
  end

  # Get user's media posts.
  def user_media(user_id, fields: nil)
    get("/user_media", with_fields({ user_id: user_id }, fields))
  end

  # Get user's Reels.
  def user_reels(user_id, fields: nil)
    get("/user_reels", with_fields({ user_id: user_id }, fields))
  end

  # Get media the user is tagged in.
  def user_tag_media(user_id, fields: nil)
    get("/user_tag_media", with_fields({ user_id: user_id }, fields))
  end

  # Get single media item by shortcode.
  def media_by_code2(code, fields: nil)
    get("/media_by_code2", with_fields({ code: code }, fields))
  end

  # Get comments for a media shortcode.
  def media_comments(code, fields: nil)
    get("/media_comments", with_fields({ code: code }, fields))
  end

  # Get Reels that use a specific audio track.
  def reels_audio(audio_id, fields: nil)
    get("/reels_audio", with_fields({ audio_id: audio_id }, fields))
  end

  private

  def with_fields(params, fields)
    fields ? params.merge(fields: fields) : params
  end

  # Internal GET request helper with error handling.
  def get(path, params = {})
    uri = URI("#{BASE_URL}#{path}")
    uri.query = URI.encode_www_form(params) unless params.empty?

    request = Net::HTTP::Get.new(uri)
    request["x-rapidapi-key"] = @api_key
    request["x-rapidapi-host"] = "instagram-cheapest.p.rapidapi.com"

    response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true,
                               open_timeout: 10, read_timeout: 30) do |http|
      http.request(request)
    end

    unless response.is_a?(Net::HTTPSuccess)
      warn "Request failed: #{response.code} #{response.message}"
      raise "HTTP #{response.code}: #{response.body[0, 200]}"
    end

    JSON.parse(response.body)
  end
end

if $PROGRAM_NAME == __FILE__
  # Initialize client (reads RAPIDAPI_KEY from environment)
  client = InstagramCheapest.new

  puts "=== Example 1: Get user profile by username ==="
  user = client.userinfo("nike")
  puts JSON.pretty_generate(user)
  puts

  puts "=== Example 2: Get user profile with 'fields' parameter (reduced bandwidth) ==="
  # Only request specific fields to minimize response size and bandwidth costs
  user_slim = client.userinfo("nike", fields: "username,full_name,follower_count")
  puts JSON.pretty_generate(user_slim)
  puts

  puts "=== Example 3: Get username by UID ==="
  username_data = client.username_by_uid("25025320")
  puts JSON.pretty_generate(username_data)
end
