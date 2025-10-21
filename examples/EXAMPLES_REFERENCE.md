# Example Skills Reference Guide

This document provides detailed information about each example skill, including complete SKILL.md content, structure details, and learning points.

## Accessing Full Examples

The complete example skills can be accessed from:
- **Source Repository**: https://github.com/anthropics/skills
- **Browse Online**: https://github.com/anthropics/skills/tree/main

For local development and study, you can clone the repository:
```bash
git clone https://github.com/anthropics/skills.git
```

---

## Example 1: template-skill

### Overview
The minimal skill example - just the bare essentials required for a valid skill.

### Structure
```
template-skill/
└── SKILL.md
```

### SKILL.md Content
```markdown
---
name: template-skill
description: A basic template to use as a starting point for new skills
---

# Template Skill

This is a basic skill template demonstrating the minimum requirements for a valid skill.

## Usage

Replace this content with your skill's instructions, guidelines, and examples.

## Structure

Every skill must have:
1. A `SKILL.md` file with YAML frontmatter
2. A `name` field (hyphen-case, matching directory name)
3. A `description` field explaining what the skill does

Optional resources can be added:
- `scripts/` - Executable code
- `references/` - Documentation to load into context
- `assets/` - Files used in output
```

### Key Learning Points
- **Minimal requirements**: Only SKILL.md with frontmatter is required
- **YAML frontmatter**: name and description fields are mandatory
- **Naming convention**: Hyphen-case for skill names
- **Directory matching**: Skill name must match directory name

### When to Use This Pattern
- Quick prototyping of new skills
- Simple instruction-only skills with no bundled resources
- Understanding minimum skill requirements
- Teaching skill basics

---

## Example 2: internal-comms

### Overview
Workflow-based skill for writing different types of internal communications.

### Structure
```
internal-comms/
├── SKILL.md
└── examples/
    ├── 3p-updates.md
    ├── company-newsletter.md
    ├── faq-answers.md
    └── general-comms.md
```

### Pattern Highlights
```markdown
## How to use this skill

1. **Identify the communication type** from the request
2. **Load the appropriate guideline file** from examples/:
   - 3p-updates.md - Progress/Plans/Problems team updates
   - company-newsletter.md - Company-wide newsletters
   - faq-answers.md - Frequently asked questions
   - general-comms.md - General communications
3. **Follow the specific instructions** in that file
```

### Key Learning Points
- **Decision tree pattern**: SKILL.md acts as router to specific guidelines
- **Progressive disclosure**: Load only the guideline needed for the task
- **Multiple workflows**: Different files for different communication types
- **Context efficiency**: Main doc stays concise, details in references

### When to Use This Pattern
- Skills with multiple distinct workflows or modes
- When different scenarios need different instructions
- To avoid overloading main SKILL.md with all scenarios
- For skills where one approach doesn't fit all use cases

---

## Example 3: theme-factory

### Overview
Collection of 10 professional themes (colors + fonts) that can be applied to artifacts.

### Structure
```
theme-factory/
├── SKILL.md
├── themes/
│   ├── ocean-depths.md
│   ├── sunset-boulevard.md
│   ├── forest-canopy.md
│   ├── modern-minimalist.md
│   ├── golden-hour.md
│   ├── arctic-frost.md
│   ├── desert-rose.md
│   ├── tech-innovation.md
│   ├── botanical-garden.md
│   └── midnight-galaxy.md
└── assets/
    └── theme-showcase.pdf
```

### Pattern Highlights
```markdown
## Usage Instructions

1. When a user requests themed styling for an artifact
2. Present the 10 available themes from themes/ directory
3. User selects preferred theme
4. Load the selected theme file
5. Apply colors and fonts consistently
```

### Key Learning Points
- **Library pattern**: Pre-built options user can select from
- **Reference organization**: Each theme in separate file for modularity
- **Asset inclusion**: PDF showcase for visual preview
- **On-demand loading**: Only load selected theme, not all 10
- **Custom generation**: Can create new themes on-the-fly if needed

