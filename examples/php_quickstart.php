<?php
/**
 * Instagram Cheapest API - PHP Quickstart
 *
 * Requirements: PHP 7.4+ with cURL extension
 * Run: export RAPIDAPI_KEY='your-key-here' && php php_quickstart.php
 *
 * Docs: https://rapidapi.com/liucccccccccccc/api/instagram-cheapest
 */

define('BASE_URL', 'https://instagram-cheapest.p.rapidapi.com/api/v1/instagram');

class InstagramCheapest {
    private $apiKey;
    private $headers;

    public function __construct($apiKey = null) {
        $this->apiKey = $apiKey ?? getenv('RAPIDAPI_KEY');
        if (!$this->apiKey) {
            throw new Exception('RAPIDAPI_KEY not found. Set it via environment variable or pass to constructor.');
        }
        $this->headers = [
            'x-rapidapi-key: ' . $this->apiKey,
            'x-rapidapi-host: instagram-cheapest.p.rapidapi.com'
        ];
    }

    private function get($path, $params = []) {
        $url = BASE_URL . $path;
        if (!empty($params)) {
            $url .= '?' . http_build_query($params);
        }

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $this->headers);
        curl_setopt($ch, CURLOPT_TIMEOUT, 30);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);

        if ($error) {
            throw new Exception("cURL Error: $error");
        }

        if ($httpCode >= 400) {
            throw new Exception("HTTP Error $httpCode: $response");
        }

        return json_decode($response, true);
    }

    public function userinfo($username, $fields = null) {
        $params = $fields ? ['fields' => $fields] : [];
        return $this->get("/user/$username", $params);
    }

    public function userinfoByUserId($userId, $fields = null) {
        $params = ['user_id' => $userId];
        if ($fields) $params['fields'] = $fields;
        return $this->get('/user_by_user_id', $params);
    }

    public function usernameByUid($uid) {
        return $this->get('/username_by_uid', ['uid' => $uid]);
    }

    public function userMedia($userId, $fields = null) {
        $params = ['user_id' => $userId];
        if ($fields) $params['fields'] = $fields;
        return $this->get('/user_media', $params);
    }

    public function userReels($userId, $fields = null) {
        $params = ['user_id' => $userId];
        if ($fields) $params['fields'] = $fields;
        return $this->get('/user_reels', $params);
    }

    public function userTagMedia($userId, $fields = null) {
        $params = ['user_id' => $userId];
        if ($fields) $params['fields'] = $fields;
        return $this->get('/user_tag_media', $params);
    }

    public function mediaByCode2($code, $fields = null) {
        $params = ['code' => $code];
        if ($fields) $params['fields'] = $fields;
        return $this->get('/media_by_code2', $params);
    }

    public function mediaComments($code, $fields = null) {
        $params = ['code' => $code];
        if ($fields) $params['fields'] = $fields;
        return $this->get('/media_comments', $params);
    }

    public function reelsAudio($audioId, $fields = null) {
        $params = ['audio_id' => $audioId];
        if ($fields) $params['fields'] = $fields;
        return $this->get('/reels_audio', $params);
    }
}

// Demo
try {
    // Initialize client (reads RAPIDAPI_KEY from environment)
    $client = new InstagramCheapest();

    echo "=== Example 1: Get user profile by username ===\n";
    $user = $client->userinfo('nike');
    echo json_encode($user, JSON_PRETTY_PRINT) . "\n\n";

    echo "=== Example 2: Get user profile with fields parameter (reduced bandwidth) ===\n";
    // Only request specific fields to minimize response size and bandwidth costs
    $userSlim = $client->userinfo('nike', 'username,full_name,follower_count');
    echo json_encode($userSlim, JSON_PRETTY_PRINT) . "\n\n";

    echo "=== Example 3: Get username by UID ===\n";
    $usernameData = $client->usernameByUid('25025320');
    echo json_encode($usernameData, JSON_PRETTY_PRINT) . "\n";

} catch (Exception $e) {
    fwrite(STDERR, "Error: " . $e->getMessage() . "\n");
    exit(1);
}
