# Contributing to Spotify Skills for Claude

Thank you for your interest in contributing! This project welcomes contributions of all kinds - from bug reports to new features to additional skill examples.

## 🚀 Quick Start for Contributors

1. **Fork & Clone**: Fork the repo and clone locally
2. **Set up environment**: `python -m venv .venv && .venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
3. **Install dependencies**: `pip install -r spotify-api/requirements.txt`
4. **Make changes**: Work on your feature/fix
5. **Test**: Validate your skill with `python tools/validate_skill.py ./spotify-api`
6. **Submit PR**: Open a pull request with clear description

## 🎯 Contribution Types

### 🐛 Bug Reports
**Found an issue?** [Open a bug report](https://github.com/fabioc-aloha/spotify-skill/issues/new?template=bug_report.yml)

### 💡 Feature Requests
**Have an idea?** [Suggest a feature](https://github.com/fabioc-aloha/spotify-skill/issues/new?template=feature_request.yml)

### 📖 Documentation
**Improve clarity**: Fix typos, add examples, clarify instructions

### 🔧 Code Contributions
**Bug fixes**: Address reported issues
**Features**: Add new capabilities (discuss first in issues)
**Refactoring**: Improve code quality

### 🎨 Example Skills
**Share your work**: Created a useful skill? Add it to `examples/`

## 📋 Reporting Issues

## 📋 Reporting Issues

**Include these details:**
- Clear description of the issue
- Steps to reproduce (numbered list)
- Expected vs actual behavior
- Environment: OS, Python version, Claude Desktop version
- Error messages or screenshots
- Related files (if applicable)

**Pro tip**: Check [existing issues](https://github.com/fabioc-aloha/spotify-skill/issues) first to avoid duplicates.

## 💡 Suggesting Features

## 💡 Suggesting Features

**Provide this information:**
- **Use case**: What problem does this solve?
- **Value**: Why is this important?
- **Examples**: Show what you envision (code, mockups, workflows)
- **Alternatives**: Have you considered other approaches?

**Pro tip**: Start a [Discussion](https://github.com/fabioc-aloha/spotify-skill/discussions) for major features to get community feedback first.

## 🔧 Pull Request Process

### Before You Start

1. **Check existing work**: Browse [issues](https://github.com/fabioc-aloha/spotify-skill/issues) and [PRs](https://github.com/fabioc-aloha/spotify-skill/pulls)
2. **Claim the issue**: Comment "I'll work on this" to avoid duplicate effort
3. **Discuss approach**: For large changes, outline your plan in the issue

### Development Workflow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/spotify-skill.git
cd spotify-skill

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Set up environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux
pip install -r spotify-api/requirements.txt

# 4. Make your changes
# ... edit files ...

# 5. Validate (if editing skill files)
python tools/validate_skill.py ./spotify-api

# 6. Test locally
# Test your changes thoroughly

# 7. Commit with clear messages
git add .
git commit -m "feat: add playlist shuffle feature"

# 8. Push to your fork
git push origin feature/your-feature-name

# 9. Open PR on GitHub
```

### PR Requirements

✅ **Must Have:**
- Clear description of changes
- Link to related issue(s)
- Tests pass (run validation tool)
- Documentation updated (if applicable)
- Commits are focused and well-described

✅ **Good to Have:**
- Screenshots/examples of new features
- Before/after comparisons
- Performance considerations noted

### Commit Message Format

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: add batch playlist creation tool
fix: resolve OAuth token refresh issue
docs: clarify cover art generation steps
refactor: improve error handling in spotify_client
```

## 📝 Code Standards

## 📝 Code Standards

### Python Code
- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use meaningful variable/function names
- Add docstrings for classes and functions
- Keep functions focused and small
- Handle errors gracefully with try/except

### Documentation
- Use clear, concise language
- Include practical examples
- Test all code snippets
- Check spelling and grammar
- Verify all links work

### Skill Development
- Follow [Agent Skills Spec](agent_skills_spec.md)
- Keep SKILL.md under 5,000 words
- Use YAML frontmatter correctly
- Validate before submitting: `python tools/validate_skill.py ./your-skill`

## 🎨 Contributing Example Skills

Have you created a useful skill? Share it with the community!

### What Makes a Good Example

- **Solves a real problem**: Addresses actual use cases
- **Well-documented**: Clear SKILL.md with examples
- **Different pattern**: Shows something not already covered
- **Production-ready**: Tested and working

### How to Submit

1. Create your skill in a new folder under `examples/`
2. Ensure it validates: `python tools/validate_skill.py ./examples/your-skill`
3. Add entry to `examples/README.md` with description
4. Open PR with "example:" prefix: `example: add weather API skill`

## 🧪 Testing

### Manual Testing
- Test all modified features
- Try different scenarios (success, errors, edge cases)
- Verify on your environment

### Validation Tool
```bash
# Validate skill structure
python tools/validate_skill.py ./spotify-api

