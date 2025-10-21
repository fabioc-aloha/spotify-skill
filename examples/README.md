# Example Skills Collection

This directory contains curated example skills from the [Anthropic Claude Skills repository](https://github.com/anthropics/skills) demonstrating different skill patterns, complexities, and use cases.

## Purpose

These examples complement the Spotify API skill in the parent directory by showing:
- Different architectural patterns (workflows, guidelines, toolkits)
- Various complexity levels (minimal to advanced)
- Diverse domains (creative, technical, enterprise)
- Different resource types (scripts, references, assets)

## Available Examples

### 1. **template-skill** (Minimal)
The simplest possible skill - perfect starting point for creating new skills.

**Pattern**: Basic template
**Complexity**: Minimal (1 file)
**Learn**: Minimum requirements for a valid skill
**Best For**: Understanding skill basics, quick prototyping

---

### 2. **internal-comms** (Workflow-Based)
Skill for writing internal communications with multiple guideline files.

**Pattern**: Workflow with decision tree → load appropriate guideline
**Complexity**: Simple (SKILL.md + 4 guideline files)
**Learn**: How to organize multiple reference documents, workflow-based structure
**Best For**: Skills that have different modes/workflows

---

### 3. **theme-factory** (Reference/Guidelines)
Collection of 10 professional themes (colors/fonts) for styling artifacts.

**Pattern**: Reference library with pre-built options
**Complexity**: Medium (SKILL.md + 10 theme files + showcase)
**Learn**: Asset management, theme systems, on-demand loading
**Best For**: Skills providing reusable templates or presets

---

### 4. **brand-guidelines** (Asset-Heavy)
Apply Anthropic's official brand colors and typography to artifacts.

**Pattern**: Guidelines + templates + assets
**Complexity**: Medium (guidelines + PowerPoint/image assets)
**Learn**: How to bundle templates and visual assets
**Best For**: Skills that need files used in output (logos, templates)

---

### 5. **mcp-server** (Technical Guide)
Comprehensive guide for creating Model Context Protocol (MCP) servers.

**Pattern**: Technical documentation + code examples
**Complexity**: Medium-Advanced (detailed reference docs)
**Learn**: Technical skill structure, code generation patterns
**Best For**: Developer-focused skills with code generation

---

### 6. **slack-gif-creator** (Complex Toolkit)
Advanced toolkit for creating animated GIFs optimized for Slack's constraints.

**Pattern**: Validators + composable primitives + utilities
**Complexity**: Advanced (extensive Python codebase)
**Learn**: Complex skill architecture, composable building blocks, validation systems
**Best For**: Skills with sophisticated programmatic capabilities

---

## Pattern Comparison

| Skill | Pattern Type | Resource Types | Complexity | Use Case |
|-------|-------------|----------------|------------|----------|
| **template-skill** | Basic | SKILL.md only | ⭐ Minimal | Starting point |
| **internal-comms** | Workflow | references/ | ⭐⭐ Simple | Multi-mode workflows |
| **theme-factory** | Reference Library | references/, assets/ | ⭐⭐ Medium | Template collections |
| **brand-guidelines** | Asset-Heavy | references/, assets/ | ⭐⭐⭐ Medium | Visual/template skills |
| **mcp-server** | Technical Guide | references/ | ⭐⭐⭐ Medium-Advanced | Developer tools |
| **slack-gif-creator** | Complex Toolkit | scripts/, core/ | ⭐⭐⭐⭐ Advanced | Sophisticated toolkits |

Compare with **spotify-api** (parent directory):
- Pattern: API Integration
- Resources: scripts/, references/
- Complexity: ⭐⭐⭐⭐ Advanced
- Use Case: External API integration with OAuth

---

## Learning Paths

### Beginner Path
1. Start with **template-skill** - understand basics
2. Study **internal-comms** - learn workflow patterns
3. Examine Spotify skill (../spotify-api) - see API integration

### Intermediate Path
1. **theme-factory** - understand reference libraries
2. **brand-guidelines** - learn asset management
3. **mcp-server** - explore technical documentation patterns

### Advanced Path
1. **slack-gif-creator** - study complex toolkit architecture
2. Spotify skill (../spotify-api) - see production API integration
3. Create your own hybrid skill combining patterns

---

## How to Use These Examples

### For Learning
1. **Read SKILL.md first** - understand the skill's purpose and structure
2. **Examine the resources** - see how scripts/references/assets are organized
3. **Compare patterns** - identify which pattern fits your use case
4. **Reference in your work** - adapt patterns for your own skills

### For Creating Skills
1. **Choose a pattern** that matches your needs (see comparison table above)
2. **Use as template** - copy structure and adapt to your domain
3. **Mix patterns** - combine elements from multiple examples
4. **Validate** - use tools/validate_skill.py to check structure

### For Teaching Others
- Point beginners to template-skill and internal-comms
- Show intermediate learners theme-factory and brand-guidelines
- Challenge advanced learners with slack-gif-creator patterns
- Use Spotify skill as complete production example

---

## License

All example skills in this directory are from the [Anthropic Skills repository](https://github.com/anthropics/skills) and are licensed under **Apache License 2.0**.

See the LICENSE.txt file in each skill directory for complete terms.

**Copyright**: Anthropic PBC
**Repository**: https://github.com/anthropics/skills
**Integration Date**: October 2025

---

## Additional Resources

- **Official Documentation**: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- **Agent Skills Spec**: See ../agent_skills_spec.md
- **Creation Tools**: See ../tools/ directory (init, validate, package)
- **Complete Guide**: See ../Guide/ directory for in-depth skill creation education

---

## Quick Reference

**To explore an example:**
```bash
# View the skill's main documentation
cat examples/slack-gif-creator/SKILL.md

# See the directory structure
ls -R examples/theme-factory/
```

**To use as template:**
```bash
# Copy structure to new skill
cp -r examples/template-skill/ my-new-skill/

# Edit and customize
code my-new-skill/SKILL.md
```

**To validate:**
```bash
# Check if example is valid
python tools/validate_skill.py examples/internal-comms
```

---

## Example Selection Criteria

These 6 examples were chosen to:
1. **Maximize diversity** - different patterns, complexities, domains
2. **Complement Spotify skill** - provide additional learning patterns
3. **Cover common use cases** - workflows, guidelines, toolkits, assets
4. **Progressive complexity** - minimal → simple → medium → advanced
5. **Practical applicability** - patterns you'll actually use

**Not Included** (but available in source repo):
- algorithmic-art, canvas-design - highly specialized creative skills
- artifacts-builder - requires specific tech stack knowledge
- webapp-testing - narrow use case
- document-skills (docx, pdf, pptx, xlsx) - proprietary licensing

Focus on these 6 + Spotify skill for comprehensive skill creation knowledge.
