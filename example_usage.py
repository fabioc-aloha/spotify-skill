"""
Example: Using the Spotify API Skill

This demonstrates the key features of the Spotify API skill.
"""

import sys
sys.path.insert(0, 'spotify-api/scripts')

from spotify_client import create_client_from_env
from playlist_creator import PlaylistCreator

def main():
    print("🎵 Spotify API Skill - Example Usage\n")
    
    # Initialize client from environment variables
    print("1️⃣ Initializing Spotify client...")
    client = create_client_from_env()
    
    # Refresh access token if available
    if client.refresh_token:
        client.refresh_access_token()
        print("   ✓ Access token refreshed\n")
    
    # Get current user info
    print("2️⃣ Getting user profile...")
    user = client.get_current_user()
    print(f"   ✓ Logged in as: {user.get('display_name', 'Unknown')}")
    print(f"   ✓ User ID: {user.get('id', 'Unknown')}\n")
    
    # List user's playlists
    print("3️⃣ Fetching your playlists...")
    playlists = client.get_user_playlists(limit=5)
    print(f"   ✓ Found {len(playlists)} playlists (showing first 5):")
    for i, playlist in enumerate(playlists[:5], 1):
        name = playlist.get('name', 'Unknown')
        tracks = playlist.get('tracks', {}).get('total', 0)
        print(f"      {i}. {name} ({tracks} tracks)")
    print()
    
    # Search for an artist
    print("4️⃣ Searching for 'Radiohead'...")
    artists = client.search_artists(query="Radiohead", limit=1)
    if artists:
        artist = artists[0]
        print(f"   ✓ Found: {artist.get('name')}")
        print(f"   ✓ Followers: {artist.get('followers', {}).get('total', 0):,}")
        print(f"   ✓ Genres: {', '.join(artist.get('genres', [])[:3])}")
        print()
        
        # Get top tracks
        print("5️⃣ Getting Radiohead's top tracks...")
        top_tracks = client.get_artist_top_tracks(artist['id'])[:5]
        print(f"   ✓ Top 5 tracks:")
        for i, track in enumerate(top_tracks, 1):
            print(f"      {i}. {track.get('name')}")
    print()
    
    # Search for a track
    print("6️⃣ Searching for tracks with 'karma police'...")
    tracks = client.search_tracks(query="karma police", limit=3)
    print(f"   ✓ Found {len(tracks)} tracks:")
    for i, track in enumerate(tracks, 1):
        track_name = track.get('name')
        artist_name = track.get('artists', [{}])[0].get('name', 'Unknown')
        print(f"      {i}. {track_name} - {artist_name}")
    print()
    
    print("✅ Spotify API Skill is working correctly!")
    print("\n💡 You can now use this skill to:")
    print("   - Create intelligent playlists by artist, theme, or lyrics")
    print("   - Search and discover music")
    print("   - Manage your library and playlists")
    print("   - Control playback")
    print("   - Get recommendations")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
