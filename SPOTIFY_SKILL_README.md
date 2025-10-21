# Spotify API Skill - Complete Skill Development Toolkit

## Overview

This project is a **complete Claude skill development toolkit** that combines:

1. **Production Spotify API Skill** - A fully-featured example demonstrating API integration best practices
2. **Skill Development Tools** - Automated utilities for creating, validating, and packaging skills
3. **Educational Resources** - Comprehensive guides teaching skill creation from first principles
4. **Official Specifications** - The authoritative Agent Skills Spec v1.0

Whether you want to **use** the Spotify skill or **create your own skills**, this project provides everything you need.

## Quick Navigation

### 📖 Documentation

- **USER_GUIDE.md** - Complete step-by-step Spotify skill usage guide
- **QUICK_START.md** - 5-minute Spotify skill setup
- **agent_skills_spec.md** - Official Agent Skills Specification v1.0 (NEW!)
- **INTEGRATION_SUMMARY.md** - Tools integration documentation (NEW!)
- **Guide/** - Comprehensive skill creation tutorials

### 🛠️ Development Tools (NEW!)

- **tools/init_skill.py** - Create new skills from template
- **tools/validate_skill.py** - Validate skill structure and content
- **tools/package_skill.py** - Package skills for distribution
- **tools/README.md** - Complete tool usage guide

## Quick Navigation

### 📖 Documentation

- **USER_GUIDE.md** - Complete step-by-step Spotify skill usage guide
- **QUICK_START.md** - 5-minute Spotify skill setup
- **agent_skills_spec.md** - Official Agent Skills Specification v1.0 (NEW!)
- **INTEGRATION_SUMMARY.md** - Tools integration documentation (NEW!)
- **Guide/** - Comprehensive skill creation tutorials

### 🛠️ Development Tools (NEW!)

- **tools/init_skill.py** - Create new skills from template
- **tools/validate_skill.py** - Validate skill structure and content
- **tools/package_skill.py** - Package skills for distribution
- **tools/README.md** - Complete tool usage guide

### 📦 Spotify API Skill

- **SKILL.md** - Main Claude skill documentation
- **spotify-api/scripts/** - Production Python API wrapper
- **spotify-api/references/** - Authentication and API guides

### 📚 Example Skills (NEW!)

- **examples/README.md** - Curated skill examples from Anthropic repository
- **examples/EXAMPLES_REFERENCE.md** - Detailed pattern analysis and learning guide
- **6 Example Patterns** - template-skill, internal-comms, theme-factory, brand-guidelines, mcp-server, slack-gif-creator

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

## Using the Development Tools

### Create a New Skill

```bash
# Initialize a new skill with proper structure
python tools/init_skill.py my-music-analyzer --path ./

# Edit the generated SKILL.md and customize resources
# Add your scripts, references, and assets

# Validate before distribution
python tools/validate_skill.py ./my-music-analyzer

# Package for sharing
python tools/package_skill.py ./my-music-analyzer ./dist
```

### Validate and Package Existing Skills

```bash
# Validate the Spotify API skill
python tools/validate_skill.py ./spotify-api

# Package it for distribution
python tools/package_skill.py ./spotify-api ./dist
```

See `tools/README.md` for complete tool documentation.

## Next Steps

### To Use the Spotify Skill:

1. Extract the `spotify-api.skill` file to your skills directory
2. Read `USER_GUIDE.md` for complete setup instructions
3. Follow `references/authentication_guide.md` for OAuth setup
4. Import and use `SpotifyClient` in your Claude operations

### To Learn Skill Creation:

1. Read `Guide/SKILL_CREATION_GUIDE.md` for comprehensive instruction
2. Study `examples/` for 6 curated skill patterns (minimal to advanced)
3. Examine the Spotify skill as a production API integration example
4. Consult `agent_skills_spec.md` for official requirements

### To Create Your Own Skills:

1. Use `tools/init_skill.py` to generate new skill structure
2. Choose a pattern from `examples/` that fits your use case
3. Implement following patterns from similar skills
4. Validate with `tools/validate_skill.py` before distribution
5. Package with `tools/package_skill.py` for sharing

## Integration Credits

This project includes content from the [Anthropic Claude Skills repository](https://github.com/anthropics/skills), licensed under Apache 2.0:
- Development tools (init_skill.py, validate_skill.py, package_skill.py)
- Agent Skills Specification v1.0
- Example skill patterns and references

See `INTEGRATION_SUMMARY.md` for complete integration details.

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
