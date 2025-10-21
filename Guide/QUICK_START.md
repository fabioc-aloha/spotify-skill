# Spotify API Skill - Quick Start Guide

## 5-Minute Setup

### 1. Create Spotify Developer App

1. Go to https://developer.spotify.com/dashboard
2. Log in (create account if needed)
3. Create an app
4. Accept terms
5. Copy your **Client ID** and **Client Secret**
6. Add redirect URI: `http://localhost:8888/callback`

### 2. Set Environment Variables

```bash
export SPOTIFY_CLIENT_ID="your_client_id_here"
export SPOTIFY_CLIENT_SECRET="your_client_secret_here"
export SPOTIFY_REDIRECT_URI="http://localhost:8888/callback"
```

### 3. Get Your First Access Token

Run the OAuth setup script once:

```python
import os
import webbrowser
from spotify_client import SpotifyClient

client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI")
)

# Get authorization URL
auth_url = client.get_authorization_url()
print(f"Visit: {auth_url}")
webbrowser.open(auth_url)

# After authorization, extract code from redirect URL
auth_code = input("Enter authorization code: ")

# Get tokens
token_data = client.get_access_token(auth_code)
print(f"Refresh Token: {token_data['refresh_token']}")

# Save for future use
os.environ["SPOTIFY_REFRESH_TOKEN"] = token_data["refresh_token"]
```

### 4. Start Using!

```python
import os
from spotify_client import SpotifyClient

client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    refresh_token=os.getenv("SPOTIFY_REFRESH_TOKEN")
)

# Get user playlists
playlists = client.get_user_playlists()
for p in playlists:
    print(f"📋 {p['name']} ({p['tracks']['total']} tracks)")

# Create a new playlist
new_playlist = client.create_playlist(
    name="My New Playlist",
    description="Created with Spotify API!"
)
print(f"✅ Created: {new_playlist['name']}")
```

## Common Tasks

### Create Playlist by Artist

```python
from playlist_creator import PlaylistCreator

creator = PlaylistCreator(client)

result = creator.create_from_artist(
    artist_name="The Beatles",
    playlist_name="Beatles Greatest Hits",
    limit=50
)

print(f"Created playlist with {result['tracks_added']} tracks!")
```

### Create Themed Playlist

```python
result = creator.create_from_theme(
    theme_keywords=["indie", "chill", "acoustic"],
    playlist_name="Cozy Indie Vibes",
    limit=100
)

print(f"Added {result['tracks_added']} tracks to playlist")
```

### Create Lyrics-Based Playlist

```python
result = creator.create_from_lyrics(
    lyric_keywords=["love", "heartbreak", "summer"],
    playlist_name="Emotional Journey",
    limit=100
)

print(f"Created emotional playlist with {result['tracks_added']} songs")
```

### Create from Song List

```python
songs = [
    "Shape of You - Ed Sheeran",
    "Blinding Lights - The Weeknd",
    "As It Was - Harry Styles"
]

result = creator.create_from_song_list(
    song_list=songs,
    playlist_name="My Favorites"
)

print(f"Found {result['tracks_found']} of {len(songs)} songs")
```

### Get Recommendations

```python
recommendations = client.get_recommendations(
    seed_artists=["artist_id"],
    seed_tracks=["track_id"],
    limit=50
)

for track in recommendations:
    print(f"🎵 {track['name']} - {track['artists'][0]['name']}")
```

### Search for Music

```python
# Search tracks
tracks = client.search_tracks(query="indie pop 2020-2024", limit=20)
for track in tracks:
    print(f"🎵 {track['name']} - {track['artists'][0]['name']}")

# Search artists
artists = client.search_artists(query="The Beatles")
for artist in artists:
    print(f"👤 {artist['name']} - {artist['popularity']} popularity")

# Search playlists
playlists = client.search_playlists(query="workout")
```

### Manage Tracks

```python
# Add tracks to playlist
track_ids = ["track_1", "track_2", "track_3"]
client.add_tracks_to_playlist("playlist_id", track_ids)

# Remove tracks
client.remove_tracks_from_playlist("playlist_id", track_ids)

# Get playlist tracks
tracks = client.get_playlist_tracks("playlist_id")
for track in tracks:
    print(f"🎵 {track['track']['name']}")
```

### Control Playback

```python
# Get available devices
devices = client.get_available_devices()
device_id = devices[0]['id']

# Start playback
client.start_playback(
    device_id=device_id,
    context_uri="spotify:playlist:playlist_id"
)

# Control playback
client.pause_playback(device_id)
client.next_track(device_id)
client.previous_track(device_id)

# Set volume (0-100)
client.set_volume(volume_percent=75, device_id=device_id)

# Enable shuffle
client.set_shuffle(state=True, device_id=device_id)

# Set repeat mode (off, context, track)
client.set_repeat_mode(state="context", device_id=device_id)
```

### Access User Data

```python
# Get current user profile
user = client.get_current_user()
print(f"👤 {user['display_name']} - {user['followers']['total']} followers")

# Get top artists
top_artists = client.get_top_items(
    item_type="artists",
    limit=20,
    time_range="medium_term"
)

# Get top tracks
top_tracks = client.get_top_items(
    item_type="tracks",
    limit=20,
    time_range="short_term"
)

# Get saved tracks
saved = client.get_saved_tracks(limit=50)
```

## Error Handling

```python
try:
    playlist = client.create_playlist(name="Test")
except Exception as e:
    print(f"Error: {e}")

# Automatic error handling for expired tokens
# Client refreshes automatically when needed
```

## Token Management

```python
# Tokens auto-refresh automatically
# But you can manually refresh if needed:
new_tokens = client.refresh_access_token()

# Check token expiry
import time
if client.token_expires_at and time.time() >= client.token_expires_at - 60:
    print("Token expiring soon!")
```

## Tips & Best Practices

1. **Batch Requests**: Add up to 100 tracks per request
2. **Pagination**: Use limit and offset for large result sets
3. **Error Handling**: Always wrap API calls in try-except
4. **Rate Limiting**: Respect rate limits - check Retry-After header
5. **Token Refresh**: Use refresh tokens to avoid re-authentication
6. **Search Syntax**: Use `artist:`, `track:`, `album:`, `year:` for precise searches
7. **Deduplication**: PlaylistCreator automatically deduplicates tracks

## Troubleshooting

### "Invalid Client ID"
- Check your Client ID is correct
- Verify no whitespace
- Check SPOTIFY_CLIENT_ID env var is set

### "Invalid Redirect URI"
- Must match exactly (including http/https)
- Check in Spotify Dashboard settings
- URLs are case-sensitive

### "Unauthorized (401)"
- Token may be expired - refresh it
- Check refresh token is valid
- Token may have been revoked by user

### "Forbidden (403)"
- Missing required scopes
- Check scope permissions
- May need to re-authorize

### "Too Many Requests (429)"
- Check `Retry-After` header
- Implement exponential backoff
- Batch requests to reduce rate

## Documentation

- **Full Skill Guide**: See `SKILL.md`
- **Authentication Details**: See `references/authentication_guide.md`
- **API Reference**: See `references/api_reference.md`

## What's Next?

1. ✅ You've set up authentication
2. ✅ You've created playlists
3. 🎯 Try building a complex workflow
4. 🎯 Integrate with other services
5. 🎯 Deploy to production

Happy listening! 🎵
