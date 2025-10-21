#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable zip file of a skill folder

This tool is from the Anthropic Claude Skills repository:
https://github.com/anthropics/skills

Usage:
    python package_skill.py <path/to/skill-folder> [output-directory]

Examples:
    python package_skill.py ./spotify-api
    python package_skill.py ./spotify-api ./dist
    python package_skill.py c:/Development/MySkills/my-skill ./packages

Licensed under Apache License 2.0
Copyright Anthropic, PBC
"""

import sys
import zipfile
from pathlib import Path

# Import validation from validate_skill
try:
    from validate_skill import validate_skill  # type: ignore
except ImportError:
    print("⚠️  Warning: Could not import validate_skill. Skipping validation.")
    def validate_skill(skill_path):
        return True, "Validation skipped (validate_skill.py not found)"


def package_skill(skill_path, output_dir=None):
    """
    Package a skill folder into a zip file.

    Args:
        skill_path: Path to the skill folder
        output_dir: Optional output directory for the zip file (defaults to current directory)

    Returns:
        Path to the created zip file, or None if error
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return None

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ Error: SKILL.md not found in {skill_path}")
        return None

    # Run validation before packaging
    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"✅ {message}\n")

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    zip_filename = output_path / f"{skill_name}.zip"

    # Create the zip file
    try:
        print(f"📦 Creating package: {zip_filename}")
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the skill directory
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # Skip common files that shouldn't be in package
                    if file_path.name in ['.DS_Store', 'Thumbs.db', '.gitignore']:
                        continue
                    
                    # Skip Python cache directories
                    if '__pycache__' in file_path.parts:
                        continue
                    
                    # Calculate the relative path within the zip
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  ✓ Added: {arcname}")

        print(f"\n✅ Successfully packaged skill to: {zip_filename}")
        print(f"   Size: {zip_filename.stat().st_size:,} bytes")
        return zip_filename

    except Exception as e:
        print(f"❌ Error creating zip file: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <path/to/skill-folder> [output-directory]")
        print("\nExamples:")
        print("  python package_skill.py ./spotify-api")
        print("  python package_skill.py ./spotify-api ./dist")
        print("  python package_skill.py c:/Development/MySkills/my-skill ./packages")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