### When to Use This Pattern
- Skills providing multiple template/preset options
- Reference libraries with selectable content
- Style guides and design systems
- Skills where user choice drives resource loading

---

## Example 4: brand-guidelines

### Overview
Apply Anthropic's official brand colors and typography to artifacts.

### Structure
```
brand-guidelines/
├── SKILL.md
├── references/
│   ├── brand-colors.md
│   └── typography-guidelines.md
└── assets/
    ├── anthropic-logo.png
    ├── slides-template.pptx
    └── brand-assets/
        └── [various image files]
```

### Pattern Highlights
- **Guidelines + templates**: Both documentation and usable files
- **Asset management**: Logos, templates, and visual resources
- **Reference docs**: Detailed color palettes and typography specs
- **Output files**: Templates that get used/modified in final output

### Key Learning Points
- **Assets folder purpose**: Files NOT loaded into context, but used in output
- **Template provision**: Providing starting points for user work
- **Visual resources**: Including images and design files
- **Separation of concerns**: Guidelines (references) vs. usable files (assets)

### When to Use This Pattern
- Skills that need visual assets (logos, icons, images)
- Template-driven work (PowerPoint, Word, design files)
- Brand/design system implementations
- Skills producing styled output

---

## Example 5: mcp-server

### Overview
Comprehensive guide for creating Model Context Protocol (MCP) servers.

### Structure
```
mcp-server/
├── SKILL.md
└── references/
    ├── mcp-overview.md
    ├── server-architecture.md
    ├── tool-implementation.md
    └── deployment-guide.md
```

### Pattern Highlights
- **Technical documentation**: Detailed guides for developer tasks
- **Multi-part references**: Breaking complex topic into digestible sections
- **Code examples**: Showing implementation patterns
- **Progressive depth**: Overview → architecture → implementation → deployment

### Key Learning Points
- **Technical skill structure**: How to organize developer-focused documentation
- **Code generation guidance**: Providing patterns without rigid scripts
- **Reference depth**: When to include detailed technical specs
- **Documentation organization**: Logical flow from concepts to implementation

### When to Use This Pattern
- Developer tool creation skills
- Technical documentation and guides
- Code generation with flexibility
- Skills teaching complex technical concepts

---

## Example 6: slack-gif-creator

### Overview
Advanced toolkit for creating animated GIFs optimized for Slack's size constraints.

### Structure
```
slack-gif-creator/
├── SKILL.md
├── LICENSE.txt
├── core/
│   ├── gif_builder.py
│   ├── validators.py
│   ├── frame_composer.py
│   └── easing.py
├── templates/
│   ├── shake.py
│   ├── bounce.py
│   ├── move.py
│   ├── zoom.py
│   ├── fade.py
│   ├── explode.py
│   ├── slide.py
│   ├── pulse.py
│   ├── morph.py
│   └── kaleidoscope.py
└── references/
    └── animation-patterns.md
```

### Pattern Highlights
```python
# Composable primitives
from templates.shake import create_shake_animation
from templates.bounce import create_bounce_animation
from core.gif_builder import GIFBuilder

# Build complex animations from simple building blocks
builder = GIFBuilder(480, 480, 20)
frames = create_shake_animation(...)
builder.add_frames(frames)
builder.save('output.gif')
```

### Key Learning Points
- **Toolkit architecture**: Core + templates pattern
- **Composable building blocks**: Primitives that combine freely
- **Validation systems**: Checking constraints (file size, dimensions)
- **Helper utilities**: Optional support functions
- **Creative freedom**: Tools, not rigid recipes
- **Complexity management**: Organizing extensive codebase

### When to Use This Pattern
- Skills with sophisticated programmatic capabilities
- Composable toolkits with building blocks
- Skills requiring validation/constraints
- Complex Python/code-heavy implementations
- When users need creative flexibility within technical limits

---

## Comparison with Spotify Skill

The **spotify-api** skill (parent directory) demonstrates yet another pattern:

