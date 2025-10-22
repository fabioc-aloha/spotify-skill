"""
Test text wrapping directly
"""
import sys
import os
sys.path.insert(0, 'scripts')

from cover_art_generator import CoverArtGenerator

# Test wrapping directly
gen = CoverArtGenerator("test", "test", "test")

# Test various title lengths
test_titles = [
    "Short",
    "Medium Length Title",
    "This Is A Very Long Title That Should Wrap",
    "My Ultimate Workout Power Hour",
    "The Best Summer Rock Anthems Of All Time",
]

print("Text Wrapping Test:\n")
for title in test_titles:
    lines = gen._wrap_text(title, max_chars_per_line=20)
    print(f"Title: '{title}' ({len(title)} chars)")
    print(f"  Wrapped into {len(lines)} line(s):")
    for i, line in enumerate(lines, 1):
        print(f"    Line {i}: '{line}' ({len(line)} chars)")
    print()

# Now generate actual images
print("\nGenerating test images with various title lengths...")
print("=" * 60)

for i, title in enumerate(test_titles, 1):
    filename = f"wrap_test_{i}.png"
    print(f"\n{i}. Generating: {title}")
    gen.generate_cover_art(
        title=title,
        subtitle="Test",
        theme="energetic",
        output_path=filename
    )
    print(f"   ✓ Saved to: {filename}")

print("\n" + "=" * 60)
print("✅ All test images generated!")
print("Open the wrap_test_*.png files to verify text wrapping")
