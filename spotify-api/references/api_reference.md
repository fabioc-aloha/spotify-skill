# Spotify Web API Reference

## Table of Contents

1. [Rate Limiting](#rate-limiting)
2. [Authentication](#authentication)
3. [Response Format](#response-format)
4. [Common Endpoints](#common-endpoints)
5. [Error Handling](#error-handling)
6. [Data Types](#data-types)

## Rate Limiting

Spotify API enforces rate limiting to ensure service stability.

- **Rate Limit**: 429,400 requests per 30-minute period (general limit)
- **Header**: `Retry-After` indicates seconds to wait before retrying
- **Response Code**: `429 Too Many Requests`

**Best Practices:**
- Batch requests when possible (e.g., get up to 50 tracks in single request)
- Implement exponential backoff for retries
- Cache responses when appropriate
- Use offset/pagination for large result sets

## Authentication

### OAuth 2.0 Authorization Code Flow

Spotify uses OAuth 2.0 for user authentication and authorization.

**Endpoints:**
- Authorization: `https://accounts.spotify.com/authorize`
- Token: `https://accounts.spotify.com/api/token`

**Required Scopes:**
```
playlist-modify-public
playlist-modify-private
user-library-read
user-library-modify
user-read-private
user-read-email
user-top-read
user-read-currently-playing
user-modify-playback-state
user-read-playback-state
```

**Token Expiration:**
- Access tokens expire in 3600 seconds (1 hour)
- Use refresh token to obtain new access token without user re-authentication
- Refresh tokens do not expire (unless revoked by user)

## Response Format

### Standard Response Structure

```json
{
  "href": "https://api.spotify.com/v1/...",
  "items": [...],
  "limit": 20,
  "next": "https://api.spotify.com/v1/...?offset=20",
  "offset": 0,
  "previous": null,
  "total": 100
}
```

### Pagination

- Use `limit` parameter to control items per page (max 50)
- Use `offset` parameter for pagination
- `next` URL provides next page, `previous` URL provides previous page

Example:
```
GET /v1/me/playlists?limit=50&offset=0
GET /v1/me/playlists?limit=50&offset=50
```

## Common Endpoints

### Playlists

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/me/playlists` | Get current user's playlists |
| POST | `/v1/users/{user_id}/playlists` | Create playlist |
| GET | `/v1/playlists/{playlist_id}` | Get playlist details |
| PUT | `/v1/playlists/{playlist_id}` | Update playlist |
| DELETE | `/v1/playlists/{playlist_id}` | Delete (unfollow) playlist |
| GET | `/v1/playlists/{playlist_id}/tracks` | Get playlist tracks |
| POST | `/v1/playlists/{playlist_id}/tracks` | Add tracks to playlist |
| DELETE | `/v1/playlists/{playlist_id}/tracks` | Remove tracks from playlist |

**Notes:**
- Maximum 100 tracks per add/remove request
- Track order is preserved
- Creating/modifying requires playlist-modify scope

### Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/search` | Search across types |

**Query Parameters:**
- `q`: Search query
- `type`: `track`, `artist`, `album`, `playlist` (comma-separated)
- `limit`: 1-50 (default 20)
- `offset`: For pagination

**Search Query Syntax:**
```
# Basic search
q=The Beatles

# By field
q=artist:The Beatles
q=track:Yesterday
q=album:Abbey Road
q=year:1965

# Combined
q=artist:The Beatles track:Yesterday
q=genre:rock year:1970-1979

# Exclude
q=artist:The Beatles -live
```

### Artists

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/artists/{artist_id}` | Get artist details |
| GET | `/v1/artists/{artist_id}/top-tracks` | Get artist top tracks |
| GET | `/v1/artists/{artist_id}/albums` | Get artist albums |
| GET | `/v1/artists/{artist_id}/related-artists` | Get related artists |

### Tracks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/tracks/{track_id}` | Get track details |
| GET | `/v1/tracks` | Get multiple tracks (comma-separated IDs) |
| GET | `/v1/audio-features/{track_id}` | Get audio features |

### User

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/me` | Get current user profile |
| GET | `/v1/users/{user_id}` | Get user profile |
| GET | `/v1/me/top/{type}` | Get user's top items (tracks/artists) |
| GET | `/v1/me/tracks` | Get user's saved tracks |
| PUT | `/v1/me/tracks` | Save tracks |
| DELETE | `/v1/me/tracks` | Remove saved tracks |
| GET | `/v1/me/tracks/contains` | Check if tracks are saved |

**Time Ranges:**
- `long_term`: ~6 months
- `medium_term`: ~6 weeks (default)
- `short_term`: ~4 weeks

### Recommendations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/recommendations` | Get recommendations |
| GET | `/v1/recommendations/available-genre-seeds` | Get available genres |

**Parameters:**
- `seed_artists`: Up to 5 artist IDs
- `seed_tracks`: Up to 5 track IDs
- `seed_genres`: Up to 5 genres
- Total seeds cannot exceed 5
- `limit`: 1-100 (default 20)
- Audio feature parameters: `min_energy`, `max_energy`, `target_popularity`, etc.

### Playback

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/me/player` | Get playback state |
| GET | `/v1/me/player/currently-playing` | Get currently playing |
| GET | `/v1/me/player/devices` | Get available devices |
| PUT | `/v1/me/player/play` | Start/resume playback |
| PUT | `/v1/me/player/pause` | Pause playback |
| POST | `/v1/me/player/next` | Skip to next |
| POST | `/v1/me/player/previous` | Previous track |
| PUT | `/v1/me/player/seek` | Seek to position |
| PUT | `/v1/me/player/repeat` | Set repeat mode |
| PUT | `/v1/me/player/shuffle` | Enable/disable shuffle |
| PUT | `/v1/me/player/volume` | Set volume |

**Playback Context Types:**
- `spotify:playlist:{playlist_id}`
- `spotify:album:{album_id}`
- `spotify:artist:{artist_id}`

## Error Handling

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | OK | Success |
| 201 | Created | Resource created |
| 204 | No Content | Success (no response body) |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Invalid/expired token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limited (see header) |
| 500 | Server Error | Spotify service error |

### Error Response Format

```json
{
  "error": {
    "status": 404,
    "message": "The requested resource was not found"
  }
}
```

### Retry Strategy

1. Always check `Retry-After` header for 429 responses
2. Implement exponential backoff: wait 1s, 2s, 4s, 8s, etc.
3. Maximum 3-5 retries recommended
4. For 5xx errors, retry with backoff

## Data Types

### Track Object

```json
{
  "id": "11dFghVXANMlKmJXsNCQvb",
  "name": "Yellow",
  "artists": [{
    "id": "frXchxsSQrCQqf5K25zXiA",
    "name": "Coldplay"
  }],
  "album": {
    "id": "0VjIjW4GlUZAMYd2vXMwbU",
    "name": "Parachutes"
  },
  "duration_ms": 269373,
  "popularity": 85,
  "external_ids": {
    "isrc": "GBUM71000059",
    "ean": "5099749503584",
    "upc": "5099749503584"
  },
  "uri": "spotify:track:11dFghVXANMlKmJXsNCQvb"
}
```

### Playlist Object

```json
{
  "id": "37i9dQZF1DX",
  "name": "New Music Friday",
  "description": "Your weekly update of new tracks featured on Spotify's New Music Friday.",
  "public": true,
  "collaborative": false,
  "followers": {
    "total": 1234567
  },
  "owner": {
    "id": "spotify",
    "display_name": "Spotify"
  },
  "tracks": {
    "total": 50,
    "href": "https://api.spotify.com/v1/playlists/37i9dQZF1DX/tracks"
  },
  "uri": "spotify:playlist:37i9dQZF1DX"
}
```

### Artist Object

```json
{
  "id": "0TnOYISbd1XYRBk9FJ3x0V",
  "name": "Pitbull",
  "genres": ["reggaeton", "latin"],
  "popularity": 89,
  "followers": {
    "total": 28150384
  },
  "images": [{
    "url": "https://i.scdn.co/...",
    "height": 640,
    "width": 640
  }],
  "uri": "spotify:artist:0TnOYISbd1XYRBk9FJ3x0V"
}
```

### User Object

```json
{
  "id": "thelinmichael",
  "display_name": "Lín",
  "email": "user@example.com",
  "followers": {
    "total": 150
  },
  "images": [],
  "external_urls": {
    "spotify": "https://open.spotify.com/user/thelinmichael"
  },
  "uri": "spotify:user:thelinmichael"
}
```

### Audio Features Object

```json
{
  "acousticness": 0.00242,
  "danceability": 0.585,
  "energy": 0.842,
  "instrumentalness": 0.00686,
  "key": 9,
  "liveness": 0.0646,
  "loudness": -5.883,
  "mode": 0,
  "speechiness": 0.0556,
  "tempo": 130.039,
  "time_signature": 4,
  "valence": 0.428
}
```

**Audio Features Definitions:**
- `acousticness` (0-1): Likelihood of acoustic sound
- `danceability` (0-1): Suitability for dancing
- `energy` (0-1): Intensity and activity
- `instrumentalness` (0-1): Lack of vocals
- `liveness` (0-1): Presence of audience
- `loudness` (dB): Overall loudness
- `mode` (0/1): Minor/Major key
- `speechiness` (0-1): Presence of spoken words
- `tempo` (BPM): Overall speed
- `valence` (0-1): Musical positiveness/happiness
