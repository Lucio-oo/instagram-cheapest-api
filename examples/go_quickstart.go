package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"time"
)

// Instagram Cheapest API - Go Quickstart
// Requirements: Go 1.18+
// Run: export RAPIDAPI_KEY='your-key-here' && go run go_quickstart.go
// Docs: https://rapidapi.com/liucccccccccccc/api/instagram-cheapest

const baseURL = "https://instagram-cheapest.p.rapidapi.com/api/v1/instagram"

// InstagramCheapest is a client for the Instagram Cheapest API
type InstagramCheapest struct {
	apiKey     string
	httpClient *http.Client
}

// NewInstagramCheapest creates a new API client
func NewInstagramCheapest(apiKey string) (*InstagramCheapest, error) {
	if apiKey == "" {
		apiKey = os.Getenv("RAPIDAPI_KEY")
	}
	if apiKey == "" {
		return nil, fmt.Errorf("RAPIDAPI_KEY not found. Set it via environment variable or pass to constructor")
	}
	return &InstagramCheapest{
		apiKey: apiKey,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}, nil
}

func (c *InstagramCheapest) get(path string, params url.Values) (map[string]interface{}, error) {
	reqURL := baseURL + path
	if len(params) > 0 {
		reqURL += "?" + params.Encode()
	}

	req, err := http.NewRequest("GET", reqURL, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("x-rapidapi-key", c.apiKey)
	req.Header.Set("x-rapidapi-host", "instagram-cheapest.p.rapidapi.com")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %w", err)
	}

	if resp.StatusCode >= 400 {
		return nil, fmt.Errorf("HTTP %d: %s", resp.StatusCode, string(body))
	}

	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("failed to parse JSON: %w", err)
	}

	return result, nil
}

func (c *InstagramCheapest) Userinfo(username string, fields string) (map[string]interface{}, error) {
	params := url.Values{}
	if fields != "" {
		params.Set("fields", fields)
	}
	return c.get("/user/"+username, params)
}

func (c *InstagramCheapest) UserinfoByUserID(userID string, fields string) (map[string]interface{}, error) {
	params := url.Values{"user_id": {userID}}
	if fields != "" {
		params.Set("fields", fields)
	}
	return c.get("/user_by_user_id", params)
}

func (c *InstagramCheapest) UsernameByUID(uid string) (map[string]interface{}, error) {
	params := url.Values{"uid": {uid}}
	return c.get("/username_by_uid", params)
}

func (c *InstagramCheapest) UserMedia(userID string, fields string) (map[string]interface{}, error) {
	params := url.Values{"user_id": {userID}}
	if fields != "" {
		params.Set("fields", fields)
	}
	return c.get("/user_media", params)
}

func (c *InstagramCheapest) UserReels(userID string, fields string) (map[string]interface{}, error) {
	params := url.Values{"user_id": {userID}}
	if fields != "" {
		params.Set("fields", fields)
	}
	return c.get("/user_reels", params)
}

func (c *InstagramCheapest) UserTagMedia(userID string, fields string) (map[string]interface{}, error) {
	params := url.Values{"user_id": {userID}}
	if fields != "" {
		params.Set("fields", fields)
	}
	return c.get("/user_tag_media", params)
}

func (c *InstagramCheapest) MediaByCode2(code string, fields string) (map[string]interface{}, error) {
	params := url.Values{"code": {code}}
	if fields != "" {
		params.Set("fields", fields)
	}
	return c.get("/media_by_code2", params)
}

func (c *InstagramCheapest) MediaComments(code string, fields string) (map[string]interface{}, error) {
	params := url.Values{"code": {code}}
	if fields != "" {
		params.Set("fields", fields)
	}
	return c.get("/media_comments", params)
}

func (c *InstagramCheapest) ReelsAudio(audioID string, fields string) (map[string]interface{}, error) {
	params := url.Values{"audio_id": {audioID}}
	if fields != "" {
		params.Set("fields", fields)
	}
	return c.get("/reels_audio", params)
}

func main() {
	// Initialize client (reads RAPIDAPI_KEY from environment)
	client, err := NewInstagramCheapest("")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("=== Example 1: Get user profile by username ===")
	user, err := client.Userinfo("nike", "")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	printJSON(user)
	fmt.Println()

	fmt.Println("=== Example 2: Get user profile with fields parameter (reduced bandwidth) ===")
	// Only request specific fields to minimize response size and bandwidth costs
	userSlim, err := client.Userinfo("nike", "username,full_name,follower_count")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	printJSON(userSlim)
	fmt.Println()

	fmt.Println("=== Example 3: Get username by UID ===")
	usernameData, err := client.UsernameByUID("25025320")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	printJSON(usernameData)
}

func printJSON(data map[string]interface{}) {
	jsonBytes, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		fmt.Fprintf(os.Stderr, "JSON marshal error: %v\n", err)
		return
	}
	fmt.Println(string(jsonBytes))
}
