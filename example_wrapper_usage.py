"""
Example: Using SpotifyAPIWrapper for robust applications

This demonstrates how to use the wrapper for applications that need
graceful error handling and fallback data.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'spotify-api' / 'scripts'))

from spotify_client import SpotifyAPIWrapper, validate_credentials, get_validation_errors


def example_with_fallback():
    """Example using wrapper with fallback data."""
    print("\n" + "=" * 60)
    print("Example 1: Using SpotifyAPIWrapper with Fallback")
    print("=" * 60 + "\n")
    
    # Create wrapper with fallback enabled (default)
    wrapper = SpotifyAPIWrapper(use_fallback=True)
    
    # Check if API is available
    if wrapper.is_available():
        print("✅ Spotify API is available")
    else:
        print(f"⚠️  Spotify API unavailable: {wrapper.get_error()}")
        print("   Using fallback data instead\n")
    
    # These calls will return empty lists/mock data if API fails
    # Perfect for React apps that need to render even without API
    
    print("📊 Fetching user profile...")
    user = wrapper.get_user_profile()
    print(f"   User: {user.get('display_name', 'Unknown')}\n")
    
    print("📋 Fetching playlists...")
    playlists = wrapper.get_user_playlists(limit=5)
    print(f"   Found {len(playlists)} playlists\n")
    
    print("🔍 Searching for tracks...")
    tracks = wrapper.search_tracks("The Beatles", limit=3)
    print(f"   Found {len(tracks)} tracks\n")
    
    return wrapper.is_available()


def example_with_validation():
    """Example with upfront validation."""
    print("\n" + "=" * 60)
    print("Example 2: Validate Credentials First")
    print("=" * 60 + "\n")
    
    # Check credentials before attempting API calls
    validation = validate_credentials()
    
    print("Credential Status:")
    print(f"  Client ID:     {'✅' if validation['client_id'] else '❌'}")
    print(f"  Client Secret: {'✅' if validation['client_secret'] else '❌'}")
    print(f"  Refresh Token: {'✅' if validation['refresh_token'] else '❌'}")
    print()
    
    if not validation['all_valid']:
        print("❌ Missing credentials!\n")
        errors = get_validation_errors()
        for error in errors:
            print(f"   {error}")
        print()
        return False
    
    print("✅ All credentials present - proceeding with API calls\n")
    
    # Now safe to create wrapper
    wrapper = SpotifyAPIWrapper(use_fallback=False)  # Strict mode
    
    try:
        user = wrapper.get_user_profile()
        print(f"👤 Logged in as: {user.get('display_name')}\n")
        return True
    except Exception as e:
        print(f"❌ API call failed: {str(e)}\n")
        return False


def example_for_react_app():
    """Example data fetching for React/web apps."""
    print("\n" + "=" * 60)
    print("Example 3: Data Fetching for React Apps")
    print("=" * 60 + "\n")
    
    # Use wrapper with fallback for React apps
    # This ensures your app always has data to render
    wrapper = SpotifyAPIWrapper(use_fallback=True)
    
    # Build a data structure for your React component
    app_data = {
        'user': wrapper.get_user_profile(),
        'playlists': wrapper.get_user_playlists(limit=10),
        'isApiAvailable': wrapper.is_available(),
        'error': wrapper.get_error()
    }
    
    # Your React app can now use this data
    print("📦 Data prepared for React app:")
    print(f"   User: {app_data['user'].get('display_name')}")
    print(f"   Playlists: {len(app_data['playlists'])}")
    print(f"   API Available: {app_data['isApiAvailable']}")
    
    if not app_data['isApiAvailable']:
        print(f"   Note: Using fallback data ({app_data['error']})")
    
    print()
    
    # In your React app, you could save this as JSON:
    # import json
    # with open('public/spotify-data.json', 'w') as f:
    #     json.dump(app_data, f)
    
    return app_data


def main():
    """Run all examples."""
    print("\n🎵 Spotify API Skill - Wrapper Examples\n")
    
    # Run examples
    result1 = example_with_fallback()
    result2 = example_with_validation()
    result3 = example_for_react_app()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60 + "\n")
    
    print("💡 Key Takeaways:")
    print()
    print("1. SpotifyAPIWrapper provides graceful error handling")
    print("2. Set use_fallback=True for apps that need to render without API")
    print("3. Validate credentials before critical operations")
    print("4. Use export_data.py to pre-generate JSON for static apps")
    print()
    
    print("📚 See also:")
    print("   - spotify-api/scripts/export_data.py - Export data as JSON")
    print("   - spotify-api/scripts/test_credentials.py - Full validation")
    print()


if __name__ == '__main__':
    main()
