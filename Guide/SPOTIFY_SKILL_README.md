# Spotify API Skill - Creation Summary

## Overview

A comprehensive Claude skill for connecting to Spotify API and managing music, playlists, and playback. The skill enables intelligent playlist creation, search, user data retrieval, and playback control.

## What's Included

### 📄 SKILL.md (7 KB)
The main skill documentation including:
- **Core Capabilities**: Overview of 7 major capability areas
- **Quick Start**: Basic setup and common operations
- **Playlist Creation Workflows**: 4 distinct strategies
  - By artist/band name
  - By theme/mood keywords
  - By lyrics content
  - From specific song lists
- **Advanced Operations**: Recommendations, user profiles, top items, playback control
- **Authentication & Credentials**: Security and setup guidance
- **References**: Links to detailed API and authentication docs

### 🔧 Scripts (31.9 KB)

#### spotify_client.py (20 KB)
Complete Python wrapper for Spotify Web API with:
- **Authentication**: OAuth 2.0 flow, token management, auto-refresh
- **Playlists**: CRUD operations, track management
- **Search**: Tracks, artists, albums, playlists with advanced queries
- **Artists**: Details, top tracks, related artists, albums
- **Tracks**: Details, audio features, batch retrieval
- **Users**: Profile, top items, listening history
- **Recommendations**: Seed-based discovery
- **Playback**: Play, pause, skip, seek, volume, shuffle, repeat
- **Library**: Saved tracks management

**Methods**: 40+ methods covering all major Spotify API operations

#### playlist_creator.py (12 KB)
High-level intelligent playlist creation utility:
- `create_from_artist()` - Build playlists from artist's top tracks
- `create_from_theme()` - Theme/mood-based playlist creation
- `create_from_lyrics()` - Lyrical content-based playlists
- `create_from_song_list()` - Playlists from specific songs
- `create_from_recommendations()` - AI-powered recommendations
- `get_playlist_stats()` - Analytics for playlists

**Features**: Deduplication, batch processing, error handling

### 📚 References (18.8 KB)

#### authentication_guide.md (10 KB)
Complete authentication documentation:
- Setting up Spotify Developer App
- OAuth 2.0 Authorization Code Flow
- Credential management and storage
- Token lifecycle and refresh
- All available scopes explained
- Environment variable setup
- Security best practices
- Troubleshooting guide

#### api_reference.md (9 KB)
Comprehensive API reference:
- Rate limiting information
- Response format and pagination
- 40+ endpoint descriptions
- Search query syntax
- Error handling and HTTP status codes
- Data type structures
- Audio feature definitions

## Key Features

### ✨ Intelligent Playlist Creation
- **Artist-based**: Get all top tracks from any artist
- **Theme-based**: Create playlists by mood/genre keywords
- **Lyrics-based**: Search by emotional or thematic content
- **Custom**: Build from user-provided song lists
- **Recommended**: AI-generated playlists from seeds

### 🔐 Secure Authentication
- OAuth 2.0 implementation
- Automatic token refresh
- Environment variable support
- Secure credential storage guidance

### 🎵 Complete API Coverage
- 40+ method endpoints
- Playlist management (CRUD)
- Advanced search capabilities
- Playback control
- User library management
- Recommendations engine

### 📊 Error Handling & Rate Limiting
- Comprehensive error handling
- Automatic token expiry detection
- Rate limiting awareness
- Retry strategies documented

## Use Cases

This skill enables Claude to help with:

1. **Playlist Management**
   - "Create a playlist of all Beatles songs"
   - "Build a 'Workout' playlist with energetic tracks"
   - "Make a heartbreak recovery playlist"

2. **Music Discovery**
   - "Show me my top 20 artists from the past month"
   - "Get recommendations based on [artist name]"
   - "What songs should I add to my indie playlist?"

3. **Playback Control**
   - "Play this track on my device"
   - "What's currently playing?"
   - "Skip to the next track"

4. **Library Management**
   - "Add these songs to my favorites"
   - "Remove this track from my saved songs"
   - "List all my playlists"

## Technical Stack

- **Language**: Python 3.7+
- **Dependencies**: `requests` (for HTTP)
- **API**: Spotify Web API v1
- **Authentication**: OAuth 2.0
- **Format**: RESTful JSON API

## Installation & Setup

1. **Unzip the .skill file** to your skills directory
2. **Set environment variables**:
   ```bash
   export SPOTIFY_CLIENT_ID="your_client_id"
   export SPOTIFY_CLIENT_SECRET="your_client_secret"
   export SPOTIFY_REDIRECT_URI="http://localhost:8888/callback"
   export SPOTIFY_REFRESH_TOKEN="your_refresh_token"
   ```

3. **Create Spotify Developer App** at https://developer.spotify.com/dashboard

4. **Use with Claude**:
   ```python
   from spotify_client import SpotifyClient
   
   client = SpotifyClient(
       client_id=os.getenv("SPOTIFY_CLIENT_ID"),
       client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
       redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
       access_token=os.getenv("SPOTIFY_ACCESS_TOKEN")
   )
   
   playlists = client.get_user_playlists()
   ```

## Architecture

```
spotify-api/
├── SKILL.md                      # Main documentation
├── scripts/
│   ├── spotify_client.py         # Core API client (40+ methods)
│   └── playlist_creator.py       # High-level playlist utilities
└── references/
    ├── authentication_guide.md   # OAuth & credentials
    └── api_reference.md          # API endpoints & data types
```

## Documentation Quality

- **SKILL.md**: 7 KB of practical workflow guidance
- **Code Comments**: Comprehensive docstrings in both scripts
- **API Reference**: 9 KB with endpoint tables and examples
- **Auth Guide**: 10 KB with step-by-step setup
- **Error Handling**: Full error response documentation

## Security Considerations

- Client secret is sensitive - never commit to version control
- Use environment variables for credentials
- Tokens auto-refresh when expired
- Scopes are minimal and user-configurable
- HTTPS required for production

## Rate Limits

Spotify API allows:
- 429,400 requests per 30 minutes (general limit)
- Maximum 100 tracks per single add/remove request
- Search results limited to 50 items per request
- Recommendations limited to 100 items
- Seed limit: 5 maximum (total artists + tracks + genres)

## Next Steps

1. Extract the .skill file to your skills directory
2. Read `SKILL.md` for usage patterns
3. Follow `references/authentication_guide.md` for OAuth setup
4. Import and use `SpotifyClient` in your Claude operations

## Support

For detailed information:
- **Skill Usage**: See SKILL.md
- **API Details**: See references/api_reference.md
- **Authentication**: See references/authentication_guide.md
- **Code**: Review inline docstrings in scripts/

## File Sizes

- Total Package: 16 KB (.skill file)
- Extracted: ~58 KB
- SKILL.md: 7 KB
- spotify_client.py: 20 KB
- playlist_creator.py: 12 KB
- authentication_guide.md: 10 KB
- api_reference.md: 9 KB

---

**Skill Created**: October 21, 2025
**API Version**: Spotify Web API v1
**Python Version**: 3.7+
