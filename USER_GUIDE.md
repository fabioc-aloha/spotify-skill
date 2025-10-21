# Spotify API Skill - Complete User Guide

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation & Setup](#installation--setup)
4. [Authentication](#authentication)
5. [Basic Usage](#basic-usage)
6. [Playlist Management](#playlist-management)
7. [Intelligent Playlist Creation](#intelligent-playlist-creation)
8. [Search & Discovery](#search--discovery)
9. [Playback Control](#playback-control)
10. [User Library Management](#user-library-management)
11. [Advanced Features](#advanced-features)
12. [Troubleshooting](#troubleshooting)
13. [API Reference](#api-reference)

---

## Overview

The Spotify API Skill enables you to interact with Spotify programmatically through Python. This skill provides:

- ✅ **Complete Spotify API access** - 40+ methods covering all major operations
- ✅ **OAuth 2.0 authentication** - Secure, automatic token refresh
- ✅ **Intelligent playlist creation** - 5 different creation strategies
- ✅ **Search & discovery** - Find tracks, artists, albums, playlists
- ✅ **Playback control** - Control what's playing on your devices
- ✅ **Library management** - Manage saved tracks and playlists

### What You Can Do

- Create playlists from artist names, themes, moods, or song lists
- Search for music across Spotify's entire catalog
- Control playback on any Spotify-connected device
- Access your listening history and top items
- Get personalized recommendations
- Manage your music library

---

## Prerequisites

### Required

- **Python 3.7+** installed on your system
- **Spotify Account** (Free or Premium)
  - Premium required for playback control features
  - Free account works for playlist management and search
- **Spotify Developer App** credentials
- **Internet connection** for API access

### Python Dependencies

```bash
pip install requests
```

That's it! The skill only requires the `requests` library for HTTP operations.

---

## Installation & Setup

### Step 1: Create Spotify Developer App

1. Go to https://developer.spotify.com/dashboard
2. Log in with your Spotify account
3. Click **"Create app"**
4. Fill in the details:
   - **App name**: Choose any name (e.g., "My Playlist Manager")
   - **App description**: Brief description (e.g., "Python playlist automation")
   - **Redirect URI**: `http://localhost:8888/callback`
5. Check the box to agree to terms
6. Click **"Save"**
7. On your app's page, click **"Settings"**
8. Copy your **Client ID** and **Client Secret**

### Step 2: Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:SPOTIFY_CLIENT_ID = "your_client_id_here"
$env:SPOTIFY_CLIENT_SECRET = "your_client_secret_here"
$env:SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
```

**macOS/Linux (Bash):**
```bash
export SPOTIFY_CLIENT_ID="your_client_id_here"
export SPOTIFY_CLIENT_SECRET="your_client_secret_here"
export SPOTIFY_REDIRECT_URI="http://localhost:8888/callback"
```

**Permanent Setup (Optional):**

Add these to your shell profile (`~/.bashrc`, `~/.zshrc`, or PowerShell profile):
```bash
export SPOTIFY_CLIENT_ID="your_client_id_here"
export SPOTIFY_CLIENT_SECRET="your_client_secret_here"
export SPOTIFY_REDIRECT_URI="http://localhost:8888/callback"
export SPOTIFY_REFRESH_TOKEN="your_refresh_token_here"  # After initial auth
```

### Step 3: Install the Skill

Copy the `spotify-api` folder to your project or Python path:

```bash
# Option 1: Copy to your project
cp -r spotify-api/scripts /your/project/path/

# Option 2: Add to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/spotify-api/scripts"
```

---

## Authentication

### Initial Authentication (One-Time Setup)

Run this code once to get your refresh token:

```python
import os
import webbrowser
from spotify_client import SpotifyClient

# Initialize client
client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI")
)

# Get authorization URL
auth_url = client.get_authorization_url()
print(f"Opening browser for authorization...")
print(f"If browser doesn't open, visit: {auth_url}")
webbrowser.open(auth_url)

# After authorizing, you'll be redirected to:
# http://localhost:8888/callback?code=XXXXXXX
auth_code = input("Paste the 'code' parameter from the URL: ")

# Exchange code for tokens
token_data = client.get_access_token(auth_code)
print(f"\n✅ Authentication successful!")
print(f"Refresh Token: {token_data['refresh_token']}")
print(f"\nSave this refresh token in your environment variables:")
print(f"export SPOTIFY_REFRESH_TOKEN=\"{token_data['refresh_token']}\"")
```

### Using Refresh Token (Recommended)

After initial setup, use your refresh token for automatic authentication:

```python
import os
from spotify_client import SpotifyClient

client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    refresh_token=os.getenv("SPOTIFY_REFRESH_TOKEN")
)

# Token refreshes automatically when needed
```

### Required Scopes

The skill requests these permissions:
- `playlist-modify-public` - Create/edit public playlists
- `playlist-modify-private` - Create/edit private playlists
- `user-library-read` - Read saved tracks
- `user-library-modify` - Save/remove tracks
- `user-read-private` - Read user profile
- `user-read-email` - Read email
- `user-top-read` - Read top tracks/artists
- `user-read-currently-playing` - See what's playing
- `user-modify-playback-state` - Control playback (Premium only)
- `user-read-playback-state` - Read playback state

---

## Basic Usage

### Initialize Client

```python
import os
from spotify_client import SpotifyClient

# Create client
client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    refresh_token=os.getenv("SPOTIFY_REFRESH_TOKEN")
)

# Tokens refresh automatically - you're ready to go!
```

### Get Your Profile

```python
profile = client.get_current_user()
print(f"👤 Logged in as: {profile['display_name']}")
print(f"📧 Email: {profile['email']}")
print(f"👥 Followers: {profile['followers']['total']}")
```

### List Your Playlists

```python
playlists = client.get_user_playlists(limit=50)
for playlist in playlists:
    print(f"📋 {playlist['name']}")
    print(f"   Tracks: {playlist['tracks']['total']}")
    print(f"   Public: {playlist['public']}")
    print()
```

---

## Playlist Management

### Create a Playlist

```python
playlist = client.create_playlist(
    name="My New Playlist",
    description="Created with Spotify API",
    public=True  # Set False for private
)

print(f"✅ Created: {playlist['name']}")
print(f"🔗 URL: {playlist['external_urls']['spotify']}")
```

### Update Playlist Details

```python
client.update_playlist(
    playlist_id="playlist_id_here",
    name="Updated Playlist Name",
    description="New description",
    public=False  # Make it private
)
```

### Add Tracks to Playlist

```python
# Add tracks by ID
track_ids = ["track_id_1", "track_id_2", "track_id_3"]
client.add_tracks_to_playlist(
    playlist_id="playlist_id_here",
    track_ids=track_ids
)

# Add at specific position
client.add_tracks_to_playlist(
    playlist_id="playlist_id_here",
    track_ids=track_ids,
    position=0  # Add at the beginning
)
```

### Remove Tracks from Playlist

```python
track_ids_to_remove = ["track_id_1", "track_id_2"]
client.remove_tracks_from_playlist(
    playlist_id="playlist_id_here",
    track_ids=track_ids_to_remove
)
```

### Get Playlist Tracks

```python
tracks = client.get_playlist_tracks(
    playlist_id="playlist_id_here",
    limit=50,
    offset=0
)

for item in tracks:
    track = item['track']
    print(f"🎵 {track['name']} - {track['artists'][0]['name']}")
```

### Delete (Unfollow) Playlist

```python
client.delete_playlist(playlist_id="playlist_id_here")
```

---

## Intelligent Playlist Creation

The `PlaylistCreator` class provides high-level methods for creating playlists intelligently.

### Setup

```python
from playlist_creator import PlaylistCreator
from spotify_client import SpotifyClient
import os

client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    refresh_token=os.getenv("SPOTIFY_REFRESH_TOKEN")
)

creator = PlaylistCreator(client)
```

### Method 1: Create from Artist

Build a playlist from an artist's top tracks:

```python
result = creator.create_from_artist(
    artist_name="Taylor Swift",
    playlist_name="Taylor Swift Essentials",  # Optional
    playlist_description="Top tracks from Taylor Swift",
    public=True,
    limit=50
)

print(f"✅ Created '{result['playlist']['name']}'")
print(f"🎵 Added {result['tracks_added']} tracks")
print(f"🎤 Artist: {result['artist']}")
```

### Method 2: Create from Theme/Mood

Build a playlist based on mood or genre keywords:

```python
result = creator.create_from_theme(
    theme_keywords=["chill", "indie", "acoustic"],
    playlist_name="Chill Indie Vibes",
    playlist_description="Relaxing indie acoustic music",
    public=True,
    limit=100
)

print(f"✅ Created '{result['playlist']['name']}'")
print(f"🎵 Added {result['tracks_added']} tracks")
print(f"🏷️ Keywords: {', '.join(result['keywords'])}")
```

**Advanced Theme Queries:**

```python
# Combine genre and year
result = creator.create_from_theme(
    theme_keywords=["genre:indie year:2020-2024"],
    playlist_name="Recent Indie Hits"
)

# Mood-based
result = creator.create_from_theme(
    theme_keywords=["mood:happy", "mood:energetic"],
    playlist_name="Good Vibes Only"
)

# Multiple attributes
result = creator.create_from_theme(
    theme_keywords=["genre:electronic mood:chill tempo:slow"],
    playlist_name="Chill Electronic"
)
```

### Method 3: Create from Lyrics

Search for tracks with specific lyrical themes:

```python
result = creator.create_from_lyrics(
    lyric_keywords=["love", "heartbreak", "summer"],
    playlist_name="Love & Summer",
    playlist_description="Songs about love and summer",
    public=True,
    limit=80
)

print(f"✅ Created '{result['playlist']['name']}'")
print(f"🎵 Added {result['tracks_added']} tracks")
```

### Method 4: Create from Song List

Build a playlist from specific song names:

```python
song_list = [
    "Shape of You - Ed Sheeran",
    "Blinding Lights - The Weeknd",
    "As It Was - Harry Styles",
    "Anti-Hero - Taylor Swift",
    "Flowers - Miley Cyrus"
]

result = creator.create_from_song_list(
    song_list=song_list,
    playlist_name="My Favorites 2023",
    playlist_description="Personal favorites",
    public=False
)

print(f"✅ Created '{result['playlist']['name']}'")
print(f"🎵 Found {result['tracks_found']} tracks")
if result['not_found_songs']:
    print(f"⚠️ Could not find: {', '.join(result['not_found_songs'])}")
```

### Method 5: Create from Recommendations

Get AI-powered recommendations and create a playlist:

```python
# First, get some seed tracks or artists
top_tracks = client.get_top_items(item_type="tracks", limit=5)
seed_track_ids = [t['id'] for t in top_tracks[:2]]

# Create playlist from recommendations
result = creator.create_from_recommendations(
    playlist_name="Discover Weekly (Custom)",
    seed_tracks=seed_track_ids,
    seed_genres=["indie", "alternative"],
    playlist_description="Personalized recommendations",
    public=True,
    limit=50
)

print(f"✅ Created '{result['playlist']['name']}'")
print(f"🎵 Added {result['tracks_added']} tracks")
```

### Get Playlist Statistics

```python
stats = creator.get_playlist_stats(playlist_id="playlist_id_here")

print(f"📋 Playlist: {stats['name']}")
print(f"🎵 Total Tracks: {stats['total_tracks']}")
print(f"⏱️ Duration: {stats['total_duration_minutes']} minutes")
print(f"👤 Owner: {stats['owner']}")
print(f"👥 Followers: {stats['followers']}")
print(f"🔓 Public: {stats['public']}")
```

---

## Search & Discovery

### Search for Tracks

```python
# Simple search
tracks = client.search_tracks(query="love", limit=20)
for track in tracks:
    artist = track['artists'][0]['name']
    print(f"🎵 {track['name']} - {artist}")

# Advanced search with filters
tracks = client.search_tracks(query="artist:Beatles year:1960-1970", limit=50)
```

### Search for Artists

```python
artists = client.search_artists(query="Taylor Swift", limit=10)
for artist in artists:
    print(f"🎤 {artist['name']}")
    print(f"   Popularity: {artist['popularity']}/100")
    print(f"   Followers: {artist['followers']['total']:,}")
```

### Search for Albums

```python
albums = client.search_albums(query="Dark Side of the Moon", limit=10)
for album in albums:
    print(f"💿 {album['name']} - {album['artists'][0]['name']}")
    print(f"   Released: {album['release_date']}")
```

### Search for Playlists

```python
playlists = client.search_playlists(query="workout motivation", limit=20)
for playlist in playlists:
    print(f"📋 {playlist['name']}")
    print(f"   Tracks: {playlist['tracks']['total']}")
    print(f"   By: {playlist['owner']['display_name']}")
```

### Multi-Type Search

```python
results = client.search(
    query="jazz",
    types=["track", "artist", "album", "playlist"],
    limit=10
)

print("Tracks:", len(results.get('tracks', {}).get('items', [])))
print("Artists:", len(results.get('artists', {}).get('items', [])))
print("Albums:", len(results.get('albums', {}).get('items', [])))
print("Playlists:", len(results.get('playlists', {}).get('items', [])))
```

### Get Recommendations

```python
# Get recommendations based on seeds
recommendations = client.get_recommendations(
    seed_artists=["artist_id_1"],
    seed_tracks=["track_id_1"],
    seed_genres=["indie", "alternative"],
    limit=50
)

for track in recommendations:
    print(f"🎵 {track['name']} - {track['artists'][0]['name']}")

# Get available genres for seeds
genres = client.get_available_genres()
print(f"Available genres: {', '.join(genres[:20])}...")
```

### Get Artist Information

```python
# Get artist details
artist = client.get_artist(artist_id="artist_id_here")
print(f"🎤 {artist['name']}")
print(f"🎭 Genres: {', '.join(artist['genres'])}")
print(f"⭐ Popularity: {artist['popularity']}/100")

# Get artist's top tracks
top_tracks = client.get_artist_top_tracks(artist_id="artist_id_here")
for track in top_tracks[:10]:
    print(f"🎵 {track['name']}")

# Get related artists
related = client.get_related_artists(artist_id="artist_id_here", limit=10)
for artist in related:
    print(f"🎤 {artist['name']}")

# Get artist's albums
albums = client.get_artist_albums(artist_id="artist_id_here", limit=50)
for album in albums:
    print(f"💿 {album['name']} ({album['release_date']})")
```

---

## Playback Control

**Note:** Playback control features require **Spotify Premium**.

### Get Available Devices

```python
devices = client.get_available_devices()
for device in devices:
    print(f"🔊 {device['name']} ({device['type']})")
    print(f"   Active: {device['is_active']}")
    print(f"   Volume: {device['volume_percent']}%")
    print(f"   ID: {device['id']}")
```

### Get Currently Playing

```python
current = client.get_currently_playing()
if current and 'item' in current:
    track = current['item']
    artist = track['artists'][0]['name']
    print(f"🎵 Now Playing: {track['name']} - {artist}")
    print(f"⏱️ Progress: {current['progress_ms'] // 1000}s / {track['duration_ms'] // 1000}s")
    print(f"🔀 Shuffle: {current['shuffle_state']}")
    print(f"🔁 Repeat: {current['repeat_state']}")
else:
    print("Nothing is currently playing")
```

### Start Playback

```python
# Play specific tracks
track_uris = [
    "spotify:track:track_id_1",
    "spotify:track:track_id_2"
]
client.start_playback(
    device_id="device_id_here",  # Optional
    track_uris=track_uris
)

# Play from a playlist/album (context)
client.start_playback(
    device_id="device_id_here",
    context_uri="spotify:playlist:playlist_id_here",
    offset=0  # Start from first track
)
```

### Pause Playback

```python
client.pause_playback(device_id="device_id_here")  # device_id optional
```

### Skip Tracks

```python
# Next track
client.next_track(device_id="device_id_here")

# Previous track
client.previous_track(device_id="device_id_here")
```

### Seek to Position

```python
# Seek to 1 minute 30 seconds (90000 milliseconds)
client.seek_to_position(position_ms=90000, device_id="device_id_here")
```

### Control Repeat Mode

```python
# Options: "off", "context" (playlist/album), "track"
client.set_repeat_mode(state="context", device_id="device_id_here")
```

### Control Shuffle

```python
# Enable shuffle
client.set_shuffle(state=True, device_id="device_id_here")

# Disable shuffle
client.set_shuffle(state=False, device_id="device_id_here")
```

### Set Volume

```python
# Set volume to 50%
client.set_volume(volume_percent=50, device_id="device_id_here")
```

---

## User Library Management

### Get Saved Tracks

```python
saved = client.get_saved_tracks(limit=50, offset=0)
for item in saved:
    track = item['track']
    print(f"💚 {track['name']} - {track['artists'][0]['name']}")
    print(f"   Added: {item['added_at']}")
```

### Save Tracks

```python
track_ids = ["track_id_1", "track_id_2", "track_id_3"]
client.save_tracks(track_ids)
print("✅ Tracks saved to library")
```

### Remove Saved Tracks

```python
track_ids = ["track_id_1", "track_id_2"]
client.remove_saved_tracks(track_ids)
print("🗑️ Tracks removed from library")
```

### Check if Tracks Are Saved

```python
track_ids = ["track_id_1", "track_id_2", "track_id_3"]
saved_status = client.check_saved_tracks(track_ids)
for track_id, is_saved in zip(track_ids, saved_status):
    status = "💚 Saved" if is_saved else "❌ Not saved"
    print(f"{track_id}: {status}")
```

### Get Top Tracks

```python
# Time ranges: "short_term" (4 weeks), "medium_term" (6 months), "long_term" (all time)
top_tracks = client.get_top_items(
    item_type="tracks",
    limit=50,
    time_range="medium_term"
)

for i, track in enumerate(top_tracks, 1):
    print(f"{i}. 🎵 {track['name']} - {track['artists'][0]['name']}")
```

### Get Top Artists

```python
top_artists = client.get_top_items(
    item_type="artists",
    limit=50,
    time_range="long_term"
)

for i, artist in enumerate(top_artists, 1):
    print(f"{i}. 🎤 {artist['name']}")
    print(f"   Genres: {', '.join(artist['genres'][:3])}")
```

---

## Advanced Features

### Get Track Details

```python
track = client.get_track(track_id="track_id_here")
print(f"🎵 {track['name']}")
print(f"🎤 Artist: {track['artists'][0]['name']}")
print(f"💿 Album: {track['album']['name']}")
print(f"⏱️ Duration: {track['duration_ms'] // 1000}s")
print(f"⭐ Popularity: {track['popularity']}/100")
print(f"🔗 URL: {track['external_urls']['spotify']}")
```

### Get Multiple Tracks

```python
track_ids = ["track_id_1", "track_id_2", "track_id_3"]
tracks = client.get_tracks(track_ids)
for track in tracks:
    print(f"🎵 {track['name']} - {track['artists'][0]['name']}")
```

### Get Audio Features

```python
features = client.get_track_audio_features(track_id="track_id_here")
print(f"🎹 Key: {features['key']}")
print(f"🎼 Mode: {features['mode']}")
print(f"⏱️ Tempo: {features['tempo']} BPM")
print(f"🔊 Loudness: {features['loudness']} dB")
print(f"🎭 Energy: {features['energy']}")
print(f"💃 Danceability: {features['danceability']}")
print(f"🎺 Instrumentalness: {features['instrumentalness']}")
print(f"😊 Valence (happiness): {features['valence']}")
```

### Get Album Information

```python
album = client.get_album(album_id="album_id_here")
print(f"💿 {album['name']}")
print(f"🎤 Artist: {album['artists'][0]['name']}")
print(f"📅 Released: {album['release_date']}")
print(f"🎵 Tracks: {album['total_tracks']}")
print(f"🎭 Genres: {', '.join(album['genres']) if album['genres'] else 'N/A'}")

# Get album tracks
tracks = client.get_album_tracks(album_id="album_id_here")
for track in tracks:
    print(f"  {track['track_number']}. {track['name']}")
```

### Pagination Example

```python
# Get all user playlists (handling pagination)
all_playlists = []
offset = 0
limit = 50

while True:
    batch = client.get_user_playlists(limit=limit, offset=offset)
    if not batch:
        break
    all_playlists.extend(batch)
    offset += limit
    if len(batch) < limit:
        break

print(f"Total playlists: {len(all_playlists)}")
```

---

## Troubleshooting

### Common Issues

#### "No module named 'spotify_client'"

**Solution:** Ensure you're in the correct directory or add to Python path:
```python
import sys
sys.path.append('/path/to/spotify-api/scripts')
```

#### "Invalid client_id or client_secret"

**Solutions:**
1. Verify credentials in Spotify Dashboard
2. Check environment variables are set correctly:
   ```python
   import os
   print(os.getenv("SPOTIFY_CLIENT_ID"))
   ```
3. Ensure no extra spaces or quotes in credentials

#### "Token expired" or "Unauthorized"

**Solutions:**
1. Refresh your token:
   ```python
   client.refresh_access_token()
   ```
2. Check your refresh token is valid
3. Re-authenticate if refresh token is invalid

#### "429 Rate Limit Exceeded"

**Solutions:**
1. Add delays between requests:
   ```python
   import time
   time.sleep(1)  # Wait 1 second
   ```
2. Use batch operations when possible (up to 50-100 items)
3. Implement exponential backoff for retries

#### "No active device found"

**Solutions:**
1. Open Spotify on any device (phone, desktop, web player)
2. Start playing something briefly
3. Check available devices:
   ```python
   devices = client.get_available_devices()
   print(devices)
   ```

#### "Premium required" for playback control

**Solution:** Playback control features require Spotify Premium. Playlist management and search work with free accounts.

### Debugging Tips

**Enable verbose logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check API response:**
```python
try:
    result = client.get_user_playlists()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

**Verify token status:**
```python
import time
if client.token_expires_at:
    remaining = client.token_expires_at - time.time()
    print(f"Token expires in {remaining:.0f} seconds")
```

---

## API Reference

### SpotifyClient Methods

#### Authentication
- `get_authorization_url(scope)` - Generate OAuth URL
- `get_access_token(auth_code)` - Exchange code for token
- `refresh_access_token(refresh_token)` - Refresh expired token

#### Playlists
- `get_user_playlists(limit, offset)` - List user's playlists
- `create_playlist(name, description, public)` - Create new playlist
- `get_playlist(playlist_id)` - Get playlist details
- `update_playlist(playlist_id, name, description, public)` - Update playlist
- `delete_playlist(playlist_id)` - Unfollow playlist
- `get_playlist_tracks(playlist_id, limit, offset)` - Get tracks
- `add_tracks_to_playlist(playlist_id, track_ids, position)` - Add tracks
- `remove_tracks_from_playlist(playlist_id, track_ids)` - Remove tracks

#### Search
- `search_tracks(query, limit)` - Search tracks
- `search_artists(query, limit)` - Search artists
- `search_albums(query, limit)` - Search albums
- `search_playlists(query, limit)` - Search playlists
- `search(query, types, limit)` - Multi-type search

#### Artists
- `get_artist(artist_id)` - Get artist details
- `get_artist_top_tracks(artist_id, market, limit)` - Artist's top tracks
- `get_related_artists(artist_id, limit)` - Related artists
- `get_artist_albums(artist_id, limit, offset)` - Artist's albums

#### Tracks
- `get_track(track_id)` - Get track details
- `get_tracks(track_ids)` - Get multiple tracks
- `get_track_audio_features(track_id)` - Audio features

#### Albums
- `get_album(album_id)` - Get album details
- `get_album_tracks(album_id, limit, offset)` - Album tracks

#### User
- `get_current_user()` - Current user profile
- `get_user(user_id)` - User profile by ID
- `get_top_items(item_type, limit, offset, time_range)` - Top tracks/artists

#### Library
- `get_saved_tracks(limit, offset)` - Saved tracks
- `save_tracks(track_ids)` - Save tracks
- `remove_saved_tracks(track_ids)` - Remove saved tracks
- `check_saved_tracks(track_ids)` - Check if saved

#### Recommendations
- `get_recommendations(seed_artists, seed_tracks, seed_genres, limit)` - Get recommendations
- `get_available_genres()` - Available genre seeds

#### Playback (Premium only)
- `get_currently_playing()` - Currently playing track
- `get_available_devices()` - Available devices
- `start_playback(device_id, context_uri, track_uris, offset)` - Start playback
- `pause_playback(device_id)` - Pause
- `next_track(device_id)` - Next track
- `previous_track(device_id)` - Previous track
- `seek_to_position(position_ms, device_id)` - Seek
- `set_repeat_mode(state, device_id)` - Set repeat
- `set_shuffle(state, device_id)` - Set shuffle
- `set_volume(volume_percent, device_id)` - Set volume

### PlaylistCreator Methods

- `create_from_artist(artist_name, playlist_name, playlist_description, public, limit)` - Create from artist
- `create_from_theme(theme_keywords, playlist_name, playlist_description, public, limit)` - Create from theme
- `create_from_lyrics(lyric_keywords, playlist_name, playlist_description, public, limit)` - Create from lyrics
- `create_from_song_list(song_list, playlist_name, playlist_description, public)` - Create from song list
- `create_from_recommendations(playlist_name, seed_artists, seed_tracks, seed_genres, playlist_description, public, limit)` - Create from recommendations
- `get_playlist_stats(playlist_id)` - Get playlist statistics

---

## Rate Limits & Best Practices

### Spotify API Limits

- **Rate Limit**: ~180 requests per minute per user
- **Batch Limits**:
  - 50 tracks per search request
  - 100 tracks per playlist add/remove
  - 50 items for most bulk operations
- **Total Seeds**: Max 5 (artists + tracks + genres combined)

### Best Practices

1. **Use batch operations** when possible
2. **Implement retry logic** with exponential backoff
3. **Cache results** when appropriate
4. **Handle pagination** for large result sets
5. **Store refresh token securely** (never commit to git)
6. **Use environment variables** for credentials
7. **Check token expiry** before long-running operations

---

## Additional Resources

- **Official Spotify API Docs**: https://developer.spotify.com/documentation/web-api
- **Authentication Guide**: See `references/authentication_guide.md`
- **API Reference**: See `references/api_reference.md`
- **Skill Creation Guide**: See `Guide/SKILL_CREATION_GUIDE.md`

---

## Support & Contributing

### Getting Help

1. Check this user guide
2. Review `references/authentication_guide.md` for auth issues
3. Check `references/api_reference.md` for API details
4. See `TROUBLESHOOTING` section above

### Reporting Issues

When reporting issues, include:
- Python version
- Error message and stack trace
- Code snippet that reproduces the issue
- Spotify account type (Free/Premium)

---

**Version**: 1.0
**Last Updated**: October 21, 2025
**License**: See project LICENSE file
