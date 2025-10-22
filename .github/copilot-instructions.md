# Copilot Instructions - Spotify Skill Project

## Project Overview

This project is an **example of Claude Desktop Skills** - specifically demonstrating how to create production-ready skills that extend Claude's capabilities. The Spotify API Skill serves as a comprehensive reference implementation for building API integration skills.

### What This Project Is

- **Primary Purpose**: Educational example and template for creating Claude Desktop Skills
- **Secondary Purpose**: Production-ready Spotify API integration skill
- **Audience**: Developers learning to create custom Claude skills
- **Status**: Complete, production-ready, fully documented

### Project Type

This is a **Complete Skill Development Toolkit** that includes:

1. A complete working skill (Spotify API integration)
2. **Automated development tools** (init, validate, package) - NEW!
3. **Official specifications** (Agent Skills Spec v1.0) - NEW!
4. Comprehensive guides for creating any type of skill
5. Interactive workbooks and templates
6. Advanced patterns and examples
7. Best practices and troubleshooting

---

## What Are Claude Desktop Skills?

### Definition

**Skills** are modular, self-contained packages that extend Claude's capabilities by providing:

- Specialized workflows for specific domains
- Tool integrations (APIs, file formats, services)
- Domain expertise and procedural knowledge
- Bundled resources (scripts, references, assets)

**Official Documentation**: For up-to-date information on creating custom skills, see:

