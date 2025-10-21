# Skill Creation Workbook & Templates

## Interactive Planning Guide

This workbook helps you plan and create a Claude skill step-by-step.

---

## PHASE 1: DISCOVERY

### 1.1 Define Your Skill

**What problem does your skill solve?**
```
Example: Enable Claude to create and manage Spotify playlists intelligently

Your answer:
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
```

**Who will use this skill?**
```
Example: Users who need music automation without manual playlist management

Your answer:
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
```

**In one sentence, what does your skill do?**
```
Example: Enables intelligent Spotify playlist creation from artists, themes, lyrics, or song lists

Your answer:
_____________________________________________________________
```

### 1.2 Identify Use Cases

Fill in 5-10 concrete examples of how users will use your skill:

```
Use Case #1
Trigger: ________________________________________________________
Goal: ________________________________________________________
Required Skills: ________________________________________________________

Use Case #2
Trigger: ________________________________________________________
Goal: ________________________________________________________
Required Skills: ________________________________________________________

Use Case #3
Trigger: ________________________________________________________
Goal: ________________________________________________________
Required Skills: ________________________________________________________

Use Case #4
Trigger: ________________________________________________________
Goal: ________________________________________________________
Required Skills: ________________________________________________________

Use Case #5
Trigger: ________________________________________________________
Goal: ________________________________________________________
Required Skills: ________________________________________________________
```

### 1.3 Identify Constraints

**Rate Limits/Quotas:**
```
_____________________________________________________________
_____________________________________________________________
```

**Authentication Requirements:**
```
_____________________________________________________________
_____________________________________________________________
```

**Environment/System Requirements:**
```
_____________________________________________________________
_____________________________________________________________
```

**Known Limitations:**
```
_____________________________________________________________
_____________________________________________________________
```

---

## PHASE 2: PLANNING

### 2.1 Resource Inventory

Based on your use cases, what resources do you need?

#### Scripts You'll Need

```
Script Name: ____________________
Purpose: ____________________
Functionality: ____________________
□ Core functionality (must have)
□ Helper utility (nice to have)

Script Name: ____________________
Purpose: ____________________
Functionality: ____________________
□ Core functionality (must have)
□ Helper utility (nice to have)

Script Name: ____________________
Purpose: ____________________
Functionality: ____________________
□ Core functionality (must have)
□ Helper utility (nice to have)
```

#### Reference Documents Needed

```
Document Name: ____________________
Content: ____________________
Size Estimate: ____ KB
□ Essential (must have)
□ Reference (nice to have)

Document Name: ____________________
Content: ____________________
Size Estimate: ____ KB
□ Essential (must have)
□ Reference (nice to have)

Document Name: ____________________
Content: ____________________
Size Estimate: ____ KB
□ Essential (must have)
□ Reference (nice to have)
```

#### Assets You'll Need

```
Asset Name: ____________________
Type: ____________________
Usage: ____________________
□ Required in output
□ Template/boilerplate

Asset Name: ____________________
Type: ____________________
Usage: ____________________
□ Required in output
□ Template/boilerplate
```

### 2.2 Feature Matrix

| Feature | Scope | Complexity | Priority | Assigned To | Status |
|---------|-------|-----------|----------|------------|--------|
| | High/Med/Low | High/Med/Low | 1-10 | | To-do |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |

### 2.3 Documentation Structure

Sketch your SKILL.md structure:

```
# Skill Title

## Overview
[1-2 sentences]

## Core Capabilities
- Feature 1
- Feature 2
- Feature 3

## Quick Start
[Code example]

## Workflows
### Workflow 1: [Name]
### Workflow 2: [Name]
### Workflow 3: [Name]

## References
- references/api_guide.md
- references/setup.md
```

---

## PHASE 3: DEVELOPMENT

### 3.1 Skill Configuration

**Skill Name:** `____________________`

**Description (be specific and include keywords):**
```
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
```

**Python Version Required:** 
```
☐ 3.7+  ☐ 3.8+  ☐ 3.9+  ☐ 3.10+  ☐ 3.11+
```

**External Dependencies:**
```
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
```

### 3.2 Script Template

Use this template for each script you create:

