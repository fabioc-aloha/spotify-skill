# Spotify API Skill - Quick Reference Card

**One-page reference for common operations**

---

## Setup (One-Time)

```python
import os
from spotify_client import SpotifyClient

client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    refresh_token=os.getenv("SPOTIFY_REFRESH_TOKEN")
)
```

---

## Quick Operations

### Search

```python
# Search tracks
tracks = client.search_tracks("love songs", limit=20)

# Search artists
artists = client.search_artists("Taylor Swift", limit=5)

# Advanced search
tracks = client.search_tracks("artist:Beatles year:1960-1970", limit=50)
```

### Playlists

```python
# List playlists
playlists = client.get_user_playlists(limit=50)

# Create playlist
playlist = client.create_playlist("My Playlist", "Description", public=True)

# Add tracks
client.add_tracks_to_playlist(playlist['id'], ["track_id_1", "track_id_2"])

# Get playlist tracks
tracks = client.get_playlist_tracks(playlist_id, limit=50)
```

### Intelligent Playlist Creation

```python
from playlist_creator import PlaylistCreator
creator = PlaylistCreator(client)

# From artist
creator.create_from_artist("The Beatles", "Beatles Hits", limit=50)

# From theme
creator.create_from_theme(["chill", "indie"], "Chill Vibes", limit=100)

# From song list
songs = ["Shape of You", "Blinding Lights", "As It Was"]
creator.create_from_song_list(songs, "My Favorites")

# From recommendations
creator.create_from_recommendations(
    "Discover Weekly",
    seed_tracks=["track_id"],
    seed_genres=["indie"],
    limit=50
)
```

### User Data

```python
# Current user
profile = client.get_current_user()

# Top tracks (short_term, medium_term, long_term)
top_tracks = client.get_top_items("tracks", limit=20, time_range="medium_term")

# Top artists
top_artists = client.get_top_items("artists", limit=20, time_range="short_term")

# Saved tracks
saved = client.get_saved_tracks(limit=50)
```

### Artist Info

```python
# Search for artist
artists = client.search_artists("Taylor Swift", limit=1)
artist_id = artists[0]['id']

# Get details
artist = client.get_artist(artist_id)

# Top tracks
top_tracks = client.get_artist_top_tracks(artist_id)

# Related artists
related = client.get_related_artists(artist_id)

# Albums
albums = client.get_artist_albums(artist_id)
```

### Playback Control (Premium Only)

```python
# Currently playing
current = client.get_currently_playing()

# Available devices
devices = client.get_available_devices()

# Play
client.start_playback(device_id="device_id", track_uris=["spotify:track:id"])

# Pause
client.pause_playback()

# Next/Previous
client.next_track()
client.previous_track()

# Shuffle & Repeat
client.set_shuffle(True)
client.set_repeat_mode("context")  # off, context, track

# Volume
client.set_volume(50)  # 0-100
```

### Library Management

```python
# Save tracks
client.save_tracks(["track_id_1", "track_id_2"])

# Remove tracks
client.remove_saved_tracks(["track_id_1"])

# Check if saved
is_saved = client.check_saved_tracks(["track_id_1", "track_id_2"])
```

### Track Details

```python
# Get track info
track = client.get_track("track_id")

# Multiple tracks
tracks = client.get_tracks(["track_id_1", "track_id_2"])

# Audio features
features = client.get_track_audio_features("track_id")
# Returns: tempo, energy, danceability, valence, etc.
```

### Recommendations

```python
# Get recommendations
recs = client.get_recommendations(
    seed_artists=["artist_id"],
    seed_tracks=["track_id"],
    seed_genres=["indie", "pop"],
    limit=50
)

# Available genres
genres = client.get_available_genres()
```

---

## Common Patterns

### Pagination