- [Official Claude Skills Documentation](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Official Skills Examples Repository](https://github.com/anthropics/skills)

### Skill Architecture

```
skill-name/
├── SKILL.md                    # Required: Main documentation with YAML frontmatter
├── scripts/                    # Optional: Executable Python/JS code
│   ├── main_script.py
│   └── helper_script.py
├── references/                 # Optional: Reference documentation
│   ├── api_reference.md
│   └── authentication_guide.md
└── assets/                     # Optional: Templates, images, etc.
    └── template.docx
```

### Core Principles of Skill Creation

1. **Concise is Key** - Context window is shared; only include what Claude doesn't know
2. **Set Appropriate Degrees of Freedom** - Match specificity to task complexity
3. **Progressive Disclosure** - Load content as needed (metadata → SKILL.md → resources)
4. **Single Source of Truth** - No duplicated information across files

---

## Project Structure

### Main Components

```
Spotify-Skill/
├── README.md                   # Main repository documentation
├── SPOTIFY_SKILL_README.md     # Complete project overview
├── USER_GUIDE.md               # Complete usage guide
├── QUICK_START.md              # 5-minute setup guide
├── agent_skills_spec.md        # Official Agent Skills Spec v1.0
├── spotify-api.skill           # Packaged skill (git ignored)
│
├── .github/                    # Repository assets
│   ├── copilot-instructions.md # AI assistant instructions
│   ├── banner-dark.svg         # Dark theme banner
│   └── banner-light.svg        # Light theme banner
│
├── tools/                      # Skill development utilities
│   ├── init_skill.py           # Create new skills from template
│   ├── validate_skill.py       # Validate skill structure
│   ├── package_skill.py        # Package skills for distribution
│   └── README.md               # Tool documentation
│
├── examples/                   # Curated skill examples
│   ├── README.md               # Pattern comparison and selection guide
│   └── EXAMPLES_REFERENCE.md   # Detailed analysis of 6 example patterns
│
├── spotify-api/                # Skill source files
│   ├── SKILL.md                # Main skill documentation (REQUIRED)
│   ├── .env                    # Spotify credentials (git ignored)
│   ├── scripts/
│   │   ├── spotify_client.py  # Core API wrapper (40+ methods)
│   │   └── playlist_creator.py # High-level playlist utilities
│   └── references/
│       ├── api_reference.md    # Spotify API reference
│       └── authentication_guide.md # OAuth 2.0 setup
│
└── Guide/                      # Skill creation education
    ├── 00_START_HERE.md        # Entry point for learning
    ├── INDEX.md                # Navigation guide
    ├── SKILL_CREATION_GUIDE.md # Complete skill creation guide
    ├── SKILL_CREATION_WORKBOOK.md # Interactive planning templates
    ├── ADVANCED_SKILL_EXAMPLES.md # Patterns and examples
    └── SPOTIFY_CREDENTIALS_SETUP.md # Credential setup guide
```

---

## Guide Folder Knowledge

The `Guide/` folder contains the **complete educational curriculum** for skill creation:

### 1. Navigation Documents

**`00_START_HERE.md`** - Primary entry point

- Explains what's in the package
- Provides learning paths based on goals
- Recommends reading order
- Estimated time commitments

**`INDEX.md`** - Comprehensive navigation

- Quick reference table for all documents
- Goal-based navigation ("I want to...")
- Learning paths (Beginner → Intermediate → Advanced)
- Document sizes and purposes

### 2. Core Educational Content

**`SKILL_CREATION_GUIDE.md`** (~15 KB, 1116 lines) - **THE MAIN GUIDE**

Complete education on skill creation including:

**Section 1: What Are Skills?**

- Definition and purpose
- Types of skills (API, document processing, code generation, etc.)
- What skills provide vs. what Claude already knows

**Section 2: Core Principles** (CRITICAL)

1. **Concise is Key** - Challenge every sentence, share context window
2. **Set Appropriate Degrees of Freedom**:
   - High freedom: Text-based guidance (blog posts, creative work)
   - Medium freedom: Pseudocode with parameters (data processing)
   - Low freedom: Exact scripts (fragile operations)
3. **Context Window Efficiency**: Progressive disclosure (metadata → SKILL.md → resources)
4. **Single Source of Truth**: No duplication

**Section 3: Skill Architecture**

- Directory structure requirements
- SKILL.md with YAML frontmatter (required)
- Scripts folder (optional, for reusable code)
- References folder (optional, for detailed docs)
- Assets folder (optional, for templates/images)

**Section 4: 6-Step Creation Process**

1. Define scope and purpose
2. Identify required resources
3. Create SKILL.md structure
4. Implement scripts/resources
5. Package the skill
6. Test and iterate

**Section 5-10**: Planning, implementation, best practices, real examples, patterns, troubleshooting

### 3. Interactive Planning

**`SKILL_CREATION_WORKBOOK.md`** (~12 KB, 709 lines)

Fill-in-the-blank templates for planning YOUR skill:

**Phase 1: Discovery**

- Define the problem and solution
- Identify use cases (triggers, goals, requirements)
- Document constraints (rate limits, auth, environment)

**Phase 2: Planning**

- Resource inventory (scripts, docs, assets)
- Feature matrix (scope, complexity, priority)
- Documentation structure outline
- Decision trees for common choices

**Phase 3-7**: Development checklist, validation, packaging, testing

### 4. Advanced Patterns

**`ADVANCED_SKILL_EXAMPLES.md`** (~18 KB, 872 lines)

Five complete skill patterns with code:

1. **API Wrapper Skills** (like Spotify)

   - Client class pattern
   - Token management
   - Error handling and retries
   - Rate limiting awareness
2. **Document Processing Skills**

   - Template-based generation
   - Asset management
   - Format conversion
3. **Multi-Domain Skills**

   - Organizing complex capabilities
   - Cross-referencing sections
   - Navigation strategies
4. **Code Generation Skills**

   - Boilerplate and scaffolding
   - Parameter substitution
   - Framework-specific patterns
5. **Learning/Reference Skills**

   - Structured educational content
   - Progressive curriculum design
   - Interactive elements

Each example includes:

- Complete directory structure
- SKILL.md template
- Script patterns
- Best practices
- Common pitfalls

---

## The Spotify Skill Example

### What It Does

A production-ready skill that enables Claude to:

1. **Create intelligent playlists** (5 methods):
   - By artist/band name
   - By theme/mood keywords
   - By lyrical content
   - From specific song lists
   - From AI recommendations
2. **Manage playlists** (CRUD operations)
3. **Search music** (tracks, artists, albums, playlists)
4. **Control playback** (play, pause, skip, volume, shuffle)
5. **Access user data** (profile, top items, listening history)

### Technical Implementation

**`spotify_client.py`** (570 lines, 20 KB)

- 40+ methods covering Spotify Web API
- OAuth 2.0 authentication with auto-refresh
- Comprehensive error handling
- Rate limiting awareness
- Token lifecycle management

**`playlist_creator.py`** (332 lines, 12 KB)

- High-level intelligent playlist creation
- Deduplication and batch processing
- Five creation strategies
- Analytics and statistics

**`SKILL.md`** (240 lines, 7 KB)

- YAML frontmatter with name and description
- Quick start examples
- Four complete workflows
- References to detailed guides

**References/** (31 KB total)

- `authentication_guide.md` - Complete OAuth setup (10 KB)
- `api_reference.md` - Endpoints and error handling (9 KB)

### Key Patterns Demonstrated

1. **Progressive Disclosure**: Metadata → Quick start → Deep documentation
2. **Single Source of Truth**: API details in reference, not duplicated
3. **Appropriate Freedom**: High-level methods (medium freedom) + exact scripts (low freedom)
4. **Context Efficiency**: Concise SKILL.md, detailed references on-demand

---

## Key Learnings for AI Assistants

### When Working on This Project

1. **This is an educational project**: The primary goal is teaching skill creation, not just building a Spotify integration
2. **The Spotify skill is the example**: It demonstrates best practices, not an end in itself
3. **Guide/ folder is the curriculum**: Treat it as authoritative documentation
4. **Patterns are transferable**: The Spotify patterns apply to ANY API integration skill

### Skill Creation Best Practices (from Guide)

#### Writing SKILL.md

✅ **DO:**

- Start with clear YAML frontmatter (name, description)
- Provide immediate quick start code
- Show 3-5 common workflows with examples
- Link to detailed references, don't duplicate
- Keep under 5,000 words (~500 lines)
- Use concise code examples over verbose explanations

❌ **DON'T:**

- Explain what Claude already knows
- Duplicate information across files
- Write long prose when code examples suffice
- Include every edge case in main doc
- Exceed context window budget

#### Scripts Strategy

**Include scripts when:**

- Code is written repeatedly (boilerplate elimination)
- Operations are fragile or must be consistent
- Performance matters (avoid re-generation)
- Complex multi-step procedures

**Keep as instructions when:**

- Multiple valid approaches exist
- Customization is expected
- Code is simple/obvious
- Token cost > benefit

#### Resource Organization

```
SKILL.md (Essential)
├─ Quick overview and navigation
├─ Common patterns (3-5 examples)
└─ Links to deeper resources

scripts/ (Reusable code)
├─ Main client/wrapper
└─ Utility functions

references/ (Detailed docs)
├─ API reference (load on-demand)
└─ Setup/configuration guides

assets/ (Templates/images)
└─ Output templates, logos, etc.
```

### Common Skill Types

From `ADVANCED_SKILL_EXAMPLES.md`:

1. **API Wrapper Skills** (Spotify example) - External service integration
2. **Document Processing** - DOCX, PDF, XLSX manipulation
3. **Code Generation** - Framework boilerplate and scaffolding
4. **Business Logic** - Company processes and workflows
5. **Data Analysis** - Database schemas and query templates
6. **Specialized Tools** - Domain-specific utilities
7. **Brand Guidelines** - Templates and style standards
8. **Learning Materials** - Educational content and tutorials

---

## Development Tools (NEW!)

The project includes automated utilities from the [Anthropic Skills repository](https://github.com/anthropics/skills) for skill development:

### Available Tools

1. **`tools/init_skill.py`** - Skill Initializer

   - Creates new skill directories with proper structure
   - Generates SKILL.md with YAML frontmatter template
   - Creates example scripts/, references/, assets/ directories
   - Provides TODO markers and guidance comments
   - Usage: `python tools/init_skill.py <skill-name> --path <output-path>`
2. **`tools/validate_skill.py`** - Skill Validator

   - Validates SKILL.md format and content
   - Checks YAML frontmatter (name, description required)
   - Verifies naming conventions (hyphen-case)
   - Ensures skill name matches directory name
   - Detects incomplete TODO placeholders
   - Usage: `python tools/validate_skill.py <skill-directory>`
3. **`tools/package_skill.py`** - Skill Packager

   - Creates distributable .zip packages
   - Automatically validates before packaging
   - Excludes system files and cache directories
   - Maintains proper directory structure
   - Usage: `python tools/package_skill.py <skill-directory> [output-dir]`

### Tool Usage Workflow

```bash
# 1. Create a new skill
python tools/init_skill.py my-new-skill --path ./

# 2. Edit the generated SKILL.md and add your code
# (Replace TODOs, add scripts, references, assets)

# 3. Validate before distribution
python tools/validate_skill.py ./my-new-skill

# 4. Package for sharing
python tools/package_skill.py ./my-new-skill ./dist
```

### Integration Details

- **Source**: Anthropic Claude Skills repository (skill-creator skill)
- **License**: Apache 2.0
- **Documentation**: See `tools/README.md` for complete guide
- **Integration Summary**: See `INTEGRATION_SUMMARY.md` for full details
- **Official Spec**: See `agent_skills_spec.md` for format requirements

---

## Development Workflow

### Using the Development Tools

**Create New Skills:**

```bash
python tools/init_skill.py my-api-skill --path ./
# Edit generated files, then validate and package
```

**Validate Existing Skills:**

```bash
python tools/validate_skill.py ./spotify-api
```

**Package for Distribution:**

```bash
python tools/package_skill.py ./spotify-api ./dist
```

### For Modifying the Spotify Skill

1. **Edit source files** in `spotify-api/` folder
2. **Test scripts** directly with Python
3. **Update SKILL.md** if APIs change
4. **Regenerate .skill package** if distributing

### For Creating New Skills

Follow the **6-Step Process** from `SKILL_CREATION_GUIDE.md`:

1. **Define**: Scope, purpose, use cases
2. **Identify**: Required resources (scripts, docs, assets)
3. **Structure**: Create SKILL.md outline
4. **Implement**: Write scripts and references
5. **Package**: Bundle into .skill file
6. **Test**: Validate with real use cases

Use `SKILL_CREATION_WORKBOOK.md` for step-by-step planning.

### For Helping Users Learn

**Beginner Path** (2-3 hours):

1. Read `SKILL_CREATION_GUIDE.md` sections 1-3
2. Review `SPOTIFY_SKILL_README.md`
3. Skim `ADVANCED_SKILL_EXAMPLES.md` (Example 1)

**Intermediate Path** (4-6 hours):

1. Complete full `SKILL_CREATION_GUIDE.md`
2. Study `ADVANCED_SKILL_EXAMPLES.md` patterns
3. Work through `SKILL_CREATION_WORKBOOK.md`

**Advanced Path** (2-3 hours):

1. Deep dive into specific patterns
2. Study error handling strategies
3. Implement complex multi-domain skills

---

## Technology Stack

### Spotify Skill Implementation

- **Language**: Python 3.x
- **API**: Spotify Web API (REST)
- **Authentication**: OAuth 2.0 Authorization Code Flow
- **Dependencies**: `requests` (HTTP), `base64`, `json`
- **Key Libraries**: None (pure Python + requests)

### Skill Format

- **Package Format**: ZIP archive with `.skill` extension
- **Required File**: `SKILL.md` with YAML frontmatter
- **Optional Folders**: `scripts/`, `references/`, `assets/`
- **Encoding**: UTF-8 text files

---

## File Relationships

### Documentation Hierarchy

```
Entry Points:
├─ README.md ──→ "Repository landing page"
├─ SPOTIFY_SKILL_README.md ──→ "Complete project overview"
├─ USER_GUIDE.md ──→ "Complete usage guide"
├─ QUICK_START.md ──→ "5-minute setup"
├─ Guide/00_START_HERE.md ──→ "New to skills? Start here"
└─ Guide/INDEX.md ──→ "Need navigation? Go here"

Main Educational Content:
├─ Guide/SKILL_CREATION_GUIDE.md ──→ Complete textbook
├─ Guide/SKILL_CREATION_WORKBOOK.md ──→ Interactive planning
└─ Guide/ADVANCED_SKILL_EXAMPLES.md ──→ Pattern library

Example Skills:
├─ examples/README.md ──→ Pattern comparison and selection
└─ examples/EXAMPLES_REFERENCE.md ──→ Detailed analysis of 6 patterns

Spotify Skill Documentation:
├─ spotify-api/SKILL.md ──→ Main skill doc (loaded by Claude)
├─ spotify-api/references/authentication_guide.md ──→ OAuth setup
└─ spotify-api/references/api_reference.md ──→ API details
```

### Code Relationships

```
spotify_client.py (Base client)
├─ Handles authentication
├─ Provides 40+ API methods
├─ Token management
└─ Error handling

playlist_creator.py (High-level utilities)
├─ Uses spotify_client.py
├─ Implements 5 creation strategies
└─ Adds convenience features

SKILL.md (Orchestration)
├─ References both scripts
├─ Shows usage patterns
└─ Links to detailed guides
```

---

## Common Tasks

### Testing the Spotify Skill Locally

```powershell
# Set environment variables
$env:SPOTIFY_CLIENT_ID = "your_client_id"
$env:SPOTIFY_CLIENT_SECRET = "your_client_secret"
$env:SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

# Run OAuth flow (one-time setup)
python spotify-api/scripts/spotify_client.py

# Test playlist creation
python -c "from playlist_creator import PlaylistCreator; from spotify_client import SpotifyClient; ..."
```

### Creating a New Skill (Quick Reference)

1. **Plan**: Fill out `SKILL_CREATION_WORKBOOK.md` Phase 1-2
2. **Structure**: Create folder with `SKILL.md`
3. **Implement**: Add scripts/references as needed
4. **Test**: Validate use cases
5. **Package**: ZIP with `.skill` extension

### Updating Documentation

- **User-facing changes**: Update `SKILL.md` first
- **API changes**: Update `references/api_reference.md`
- **Setup changes**: Update `references/authentication_guide.md`
- **New features**: Add to `SKILL.md` workflows, update README

---

## Authentication & Security Notes

### Spotify OAuth 2.0 Flow

1. **App Registration**: Create app at developer.spotify.com/dashboard
2. **Authorization**: User visits authorization URL, grants permissions
3. **Token Exchange**: Exchange auth code for access + refresh tokens
4. **Token Refresh**: Access tokens expire in 1 hour, refresh automatically
5. **Storage**: Store refresh token securely (environment variables recommended)

### Required Scopes

```
playlist-modify-public     # Create/edit public playlists
playlist-modify-private    # Create/edit private playlists
user-library-read          # Access saved tracks
user-library-modify        # Save/remove tracks
user-read-private          # Read user profile
user-read-email            # Read user email
user-top-read              # Read top artists/tracks
user-read-currently-playing # Read current playback
user-modify-playback-state # Control playback
user-read-playback-state   # Read playback state
```

### Security Best Practices

- ✅ Store credentials in environment variables
- ✅ Use HTTPS redirect URIs in production
- ✅ Never commit tokens to version control
- ✅ Implement token refresh before expiry
- ✅ Handle authorization errors gracefully

---

## Troubleshooting

### Common Issues

**"No module named 'spotify_client'"**

- Ensure you're running from correct directory
- Add scripts folder to Python path

**"Invalid client_id/client_secret"**

- Verify credentials from Spotify dashboard
- Check environment variables are set

**"Token expired"**

- Call `refresh_access_token()` with refresh token
- Implement automatic refresh in long-running processes

**"Rate limit exceeded"**

- Implement exponential backoff
- Reduce request frequency
- Use batch operations (up to 100 items)

### Learning Path Issues

**"Don't know where to start"**
→ Read `Guide/00_START_HERE.md`, follow your goal's path

**"Overwhelmed by content"**
→ Start with `SKILL_CREATION_GUIDE.md` sections 1-3 only

**"Need a specific pattern"**
→ Search `ADVANCED_SKILL_EXAMPLES.md` for your skill type

---

## Additional Context

### Official Documentation

For the most current and official guidance on creating Claude Desktop Skills, always refer to:

- **Official Guide**: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- **Official Examples Repository**: https://github.com/anthropics/skills

This project's Guide folder provides in-depth educational content that complements the official documentation with detailed patterns, examples, and best practices.

### Project History

This project serves as:

1. **Reference implementation** of skill creation best practices
2. **Educational resource** for developers learning skill creation
3. **Production example** showing real-world complexity
4. **Template** for API integration skills

### Design Decisions

**Why Spotify?**

- Popular, well-documented API
- Complex enough to demonstrate real patterns
- Simple enough to remain understandable
- Multiple interaction styles (search, CRUD, playback)

**Why This Structure?**

- Separates learning (Guide/) from implementation (spotify-api/)
- Demonstrates progressive disclosure
- Shows single source of truth
- Balances completeness with conciseness

**Why Include Full Guides?**

- Makes project self-contained
- Provides context for design decisions
- Enables learning without external resources
- Documents the "why" behind patterns

---

## When Assisting Users

### If They Want to Learn Skill Creation:

1. Direct them to the [official Claude documentation](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) for current specifications
2. Point them to the [official skills examples repository](https://github.com/anthropics/skills) for more examples
3. Direct them to `examples/` for curated example patterns
4. Guide them to `Guide/00_START_HERE.md` for in-depth learning
5. Recommend the appropriate learning path based on experience
6. Reference specific sections from `SKILL_CREATION_GUIDE.md`
7. Use Spotify skill as concrete API integration example

### If They Want to Use the Spotify Skill:

1. Direct them to `QUICK_START.md`
2. Help with OAuth setup from `authentication_guide.md`
3. Show examples from `SKILL.md`
4. Reference API details from `api_reference.md`

### If They Want to Create Similar Skills:

1. Help them choose a pattern from `examples/README.md`
2. Study detailed analysis in `examples/EXAMPLES_REFERENCE.md`
3. Use Spotify as API integration template
4. Apply patterns from `ADVANCED_SKILL_EXAMPLES.md`
5. Work through `SKILL_CREATION_WORKBOOK.md`
6. Reference core principles from `SKILL_CREATION_GUIDE.md`

### If They Want to Modify This Project:

1. Understand the educational purpose
2. Maintain the skill creation patterns
3. Update both implementation and documentation
4. Keep Guide/ and examples/ content in sync

---

## Summary for AI Assistants

**This project is a teaching tool first, Spotify integration second.**

The Spotify API Skill is the **flagship example** demonstrating how to create professional Claude Desktop Skills. The `Guide/` folder contains a complete curriculum teaching skill creation principles, patterns, and best practices.

When working with this project:

- **Respect the educational purpose** - changes should maintain instructional value
- **Follow the documented patterns** - they're intentional teaching examples
- **Reference the guides** - they contain the "why" behind decisions
- **Maintain consistency** - between implementation and documentation
- **Think transferability** - patterns should work for other skill types

The goal is helping developers create their own high-quality skills using this as a reference.
