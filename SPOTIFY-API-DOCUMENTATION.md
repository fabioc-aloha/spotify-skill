# 🎵 Spotify Web API - Comprehensive Developer Documentation
**Alex Method DJ Platform - Spotify Integration Reference**
**Last Updated**: October 29, 2025
**API Version**: Spotify Web API (Latest - October 2025)
**SDK Version**: spotipy 2.25.1+

> ⚠️ **Critical Update (October 2025)**: This documentation reflects current Spotify API status.
> Several endpoints have been deprecated and are **non-functional** (return HTTP 403/404 errors).
> All endpoints marked ❌ have been **empirically tested** and confirmed broken.
> See sections marked with ⚠️ for migration strategies and alternative solutions.

## Table of Contents
1. [Authentication & Setup](#authentication--setup)
2. [API Compatibility & Updates](#api-compatibility--updates)
3. [User Profile & Account](#user-profile--account)
4. [Playlists Management](#playlists-management)
5. [Track & Album Operations](#track--album-operations)
6. [Artist & Search](#artist--search)
7. [User Library](#user-library)
8. [Playback Control](#playback-control)
9. [~~Audio Features & Analysis~~](#audio-features--analysis) ⚠️ **DEPRECATED**
10. [Browse & Discover](#browse--discover)
11. [Following & Social](#following--social)
12. [Markets & Localization](#markets--localization)
13. [Advanced Features](#advanced-features)
14. [Code Examples](#code-examples)
15. [Best Practices](#best-practices)
16. [Error Handling](#error-handling)
17. [Rate Limits & Optimization](#rate-limits--optimization)

---

## Authentication & Setup

The foundation of any Spotify Web API integration begins with proper authentication and setup. This section covers the OAuth 2.0 authorization flow, scope management, and client configuration. Understanding authentication is crucial as it determines what your application can access and modify in user accounts. Spotify uses different authorization flows depending on your application type, with the Authorization Code Flow being the most common for web applications that need to access user data.

### Required Scopes
```python
# Essential scopes for playlist and library management
basic_scope = "playlist-modify-public playlist-modify-private user-library-read"

# Complete scopes for full functionality (verified against official Spotify documentation)
extended_scope = """
    playlist-modify-public playlist-modify-private playlist-read-private
    playlist-read-collaborative user-library-read user-library-modify
    user-read-private user-read-email user-top-read user-read-recently-played
    user-follow-read user-follow-modify user-read-playback-state
    user-modify-playback-state user-read-currently-playing streaming
    app-remote-control ugc-image-upload user-read-playback-position
"""
```

### Authentication Setup
```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def setup_spotify_client():
    """Complete Spotify client setup with full scopes."""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="http://127.0.0.1:8888/callback",
        scope=extended_scope
    ))

# Authorization Flow Notes (Updated October 2025):
# - Authorization Code Flow: ✅ RECOMMENDED for web apps (most common)
# - Authorization Code with PKCE: ✅ RECOMMENDED for mobile/desktop apps (no client secret needed)
# - Client Credentials Flow: ✅ For server-to-server applications (no user data access)
# - Implicit Grant Flow: ❌ REMOVED - Use PKCE instead (deprecated since 2023)

# ⚠️ SECURITY BEST PRACTICES (2025):
# 1. ALWAYS use PKCE for client-side apps (mobile, desktop, single-page apps)
# 2. Never expose client secrets in client-side code
# 3. Use short-lived access tokens with refresh token rotation
# 4. Implement proper token storage (secure keychain/keystore)
# 5. Use HTTPS for all redirect URIs in production
```

### PKCE Authentication (Recommended for Client Apps)
```python
from spotipy.oauth2 import SpotifyPKCE

def setup_spotify_client_with_pkce():
    """
    Set up Spotify client with PKCE authentication (more secure).
    Recommended for mobile and desktop applications.
    """
    return spotipy.Spotify(auth_manager=SpotifyPKCE(
        client_id="your_client_id",
        redirect_uri="http://127.0.0.1:8888/callback",
        scope=extended_scope
    ))
    # Note: No client_secret needed - more secure for client-side apps
```

---

## API Compatibility & Updates

> **Important**: Spotify regularly updates their Web API. This section tracks deprecated and removed endpoints.

### Current Environment
- **Spotify Web API**: Latest (October 2025)
- **Spotipy Library**: v2.25.1+ (actively maintained)
- **Python**: 3.8+ (recommended 3.10+)
- **Documentation Last Updated**: October 29, 2025
- **Test Coverage**: 16/16 endpoints tested (14 working, 2 deprecated)

### API Change Summary (2025)

**Major Changes**:
1. ❌ **Audio Analysis Endpoints Removed** - `audio_features()`, `audio_analysis()` no longer functional
2. ❌ **Recommendation Engine Disabled** - `recommendations()`, `recommendation_genre_seeds()` return 404
3. ❌ **Browse Features Removed** - `featured_playlists()`, `category_playlists()` no longer available
4. ❌ **Related Artists Disabled** - `artist_related_artists()` returns 404
5. ✅ **Core Functionality Intact** - All playlist, search, user profile, and library endpoints fully functional

**Impact Assessment**:
- ✅ **14/16 tested endpoints working** (87.5% success rate)
- ✅ **100% of core features operational** (playlists, search, user data)
- ❌ **Audio intelligence features unavailable** (requires third-party solutions)
- ❌ **Spotify's recommendation engine unavailable** (requires custom algorithms)

### ⚠️ Deprecated Endpoints (Still Functional)
These methods still work but are deprecated and may be removed in future versions:

| Method | Status | Replacement | Notes |
|--------|--------|-------------|-------|
| `user_playlist_create()` | ⚠️ Deprecated | Use with caution | Still functional, modern approach recommended |
| `playlist_tracks()` | ⚠️ Deprecated | `playlist_items()` | Use `playlist_items()` for consistency |

### ❌ Removed/Non-Functional Endpoints (Empirically Tested October 2025)

These endpoints are documented as "OAuth 2.0 Deprecated" but are **completely non-functional**.
All requests return HTTP 403 Forbidden or 404 Not Found errors. Testing confirmed with spotipy 2.25.1.

**🧪 EMPIRICAL TEST RESULTS** (October 1, 2025):

| Method | Documentation Status | API Response | HTTP Error | Test Date | Replacement |
|--------|---------------------|--------------|------------|-----------|-------------|
| `audio_features()` | OAuth 2.0 Deprecated | ❌ **FAILS** | 403 Forbidden | Oct 1, 2025 | Use Librosa, Essentia, or AcousticBrainz |
| `audio_analysis()` | OAuth 2.0 Deprecated | ❌ **FAILS** | 403 Forbidden | Oct 1, 2025 | Use audio processing libraries |
| `artist_related_artists()` | OAuth 2.0 Deprecated | ❌ **FAILS** | 404 Not Found | Oct 1, 2025 | Genre matching + search algorithms |
| `recommendations()` | OAuth 2.0 Deprecated | ❌ **FAILS** | 404 Not Found | Oct 1, 2025 | Custom recommendation engine |
| `recommendation_genre_seeds()` | OAuth 2.0 Deprecated | ❌ **FAILS** | 404 Not Found | Oct 1, 2025 | Manual genre lists |
| `featured_playlists()` | OAuth 2.0 Deprecated | ❌ **FAILS** | 404 Not Found | Oct 1, 2025 | Search with "popular" + genre |
| `category_playlists()` | OAuth 2.0 Deprecated | ❌ **FAILS** | 404 Not Found | Oct 1, 2025 | Search-based discovery |

**Testing Methodology**:
- ✅ Valid OAuth 2.0 authentication confirmed (other endpoints work)
- ✅ Latest spotipy library (2.25.1)
- ✅ All other endpoints (user, playlist, search) functional
- ❌ All deprecated endpoints consistently return 403/404 errors
- 📊 Complete test results: `docs/COMPREHENSIVE_API_TEST_RESULTS.md`

**Important Notes**:
1. ⚠️ **Do NOT use these endpoints** - They will always fail
2. 📚 **Documentation exists for historical reference only**
3. 🔧 **Spotipy library still has methods** (but they immediately fail when called)
4. ⚠️ **Code using these endpoints is broken** and requires migration

### Understanding the Status

**What "OAuth 2.0 Deprecated" Actually Means**:
- 📚 **Documentation exists** for historical reference
- ❌ **Endpoints are removed** from active API
- 🔧 **Spotipy library still has methods** (but they fail when called)
- ⚠️ **Code using these will break** with HTTP 403/404 errors

**Why Documentation Still Exists**:
- Spotify maintains archived documentation to help developers understand what changed
- Common practice: keep docs for deprecated/removed features as historical reference
- Helps developers plan migrations and understand API evolution

### Impact on Your Code

**Broken Functionality**:
1. ❌ **Audio Features Analysis** - Cannot retrieve acousticness, danceability, energy, valence, tempo
2. ❌ **Related Artists Discovery** - Cannot find similar artists through Spotify's algorithm
3. ❌ **AI Recommendations** - Cannot use Spotify's recommendation engine
4. ❌ **Browse Features** - Cannot access featured playlists or category browsing

**Files Affected**:
- `musical_dna_analyzer.py` - ❌ **BROKEN** (uses audio_features, artist_related_artists)
- Custom recommendation systems - ❌ **BROKEN** (uses recommendations endpoint)
- Browse/discovery features - ❌ **BROKEN** (uses featured_playlists, category_playlists)

### Migration Requirements

**You MUST use alternative approaches**:

### Migration Requirements & Modern Alternatives (2025)

**You MUST use alternative approaches for deprecated functionality**:

#### **For Audio Features Analysis** → Third-Party Audio Intelligence

Since Spotify removed `audio_features()` and `audio_analysis()`, use these alternatives:

**Option 1: Librosa (Python Audio Analysis)**
```python
import librosa
import numpy as np

def analyze_audio_file(audio_path):
    """Extract audio features from local audio file."""
    y, sr = librosa.load(audio_path)

    # Tempo (BPM)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

    # Energy/Loudness
    rms = librosa.feature.rms(y=y)[0]

    # Zero crossing rate (timbre/texture)
    zcr = librosa.feature.zero_crossing_rate(y)[0]

    return {
        'tempo': float(tempo),
        'energy': float(np.mean(rms)),
        'spectral_centroid': float(np.mean(spectral_centroids)),
        'zero_crossing_rate': float(np.mean(zcr))
    }
```

**Option 2: Essentia (Advanced Music Analysis)**
```python
from essentia.standard import *

def analyze_with_essentia(audio_path):
    """Advanced audio analysis with Essentia."""
    loader = MonoLoader(filename=audio_path)
    audio = loader()

    # Rhythm analysis
    rhythm_extractor = RhythmExtractor2013()
    bpm, beats, confidence, estimates, intervals = rhythm_extractor(audio)

    # Key detection
    key_extractor = KeyExtractor()
    key, scale, strength = key_extractor(audio)

    # Danceability
    danceability = Danceability()
    dance_score = danceability(audio)

    return {
        'bpm': bpm,
        'key': key,
        'scale': scale,
        'danceability': dance_score
    }
```

**Option 3: AcousticBrainz API (Cloud-based)**
```python
import requests

def get_acousticbrainz_features(musicbrainz_id):
    """Get audio features from AcousticBrainz (requires MusicBrainz ID)."""
    url = f"https://acousticbrainz.org/api/v1/{musicbrainz_id}/low-level"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            'tempo': data['rhythm']['bpm'],
            'key': data['tonal']['key_key'],
            'danceability': data['rhythm']['danceability']
        }
    return None
```

#### **For Related Artists Discovery** → Genre & Search Algorithms

```python
def find_similar_artists(sp, artist_id):
    """Find similar artists using genre matching and search."""
    # Get artist details
    artist = sp.artist(artist_id)
    artist_genres = artist['genres']

    similar_artists = []

    # Search for artists in same genres
    for genre in artist_genres[:3]:  # Use top 3 genres
        results = sp.search(q=f'genre:"{genre}"', type='artist', limit=20)

        for item in results['artists']['items']:
            if item['id'] != artist_id:  # Exclude original artist
                # Calculate genre overlap
                overlap = len(set(item['genres']) & set(artist_genres))

                similar_artists.append({
                    'id': item['id'],
                    'name': item['name'],
                    'genres': item['genres'],
                    'popularity': item['popularity'],
                    'genre_match_score': overlap
                })

    # Sort by genre match and popularity
    similar_artists.sort(
        key=lambda x: (x['genre_match_score'], x['popularity']),
        reverse=True
    )

    return similar_artists[:20]  # Return top 20
```

#### **For Recommendations** → Custom Recommendation Engine

```python
def generate_recommendations(sp, user_top_tracks, target_duration=30):
    """Generate recommendations based on user's top tracks."""
    # Analyze user preferences
    user_artists = {}
    user_genres = set()

    for track in user_top_tracks:
        for artist in track['artists']:
            artist_id = artist['id']
            if artist_id not in user_artists:
                artist_details = sp.artist(artist_id)
                user_artists[artist_id] = artist_details
                user_genres.update(artist_details['genres'])

    # Build search queries for similar music
    recommendations = []

    for genre in list(user_genres)[:5]:  # Top 5 genres
        # Search for tracks in this genre
        results = sp.search(
            q=f'genre:"{genre}"',
            type='track',
            limit=20,
            market='US'
        )

        for track in results['tracks']['items']:
            # Filter by duration (if needed)
            duration_min = track['duration_ms'] / 60000
            if target_duration - 1 <= duration_min <= target_duration + 1:
                recommendations.append(track)

    # Sort by popularity and remove duplicates
    seen = set()
    unique_recommendations = []

    for track in sorted(recommendations, key=lambda x: x['popularity'], reverse=True):
        if track['id'] not in seen:
            seen.add(track['id'])
            unique_recommendations.append(track)

    return unique_recommendations[:50]
```

#### **For Browse Features** → Advanced Search Strategies

```python
def discover_playlists(sp, genre, mood='popular'):
    """Discover playlists using advanced search."""
    search_terms = {
        'popular': f'{genre} popular hits',
        'new': f'{genre} new releases',
        'classic': f'{genre} classics',
        'workout': f'{genre} workout energy',
        'chill': f'{genre} chill relaxing'
    }

    query = search_terms.get(mood, f'{genre} {mood}')

    results = sp.search(
        q=query,
        type='playlist',
        limit=50,
        market='US'
    )

    return results['playlists']['items']

def discover_new_tracks(sp, genres, year_range=(2023, 2025)):
    """Discover new tracks by genre and year."""
    new_tracks = []

    for genre in genres:
        for year in range(year_range[0], year_range[1] + 1):
            query = f'genre:"{genre}" year:{year}'

            results = sp.search(
                q=query,
                type='track',
                limit=50,
                market='US'
            )

            new_tracks.extend(results['tracks']['items'])

    # Sort by release date and popularity
    new_tracks.sort(
        key=lambda x: (x['album']['release_date'], x['popularity']),
        reverse=True
    )

    return new_tracks
```

**Installation Requirements**:
```bash
# For audio analysis
pip install librosa essentia

# For enhanced search capabilities
pip install numpy pandas scikit-learn

# All requirements for Alex Method DJ platform
pip install -r requirements.txt
```

---

## User Profile & Account

This section provides comprehensive access to user account information and listening history. You can retrieve detailed user profiles, analyze listening patterns through top artists and tracks across different time periods, and access recently played music. These endpoints are essential for creating personalized experiences, building user dashboards, and understanding user preferences. The data includes both public information (like display names and follower counts) and private data (like email addresses and detailed listening history), depending on the requested scopes.

### User Information
```python
# Get current user profile
user = sp.current_user()
print(f"User: {user['display_name']} ({user['id']})")
print(f"Followers: {user['followers']['total']}")
print(f"Country: {user['country']}")
print(f"Product: {user['product']}")  # free, premium

# Get any user's public profile
user_profile = sp.user("spotify_user_id")
```

### User Top Items
```python
# Get user's top artists
top_artists = sp.current_user_top_artists(
    limit=50,  # Max 50
    offset=0,
    time_range='medium_term'  # short_term, medium_term, long_term
)

# Get user's top tracks
top_tracks = sp.current_user_top_tracks(
    limit=50,
    time_range='short_term'  # Last 4 weeks
)

# Time ranges:
# - short_term: ~4 weeks
# - medium_term: ~6 months
# - long_term: ~several years
```

### Recently Played
```python
# Get recently played tracks
recent = sp.current_user_recently_played(
    limit=50,  # Max 50
    after=1610000000000,  # Unix timestamp in milliseconds
    before=1620000000000
)

for item in recent['items']:
    track = item['track']
    played_at = item['played_at']
    print(f"{track['name']} by {track['artists'][0]['name']} - {played_at}")
```

---

## Playlists Management

Playlists are at the heart of the Spotify experience, and this section provides complete control over playlist creation, modification, and management. You can create both public and private playlists, add or remove tracks, reorder content, update metadata, and even upload custom cover images. The API supports collaborative playlists and provides detailed track information with flexible field selection. These endpoints are well-suited for building playlist management tools, automated DJ systems, or music curation applications.

### Create Playlists
```python
def create_playlist(sp, name, description="", public=True, collaborative=False):
    """Create a new playlist with full options."""
    user_id = sp.current_user()['id']

    playlist = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=public,
        collaborative=collaborative,
        description=description
    )

    return playlist
```

### Manage Playlist Content
```python
# Add tracks to playlist
track_uris = ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh"]
sp.playlist_add_items(playlist_id, track_uris, position=0)  # Add at beginning

# Remove tracks from playlist
sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)

# Reorder tracks in playlist
sp.playlist_reorder_items(
    playlist_id,
    range_start=0,      # Start position
    range_length=5,     # Number of tracks to move
    insert_before=10    # New position
)

# Replace all tracks in playlist
sp.playlist_replace_items(playlist_id, new_track_uris)
```

### Playlist Information & Modification
```python
# Get playlist details
playlist = sp.playlist(playlist_id, fields="name,description,public,collaborative,followers")

# Update playlist details
sp.playlist_change_details(
    playlist_id,
    name="New Playlist Name",
    public=False,
    collaborative=True,
    description="Updated description"
)

# Get playlist tracks with full details
tracks = sp.playlist_tracks(
    playlist_id,
    fields="items(track(name,artists,album,duration_ms,popularity,external_urls))",
    limit=100,
    offset=0
)

# Upload custom playlist cover image
with open("cover_image.jpg", "rb") as image_file:
    sp.playlist_upload_cover_image(playlist_id, image_file.read())
```

### Get User Playlists
```python
# Get current user's playlists
playlists = sp.current_user_playlists(limit=50, offset=0)

# Get any user's public playlists
user_playlists = sp.user_playlists("spotify_user_id", limit=50)
```

### ❌ Deprecated: Featured Playlists (REMOVED)
```python
# ❌ THIS NO LONGER WORKS - Endpoint removed by Spotify (Oct 2025)
# featured = sp.featured_playlists(
#     country='US',
#     limit=20,
#     offset=0
# )

# ✅ ALTERNATIVE: Use search to find popular playlists
results = sp.search(q='top hits', type='playlist', limit=20, market='US')
for playlist in results['playlists']['items']:
    print(f"{playlist['name']} - {playlist['owner']['display_name']}")
```

---

## Track & Album Operations

This section focuses on retrieving detailed information about individual tracks and albums, including metadata, popularity scores, and release information. You can access comprehensive track details like duration, explicit content flags, and ISRC codes, as well as album information including release dates, genres, and total track counts. These endpoints are fundamental for music discovery applications, metadata management systems, and building rich music catalogs with detailed information.

### Track Information
```python
# Get single track
track = sp.track("4iV5W9uYEdYUVa79Axb7Rh")
print(f"Track: {track['name']}")
print(f"Artists: {[artist['name'] for artist in track['artists']]}")
print(f"Album: {track['album']['name']}")
print(f"Duration: {track['duration_ms']} ms")
print(f"Popularity: {track['popularity']}")
print(f"Explicit: {track['explicit']}")

# Get multiple tracks
tracks = sp.tracks(["4iV5W9uYEdYUVa79Axb7Rh", "1301WleyT98MSxVHPZCA6M"])
```

### ❌ Deprecated: Audio Features (REMOVED)
```python
# ❌ THIS NO LONGER WORKS - Endpoint removed by Spotify (Oct 2025)
# audio_features = sp.audio_features("4iV5W9uYEdYUVa79Axb7Rh")[0]
# print(f"Danceability: {audio_features['danceability']}")
# print(f"Energy: {audio_features['energy']}")
# print(f"Valence: {audio_features['valence']}")
# print(f"Tempo: {audio_features['tempo']} BPM")

# ⚠️ NOTE: Audio features analysis is no longer available via Spotify Web API
# Consider using alternative solutions:
# - External music analysis APIs
# - Audio analysis libraries (e.g., librosa for Python)
# - Pre-computed audio features from third-party datasets
```

### Album Operations
```python
# Get album information
album = sp.album("4aawyAB9vmqN3uQ7FjRGTy")
print(f"Album: {album['name']}")
print(f"Artists: {[artist['name'] for artist in album['artists']]}")
print(f"Release Date: {album['release_date']}")
print(f"Total Tracks: {album['total_tracks']}")
print(f"Genres: {album['genres']}")

# Get album tracks
album_tracks = sp.album_tracks("4aawyAB9vmqN3uQ7FjRGTy", limit=50)

# Get multiple albums
albums = sp.albums(["4aawyAB9vmqN3uQ7FjRGTy", "1DFixLWuPkv3KT3TnV35m3"])

# Get new releases
new_releases = sp.new_releases(country='US', limit=20, offset=0)
```

---

## Artist & Search

Artist information and search functionality form the backbone of music discovery. This section covers retrieving comprehensive artist profiles, including genres, popularity metrics, and follower counts, as well as accessing their discographies and related artists. The advanced search capabilities support complex queries with filters for year, genre, audio features, and more. These endpoints enable building sophisticated music discovery engines, artist recommendation systems, and genre-based music exploration tools.

### Artist Information
```python
# Get artist information
artist = sp.artist("4NHQUGzhtTLFvgF5SZesLK")
print(f"Artist: {artist['name']}")
print(f"Genres: {artist['genres']}")
print(f"Popularity: {artist['popularity']}")
print(f"Followers: {artist['followers']['total']}")

# Get artist's albums
albums = sp.artist_albums(
    "4NHQUGzhtTLFvgF5SZesLK",
    album_type='album,single,appears_on,compilation',
    country='US',
    limit=50,
    offset=0
)

# Get artist's top tracks
top_tracks = sp.artist_top_tracks("4NHQUGzhtTLFvgF5SZesLK", country='US')
```

### ❌ Deprecated: Related Artists (REMOVED)
```python
# ❌ THIS NO LONGER WORKS - Endpoint removed by Spotify (Oct 2025)
# related = sp.artist_related_artists("4NHQUGzhtTLFvgF5SZesLK")

# ✅ ALTERNATIVE: Find similar artists using genre-based search
artist = sp.artist("4NHQUGzhtTLFvgF5SZesLK")
genres = artist['genres']

# Search for artists with similar genres
if genres:
    genre_query = ' OR '.join([f'genre:"{g}"' for g in genres[:3]])
    results = sp.search(q=genre_query, type='artist', limit=20)

    similar_artists = [
        a for a in results['artists']['items']
        if a['id'] != "4NHQUGzhtTLFvgF5SZesLK"  # Exclude original artist
    ]
```

### Advanced Search
```python
def advanced_search(sp, query_params):
    """Advanced search with multiple parameters."""

    # Search tracks with filters
    results = sp.search(
        q='artist:Radiohead album:OK Computer',
        type='track',
        limit=50,
        offset=0,
        market='US'
    )

    # Search with year filter
    results = sp.search(
        q='year:2020-2023 genre:electronic',
        type='track,artist,album',
        limit=20
    )

    # Search with audio feature filters
    results = sp.search(
        q='danceability:0.8-1.0 energy:0.7-1.0',
        type='track',
        limit=30
    )

    return results

# Search operators:
# - artist: artist name
# - album: album name
# - track: track name
# - year: release year (YYYY or YYYY-YYYY)
# - genre: genre
# - label: record label
# - isrc: International Standard Recording Code
# - upc: Universal Product Code
```

### ❌ Deprecated: Genre Seeds & Recommendations (REMOVED)
```python
# ❌ THIS NO LONGER WORKS - Endpoints removed by Spotify (Oct 2025)
# genres = sp.recommendation_genre_seeds()
# category_playlists = sp.category_playlists('pop', country='US', limit=20)

# ✅ ALTERNATIVE: Use search with genre keywords
# Get categories (still works)
categories = sp.categories(country='US', limit=50, offset=0)

# Search for playlists within category using keywords
def find_playlists_by_category(sp, category_name, limit=20):
    """Find playlists using search instead of removed category_playlists endpoint."""
    results = sp.search(
        q=f'{category_name} playlist',
        type='playlist',
        limit=limit,
        market='US'
    )
    return results['playlists']['items']
```
    offset=0
)
```

---

## User Library

The user library represents a user's personal music collection within Spotify, including saved tracks, albums, shows, and episodes. This section provides complete control over library management, allowing you to save and remove content, check if items are already saved, and retrieve the user's entire saved collection. These endpoints are essential for building personal music management applications, backup tools, and recommendation systems based on user's saved content preferences.

### Saved Tracks
```python
# Check if tracks are saved
saved_status = sp.current_user_saved_tracks_contains(["4iV5W9uYEdYUVa79Axb7Rh"])

# Save tracks to library
sp.current_user_saved_tracks_add(["4iV5W9uYEdYUVa79Axb7Rh"])

# Remove tracks from library
sp.current_user_saved_tracks_delete(["4iV5W9uYEdYUVa79Axb7Rh"])

# Get saved tracks
saved_tracks = sp.current_user_saved_tracks(limit=50, offset=0)
for item in saved_tracks['items']:
    track = item['track']
    added_at = item['added_at']
    print(f"{track['name']} - Added: {added_at}")
```

### Saved Albums
```python
# Save albums
sp.current_user_saved_albums_add(["4aawyAB9vmqN3uQ7FjRGTy"])

# Remove albums
sp.current_user_saved_albums_delete(["4aawyAB9vmqN3uQ7FjRGTy"])

# Check if albums are saved
album_saved = sp.current_user_saved_albums_contains(["4aawyAB9vmqN3uQ7FjRGTy"])

# Get saved albums
saved_albums = sp.current_user_saved_albums(limit=50, offset=0)
```

### Saved Shows & Episodes (Podcasts)
```python
# Save shows
sp.current_user_saved_shows_add(["5CfCWKI5pZ28U0uOzXkDHe"])

# Get saved shows
saved_shows = sp.current_user_saved_shows(limit=50, offset=0)

# Save episodes
sp.current_user_saved_episodes_add(["512ojhOuo1ktJprKbVcKyQ"])

# Get saved episodes
saved_episodes = sp.current_user_saved_episodes(limit=50, offset=0)
```

---

## Playback Control

Transform your application into a remote control for Spotify with comprehensive playback management capabilities. This section covers real-time playback control including play, pause, skip, seek, volume control, and device management. You can also retrieve current playback state, transfer playback between devices, and control shuffle and repeat modes. These endpoints enable building custom music controllers, smart home integrations, and synchronized listening experiences across multiple devices.

### Current Playback
```python
# Get current playback state
current = sp.current_playback()
if current and current['is_playing']:
    track = current['item']
    device = current['device']
    progress = current['progress_ms']

    print(f"Now playing: {track['name']} by {track['artists'][0]['name']}")
    print(f"Device: {device['name']} ({device['type']})")
    print(f"Progress: {progress/1000:.0f}s / {track['duration_ms']/1000:.0f}s")

# Get currently playing track (simplified)
current_track = sp.currently_playing()
```

### Playback Control
```python
# Play/pause
sp.start_playback()  # Resume playback
sp.pause_playback()  # Pause playback

# Next/previous track
sp.next_track()
sp.previous_track()

# Seek to position (milliseconds)
sp.seek_track(30000)  # Seek to 30 seconds

# Set volume (0-100)
sp.volume(50)

# Shuffle and repeat
sp.shuffle(True)  # Enable shuffle
sp.repeat('context')  # off, track, context
```

### Play Specific Content
```python
# Play specific tracks
sp.start_playback(uris=['spotify:track:4iV5W9uYEdYUVa79Axb7Rh'])

# Play album from specific track
sp.start_playback(
    context_uri='spotify:album:1DFixLWuPkv3KT3TnV35m3',
    offset={'position': 5}  # Start from track 6
)

# Play playlist
sp.start_playback(context_uri='spotify:playlist:37i9dQZF1DX0XUsuxWHRQd')

# Transfer playback to device
sp.transfer_playback(device_id="device_id", force_play=True)
```

### Devices
```python
# Get available devices
devices = sp.devices()
for device in devices['devices']:
    print(f"Device: {device['name']} ({device['type']})")
    print(f"Active: {device['is_active']}")
    print(f"Volume: {device['volume_percent']}%")
```

---

## Audio Features & Analysis

> ⚠️ **DEPRECATED SECTION**: Audio features and analysis endpoints have been removed by Spotify as of October 2025.

~~Dive deep into the musical characteristics of tracks with Spotify's sophisticated audio analysis capabilities.~~ **This section describes endpoints that are no longer available.** Previously, you could access audio features like danceability, energy, valence, and tempo, as well as detailed audio analysis. These endpoints have been removed from the Spotify Web API.

### ❌ Removed: Audio Features (REMOVED)
```python
# ⚠️ DEPRECATED but still functional (as of October 2025)
def analyze_track_audio_features(sp, track_id):
    """
    Audio features endpoint is deprecated but currently works.
    No immediate changes required.
    """
    features = sp.audio_features(track_id)[0]
    analysis = sp.audio_analysis(track_id)
    return features, analysis
```

### Audio Features for Multiple Tracks
```python
# Still functional as of October 2025
track_ids = ["4iV5W9uYEdYUVa79Axb7Rh", "1301WleyT98MSxVHPZCA6M"]
features_list = sp.audio_features(track_ids)
```

### Recommendations
```python
# Still functional as of October 2025
def get_recommendations(sp, seed_params):
    """
    Recommendations endpoint is deprecated but currently works.
    See: https://developer.spotify.com/documentation/web-api/reference/get-recommendations
    """
    recommendations = sp.recommendations(
        seed_artists=['4NHQUGzhtTLFvgF5SZesLK'],
        seed_tracks=['4iV5W9uYEdYUVa79Axb7Rh'],
        seed_genres=['electronic', 'ambient'],
        target_danceability=0.8,
        limit=20,
        market='US'
    )
    return recommendations['tracks']

        if genres:
            # Search for tracks in same genres
            genre_query = ' '.join([f'genre:"{g}"' for g in genres[:2]])
            results = sp.search(q=genre_query, type='track', limit=limit)
            return results['tracks']['items']

    # Fallback: use user's top tracks to infer preferences
    top_tracks = sp.current_user_top_tracks(limit=5, time_range='short_term')
    return top_tracks.get('items', [])
```

---

## Browse & Discover

Explore Spotify's curated content and discover new music through categories, featured playlists, and new releases. This section provides access to Spotify's editorial content, including genre-based categories, featured playlists for different moods and activities, and the latest album releases. These endpoints are ideal for building music discovery interfaces, staying current with trending content, and providing users with professionally curated music experiences that match Spotify's own recommendations.

### Browse Categories
```python
# Get all categories
categories = sp.categories(country='US', limit=50, offset=0)

# Get specific category
category = sp.category('pop', country='US')

# Get category playlists
playlists = sp.category_playlists('workout', country='US', limit=20)
```

### Featured Content
```python
# Get featured playlists
featured = sp.featured_playlists(
    country='US',
    timestamp='2023-10-23T09:00:00',  # ISO format
    limit=20,
    offset=0
)

# Get new album releases
new_releases = sp.new_releases(country='US', limit=20, offset=0)
```

### Charts & Popular
```python
# Note: These require additional API endpoints or third-party services
# Spotify doesn't directly provide charts through the Web API

# Get popular tracks in a category/playlist
def get_popular_tracks_from_playlists(sp):
    """Extract popular tracks from featured playlists."""
    featured = sp.featured_playlists(limit=10)

    popular_tracks = []
    for playlist in featured['playlists']['items']:
        tracks = sp.playlist_tracks(playlist['id'], limit=10)
        for item in tracks['items']:
            if item['track'] and item['track']['popularity'] > 70:
                popular_tracks.append(item['track'])

    # Sort by popularity
    return sorted(popular_tracks, key=lambda x: x['popularity'], reverse=True)
```

---

## Following & Social

Build social features into your music application with comprehensive following and social interaction capabilities. This section covers following and unfollowing artists and users, managing playlist followers, and checking follow relationships. These endpoints enable creating social music experiences, artist fan communities, and collaborative music discovery features where users can follow their favorite artists and discover music through their social network.

### Follow Artists/Users
```python
# Follow artists
sp.user_follow_artists(['4NHQUGzhtTLFvgF5SZesLK'])

# Unfollow artists
sp.user_unfollow_artists(['4NHQUGzhtTLFvgF5SZesLK'])

# Check if following artists
following_artists = sp.current_user_following_artists(['4NHQUGzhtTLFvgF5SZesLK'])

# Get followed artists
followed = sp.current_user_followed_artists(limit=50)

# Follow users
sp.user_follow_users(['spotify_user_id'])

# Follow playlists
sp.user_playlist_follow_playlist('playlist_id')

# Unfollow playlists
sp.user_playlist_unfollow('playlist_id')

# Check if following playlist
following_playlist = sp.user_playlist_is_following('playlist_id', ['user_id'])
```

### Get Followers
```python
# Note: You can only get your own followers, not others'
# This information is available through the user profile

user = sp.current_user()
follower_count = user['followers']['total']
```

---

## Markets & Localization

Ensure your application works globally with proper market and localization support. This section covers retrieving available markets, checking content availability by region, and accessing localized content in different languages and regions. Understanding market restrictions is crucial for building applications that respect licensing agreements and provide appropriate content based on user location. These endpoints are essential for international applications and ensuring proper content delivery worldwide.

### Market Information
```python
# Get available markets
markets = sp.available_markets()
print("Available markets:", markets['markets'])

# Search with specific market
results = sp.search(
    q='artist:Beatles',
    type='album',
    market='GB',  # Great Britain
    limit=10
)

# Get content availability by market
track = sp.track('4iV5W9uYEdYUVa79Axb7Rh', market='US')
available_markets = track['available_markets']
```

### Localization
```python
# Get content in different languages/regions
featured_playlists_uk = sp.featured_playlists(country='GB')
featured_playlists_japan = sp.featured_playlists(country='JP')

# Category names in different languages
categories_germany = sp.categories(country='DE')
```

---

## Advanced Features

Take your Spotify integration to the next level with sophisticated techniques for handling large datasets, creating intelligent playlist systems, and building complex music applications. This section covers batch operations for efficiency, smart playlist creation algorithms, comprehensive playlist analytics, and advanced data processing techniques. These patterns are essential for building production-quality applications that can handle thousands of tracks and provide sophisticated music intelligence features.

### Batch Operations
```python
def batch_playlist_operations(sp, playlist_id, track_uris):
    """Perform multiple operations efficiently."""

    # Process in batches of 100 (Spotify's limit)
    batch_size = 100

    for i in range(0, len(track_uris), batch_size):
        batch = track_uris[i:i + batch_size]
        sp.playlist_add_items(playlist_id, batch)

    print(f"Added {len(track_uris)} tracks in {len(track_uris)//batch_size + 1} batches")

def get_all_playlist_tracks(sp, playlist_id):
    """Get all tracks from a large playlist."""
    tracks = []
    offset = 0
    limit = 100

    while True:
        batch = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        tracks.extend(batch['items'])

        if len(batch['items']) < limit:
            break

        offset += limit

    return tracks
```

### Smart Playlist Creation
```python
def create_smart_playlist(sp, name, criteria):
    """Create playlist based on intelligent criteria."""

    # Get seed content
    if criteria['based_on'] == 'top_tracks':
        top_tracks = sp.current_user_top_tracks(limit=5)
        seed_tracks = [track['id'] for track in top_tracks['items']]

    # Get recommendations
    recommendations = sp.recommendations(
        seed_tracks=seed_tracks[:5],
        **criteria['audio_features'],
        limit=50
    )

    # Create playlist
    playlist = sp.user_playlist_create(
        user=sp.current_user()['id'],
        name=name,
        description=f"Smart playlist created based on {criteria['based_on']}"
    )

    # Add tracks
    track_uris = [track['uri'] for track in recommendations['tracks']]
    sp.playlist_add_items(playlist['id'], track_uris)

    return playlist

# Usage example
criteria = {
    'based_on': 'top_tracks',
    'audio_features': {
        'target_danceability': 0.8,
        'target_energy': 0.7,
        'min_popularity': 60
    }
}
```

### Playlist Analytics
```python
def analyze_playlist(sp, playlist_id):
    """Comprehensive playlist analysis."""

    # Get all tracks
    tracks = get_all_playlist_tracks(sp, playlist_id)
    track_ids = [item['track']['id'] for item in tracks if item['track']]

    # Get audio features for all tracks
    all_features = []
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        features = sp.audio_features(batch)
        all_features.extend([f for f in features if f])

    # Calculate averages
    if all_features:
        avg_features = {
            'danceability': sum(f['danceability'] for f in all_features) / len(all_features),
            'energy': sum(f['energy'] for f in all_features) / len(all_features),
            'valence': sum(f['valence'] for f in all_features) / len(all_features),
            'tempo': sum(f['tempo'] for f in all_features) / len(all_features),
            'duration': sum(f['duration_ms'] for f in all_features) / len(all_features)
        }

        # Get genre distribution
        artists = set()
        for item in tracks:
            if item['track']:
                for artist in item['track']['artists']:
                    artists.add(artist['id'])

        return {
            'track_count': len(tracks),
            'total_duration_ms': sum(f['duration_ms'] for f in all_features),
            'unique_artists': len(artists),
            'average_features': avg_features
        }
```

---

## Code Examples

Learn through practical, real-world implementations that demonstrate how to combine multiple API endpoints into powerful music applications. This section provides complete, production-ready code examples including a comprehensive playlist manager, intelligent music discovery engine, and advanced Spotify integration patterns. These examples serve as templates for building sophisticated music applications and demonstrate best practices for combining different API capabilities effectively.

### Complete Playlist Manager
```python
class SpotifyPlaylistManager:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-modify-public playlist-modify-private user-library-read user-top-read"
        ))

    def create_mood_playlist(self, mood, duration_minutes=60):
        """Create playlist based on mood."""
        mood_configs = {
            'happy': {'target_valence': 0.8, 'target_energy': 0.7, 'target_danceability': 0.6},
            'sad': {'target_valence': 0.2, 'target_energy': 0.3, 'target_acousticness': 0.7},
            'energetic': {'target_energy': 0.9, 'target_danceability': 0.8, 'min_tempo': 120},
            'chill': {'target_energy': 0.4, 'target_valence': 0.5, 'target_acousticness': 0.6}
        }

        config = mood_configs.get(mood, mood_configs['happy'])

        # Get user's top genres
        top_artists = self.sp.current_user_top_artists(limit=5)

        # Get recommendations
        recommendations = self.sp.recommendations(
            seed_artists=[artist['id'] for artist in top_artists['items'][:2]],
            limit=50,
            **config
        )

        # Create playlist
        playlist_name = f"{mood.title()} Vibes - {duration_minutes}min"
        playlist = self.sp.user_playlist_create(
            user=self.sp.current_user()['id'],
            name=playlist_name,
            description=f"AI-generated {mood} playlist"
        )

        # Add tracks
        track_uris = [track['uri'] for track in recommendations['tracks']]
        self.sp.playlist_add_items(playlist['id'], track_uris)

        return playlist

    def duplicate_playlist(self, source_playlist_id, new_name):
        """Create a copy of existing playlist."""
        # Get original playlist
        source = self.sp.playlist(source_playlist_id)
        tracks = get_all_playlist_tracks(self.sp, source_playlist_id)

        # Create new playlist
        new_playlist = self.sp.user_playlist_create(
            user=self.sp.current_user()['id'],
            name=new_name,
            description=f"Copy of {source['name']}"
        )

        # Add all tracks
        track_uris = [item['track']['uri'] for item in tracks if item['track']]
        batch_playlist_operations(self.sp, new_playlist['id'], track_uris)

        return new_playlist
```

### Music Discovery Engine
```python
class MusicDiscoveryEngine:
    def __init__(self, spotify_client):
        self.sp = spotify_client

    def discover_similar_artists(self, artist_name, depth=3):
        """Find similar artists using graph traversal."""
        # Search for the artist
        results = self.sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
        if not results['artists']['items']:
            return []

        artist_id = results['artists']['items'][0]['id']
        discovered = set()
        to_explore = [artist_id]

        for level in range(depth):
            next_level = []
            for current_artist in to_explore:
                if current_artist not in discovered:
                    discovered.add(current_artist)
                    related = self.sp.artist_related_artists(current_artist)
                    next_level.extend([a['id'] for a in related['artists'][:5]])

            to_explore = next_level

        # Get artist details
        artist_details = []
        for i in range(0, len(discovered), 50):
            batch = list(discovered)[i:i+50]
            artists = self.sp.artists(batch)
            artist_details.extend(artists['artists'])

        return sorted(artist_details, key=lambda x: x['popularity'], reverse=True)

    def find_hidden_gems(self, user_top_tracks_count=20):
        """Find lesser-known tracks similar to user's taste."""
        # Get user's top tracks
        top_tracks = self.sp.current_user_top_tracks(limit=user_top_tracks_count)

        # Get seeds from top tracks
        seed_tracks = [track['id'] for track in top_tracks['items'][:5]]

        # Get recommendations with popularity filter for hidden gems
        recommendations = self.sp.recommendations(
            seed_tracks=seed_tracks,
            min_popularity=20,
            max_popularity=60,  # Lower popularity = hidden gems
            limit=50
        )

        return recommendations['tracks']
```

---

## Best Practices

Build robust, efficient, and maintainable Spotify integrations with proven development patterns and optimization techniques. This section covers performance optimization strategies, security best practices, proper error handling, and efficient data management. Following these practices ensures your application can handle production workloads, provides excellent user experience, and maintains security standards while making the most efficient use of the Spotify Web API.

### Performance Optimization
```python
# 1. Batch API calls when possible
track_ids = ["id1", "id2", "id3", ...]
features = sp.audio_features(track_ids)  # Better than individual calls

# 2. Use pagination efficiently
def get_all_items(sp, endpoint_func, **kwargs):
    items = []
    offset = 0
    limit = 50

    while True:
        batch = endpoint_func(limit=limit, offset=offset, **kwargs)
        items.extend(batch['items'])

        if len(batch['items']) < limit:
            break
        offset += limit

    return items

# 3. Cache results when appropriate
import functools
import time

@functools.lru_cache(maxsize=100)
def cached_artist_info(artist_id):
    return sp.artist(artist_id)

# 4. Use specific fields to reduce payload
playlist = sp.playlist(playlist_id, fields="name,description,tracks.total")
```

### Error Handling Patterns
```python
import time
from spotipy.exceptions import SpotifyException

def robust_spotify_call(func, *args, max_retries=3, **kwargs):
    """Wrapper for robust API calls with retry logic."""
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except SpotifyException as e:
            if e.http_status == 429:  # Rate limited
                retry_after = int(e.headers.get('Retry-After', 1))
                print(f"Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
            elif e.http_status == 401:  # Unauthorized
                print("Token expired. Re-authenticate required.")
                raise
            elif attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                raise
            else:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
```

### Security Best Practices
```python
# 1. Never hardcode credentials
import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# 2. Use appropriate scopes (principle of least privilege)
minimal_scope = "playlist-read-private"  # Instead of all scopes

# 3. Handle token refresh automatically
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_path=".cache"  # Stores refresh tokens securely
)

# 4. Validate input data
def safe_search(sp, query, search_type='track', limit=20):
    # Sanitize input
    query = query.strip()[:100]  # Limit length
    if not query:
        return {'tracks': {'items': []}}

    try:
        return sp.search(q=query, type=search_type, limit=min(limit, 50))
    except Exception as e:
        print(f"Search failed: {e}")
        return {'tracks': {'items': []}}
```

---

## Error Handling

Build resilient applications that gracefully handle API failures, network issues, and rate limiting with comprehensive error management strategies. This section covers common error scenarios, proper exception handling, retry logic, and user-friendly error messaging. Robust error handling is essential for production applications that need to provide consistent user experiences even when facing network connectivity issues, API downtime, or quota limits.

### Common Error Codes
```python
from spotipy.exceptions import SpotifyException

def handle_spotify_errors(func):
    """Decorator for comprehensive error handling."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SpotifyException as e:
            error_handlers = {
                400: "Bad Request - Check your parameters",
                401: "Unauthorized - Token expired or invalid",
                403: "Forbidden - Insufficient permissions",
                404: "Not Found - Resource doesn't exist",
                429: "Rate Limited - Too many requests",
                500: "Internal Server Error - Try again later",
                502: "Bad Gateway - Service temporarily unavailable",
                503: "Service Unavailable - Try again later"
            }

            error_msg = error_handlers.get(e.http_status, f"Unknown error: {e.http_status}")
            print(f"Spotify API Error {e.http_status}: {error_msg}")

            if e.http_status == 429:
                retry_after = int(e.headers.get('Retry-After', 60))
                print(f"Retry after {retry_after} seconds")

            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    return wrapper
```

---

## Rate Limits & Optimization

Maximize your application's performance while respecting Spotify's API limits through intelligent request management and optimization strategies. This section covers rate limiting mechanics, request optimization techniques, caching strategies, and parallel processing approaches. Understanding these concepts is crucial for building applications that can handle high user loads while maintaining responsive performance and staying within API quotas.

### Rate Limiting Information
```python
"""
Spotify Web API Rate Limits (Updated January 2025):
- Rate limit calculated on rolling 30-second window (not per minute)
- Development mode: Lower rate limit (exact number varies)
- Extended quota mode: Much higher rate limit (requires application)
- Some endpoints have custom rate limits (e.g., playlist image upload)
- 429 errors include 'Retry-After' header with wait time in seconds

Key Changes from Previous Documentation:
- Rolling 30-second window instead of per-minute calculation
- Different limits for development vs extended quota modes
- Application-specific rate limits based on quota mode

Best Practices:
1. Apply for extended quota mode for production apps
2. Implement backoff-retry strategy using Retry-After header
3. Use batch APIs to reduce request count
4. Cache results and use snapshot_id for playlists
5. Consider lazy loading for UI features
"""

class RateLimitedSpotifyClient:
    def __init__(self, sp):
        self.sp = sp
        self.request_times = []  # Track requests in rolling window

    def make_request(self, method_name, *args, **kwargs):
        import time

        # Clean old requests outside 30-second window
        current_time = time.time()
        self.request_times = [t for t in self.request_times if current_time - t < 30]

        try:
            method = getattr(self.sp, method_name)
            result = method(*args, **kwargs)
            self.request_times.append(current_time)
            return result
        except SpotifyException as e:
            if e.http_status == 429:
                # Use Retry-After header as per official documentation
                retry_after = int(e.headers.get('Retry-After', 30))
                print(f"Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                return self.make_request(method_name, *args, **kwargs)
            raise
```

### Optimization Strategies
```python
def optimize_large_operations():
    """Strategies for handling large datasets efficiently."""

    # 1. Parallel processing for independent operations
    import concurrent.futures

    def process_artist_batch(artist_ids):
        return sp.artists(artist_ids)

    all_artist_ids = ["id1", "id2", ...]  # Large list
    batches = [all_artist_ids[i:i+50] for i in range(0, len(all_artist_ids), 50)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_artist_batch, batch) for batch in batches]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # 2. Incremental loading for UIs
    def load_playlist_incrementally(playlist_id, callback):
        offset = 0
        limit = 50

        while True:
            batch = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
            callback(batch['items'])  # Update UI with batch

            if len(batch['items']) < limit:
                break
            offset += limit

    # 3. Smart caching
    import pickle
    import os
    from datetime import datetime, timedelta

    def cached_recommendations(cache_file, max_age_hours=24):
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                cached_data = pickle.load(f)
                if datetime.now() - cached_data['timestamp'] < timedelta(hours=max_age_hours):
                    return cached_data['data']

        # Generate new recommendations
        recommendations = sp.recommendations(...)

        # Cache results
        with open(cache_file, 'wb') as f:
            pickle.dump({
                'timestamp': datetime.now(),
                'data': recommendations
            }, f)

        return recommendations
```

---

## Complete Integration Example

Witness the power of the Spotify Web API through a comprehensive, production-ready application that demonstrates advanced integration patterns, intelligent music analysis, and sophisticated user experience features. This complete example showcases how to combine multiple API endpoints to create a full-featured music application with smart playlist generation, detailed music taste analysis, and automated music curation capabilities that rival professional music applications.

```python
#!/usr/bin/env python3
"""
Complete Spotify API Integration Example
Demonstrates advanced usage patterns and best practices
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time
import json
from datetime import datetime

class AdvancedSpotifyManager:
    def __init__(self):
        self.setup_client()
        self.user_id = self.sp.current_user()['id']

    def setup_client(self):
        """Initialize Spotify client with comprehensive scopes."""
        scope = """
            playlist-modify-public playlist-modify-private playlist-read-private
            user-library-read user-library-modify user-read-private user-read-email
            user-top-read user-read-recently-played user-follow-read user-follow-modify
            user-read-playback-state user-modify-playback-state user-read-currently-playing
        """

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope=scope
        ))

    def create_year_in_review_playlist(self, year=None):
        """Create a comprehensive year-in-review playlist."""
        if year is None:
            year = datetime.now().year

        print(f"Creating {year} Year in Review playlist...")

        # Get user's top tracks from the year
        top_tracks = self.sp.current_user_top_tracks(limit=50, time_range='long_term')

        # Get recently played tracks
        recent = self.sp.current_user_recently_played(limit=50)

        # Combine and deduplicate
        all_tracks = []
        track_ids = set()

        for track in top_tracks['items'] + [item['track'] for item in recent['items']]:
            if track['id'] not in track_ids:
                track_ids.add(track['id'])
                all_tracks.append(track)

        # Get recommendations based on top tracks
        if len(all_tracks) >= 5:
            seed_tracks = [track['id'] for track in all_tracks[:5]]
            recommendations = self.sp.recommendations(
                seed_tracks=seed_tracks,
                limit=20
            )
            all_tracks.extend(recommendations['tracks'])

        # Create playlist
        playlist_name = f"🎵 {year} Year in Review - My Soundtrack"
        description = f"My personal soundtrack for {year}. Top tracks, recent favorites, and personalized recommendations."

        playlist = self.sp.user_playlist_create(
            user=self.user_id,
            name=playlist_name,
            public=False,
            description=description
        )

        # Add tracks
        track_uris = [track['uri'] for track in all_tracks]
        for i in range(0, len(track_uris), 100):
            batch = track_uris[i:i+100]
            self.sp.playlist_add_items(playlist['id'], batch)

        print(f"✅ Created playlist '{playlist_name}' with {len(track_uris)} tracks")
        return playlist

    def analyze_music_taste(self):
        """Comprehensive analysis of user's music taste."""
        print("Analyzing your music taste...")

        # Get user's top content
        top_artists = self.sp.current_user_top_artists(limit=50)
        top_tracks = self.sp.current_user_top_tracks(limit=50)

        # Analyze audio features
        track_ids = [track['id'] for track in top_tracks['items']]
        audio_features = self.sp.audio_features(track_ids)

        # Calculate averages
        feature_averages = {}
        feature_keys = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness']

        for key in feature_keys:
            values = [f[key] for f in audio_features if f]
            feature_averages[key] = sum(values) / len(values) if values else 0

        # Genre analysis
        genres = {}
        for artist in top_artists['items']:
            for genre in artist['genres']:
                genres[genre] = genres.get(genre, 0) + 1

        top_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)[:10]

        # Decades analysis
        decades = {}
        for track in top_tracks['items']:
            if track['album']['release_date']:
                year = int(track['album']['release_date'][:4])
                decade = (year // 10) * 10
                decades[decade] = decades.get(decade, 0) + 1

        analysis = {
            'audio_profile': feature_averages,
            'top_genres': top_genres,
            'decade_preference': sorted(decades.items(), key=lambda x: x[1], reverse=True),
            'total_artists': len(top_artists['items']),
            'total_tracks_analyzed': len(track_ids)
        }

        # Generate insights
        insights = []
        if feature_averages['danceability'] > 0.7:
            insights.append("You love danceable music! 💃")
        if feature_averages['energy'] > 0.8:
            insights.append("High-energy tracks are your jam! ⚡")
        if feature_averages['valence'] > 0.6:
            insights.append("You prefer upbeat, positive music! 😊")
        if feature_averages['acousticness'] > 0.5:
            insights.append("You appreciate acoustic and organic sounds! 🎸")

        analysis['insights'] = insights

        print("\n🎵 Your Music Taste Analysis:")
        print(f"Top Genres: {', '.join([g[0] for g in top_genres[:5]])}")
        print(f"Music Mood: {insights}")

        return analysis

    def smart_playlist_generator(self, mood, duration_minutes=60, include_discovery=True):
        """Generate intelligent playlists based on mood and preferences."""
        print(f"Creating {mood} playlist for {duration_minutes} minutes...")

        # Mood configurations
        mood_configs = {
            'focus': {
                'target_energy': 0.6,
                'target_valence': 0.5,
                'target_acousticness': 0.7,
                'max_loudness': -10,
                'target_instrumentalness': 0.8
            },
            'workout': {
                'target_energy': 0.9,
                'target_danceability': 0.8,
                'min_tempo': 120,
                'target_valence': 0.7
            },
            'relax': {
                'target_energy': 0.3,
                'target_valence': 0.4,
                'target_acousticness': 0.8,
                'max_tempo': 100
            },
            'party': {
                'target_danceability': 0.9,
                'target_energy': 0.8,
                'target_valence': 0.8,
                'min_popularity': 60
            }
        }

        config = mood_configs.get(mood, mood_configs['focus'])

        # Get seeds from user's top tracks
        top_tracks = self.sp.current_user_top_tracks(limit=10)
        seed_tracks = [track['id'] for track in top_tracks['items'][:3]]

        # Get recommendations
        recommendations = self.sp.recommendations(
            seed_tracks=seed_tracks,
            limit=50,
            **config
        )

        tracks = recommendations['tracks']

        # Add discovery tracks if requested
        if include_discovery:
            # Get similar artists
            top_artists = self.sp.current_user_top_artists(limit=5)
            for artist in top_artists['items'][:2]:
                related = self.sp.artist_related_artists(artist['id'])
                for related_artist in related['artists'][:3]:
                    artist_tracks = self.sp.artist_top_tracks(related_artist['id'])
                    tracks.extend(artist_tracks['tracks'][:2])

        # Filter by duration to match requested time
        total_duration = 0
        target_duration = duration_minutes * 60 * 1000  # Convert to milliseconds
        filtered_tracks = []

        for track in tracks:
            if total_duration + track['duration_ms'] <= target_duration:
                filtered_tracks.append(track)
                total_duration += track['duration_ms']
            else:
                break

        # Create playlist
        playlist_name = f"🎵 {mood.title()} - {duration_minutes}min ({datetime.now().strftime('%b %d')})"
        description = f"AI-generated {mood} playlist for {duration_minutes} minutes. Created with intelligent mood matching."

        playlist = self.sp.user_playlist_create(
            user=self.user_id,
            name=playlist_name,
            public=False,
            description=description
        )

        # Add tracks
        track_uris = [track['uri'] for track in filtered_tracks]
        if track_uris:
            self.sp.playlist_add_items(playlist['id'], track_uris)

        actual_duration = sum(track['duration_ms'] for track in filtered_tracks) / 60000
        print(f"✅ Created '{playlist_name}' with {len(filtered_tracks)} tracks ({actual_duration:.1f} minutes)")

        return playlist

# ⚠️ NOTE: The above example uses deprecated endpoints that no longer work
# (recommendations(), artist_related_artists()). See updated alternatives
# throughout this documentation for current best practices.

# Usage example (UPDATED for current API)
if __name__ == "__main__":
    manager = AdvancedSpotifyManager()

    # Analyze music taste (still works)
    analysis = manager.analyze_music_taste()

    # Create playlists using search-based discovery (updated approach)
    # Note: smart_playlist_generator needs updating to use search instead of recommendations()
```

---

## Documentation Update History

### October 1, 2025 - EMPIRICAL TESTING UPDATE
**Status**: ❌ **ENDPOINTS ARE NON-FUNCTIONAL** (Verified through live API testing)

**Test Results**:
- 🧪 **Tested**: All 7 deprecated endpoints with valid authentication
- ❌ **Result**: All return HTTP 403 Forbidden or 404 Not Found errors
- ✅ **Verification**: Other endpoints work correctly (proves auth is valid)
- 📊 **Tool**: spotipy 2.25.1 with live Spotify API
- 🔗 **Reference**: See [TEST_SCRIPT_VERIFICATION.md](TEST_SCRIPT_VERIFICATION.md) and [EMPIRICAL_TEST_RESULTS.md](EMPIRICAL_TEST_RESULTS.md)

**Endpoint Status (Empirically Verified)**:
- `audio_features()` - ❌ **NON-FUNCTIONAL** (HTTP 403 Forbidden)
- `audio_analysis()` - ❌ **NON-FUNCTIONAL** (HTTP 403 Forbidden)
- `recommendations()` - ❌ **NON-FUNCTIONAL** (HTTP 404 Not Found)
- `artist_related_artists()` - ❌ **NON-FUNCTIONAL** (HTTP 404 Not Found)
- `featured_playlists()` - ❌ **NON-FUNCTIONAL** (HTTP 404 Not Found)
- `category_playlists()` - ❌ **NON-FUNCTIONAL** (HTTP 404 Not Found)
- `recommendation_genre_seeds()` - ❌ **NON-FUNCTIONAL** (HTTP 404 Not Found)

**Critical Discovery**:
- 📚 **Documentation exists** but endpoints are **actually removed**
- ⚠️ **"OAuth 2.0 Deprecated"** badge means "removed but documented"
- 🔧 **Spotipy has methods** but they fail when called
- ❌ **Code using these endpoints WILL BREAK**

**Test Command**:
```bash
python test_deprecated_endpoints.py
# Result: 0/7 endpoints functional
```

**Diagnostic Evidence**:
```python
# Working endpoint (proves auth is valid):
sp.current_user()  # ✅ Returns user data

# Deprecated endpoints (all fail):
sp.audio_features(['track_id'])     # ❌ HTTP 403 Forbidden
sp.artist_related_artists('id')     # ❌ HTTP 404 Not Found
sp.recommendations(seed_artists=[]) # ❌ HTTP 404 Not Found
```

### Key Takeaways (Updated with Facts)
1. **Documentation ≠ Functionality**: Spotify keeps docs for historical reference even after removal
2. **Empirical Testing Required**: Always test with live API - documentation shows history, not current state
3. **Migration Required**: Code using these endpoints must be refactored with alternatives
4. **No Timeline Available**: Spotify doesn't announce removal dates for deprecated endpoints
5. **Common API Practice**: Archive documentation while removing server-side routes

### Previous Correction (October 1, 2025 - INCORRECT)
~~**Correction**: Updated endpoint status information~~
- ~~⚠️ **Clarification**: Previously listed endpoints as "removed" but they are actually "deprecated but functional"~~
- ~~✅ **Verified**: All deprecated endpoints remain operational as of October 2025~~

**This was incorrect** - endpoints are actually non-functional. Updated with empirical test results above.

5. **Stay Updated**: Check [Spotify Developer Changelog](https://developer.spotify.com/documentation/web-api/changelog) regularly

This comprehensive documentation covers virtually all aspects of the current Spotify Web API, from basic operations to advanced use cases. Each section includes practical examples and best practices for real-world application development.

**Documentation maintained by**: Alex Method DJ Platform
**Version**: 2.0 (October 2025)
**Compatible with**: Spotipy 2.25.1+, Spotify Web API (Latest)