```python
all_items = []
offset = 0
limit = 50

while True:
    batch = client.get_user_playlists(limit=limit, offset=offset)
    if not batch:
        break
    all_items.extend(batch)
    offset += limit
    if len(batch) < limit:
        break
```

### Batch Processing

```python
# Add tracks in batches of 100
track_ids = [...]  # Your track IDs
for i in range(0, len(track_ids), 100):
    batch = track_ids[i:i+100]
    client.add_tracks_to_playlist(playlist_id, batch)
```

### Error Handling

```python
try:
    result = client.create_playlist("My Playlist")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 429:
        print("Rate limited. Wait and retry.")
    elif e.response.status_code == 401:
        print("Token expired. Refreshing...")
        client.refresh_access_token()
    else:
        print(f"Error: {e}")
```

### Extract IDs from Search

```python
# Search and get IDs
tracks = client.search_tracks("chill vibes", limit=50)
track_ids = [track['id'] for track in tracks]

# Artists
artists = client.search_artists("indie", limit=20)
artist_ids = [artist['id'] for artist in artists]
```

---

## Environment Variables

```bash
# Required
SPOTIFY_CLIENT_ID="your_client_id"
SPOTIFY_CLIENT_SECRET="your_client_secret"
SPOTIFY_REDIRECT_URI="http://localhost:8888/callback"

# After first auth
SPOTIFY_REFRESH_TOKEN="your_refresh_token"
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| "No module named 'spotify_client'" | Add to Python path or copy files |
| "Invalid credentials" | Check CLIENT_ID and CLIENT_SECRET |
| "Token expired" | Call `client.refresh_access_token()` |
| "429 Rate limit" | Wait 60 seconds, implement delays |
| "No active device" | Open Spotify on any device |
| "Premium required" | Upgrade for playback control |

---

## API Limits

- **Rate Limit**: ~180 requests/minute
- **Playlist Add**: Max 100 tracks per request
- **Search Results**: Max 50 per request
- **Recommendation Seeds**: Max 5 total (artists + tracks + genres)
- **Bulk Operations**: Usually max 50 items

---

## Search Query Syntax

```python
# Simple
"love songs"

# Artist filter
"artist:Beatles"

# Year filter
"year:2020-2024"

# Genre filter
"genre:indie"

# Combined
"artist:Taylor Swift year:2019-2024"
"genre:rock year:1970-1980"
"mood:happy genre:pop"
```

---

## Useful Track/Playlist Properties

```python
# Track
track['id']                    # Track ID
track['name']                  # Track name
track['artists'][0]['name']    # Artist name
track['album']['name']         # Album name
track['duration_ms']           # Duration in milliseconds
track['popularity']            # 0-100
track['external_urls']['spotify']  # Spotify URL

# Playlist
playlist['id']                 # Playlist ID
playlist['name']               # Playlist name
playlist['tracks']['total']    # Number of tracks
playlist['public']             # Public/private
playlist['owner']['display_name']  # Owner name
```

---

## Time Ranges for Top Items

- `"short_term"` - Last 4 weeks
- `"medium_term"` - Last 6 months (default)
- `"long_term"` - All time

---

## Audio Features

```python
features = client.get_track_audio_features(track_id)

# Returns:
features['tempo']              # BPM
features['energy']             # 0.0-1.0
features['danceability']       # 0.0-1.0
features['valence']            # 0.0-1.0 (happiness)
features['acousticness']       # 0.0-1.0
features['instrumentalness']   # 0.0-1.0
features['loudness']           # dB
features['key']                # 0-11 (pitch class)
features['mode']               # 0=minor, 1=major
```

---

## Complete Documentation

- **📖 USER_GUIDE.md** - Full user guide
- **⚡ QUICK_START.md** - 5-minute setup
- **🔧 SKILL.md** - Claude skill format
- **🔐 references/authentication_guide.md** - OAuth setup
- **📚 references/api_reference.md** - API details

---

**Version**: 1.0 | **Updated**: October 21, 2025
