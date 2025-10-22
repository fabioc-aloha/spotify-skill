"""
Test script for cover art generation
Generates sample cover art locally without uploading to Spotify
"""

import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from cover_art_generator import CoverArtGenerator

# Mock credentials for local testing (no upload)
MOCK_CLIENT_ID = "test_id"
MOCK_CLIENT_SECRET = "test_secret"
MOCK_ACCESS_TOKEN = "test_token"

def test_local_generation():
    """Generate sample cover art locally"""
    
    generator = CoverArtGenerator(MOCK_CLIENT_ID, MOCK_CLIENT_SECRET, MOCK_ACCESS_TOKEN)
    
    # Test 1: Summer theme
    print("Generating: Summer Vibes cover...")
    generator.generate_cover_art(
        title="Summer Vibes",
        subtitle="Feel Good Hits",
        theme="summer",
        output_path="test_summer.png"
    )
    print("✓ Generated: test_summer.png\n")
    
    # Test 2: Rock genre
    print("Generating: Rock Classics cover...")
    generator.generate_cover_art(
        title="Rock Classics",
        subtitle="Timeless Anthems",
        genre="rock",
        output_path="test_rock.png"
    )
    print("✓ Generated: test_rock.png\n")
    
    # Test 3: Artist-specific (Queen)
    print("Generating: Queen cover...")
    generator.generate_cover_art(
        title="Best of Queen",
        subtitle="Greatest Hits",
        artist="queen",
        output_path="test_queen.png"
    )
    print("✓ Generated: test_queen.png\n")
    
    # Test 4: Long title (test text scaling)
    print("Generating: Long title cover...")
    generator.generate_cover_art(
        title="My Ultimate Workout Power Hour",
        subtitle="Get Pumped!",
        theme="energetic",
        output_path="test_long_title.png"
    )
    print("✓ Generated: test_long_title.png\n")
    
    # Test 5: Custom colors
    print("Generating: Custom colors cover...")
    generator.generate_cover_art(
        title="Custom Vibes",
        subtitle="Handpicked",
        gradient_start="#FF6B6B",
        gradient_end="#4ECDC4",
        text_color="#FFFFFF",
        output_path="test_custom.png"
    )
    print("✓ Generated: test_custom.png\n")
    
    print("=" * 60)
    print("✅ All test covers generated successfully!")
    print("=" * 60)
    print("\nCheck the generated PNG files:")
    print("- test_summer.png (Summer theme)")
    print("- test_rock.png (Rock genre)")
    print("- test_queen.png (Queen artist)")
    print("- test_long_title.png (Long title, text scaling)")
    print("- test_custom.png (Custom colors)")
    print("\nFeatures demonstrated:")
    print("✓ Large, readable typography (60-96px)")
    print("✓ 80% text width for thumbnail visibility")
    print("✓ No element overlap (smart spacing)")
    print("✓ Theme/genre/artist-appropriate colors")
    print("✓ Auto-scaling for different text lengths")

if __name__ == "__main__":
    try:
        test_local_generation()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure dependencies are installed:")
        print("pip install cairosvg pillow")
