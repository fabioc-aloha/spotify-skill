# Agent Skills Specification

**Version:** 1.0
**Date:** October 16, 2024
**Source:** [Anthropic Claude Skills Repository](https://github.com/anthropics/skills)

---

## Overview

A **skill** is a folder of instructions, scripts, and resources that AI agents can discover and load dynamically to perform better at specific tasks. To be recognized as a skill, a folder must contain a `SKILL.md` file.

This specification defines the structure and requirements for creating Claude Desktop Skills.

---

## Skill Folder Layout

### Minimal Skill

A minimal skill folder looks like this:

```
my-skill/
  ├── SKILL.md
```

### Complete Skill with Resources

More complex skills can add additional directories and files as needed:

```
my-skill/
  ├── SKILL.md (required)
  ├── scripts/          (optional)
  │   ├── example.py
  │   └── helper.sh
  ├── references/       (optional)
  │   ├── api_docs.md
  │   └── workflows.md
  └── assets/          (optional)
      ├── template.docx
      └── logo.png
```

---

## The SKILL.md File

The skill's "entrypoint" is the `SKILL.md` file. It is the **only file required** to exist. The file must start with YAML frontmatter followed by regular Markdown content.

### YAML Frontmatter

The YAML frontmatter appears at the beginning of `SKILL.md`, enclosed by `---` markers.

#### Required Properties

1. **`name`** (required)
   - The name of the skill in hyphen-case
   - Restricted to lowercase Unicode alphanumeric characters and hyphens
   - Must match the name of the directory containing the SKILL.md
   - Example: `spotify-api`, `data-analyzer`, `pdf-processor`

2. **`description`** (required)
   - Description of what the skill does and when Claude should use it
   - Should be clear and specific about triggering scenarios
   - Write in third person (e.g., "This skill should be used when...")
   - Minimum 20 characters recommended
   - Example: `"Comprehensive Spotify API integration for searching music, managing playlists, and controlling playback. This skill should be used when working with Spotify's Web API."`

#### Optional Properties

1. **`license`**
   - The license applied to the skill
   - Keep it short (either the name of a license or the name of a bundled license file)
   - Example: `Apache 2.0` or `LICENSE.txt`

2. **`allowed-tools`**
   - A list of tools that are pre-approved to run
   - Currently only supported in Claude Code
   - Example: `["python", "bash"]`

3. **`metadata`**
   - A map from string keys to string values
   - Clients can use this to store additional properties not defined by the Agent Skills Spec
   - Recommend making key names reasonably unique to avoid accidental conflicts
   - Example:
     ```yaml
     metadata:
       version: "1.0"
       author: "Your Name"
       created: "2024-01-15"
     ```

#### Example Frontmatter

```yaml
---
name: spotify-api
description: Comprehensive Spotify API integration for searching music, managing playlists, controlling playback, and analyzing user listening data. This skill should be used when working with Spotify's Web API.
license: Apache 2.0
metadata:
  version: "1.0"
  author: "Example Developer"
---
```

### Markdown Body

The Markdown body has **no restrictions** on its content. It should contain:

- Instructions for Claude to follow
- Examples and use cases
- References to bundled resources (scripts, references, assets)
- Workflow guidance
- Best practices

The body can be structured however best serves the skill's purpose. Common patterns include:

- **Workflow-Based**: Step-by-step procedures
- **Task-Based**: Different operations organized by category
- **Reference-Based**: Guidelines and specifications
- **Capabilities-Based**: Feature-oriented organization

---

## Bundled Resources (Optional)

Skills can include additional folders containing resources that extend functionality:

### scripts/

Executable code (Python, Bash, etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

**When to include:**
- Same code is being rewritten repeatedly
- Deterministic reliability is needed
- Performance matters (avoid re-generation)

**Examples:**
- `spotify_client.py` - API wrapper with authentication
- `playlist_creator.py` - High-level playlist utilities
- `data_processor.sh` - Batch data processing script

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment-specific adjustments.

### references/

Documentation and reference material intended to be loaded into context as needed to inform Claude's process and thinking.

**When to include:**
- For documentation that Claude should reference while working
- Content is too detailed for SKILL.md
- Information is only needed for specific use cases

**Examples:**
- `api_reference.md` - Complete API documentation
- `authentication_guide.md` - OAuth setup instructions
- `database_schema.md` - Database structure and relationships
- `company_policies.md` - Business rules and guidelines

**Best practice:** If files are large (>10k words), include grep search patterns in SKILL.md to help Claude find relevant sections.

**Avoid duplication:** Information should live in either SKILL.md or references files, not both. Prefer references for detailed information.

### assets/

Files not intended to be loaded into context, but rather used within the output Claude produces.

**When to include:**
- The skill needs files that will be used in final output
- Templates, images, or boilerplate code are required

**Examples:**
- `logo.png` - Brand assets
- `template.pptx` - PowerPoint template
- `frontend-template/` - HTML/React boilerplate directory
- `custom-font.ttf` - Typography assets

**Benefits:** Separates output resources from documentation, enables Claude to use files without loading them into context window.

---

## Progressive Disclosure Design

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - Loaded when skill triggers (<5k words recommended)
3. **Bundled resources** - Loaded as needed by Claude (Unlimited*)

*Unlimited because scripts can be executed without reading into context window.

This design ensures context efficiency while providing comprehensive capabilities.

---

## Naming Conventions

### Skill Names

Must follow **hyphen-case** format:

**Valid:**
- `spotify-api` ✅
- `data-analyzer` ✅
- `pdf-processor-v2` ✅

**Invalid:**
- `Spotify-API` ❌ (contains uppercase)
- `data_analyzer` ❌ (uses underscore)
- `-my-skill` ❌ (starts with hyphen)
- `my--skill` ❌ (consecutive hyphens)
- `my-skill-` ❌ (ends with hyphen)

### File Names

- **SKILL.md**: Must be named exactly `SKILL.md` (case-sensitive)
- **scripts/**: Any valid filename for the programming language (`.py`, `.sh`, `.js`, etc.)
- **references/**: Typically `.md` or `.txt` files, but any text format works
- **assets/**: Any file type is acceptable

---

## Distribution Format

Skills can be distributed in two ways:

1. **Folder**: The skill directory can be copied as-is
2. **ZIP Archive**: Package the skill directory into a `.zip` file

When packaging as ZIP:
- Use the skill name as the filename (e.g., `spotify-api.zip`)
- Maintain the directory structure inside the ZIP
- The skill directory should be the root level inside the ZIP
- Exclude common system files (`.DS_Store`, `Thumbs.db`, `__pycache__/`)

---

## Validation Checklist

Before distributing a skill, verify:

- ✅ `SKILL.md` exists in the skill directory
- ✅ YAML frontmatter is properly formatted (enclosed in `---`)
- ✅ `name` field exists and is in hyphen-case
- ✅ `description` field exists and is complete (no TODO placeholders)
- ✅ Skill name matches directory name exactly
- ✅ Description is at least 20 characters and explains when to use the skill
- ✅ No angle brackets (`<` or `>`) in description
- ✅ Markdown body exists and has content
- ✅ Optional directories (`scripts/`, `references/`, `assets/`) contain appropriate files
- ✅ No excessive TODO markers remain in the body

---

## Complete Example

### Directory Structure

```
spotify-api/
  ├── SKILL.md
  ├── scripts/
  │   ├── spotify_client.py
  │   └── playlist_creator.py
  ├── references/
  │   ├── api_reference.md
  │   └── authentication_guide.md
```

### SKILL.md Example

```markdown
---
name: spotify-api
description: Comprehensive Spotify API integration for searching music, managing playlists, controlling playback, and analyzing user listening data. This skill should be used when working with Spotify's Web API.
license: Apache 2.0
---

# Spotify API Skill

## Overview

This skill provides comprehensive integration with Spotify's Web API, enabling intelligent playlist creation, music search, playback control, and user data analysis.

## Quick Start

### Creating a Playlist by Artist

```python
from scripts.spotify_client import SpotifyClient
from scripts.playlist_creator import PlaylistCreator

# Initialize clients
client = SpotifyClient()
creator = PlaylistCreator(client)

# Create playlist with top tracks from artist
playlist = creator.create_playlist_by_artist(
    artist_name="Radiohead",
    playlist_name="Best of Radiohead",
    num_tracks=30
)
```

## Authentication

See `references/authentication_guide.md` for complete OAuth 2.0 setup instructions.

## API Reference

Detailed endpoint documentation is available in `references/api_reference.md`.
```

---

## Additional Information

For a minimal example, see the `template-skill` in the [Anthropic Skills repository](https://github.com/anthropics/skills).

---

## Version History

- **1.0** (2024-10-16) - Public Launch

---

## References

- **Official Skills Documentation**: https://support.claude.com/en/articles/12512198-creating-custom-skills
- **Anthropic Skills Repository**: https://github.com/anthropics/skills
- **Agent Skills Blog Post**: https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

---

## License

This specification document is derived from the [Anthropic Claude Skills repository](https://github.com/anthropics/skills) and is provided under the Apache License 2.0.

Copyright Anthropic, PBC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