```python
"""
[Module name]

[Description of what this module does]
"""

from typing import Dict, List, Optional, Any


class [ClassName]:
    """[Brief description]."""
    
    def __init__(self, [parameters]):
        """Initialize.
        
        Args:
            [param]: [description]
            
        Raises:
            [ExceptionType]: [when]
        """
        self.attribute = value
    
    def method_one(self, param: str) -> Dict[str, Any]:
        """Do something.
        
        Args:
            param: Description
            
        Returns:
            Dictionary with results
            
        Raises:
            ValueError: If invalid
        """
        # Implementation
        return result
    
    def method_two(self) -> List[str]:
        """Do another thing.
        
        Returns:
            List of items
        """
        # Implementation
        return items
```

### 3.3 Reference Document Template

```markdown
# [Topic] Reference

## Table of Contents
1. [Section 1](#section-1)
2. [Section 2](#section-2)
3. [Section 3](#section-3)

## Section 1: [Name]

Description...

### Subsection 1.1
Details...

## Section 2: [Name]

Description...

### Subsection 2.1
Details...

## Section 3: [Name]

Description...
```

### 3.4 SKILL.md Template

```markdown
---
name: your-skill-name
description: Comprehensive description including what it does 
and specific scenarios for when to use it. Include key terms 
that make it discoverable.
---

# Skill Title

## Overview

[1-2 sentences explaining what this enables]

## Core Capabilities

1. **Capability 1** - What it does
2. **Capability 2** - What it does
3. **Capability 3** - What it does

## Quick Start

```python
# Minimal working example
from your_module import YourClass

obj = YourClass(param="value")
result = obj.do_something()
print(result)
```

## Common Workflows

### Workflow 1: [Name]

[Description of what this workflow accomplishes]

```python
# Code example
result = obj.workflow_1(param="value")
```

### Workflow 2: [Name]

[Description of what this workflow accomplishes]

```python
# Code example
result = obj.workflow_2(option="value")
```

### Workflow 3: [Name]

[Description of what this workflow accomplishes]

```python
# Code example
result = obj.workflow_3()
```

## Advanced Usage

See `references/advanced_guide.md` for detailed patterns.

## References

- `references/api_reference.md` - Complete API documentation
- `references/authentication.md` - Setup and credentials
- `references/examples.md` - Additional code examples
```

---

## PHASE 4: TESTING

### 4.1 Script Testing Checklist

For each script, verify:

```
Script: ____________________

□ Imports work correctly
□ Class/function instantiation works
□ Core methods execute without errors
□ Error handling works as expected
□ All docstrings are present
□ Code follows style guidelines
□ Example code from docs runs
□ Performance is acceptable
□ No security issues
□ Dependencies are documented
```

### 4.2 Documentation Validation

```
SKILL.md
□ YAML frontmatter is valid
□ name field present
□ description field present
□ Description is specific and clear
□ Overview section present
□ Quick start code example works
□ All references exist
□ No broken links
□ Grammar/spelling checked

References
□ All referenced files exist
□ Content is accurate
□ Examples are correct
□ No duplication with SKILL.md
□ Clear and organized

Assets
□ All files needed for output
□ Templates are production-ready
□ No unnecessary files
```

### 4.3 Packaging Validation

```bash
# Run this command and verify
python3 /mnt/skills/examples/skill-creator/scripts/package_skill.py ./your-skill

# Expected output:
# ✅ Skill is valid!
# ✅ Successfully packaged skill to: your-skill.skill

# Then verify contents:
unzip -l your-skill.skill

# Should show:
# your-skill/SKILL.md
# your-skill/scripts/...
# your-skill/references/...
```

---

## PHASE 5: DOCUMENTATION

### 5.1 Quick Start Guide Template

```markdown
# [Skill Name] - Quick Start

## 5-Minute Setup

1. [First step]
2. [Second step]
3. [Third step]

## First Command

```python
[Working example]
```

## Common Tasks

[5-10 common task examples]

## Troubleshooting

[Common issues and solutions]
```

### 5.2 Overview Document Template