### Pattern: API Integration with Authentication
```
spotify-api/
├── SKILL.md
├── scripts/
│   ├── spotify_client.py      # API wrapper class
│   └── playlist_creator.py    # High-level utilities
└── references/
    ├── api_reference.md        # Endpoint documentation
    └── authentication_guide.md # OAuth 2.0 setup
```

### Similar to:
- **slack-gif-creator**: Complex Python codebase, composable methods
- **mcp-server**: Technical implementation guidance

### Different from:
- **Unique pattern**: OAuth authentication flow management
- **API wrapper approach**: Client class with 40+ methods
- **Token lifecycle**: Handling access/refresh tokens
- **Rate limiting**: Awareness of API constraints

### Learning Value:
The Spotify skill shows how to:
1. Wrap external APIs with Python classes
2. Manage authentication lifecycles
3. Handle errors and retries
4. Provide both low-level and high-level interfaces
5. Document API integration patterns

---

## Pattern Selection Guide

### Choose **template-skill** when:
- Starting from scratch
- Very simple instruction-only skill
- Learning the basics
- Quick prototyping

### Choose **internal-comms** when:
- Multiple distinct workflows
- Different scenarios need different instructions
- Want to avoid overloading main doc
- Context efficiency is important

### Choose **theme-factory** when:
- Providing pre-built options/templates
- User selects from library
- Style guides and design systems
- Reference collections

### Choose **brand-guidelines** when:
- Need visual assets (logos, images)
- Providing templates users will modify
- Brand/design implementation
- Output includes styled documents

### Choose **mcp-server** when:
- Developer-focused technical skill
- Complex documentation needs
- Code generation with flexibility
- Teaching technical concepts

### Choose **slack-gif-creator** when:
- Sophisticated programmatic toolkit
- Composable building blocks
- Validation/constraint systems
- Creative freedom within technical limits

### Choose **spotify-api** (parent) when:
- Integrating external APIs
- Authentication/OAuth flows needed
- API wrapper class approach
- Complex token management

---

## Mixing Patterns

Most production skills combine multiple patterns. For example:

**Spotify skill uses:**
- API Integration pattern (main)
- Technical Guide pattern (references/)
- Composable Toolkit pattern (multiple creation methods)

**You might combine:**
- Workflow + Templates (internal-comms + theme-factory)
- API Integration + Assets (spotify-api + brand-guidelines)
- Technical Guide + Toolkit (mcp-server + slack-gif-creator)

**Don't feel limited to one pattern** - analyze your needs and mix approaches!

---

## Full Source Code Access

To study the complete implementation of any example:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anthropics/skills.git
   cd skills
   ```

2. **Browse specific skill**:
   ```bash
   # View structure
   ls -R slack-gif-creator/

   # Read SKILL.md
   cat slack-gif-creator/SKILL.md

   # Study Python code
   cat slack-gif-creator/core/gif_builder.py
   ```

3. **Try validating**:
   ```bash
   # Use the validator from this project
   python tools/validate_skill.py path/to/skills/slack-gif-creator
   ```

---

## Integration with This Project

These examples work together with:

1. **Guide/ folder** - Educational content on skill creation principles
2. **tools/ directory** - Automated tools (init, validate, package)
3. **spotify-api/** - Production example of API integration
4. **agent_skills_spec.md** - Official specification

**Learning Flow**:
1. Read Guide/SKILL_CREATION_GUIDE.md for principles
2. Study examples/ for concrete patterns
3. Examine spotify-api/ for production quality
4. Use tools/ to create your own skills

---

## License Compliance

All examples referenced from:
- **Repository**: https://github.com/anthropics/skills
- **License**: Apache License 2.0
- **Copyright**: Anthropic PBC

When using these patterns:
- ✅ Study and learn from them freely
- ✅ Adapt patterns for your own skills
- ✅ Reference them in documentation
- ✅ Share knowledge with others
- ⚠️ Maintain attribution when copying substantial code
- ⚠️ Include Apache 2.0 license if distributing derivatives

---

## Questions?

- **Official Docs**: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- **Source Repo**: https://github.com/anthropics/skills
- **This Project**: See SPOTIFY_SKILL_README.md for complete overview

Happy skill creating! 🚀