# Package to check contents
python tools/package_skill.py ./spotify-api ./test-dist
```

## 📚 Documentation Changes

## 📚 Documentation Changes

**Checklist:**
- [ ] Information is accurate and up-to-date
- [ ] Examples are tested and work
- [ ] Links are valid
- [ ] Spelling and grammar checked
- [ ] Follows existing formatting style
- [ ] Cross-references updated if needed

**Files to Update:**
- `README.md` - Overview and quick reference
- `USER_GUIDE.md` - Comprehensive usage instructions
- `QUICK_START.md` - Fast setup guide
- `CHANGELOG.md` - Version history (for releases)
- Skill-specific docs in `spotify-api/`

## 🗣️ Getting Help

**Before Starting:**
- Read [USER_GUIDE.md](USER_GUIDE.md) for comprehensive documentation
- Check [Guide/00_START_HERE.md](Guide/00_START_HERE.md) for skill creation help
- Browse [GitHub Discussions](https://github.com/fabioc-aloha/spotify-skill/discussions)

**Need Assistance:**
- 💬 **Questions**: Use [GitHub Discussions](https://github.com/fabioc-aloha/spotify-skill/discussions)
- 🐛 **Bugs**: [Open an issue](https://github.com/fabioc-aloha/spotify-skill/issues/new?template=bug_report.yml)
- 🔍 **Clarifications**: Comment on relevant issues/PRs

## ✅ PR Review Process

### What to Expect

1. **Automated checks**: Validation and linting run automatically
2. **Maintainer review**: Usually within 2-3 business days
3. **Feedback**: We may request changes or clarifications
4. **Iteration**: Update your PR based on feedback
5. **Merge**: Once approved, we'll merge your contribution!

### Tips for Faster Review

- Keep PRs focused (one feature/fix per PR)
- Respond to feedback promptly
- Be patient and professional
- Update your branch if conflicts arise

## 🤝 Code of Conduct

### Our Standards

- **Be respectful**: Treat everyone with kindness and respect
- **Be inclusive**: Welcome people of all backgrounds and experience levels
- **Be constructive**: Provide helpful feedback, not just criticism
- **Be patient**: Remember everyone is learning
- **Be collaborative**: Work together to solve problems

### Unacceptable Behavior

- Harassment, trolling, or personal attacks
- Spam or off-topic content
- Sharing private information without consent
- Violation of privacy or security

**Reporting**: Email maintainers or use GitHub's reporting features

## 🎯 Priority Areas

Want to make a high-impact contribution? Focus on these areas:

### High Priority
- 🐛 **Bug fixes** - See [issues labeled "bug"](https://github.com/fabioc-aloha/spotify-skill/labels/bug)
- 📖 **Documentation improvements** - Clarify confusing sections
- 🎨 **Example skills** - More real-world patterns

### Medium Priority
- ✨ **New features** - Enhance existing capabilities
- 🧪 **Test coverage** - Add validation and error handling
- ♿ **Accessibility** - Improve cover art contrast and readability

### Community Requests
- Check [issues labeled "enhancement"](https://github.com/fabioc-aloha/spotify-skill/labels/enhancement)
- Vote with 👍 on features you'd like to see
- Comment with your use cases

## 📄 License

By contributing, you agree that your contributions will be licensed under the **Apache License 2.0**.

Your contributions will be attributed in:
- Git commit history
- Release notes (for significant contributions)
- CHANGELOG.md (for features and major fixes)

---

## 🎉 Thank You!

Every contribution matters - whether it's a typo fix or a major feature. Thank you for helping make **Spotify Skills for Claude** better for everyone!

**Join the community:**
- ⭐ [Star the repo](https://github.com/fabioc-aloha/spotify-skill)
- 💬 [Join discussions](https://github.com/fabioc-aloha/spotify-skill/discussions)
- 🐦 Share with others

---

<div align="center">

**Questions?** Check our [Documentation](USER_GUIDE.md) or [Start a Discussion](https://github.com/fabioc-aloha/spotify-skill/discussions)

**Current Release**: [v0.9.0](https://github.com/fabioc-aloha/spotify-skill/releases/tag/v0.9.0)

</div>
