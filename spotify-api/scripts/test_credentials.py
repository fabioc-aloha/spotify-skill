"""
Spotify API Skill - Credential and API Test

Run this script to verify your Spotify credentials are correctly configured
and the API is accessible.
"""

import sys
from pathlib import Path

# Add current directory (scripts) to path
sys.path.insert(0, str(Path(__file__).parent))

from spotify_client import create_client_from_env, check_network_access, NetworkAccessError, validate_credentials, get_validation_errors

def test_credentials():
    """Test if credentials are loaded and valid."""
    print("=" * 60)
    print("Spotify API Skill - Credential Test")
    print("=" * 60)
    print()
    
    try:
        # Test 0: Check network access first
        print("0️⃣ Checking network access to api.spotify.com...")
        try:
            check_network_access()
            print("   ✓ Network access OK - api.spotify.com is reachable")
        except NetworkAccessError as e:
            print(str(e))
            return False
        print()
        
        # Test 0.5: Validate credentials before loading
        print("0️⃣.5 Validating credentials...")
        validation = validate_credentials()
        
        if not validation['all_valid']:
            print("   ❌ Credential validation failed!\n")
            errors = get_validation_errors()
            for error in errors:
                print(f"   {error}")
            print()
            return False
        
        print("   ✓ All required credentials found")
        print()
        
        # Test 1: Load credentials
        print("1️⃣ Loading credentials from .env file...")
        client = create_client_from_env()
        print(f"   ✓ Client ID: {client.client_id[:15]}...")
        print(f"   ✓ Client Secret: {client.client_secret[:15]}...")
        print(f"   ✓ Redirect URI: {client.redirect_uri}")
        
        if not client.refresh_token:
            print("\n⚠️  WARNING: No refresh token found!")
            print("   You need to complete OAuth flow to get a refresh token.")
            print("   See references/authentication_guide.md for instructions.")
            return False
        
        print(f"   ✓ Refresh Token: {client.refresh_token[:25]}...")
        print()
        
        # Test 2: Refresh access token
        print("2️⃣ Refreshing access token...")
        token_data = client.refresh_access_token()
        print(f"   ✓ Access token obtained: {client.access_token[:25]}...")
        print(f"   ✓ Token expires in: {token_data.get('expires_in', 'unknown')} seconds")
        print()
        
        # Test 3: Make API call
        print("3️⃣ Testing API access...")
        user = client.get_current_user()
        print(f"   ✓ Successfully connected to Spotify API!")
        print(f"   ✓ User: {user.get('display_name', 'N/A')}")
        print(f"   ✓ User ID: {user.get('id', 'N/A')}")
        print(f"   ✓ Email: {user.get('email', 'N/A')}")
        print(f"   ✓ Country: {user.get('country', 'N/A')}")
        print(f"   ✓ Product: {user.get('product', 'N/A')}")
        print()
        
        # Test 4: Quick functionality check
        print("4️⃣ Testing basic functionality...")
        playlists = client.get_user_playlists(limit=3)
        print(f"   ✓ Found {len(playlists)} playlists")
        
        artists = client.search_artists(query="The Beatles", limit=1)
        print(f"   ✓ Search working (found: {artists[0]['name'] if artists else 'none'})")
        print()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("Your Spotify API skill is configured correctly and ready to use!")
        print()
        
        return True
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print()
        print("Please check your .env file and ensure all required credentials are set:")
        print("  - SPOTIFY_CLIENT_ID")
        print("  - SPOTIFY_CLIENT_SECRET")
        print("  - SPOTIFY_REFRESH_TOKEN")
        print()
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_credentials()
    sys.exit(0 if success else 1)