```markdown
# [Skill Name] - Project Overview

## What's Included

[List all components]

## Key Features

[5-10 main features]

## Use Cases

[5-10 example use cases]

## Getting Started

[Quick instructions]

## File Structure

[Directory layout explanation]
```

---

## PHASE 6: PACKAGING

### 6.1 Pre-Packaging Checklist

Before running package_skill.py:

```
☐ All scripts tested and working
☐ All references verified
☐ SKILL.md complete and error-free
☐ Removed unused template files
☐ All docstrings present
☐ No broken imports
☐ No hardcoded credentials
☐ Error handling implemented
☐ Performance acceptable
☐ Documentation clear
☐ Examples tested
☐ No typos in descriptions
```

### 6.2 Packaging Commands

```bash
# Initialize (only if starting fresh)
python3 /mnt/skills/examples/skill-creator/scripts/init_skill.py your-skill-name --path ~/skills

# Package when ready
python3 /mnt/skills/examples/skill-creator/scripts/package_skill.py ~/skills/your-skill-name

# Package to specific output
python3 /mnt/skills/examples/skill-creator/scripts/package_skill.py ~/skills/your-skill-name ./dist

# Verify the package
unzip -l your-skill-name.skill

# Create complete bundle (optional)
zip -r your-skill-complete.zip your-skill-name.skill documentation.md quick_start.md
```

---

## PHASE 7: ITERATION

### 7.1 Feedback Collection

After releasing your skill, track feedback:

```
Issue #1
Reported: ____________________
Impact: High / Medium / Low
Fix: ____________________
Status: ☐ Fixed ☐ Won't fix ☐ Pending

Issue #2
Reported: ____________________
Impact: High / Medium / Low
Fix: ____________________
Status: ☐ Fixed ☐ Won't fix ☐ Pending

Issue #3
Reported: ____________________
Impact: High / Medium / Low
Fix: ____________________
Status: ☐ Fixed ☐ Won't fix ☐ Pending
```

### 7.2 Versioning

Track your skill versions:

```
Version 1.0 (Initial Release)
- Features: [list]
- Date: [date]

Version 1.1 (Improvements)
- Added: [feature]
- Fixed: [bug]
- Date: [date]

Version 2.0 (Major Update)
- Breaking changes: [list]
- New features: [list]
- Date: [date]
```

### 7.3 Improvement Cycle

```
Usage → Feedback → Analysis → Implementation → Testing → Repackage

Repeat for each major iteration
```

---

## Example: Spotify Skill

### Completed PHASE 1

**Problem:** Users can't easily create intelligent playlists programmatically

**Users:** Music automation enthusiasts, app developers

**One sentence:** Enable Claude to create and manage Spotify playlists intelligently

**5 Use Cases:**
1. Create playlist from artist name → Get top tracks
2. Create playlist from theme → Search keywords
3. Add specific songs → Manual song list
4. List playlists → Organize music
5. Control playback → Manage playback

### Completed PHASE 2

**Scripts:**
- spotify_client.py (40+ methods)
- playlist_creator.py (6 methods)

**References:**
- authentication_guide.md (OAuth setup)
- api_reference.md (All endpoints)

**Assets:** None

### Completed PHASE 3-7

Result: spotify-api.skill (production-ready)

---

## Quick Decision Tree

**Should this be a script or reference?**

```
Is it code that gets executed?
├─ YES → scripts/
└─ NO → references/

Is it large (>5k words)?
├─ YES → references/ (separate file)
└─ NO → SKILL.md (can include inline)

Will it be modified by users?
├─ YES → assets/
└─ NO → scripts/ or references/
```

**Should this be in SKILL.md or references?**

```
Is it essential for quick start?
├─ YES → SKILL.md
└─ NO → references/

Is it used frequently?
├─ YES → SKILL.md
└─ NO → references/

Is it more than 1000 words?
├─ YES → references/
└─ NO → Can be in SKILL.md
```

---

## Resources

- [Skill Creator Guide](https://example.com/skill-creator)
- [Best Practices](https://example.com/best-practices)
- [API Documentation](https://example.com/api)
- [Example Skills](https://example.com/examples)

---

## Notes Section

Use this space for your own notes:

```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

**Happy skill creating!** 🚀
