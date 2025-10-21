#!/usr/bin/env python3
"""
Skill Validator - Validates skill structure and content

This tool is from the Anthropic Claude Skills repository:
https://github.com/anthropics/skills

Usage:
    python validate_skill.py <skill_directory>

Examples:
    python validate_skill.py ./spotify-api
    python validate_skill.py c:/Development/MySkills/my-skill

Licensed under Apache License 2.0
Copyright Anthropic, PBC
"""

import sys
import os
import re
from pathlib import Path


def validate_skill(skill_path):
    """
    Validate a skill directory structure and SKILL.md content.
    
    Args:
        skill_path: Path to the skill directory
        
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    skill_path = Path(skill_path)
    
    # Check if directory exists
    if not skill_path.exists():
        return False, f"Directory not found: {skill_path}"
    
    if not skill_path.is_dir():
        return False, f"Path is not a directory: {skill_path}"
    
    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found in skill directory"
    
    # Read and validate frontmatter
    try:
        content = skill_md.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"Error reading SKILL.md: {e}"
    
    if not content.startswith('---'):
        return False, "SKILL.md must start with YAML frontmatter (---)"
    
    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid YAML frontmatter format. Must be enclosed in --- markers"
    
    frontmatter = match.group(1)
    
    # Check required fields
    if 'name:' not in frontmatter:
        return False, "Missing required 'name' field in YAML frontmatter"
    
    if 'description:' not in frontmatter:
        return False, "Missing required 'description' field in YAML frontmatter"
    
    # Extract and validate name
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if name_match:
        name = name_match.group(1).strip()
        
        # Check naming convention (hyphen-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Skill name '{name}' must be hyphen-case (lowercase letters, digits, and hyphens only)"
        
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Skill name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        
        # Check if name matches directory name
        if skill_path.name != name:
            return False, f"Skill name '{name}' in SKILL.md must match directory name '{skill_path.name}'"
    
    # Extract and validate description
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        
        # Check description is not a placeholder
        if '[TODO' in description or 'TODO:' in description:
            return False, "Description still contains TODO placeholder - please complete it"
        
        # Check minimum length
        if len(description) < 20:
            return False, f"Description is too short ({len(description)} chars). Should be at least 20 characters and explain what the skill does and when to use it"
    
    # Check that markdown body exists and is not empty
    body_match = re.search(r'^---\n.*?\n---\n(.+)', content, re.DOTALL)
    if not body_match or not body_match.group(1).strip():
        return False, "SKILL.md must have content below the YAML frontmatter"
    
    body = body_match.group(1).strip()
    
    # Check for excessive TODO markers in body
    todo_count = body.count('[TODO') + body.count('TODO:')
    if todo_count > 5:
        return False, f"SKILL.md contains {todo_count} TODO markers - please complete the skill documentation"
    
    # Validate optional directories if they exist
    warnings = []
    
    scripts_dir = skill_path / 'scripts'
    if scripts_dir.exists():
        if not scripts_dir.is_dir():
            return False, "'scripts' exists but is not a directory"
        
        script_files = list(scripts_dir.glob('*.py')) + list(scripts_dir.glob('*.sh'))
        if not script_files:
            warnings.append("'scripts/' directory exists but contains no .py or .sh files")
    
    references_dir = skill_path / 'references'
    if references_dir.exists():
        if not references_dir.is_dir():
            return False, "'references' exists but is not a directory"
        
        ref_files = list(references_dir.glob('*.md')) + list(references_dir.glob('*.txt'))
        if not ref_files:
            warnings.append("'references/' directory exists but contains no .md or .txt files")
    
    assets_dir = skill_path / 'assets'
    if assets_dir.exists():
        if not assets_dir.is_dir():
            return False, "'assets' exists but is not a directory"
    
    # Success message with any warnings
    success_msg = "✅ Skill validation passed!"
    if warnings:
        success_msg += "\n\n⚠️  Warnings:"
        for warning in warnings:
            success_msg += f"\n   - {warning}"
    
    return True, success_msg


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_skill.py <skill_directory>")
        print("\nExamples:")
        print("  python validate_skill.py ./spotify-api")
        print("  python validate_skill.py c:/Development/MySkills/my-skill")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    
    print(f"🔍 Validating skill: {skill_path}\n")
    
    valid, message = validate_skill(skill_path)
    
    print(message)
    
    sys.exit(0 if valid else 1)
