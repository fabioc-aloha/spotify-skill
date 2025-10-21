<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/fabioc-aloha/spotify-skill/main/.github/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/fabioc-aloha/spotify-skill/main/.github/banner-light.svg">
  <img alt="Spotify Skill Banner" src="https://raw.githubusercontent.com/fabioc-aloha/spotify-skill/main/.github/banner-dark.svg" width="800">
</picture>

<br/><br/>

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Claude](https://img.shields.io/badge/Claude-Skills-orange.svg)](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
[![Spotify API](https://img.shields.io/badge/Spotify-API-1DB954.svg)](https://developer.spotify.com/documentation/web-api)

**Production-ready Spotify API integration + Complete toolkit for creating Claude Desktop Skills**

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Examples](#-examples) • [Tools](#-tools)

</div>

---

## 🎯 Overview

This project is a **comprehensive Claude Desktop Skills development platform** that combines:

- 🎵 **Production Spotify API Skill** - Fully-featured example with OAuth 2.0 and 40+ methods
- 🛠️ **Automated Development Tools** - Create, validate, and package skills effortlessly
- 📚 **Educational Resources** - Complete guides teaching skill creation from first principles
- 📋 **Official Specifications** - The authoritative Agent Skills Spec v1.0
- 🎨 **6 Curated Examples** - Real-world skill patterns from Anthropic

Whether you want to **use** the Spotify skill or **create your own skills**, this project provides everything you need.

---

## ✨ Features

### 🎵 Spotify API Skill

- **Authentication**: OAuth 2.0 authorization code flow with automatic token refresh
- **Playlists**: Create, manage, and modify playlists with intelligent algorithms
- **Search**: Find tracks, artists, albums, and playlists
- **Playback Control**: Play, pause, skip, volume, shuffle, and repeat
- **User Data**: Access profile, top items, and listening history
- **Recommendations**: AI-powered music discovery

### 🛠️ Development Tools

```bash
# Create a new skill from template
python tools/init_skill.py my-new-skill --path ./

# Validate skill structure and content
python tools/validate_skill.py ./my-new-skill

# Package skill for distribution
python tools/package_skill.py ./my-new-skill ./dist
```

### 📚 Learning Resources

- **Complete Guide** - Step-by-step skill creation process
- **Interactive Workbook** - Fill-in-the-blank planning templates
- **6 Example Patterns** - From minimal to advanced complexity
- **Official Spec** - Agent Skills Specification v1.0

---

## 🚀 Quick Start

### Using the Spotify Skill

1. **Clone the repository**:
   ```bash
   git clone https://github.com/fabioc-aloha/spotify-skill.git
   cd spotify-skill
   ```

2. **Set up credentials**:
   ```bash
   # Create Spotify app at https://developer.spotify.com/dashboard
   # Copy .env.example to .env and add your credentials
   cp .env.example .env
   ```

3. **Use the skill**:
   ```python
   from spotify_client import SpotifyClient

   client = SpotifyClient()
   client.authenticate()  # Complete OAuth flow

   # Create a playlist
   from playlist_creator import PlaylistCreator
   creator = PlaylistCreator(client)
   playlist = creator.create_from_artist("The Beatles", limit=20)
   ```

See [USER_GUIDE.md](USER_GUIDE.md) for complete instructions.

### Creating Your Own Skills

1. **Initialize a new skill**:
   ```bash
   python tools/init_skill.py my-api-skill --path ./
   ```

2. **Study example patterns**:
   - Browse `examples/` for 6 curated patterns
   - Read `Guide/SKILL_CREATION_GUIDE.md` for principles

3. **Implement and validate**:
   ```bash
   # Develop your skill
   code my-api-skill/SKILL.md

   # Validate structure
   python tools/validate_skill.py ./my-api-skill

   # Package for distribution
   python tools/package_skill.py ./my-api-skill
   ```

---

## 📖 Documentation

### Main Documentation

| Document | Description |
|----------|-------------|
| [USER_GUIDE.md](USER_GUIDE.md) | Complete Spotify skill setup and usage |
| [QUICK_START.md](QUICK_START.md) | 5-minute setup guide |
| [SPOTIFY_SKILL_README.md](SPOTIFY_SKILL_README.md) | Project overview and architecture |

### Skill Creation

| Document | Description |
|----------|-------------|
| [Guide/SKILL_CREATION_GUIDE.md](Guide/SKILL_CREATION_GUIDE.md) | Complete skill creation tutorial |
| [Guide/SKILL_CREATION_WORKBOOK.md](Guide/SKILL_CREATION_WORKBOOK.md) | Interactive planning templates |
| [Guide/ADVANCED_SKILL_EXAMPLES.md](Guide/ADVANCED_SKILL_EXAMPLES.md) | 5 detailed skill patterns |
| [agent_skills_spec.md](agent_skills_spec.md) | Official Agent Skills Spec v1.0 |

### Tools & Examples

| Document | Description |
|----------|-------------|
| [tools/README.md](tools/README.md) | Development tools documentation |
| [examples/README.md](examples/README.md) | 6 curated skill patterns |
| [examples/EXAMPLES_REFERENCE.md](examples/EXAMPLES_REFERENCE.md) | Detailed pattern analysis |

---

## 🎨 Examples

This project includes documentation for **6 curated skill patterns** from the [Anthropic Skills repository](https://github.com/anthropics/skills):

| Pattern | Complexity | Best For |
|---------|-----------|----------|
| **template-skill** | ⭐ Minimal | Quick start, learning basics |
| **internal-comms** | ⭐⭐ Simple | Multi-mode workflows |
| **theme-factory** | ⭐⭐ Medium | Reference libraries |
| **brand-guidelines** | ⭐⭐⭐ Medium | Visual/template skills |
| **mcp-server** | ⭐⭐⭐ Advanced | Technical guides |
| **slack-gif-creator** | ⭐⭐⭐⭐ Advanced | Complex toolkits |

Plus the **Spotify API skill** as a production-ready API integration example!

See [examples/README.md](examples/README.md) for detailed pattern comparison.

---

## 🛠️ Tools

### Automated Development Utilities

Located in `tools/` directory:

| Tool | Purpose |
|------|---------|
| **init_skill.py** | Create new skills from template with proper structure |
| **validate_skill.py** | Validate SKILL.md format, YAML frontmatter, naming conventions |
| **package_skill.py** | Package skills as distributable .zip files |

### Usage Examples

```bash
# Create a new skill
python tools/init_skill.py weather-api --path ./skills

# Validate before distribution
python tools/validate_skill.py ./skills/weather-api

# Package for sharing
python tools/package_skill.py ./skills/weather-api ./dist
```

---

## 📂 Project Structure

```
spotify-skill/
├── spotify-api/              # Production Spotify skill
│   ├── SKILL.md             # Main skill documentation
│   ├── scripts/             # Python API wrapper (40+ methods)
│   └── references/          # API and auth guides
├── tools/                   # Development utilities
│   ├── init_skill.py        # Skill initializer
│   ├── validate_skill.py    # Skill validator
│   └── package_skill.py     # Skill packager
├── examples/                # Curated skill patterns
│   ├── README.md            # Pattern comparison
│   └── EXAMPLES_REFERENCE.md # Detailed analysis
├── Guide/                   # Educational content
│   ├── SKILL_CREATION_GUIDE.md
│   ├── SKILL_CREATION_WORKBOOK.md
│   └── ADVANCED_SKILL_EXAMPLES.md
└── agent_skills_spec.md     # Official specification
```

---

## 🎓 Learning Paths

### Beginner (2-3 hours)
1. Read `Guide/SKILL_CREATION_GUIDE.md` sections 1-3
2. Browse `examples/README.md` for pattern overview
3. Study the Spotify skill as a complete example

### Intermediate (4-6 hours)
1. Complete `Guide/SKILL_CREATION_WORKBOOK.md`
2. Deep-dive `examples/EXAMPLES_REFERENCE.md`
3. Create your first skill using the tools

### Advanced (2-3 hours)
1. Compare multiple patterns from `examples/`
2. Study Spotify skill's production architecture
3. Implement complex skills with mixed patterns

---

## 🔒 Security

This project includes proper security practices:

- ✅ `.env` files for credentials (never committed)
- ✅ OAuth 2.0 authorization code flow
- ✅ Automatic token refresh
- ✅ `.gitignore` for sensitive files
- ⚠️ Never commit API credentials to version control

---

## 📜 License

This project integrates content from multiple sources:

- **Spotify Skill Code**: Custom implementation (use freely)
- **Development Tools**: Apache License 2.0 (from [Anthropic Skills](https://github.com/anthropics/skills))
- **Agent Skills Spec**: Apache License 2.0 (from Anthropic)
- **Example Documentation**: Apache License 2.0 (referencing Anthropic Skills)

See [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md) for complete licensing details.

---

## 🙏 Acknowledgments

Special thanks to:

- **Anthropic PBC** - For open-sourcing the Agent Skills system and exemplar skills
- **Spotify** - For providing the comprehensive Web API
- **Claude** - For the amazing AI capabilities that make skills possible

---

## 🔗 Links

- **Official Claude Skills Docs**: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- **Anthropic Skills Repository**: https://github.com/anthropics/skills
- **Spotify Web API**: https://developer.spotify.com/documentation/web-api
- **Agent Skills Blog Post**: https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

---

## 💬 Support

- 📖 Read the [complete documentation](SPOTIFY_SKILL_README.md)
- 🐛 [Report issues](https://github.com/fabioc-aloha/spotify-skill/issues)
- 💡 [Submit ideas](https://github.com/fabioc-aloha/spotify-skill/discussions)

---

<div align="center">

**Built with ❤️ for the Claude Skills community**

⭐ Star this repo if you find it helpful!

</div>
