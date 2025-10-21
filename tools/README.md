# Skill Development Tools

This directory contains utilities for creating, validating, and packaging Claude skills. These tools are from the [Anthropic Claude Skills repository](https://github.com/anthropics/skills) and are licensed under Apache License 2.0.

## Tools Overview

### 🚀 init_skill.py - Skill Initializer

Creates a new skill from template with proper directory structure.

**Usage:**
```bash
python init_skill.py <skill-name> --path <output-path>
```

**Examples:**
```bash
# Create a new skill in the current directory
python init_skill.py my-music-skill --path ./

# Create a skill in a custom location
python init_skill.py data-analyzer --path c:/Development/MySkills
```

**What it creates:**
- `SKILL.md` with YAML frontmatter and template content
- `scripts/` directory with example Python script
- `references/` directory with example documentation
- `assets/` directory with example asset placeholder

### ✅ validate_skill.py - Skill Validator

Validates skill structure and content before distribution.

**Usage:**
```bash
python validate_skill.py <skill-directory>
```

**Examples:**
```bash
# Validate the Spotify API skill
python validate_skill.py ../spotify-api

# Validate a custom skill
python validate_skill.py c:/Development/MySkills/my-skill
```

**What it checks:**
- ✓ SKILL.md exists and has valid format
- ✓ YAML frontmatter contains required `name` and `description` fields
- ✓ Skill name follows hyphen-case convention
- ✓ Skill name matches directory name
- ✓ Description is complete (no TODO placeholders)
- ✓ Optional directories (scripts/, references/, assets/) are valid

### 📦 package_skill.py - Skill Packager

Creates a distributable `.zip` file of a skill. Automatically validates before packaging.

**Usage:**
```bash
python package_skill.py <skill-directory> [output-directory]
```

**Examples:**
```bash
# Package skill to current directory
python package_skill.py ../spotify-api

# Package to specific output directory
python package_skill.py ../spotify-api ./dist

# Package with custom output location
python package_skill.py c:/Development/MySkills/my-skill ./packages
```

**What it does:**
1. Validates the skill structure (runs `validate_skill.py`)
2. Creates a `.zip` file named after the skill
3. Includes all files while excluding:
   - `.DS_Store`, `Thumbs.db`, `.gitignore`
   - `__pycache__` directories
4. Maintains proper directory structure for distribution

## Quick Start Workflow

### Creating a New Skill

```bash
# 1. Initialize a new skill
python tools/init_skill.py my-new-skill --path ./

# 2. Edit the generated SKILL.md and customize resources
#    - Update the description in YAML frontmatter
#    - Replace TODO sections with actual content
#    - Customize or delete example files in scripts/, references/, assets/

# 3. Validate your skill
python tools/validate_skill.py ./my-new-skill

# 4. Package for distribution
python tools/package_skill.py ./my-new-skill ./dist
```

### Validating and Packaging Existing Skill

```bash
# Validate the Spotify API skill
python tools/validate_skill.py ./spotify-api

# Package it for distribution
python tools/package_skill.py ./spotify-api ./dist
```

## Skill Structure Requirements

A valid skill must have this minimum structure:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (required)
│   │   ├── name: skill-name (required, hyphen-case)
│   │   └── description: "..." (required, detailed)
│   └── Markdown content (required)
└── Optional directories:
    ├── scripts/    - Executable code (Python, Bash, etc.)
    ├── references/ - Documentation to load into context
    └── assets/     - Files used in output (templates, images, etc.)
```

## YAML Frontmatter Format

Required format for `SKILL.md`:

```yaml
---
name: my-skill-name
description: A clear, complete description of what this skill does and when Claude should use it. Should be specific about triggering scenarios.
---
```

Optional fields:
```yaml
---
name: my-skill-name
description: Complete description here
license: Apache 2.0
metadata:
  version: "1.0"
  author: "Your Name"
---
```

## Naming Conventions

**Skill Names:**
- Must be hyphen-case (lowercase with hyphens)
- Only lowercase letters, digits, and hyphens
- Cannot start/end with hyphen
- Cannot have consecutive hyphens
- Must match the directory name exactly

**Valid Examples:**
- `spotify-api` ✅
- `data-analyzer` ✅
- `my-skill-v2` ✅

**Invalid Examples:**
- `Spotify-API` ❌ (contains uppercase)
- `data_analyzer` ❌ (uses underscore)
- `-my-skill` ❌ (starts with hyphen)
- `my--skill` ❌ (consecutive hyphens)

## Tips and Best Practices

### Description Best Practices

- **Be specific**: Mention exact scenarios when the skill should trigger
- **Be complete**: Don't leave TODO placeholders
- **Use third person**: "This skill should be used when..." not "Use this skill when..."
- **Include file types**: If relevant, mention supported formats (.xlsx, .pdf, etc.)
- **Minimum 20 characters**: Provide enough context

**Good Example:**
```yaml
description: Comprehensive Spotify API integration for searching music, managing playlists, controlling playback, and analyzing user listening data. This skill should be used when working with Spotify's Web API, creating playlists, or analyzing music preferences.
```

**Bad Example:**
```yaml
description: [TODO: Add description]  # ❌ Placeholder
description: Spotify skill  # ❌ Too vague
```

### Resource Organization

**scripts/** - Use for:
- Python/Bash scripts that execute deterministically
- Code that would be repeatedly rewritten
- API wrappers and utility functions
- Data processing scripts

**references/** - Use for:
- API documentation
- Workflow guides
- Database schemas
- Company policies
- Detailed instructions (>1000 words)

**assets/** - Use for:
- Templates (.pptx, .docx, etc.)
- Images and icons
- Fonts
- Boilerplate code directories
- Sample data files

### Common Validation Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "SKILL.md not found" | Missing file | Create SKILL.md in skill directory |
| "Invalid frontmatter format" | Incorrect YAML | Ensure frontmatter is enclosed in `---` markers |
| "Name must be hyphen-case" | Wrong naming | Use lowercase with hyphens only |
| "Name must match directory" | Mismatch | Rename directory or update name field |
| "Description too short" | < 20 characters | Write complete, informative description |
| "Contains TODO placeholder" | Incomplete | Replace all [TODO] markers with content |

## License

These tools are from the Anthropic Claude Skills repository and are licensed under:

**Apache License 2.0**

Copyright Anthropic, PBC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use these files except in compliance with the License.
You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Additional Resources

- **Official Skills Documentation**: https://support.claude.com/en/articles/12512198-creating-custom-skills
- **Anthropic Skills Repository**: https://github.com/anthropics/skills
- **Agent Skills Blog Post**: https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Local Project Documentation**: See `../Guide/` folder for comprehensive skill creation guides

## Troubleshooting

### Script won't run
```bash
# Make script executable (Linux/Mac)
chmod +x init_skill.py

# Or run with Python explicitly
python init_skill.py my-skill --path ./
```

### Import errors in package_skill.py
The `package_skill.py` script imports `validate_skill.py`. Ensure both files are in the same directory, or the validation step will be skipped with a warning.

### Path issues on Windows
Use forward slashes or double backslashes in paths:
```bash
# Good
python init_skill.py my-skill --path c:/Development/Skills
python init_skill.py my-skill --path c:\\Development\\Skills

# Might cause issues
python init_skill.py my-skill --path c:\Development\Skills
```

## Support

For issues or questions:
1. Check the validation error message for specific guidance
2. Review the `../Guide/SKILL_CREATION_GUIDE.md` for detailed instructions
3. Examine existing skills (like `../spotify-api/`) as examples
4. Consult the official Anthropic documentation linked above
