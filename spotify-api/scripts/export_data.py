"""
Export Spotify data as JSON for use in applications without API calls.

This script fetches data from Spotify API and saves it as JSON files that can be
imported directly into React/web applications, avoiding runtime API calls.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from spotify_client import create_client_from_env, validate_credentials, get_validation_errors


class SpotifyDataExporter:
    """Export Spotify data to JSON files."""
    
    def __init__(self, output_dir: str = "exported_data"):
        """
        Initialize exporter.
        
        Args:
            output_dir: Directory to save exported JSON files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize client
        self.client = create_client_from_env()
        if self.client.refresh_token:
            self.client.refresh_access_token()
    
    def export_user_profile(self) -> Dict:
        """
        Export user profile data.
        
        Returns:
            User profile dictionary
        """
        print("📊 Exporting user profile...")
        user = self.client.get_current_user()
        
        # Sanitize data for export
        exported = {
            'id': user.get('id'),
            'display_name': user.get('display_name'),
            'email': user.get('email'),
            'country': user.get('country'),
            'product': user.get('product'),
            'followers': user.get('followers', {}).get('total', 0),
            'images': user.get('images', []),
            'external_urls': user.get('external_urls', {}),
            'exported_at': self._get_timestamp()
        }
        
        self._save_json('user_profile.json', exported)
        print(f"   ✓ Saved to {self.output_dir}/user_profile.json")
        return exported
    
    def export_playlists(self, limit: int = 50) -> List[Dict]:
        """
        Export user's playlists.
        
        Args:
            limit: Maximum number of playlists to export
            
        Returns:
            List of playlist dictionaries
        """
        print(f"📊 Exporting playlists (limit: {limit})...")
        playlists = self.client.get_user_playlists(limit=limit)
        
        # Sanitize data for export
        exported = []
        for playlist in playlists:
            exported.append({
                'id': playlist.get('id'),
                'name': playlist.get('name'),
                'description': playlist.get('description'),
                'public': playlist.get('public'),
                'tracks_total': playlist.get('tracks', {}).get('total', 0),
                'images': playlist.get('images', []),
                'external_urls': playlist.get('external_urls', {}),
                'owner': {
                    'id': playlist.get('owner', {}).get('id'),
                    'display_name': playlist.get('owner', {}).get('display_name')
                }
            })
        
        self._save_json('playlists.json', exported)
        print(f"   ✓ Saved {len(exported)} playlists to {self.output_dir}/playlists.json")
        return exported
    
    def export_top_artists(self, time_range: str = 'medium_term', limit: int = 20) -> List[Dict]:
        """
        Export user's top artists.
        
        Args:
            time_range: 'short_term', 'medium_term', or 'long_term'
            limit: Maximum number of artists to export
            
        Returns:
            List of artist dictionaries
        """
        print(f"📊 Exporting top artists ({time_range}, limit: {limit})...")
        artists = self.client.get_user_top_artists(time_range=time_range, limit=limit)
        
        # Sanitize data for export
        exported = []
        for artist in artists:
            exported.append({
                'id': artist.get('id'),
                'name': artist.get('name'),
                'genres': artist.get('genres', []),
                'popularity': artist.get('popularity'),
                'followers': artist.get('followers', {}).get('total', 0),
                'images': artist.get('images', []),
                'external_urls': artist.get('external_urls', {})
            })
        
        filename = f'top_artists_{time_range}.json'
        self._save_json(filename, exported)
        print(f"   ✓ Saved {len(exported)} artists to {self.output_dir}/{filename}")
        return exported
    
    def export_top_tracks(self, time_range: str = 'medium_term', limit: int = 20) -> List[Dict]:
        """
        Export user's top tracks.
        
        Args:
            time_range: 'short_term', 'medium_term', or 'long_term'
            limit: Maximum number of tracks to export
            
        Returns:
            List of track dictionaries
        """
        print(f"📊 Exporting top tracks ({time_range}, limit: {limit})...")
        tracks = self.client.get_user_top_tracks(time_range=time_range, limit=limit)
        
        # Sanitize data for export
        exported = []
        for track in tracks:
            exported.append({
                'id': track.get('id'),
                'name': track.get('name'),
                'artists': [{'id': a.get('id'), 'name': a.get('name')} for a in track.get('artists', [])],
                'album': {
                    'id': track.get('album', {}).get('id'),
                    'name': track.get('album', {}).get('name'),
                    'images': track.get('album', {}).get('images', [])
                },
                'duration_ms': track.get('duration_ms'),
                'popularity': track.get('popularity'),
                'preview_url': track.get('preview_url'),
                'external_urls': track.get('external_urls', {})
            })
        
        filename = f'top_tracks_{time_range}.json'
        self._save_json(filename, exported)
        print(f"   ✓ Saved {len(exported)} tracks to {self.output_dir}/{filename}")
        return exported
    
    def export_playlist_tracks(self, playlist_id: str, playlist_name: Optional[str] = None) -> List[Dict]:
        """
        Export tracks from a specific playlist.
        
        Args:
            playlist_id: Spotify playlist ID
            playlist_name: Optional name for the output file
            
        Returns:
            List of track dictionaries
        """
        print(f"📊 Exporting playlist tracks (ID: {playlist_id})...")
        tracks = self.client.get_playlist_tracks(playlist_id)
        
        # Sanitize data for export
        exported = []
        for item in tracks:
            track = item.get('track', {})
            if track:
                exported.append({
                    'id': track.get('id'),
                    'name': track.get('name'),
                    'artists': [{'id': a.get('id'), 'name': a.get('name')} for a in track.get('artists', [])],
                    'album': {
                        'id': track.get('album', {}).get('id'),
                        'name': track.get('album', {}).get('name'),
                        'images': track.get('album', {}).get('images', [])
                    },
                    'duration_ms': track.get('duration_ms'),
                    'added_at': item.get('added_at'),
                    'external_urls': track.get('external_urls', {})
                })
        
        filename = f'playlist_{playlist_name or playlist_id}.json'
        filename = filename.replace(' ', '_').replace('/', '_')
        self._save_json(filename, exported)
        print(f"   ✓ Saved {len(exported)} tracks to {self.output_dir}/{filename}")
        return exported
    
    def export_all(self):
        """Export all available data."""
        print("\n" + "=" * 60)
        print("🎵 Spotify Data Export")
        print("=" * 60 + "\n")
        
        try:
            self.export_user_profile()
            self.export_playlists()
            self.export_top_artists()
            self.export_top_tracks()
            
            print("\n" + "=" * 60)
            print("✅ Export complete!")
            print(f"📁 Files saved to: {self.output_dir.absolute()}")
            print("=" * 60 + "\n")
            
        except Exception as e:
            print(f"\n❌ Export failed: {str(e)}\n")
            raise
    
    def _save_json(self, filename: str, data: any):
        """Save data as JSON file."""
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Main entry point."""
    # Validate credentials first
    validation = validate_credentials()
    
    if not validation['all_valid']:
        print("\n❌ Missing Spotify credentials!\n")
        errors = get_validation_errors()
        for error in errors:
            print(error)
        print()
        return 1
    
    # Export data
    try:
        exporter = SpotifyDataExporter()
        exporter.export_all()
        
        print("💡 Usage in React/Web apps:")
        print("   import userData from './exported_data/user_profile.json';")
        print("   import playlists from './exported_data/playlists.json';")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        return 1


if __name__ == '__main__':
    exit(main())
