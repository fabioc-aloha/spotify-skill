---
name: spotify-api
description: Connect to Spotify API and manage playlists, search music, control playback, and create intelligent playlists by artist, theme, lyrics, or specific songs. Handles OAuth authentication, playlist CRUD operations, track management, user profile access, recommendations, and search functionality.
---

# Spotify API Skill

## Overview

This skill enables Claude to interact with the Spotify Web API to manage music, playlists, and playback. It provides authenticated access to user data and handles common music management tasks. Use this skill when users need to create playlists, search for music, manage their library, control playback, or retrieve user/artist information.

## Core Capabilities

1. **Playlist Management** - Create, list, update, and delete playlists
2. **Intelligent Playlist Creation** - Build playlists by artist/band name, themes, lyrics-based search, or specific song lists
3. **Search & Discovery** - Search for tracks, artists, albums, and playlists
4. **Track Management** - Add/remove tracks from playlists, get recommendations
5. **User Library** - Access saved tracks, user profile, and listening history
6. **Playback Control** - Play, pause, skip, and manage currently playing track
7. **Artist & User Data** - Retrieve top artists, user information, and related artists

## Quick Start

All Spotify API operations use the `SpotifyClient` class from `scripts/spotify_client.py`. The client handles OAuth authentication and provides methods for all operations.

### Basic Setup

```python
from spotify_client import SpotifyClient

# Initialize with existing credentials (assumed available)
client = SpotifyClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI",
    access_token="EXISTING_ACCESS_TOKEN"  # if available
)

# Or authenticate with refresh token
client.refresh_access_token(refresh_token="YOUR_REFRESH_TOKEN")
```

### Common Operations

**List user playlists:**
```python
playlists = client.get_user_playlists(limit=50)
```

**Create a new playlist:**
```python
playlist = client.create_playlist(
    name="My Awesome Playlist",
    description="A curated collection",
    public=True
)
```

**Search for tracks:**
```python
results = client.search_tracks(query="artist:The Beatles", limit=20)
```

**Add tracks to playlist:**
```python
client.add_tracks_to_playlist(
    playlist_id="playlist_123",
    track_ids=["track_1", "track_2", "track_3"]
)
```

## Playlist Creation Workflows

### By Artist/Band Name

Create a playlist containing all or most popular tracks by a specific artist:

```python
# Search for artist
artists = client.search_artists(query="The Beatles", limit=1)
artist_id = artists[0]['id']

# Get artist's top tracks
tracks = client.get_artist_top_tracks(artist_id=artist_id, limit=50)
track_ids = [t['id'] for t in tracks]

# Create playlist and add tracks
playlist = client.create_playlist(name="The Beatles Collection")
client.add_tracks_to_playlist(playlist['id'], track_ids)
```

### By Theme/Mood

Create thematic playlists by searching for tracks matching mood keywords:

```python
# Search by theme
theme_queries = [
    "genre:indie mood:chill",
    "genre:indie year:2020-2024"
]

all_tracks = []
for query in theme_queries:
    results = client.search_tracks(query=query, limit=50)
    all_tracks.extend(results)

# Create playlist with theme-matched tracks
playlist = client.create_playlist(name="Chill Indie Evening")
track_ids = [t['id'] for t in all_tracks[:100]]
client.add_tracks_to_playlist(playlist['id'], track_ids)
```

### By Lyrics Content

Search for tracks with specific lyrical themes using Spotify's search:

```python
# Search by lyrical content (Spotify search can include lyrics)
queries = ["love", "heartbreak", "summer", "midnight"]
all_tracks = []

for keyword in queries:
    results = client.search_tracks(query=keyword, limit=20)
    all_tracks.extend(results)

# Remove duplicates and create playlist
unique_track_ids = list(set(t['id'] for t in all_tracks))
playlist = client.create_playlist(name="Love & Heartbreak")
client.add_tracks_to_playlist(playlist['id'], unique_track_ids[:100])
```

### From Specific Song List

Create a playlist from a user-provided list of track URIs or search terms:

```python
# User provides song names or URIs
song_list = ["Shape of You", "Blinding Lights", "As It Was"]

track_ids = []
for song_name in song_list:
    results = client.search_tracks(query=song_name, limit=1)
    if results:
        track_ids.append(results[0]['id'])

# Create playlist
playlist = client.create_playlist(name="My Favorites")
client.add_tracks_to_playlist(playlist['id'], track_ids)
```

## Advanced Operations

### Get Recommendations

```python
# Get recommendations based on seed artists/tracks
recommendations = client.get_recommendations(
    seed_artists=["artist_id_1"],
    seed_tracks=["track_id_1"],
    limit=50
)
```

### Access User Profile

```python
profile = client.get_current_user()
# Returns: user_id, display_name, email, followers, images, etc.
```

### Get User's Top Items

```python
top_artists = client.get_top_items(
    item_type="artists",
    limit=20,
    time_range="medium_term"  # short_term, medium_term, long_term
)

top_tracks = client.get_top_items(
    item_type="tracks",
    limit=20,
    time_range="short_term"
)
```

### Playback Control

```python
# Start playback
client.start_playback(
    device_id="device_123",
    context_uri="spotify:playlist:playlist_id",
    offset=0
)

# Pause
client.pause_playback(device_id="device_123")

# Skip to next
client.next_track(device_id="device_123")

# Get currently playing
current = client.get_currently_playing()
```

## Authentication & Credentials

See `references/authentication_guide.md` for detailed OAuth flow setup and credential management. Ensure credentials are available in environment variables or passed at initialization:

- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REDIRECT_URI`
- `SPOTIFY_ACCESS_TOKEN` (optional, can use refresh token)
- `SPOTIFY_REFRESH_TOKEN` (for token refresh)

## API Reference

See `references/api_reference.md` for complete Spotify API endpoint documentation, rate limits, response formats, and error handling patterns.

## Scripts

### spotify_client.py

Comprehensive Python wrapper for all Spotify Web API operations. Handles authentication, token management, rate limiting, and provides methods for:
- Authentication and token refresh
- Playlist CRUD operations
- Search (tracks, artists, albums, playlists)
- Track/URI management
- User data access
- Playback control
- Recommendations engine

### playlist_creator.py

High-level utility for intelligent playlist creation from various sources (artist, theme, lyrics, song list). Encapsulates common workflows and handles track deduplication and limit management.


