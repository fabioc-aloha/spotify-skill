"""
Spotify Intelligent Playlist Creator

High-level utility for creating playlists from various sources:
- Artist/band name
- Theme/mood keywords
- Lyrics-based content search
- Specific song lists
"""

from typing import List, Dict, Optional, Any
from spotify_client import SpotifyClient


class PlaylistCreator:
    """Create playlists through various methods."""
    
    def __init__(self, client: SpotifyClient):
        """Initialize with Spotify client."""
        self.client = client
        self.max_tracks_per_playlist = 100
    
    def create_from_artist(self, artist_name: str, playlist_name: str = None,
                          playlist_description: str = "", public: bool = True,
                          limit: int = 50) -> Dict[str, Any]:
        """
        Create playlist from artist's top tracks.
        
        Args:
            artist_name: Name of artist or band
            playlist_name: Playlist name (defaults to artist name)
            playlist_description: Optional description
            public: Make playlist public
            limit: Number of tracks to add
            
        Returns:
            Playlist data with track count
        """
        # Search for artist
        artists = self.client.search_artists(query=artist_name, limit=1)
        if not artists:
            raise ValueError(f"Artist '{artist_name}' not found")
        
        artist_id = artists[0]["id"]
        artist_name_actual = artists[0]["name"]
        
        # Get artist's top tracks
        tracks = self.client.get_artist_top_tracks(
            artist_id=artist_id,
            limit=min(limit, 50)
        )
        
        track_ids = [t["id"] for t in tracks]
        
        # Create playlist
        playlist_name = playlist_name or f"{artist_name_actual} Collection"
        if not playlist_description:
            playlist_description = f"Curated collection of {artist_name_actual}'s top tracks"
        
        playlist = self.client.create_playlist(
            name=playlist_name,
            description=playlist_description,
            public=public
        )
        
        # Add tracks
        if track_ids:
            self.client.add_tracks_to_playlist(playlist["id"], track_ids)
        
        return {
            "playlist": playlist,
            "tracks_added": len(track_ids),
            "artist": artist_name_actual
        }
    
    def create_from_theme(self, theme_keywords: List[str], playlist_name: str,
                         playlist_description: str = "", public: bool = True,
                         limit: int = 100) -> Dict[str, Any]:
        """
        Create playlist based on theme/mood keywords.
        
        Args:
            theme_keywords: List of theme keywords (e.g., ["chill", "indie", "2020s"])
            playlist_name: Playlist name
            playlist_description: Optional description
            public: Make playlist public
            limit: Maximum tracks to add
            
        Returns:
            Playlist data with track count and keywords used
        """
        all_tracks = []
        track_ids_set = set()
        
        # Search for each keyword
        for keyword in theme_keywords:
            results = self.client.search_tracks(query=keyword, limit=30)
            for track in results:
                track_id = track["id"]
                if track_id not in track_ids_set:
                    all_tracks.append(track)
                    track_ids_set.add(track_id)
            
            # Stop if we have enough
            if len(all_tracks) >= limit:
                break
        
        # Limit tracks
        track_ids = [t["id"] for t in all_tracks[:limit]]
        
        if not track_ids:
            raise ValueError(f"No tracks found for theme keywords: {theme_keywords}")
        
        # Create playlist
        playlist = self.client.create_playlist(
            name=playlist_name,
            description=playlist_description,
            public=public
        )
        
        # Add tracks in batches (Spotify limit is 100 per request)
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            self.client.add_tracks_to_playlist(playlist["id"], batch)
        
        return {
            "playlist": playlist,
            "tracks_added": len(track_ids),
            "keywords": theme_keywords
        }
    
    def create_from_lyrics(self, lyric_keywords: List[str], playlist_name: str,
                          playlist_description: str = "", public: bool = True,
                          limit: int = 100) -> Dict[str, Any]:
        """
        Create playlist based on lyrical content.
        
        Args:
            lyric_keywords: List of lyrical themes (e.g., ["love", "heartbreak", "midnight"])
            playlist_name: Playlist name
            playlist_description: Optional description
            public: Make playlist public
            limit: Maximum tracks to add
            
        Returns:
            Playlist data with track count and keywords used
        """
        all_tracks = []
        track_ids_set = set()
        
        # Search for each lyric keyword
        for keyword in lyric_keywords:
            results = self.client.search_tracks(query=keyword, limit=30)
            for track in results:
                track_id = track["id"]
                if track_id not in track_ids_set:
                    all_tracks.append(track)
                    track_ids_set.add(track_id)
            
            # Stop if we have enough
            if len(all_tracks) >= limit:
                break
        
        # Limit and deduplicate
        track_ids = list(dict.fromkeys([t["id"] for t in all_tracks[:limit]]))
        
        if not track_ids:
            raise ValueError(f"No tracks found for lyric keywords: {lyric_keywords}")
        
        # Create playlist
        playlist = self.client.create_playlist(
            name=playlist_name,
            description=playlist_description,
            public=public
        )
        
        # Add tracks in batches
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            self.client.add_tracks_to_playlist(playlist["id"], batch)
        
        return {
            "playlist": playlist,
            "tracks_added": len(track_ids),
            "lyric_keywords": lyric_keywords
        }
    
    def create_from_song_list(self, song_list: List[str], playlist_name: str,
                             playlist_description: str = "", public: bool = True) -> Dict[str, Any]:
        """
        Create playlist from specific song list.
        
        Args:
            song_list: List of song names or search queries
            playlist_name: Playlist name
            playlist_description: Optional description
            public: Make playlist public
            
        Returns:
            Playlist data with found tracks and missing songs
        """
        track_ids = []
        not_found = []
        
        # Search for each song
        for song_query in song_list:
            results = self.client.search_tracks(query=song_query, limit=1)
            if results:
                track_ids.append(results[0]["id"])
            else:
                not_found.append(song_query)
        
        if not track_ids:
            raise ValueError(f"No tracks found from song list")
        
        # Create playlist
        playlist = self.client.create_playlist(
            name=playlist_name,
            description=playlist_description,
            public=public
        )
        
        # Add tracks in batches
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            self.client.add_tracks_to_playlist(playlist["id"], batch)
        
        return {
            "playlist": playlist,
            "tracks_added": len(track_ids),
            "tracks_found": len(track_ids),
            "tracks_not_found": len(not_found),
            "not_found_songs": not_found if not_found else None
        }
    
    def create_from_recommendations(self, playlist_name: str,
                                   seed_artists: List[str] = None,
                                   seed_tracks: List[str] = None,
                                   seed_genres: List[str] = None,
                                   playlist_description: str = "",
                                   public: bool = True,
                                   limit: int = 100) -> Dict[str, Any]:
        """
        Create playlist from Spotify recommendations.
        
        Args:
            playlist_name: Playlist name
            seed_artists: Artist IDs (max 5)
            seed_tracks: Track IDs (max 5)
            seed_genres: Genres (max 5)
            playlist_description: Optional description
            public: Make playlist public
            limit: Number of recommendations (max 100)
            
        Returns:
            Playlist data with track count
        """
        # Get recommendations
        recommended_tracks = self.client.get_recommendations(
            seed_artists=seed_artists,
            seed_tracks=seed_tracks,
            seed_genres=seed_genres,
            limit=min(limit, 100)
        )
        
        if not recommended_tracks:
            raise ValueError("No recommendations found for provided seeds")
        
        track_ids = [t["id"] for t in recommended_tracks]
        
        # Create playlist
        playlist = self.client.create_playlist(
            name=playlist_name,
            description=playlist_description,
            public=public
        )
        
        # Add tracks
        self.client.add_tracks_to_playlist(playlist["id"], track_ids)
        
        return {
            "playlist": playlist,
            "tracks_added": len(track_ids),
            "recommendation_seeds": {
                "artists": seed_artists or [],
                "tracks": seed_tracks or [],
                "genres": seed_genres or []
            }
        }
    
    def add_playlist_artwork(self, playlist_id: str, image_base64: str) -> None:
        """
        Add cover image to playlist (if supported by API).
        
        Note: Full image upload support requires additional endpoint.
        This is a placeholder for future enhancement.
        """
        # This would require additional implementation
        pass
    
    def get_playlist_stats(self, playlist_id: str) -> Dict[str, Any]:
        """Get statistics about a playlist."""
        playlist = self.client.get_playlist(playlist_id)
        tracks = self.client.get_playlist_tracks(playlist_id, limit=1)
        total_tracks = playlist.get("tracks", {}).get("total", 0)
        
        # Get all tracks to calculate duration
        all_tracks = []
        offset = 0
        while offset < total_tracks:
            batch = self.client.get_playlist_tracks(
                playlist_id,
                limit=50,
                offset=offset
            )
            all_tracks.extend(batch)
            offset += 50
        
        total_duration_ms = sum(
            t.get("track", {}).get("duration_ms", 0) for t in all_tracks
        )
        
        return {
            "name": playlist.get("name"),
            "total_tracks": total_tracks,
            "total_duration_minutes": total_duration_ms // 60000,
            "public": playlist.get("public"),
            "collaborative": playlist.get("collaborative"),
            "owner": playlist.get("owner", {}).get("display_name"),
            "followers": playlist.get("followers", {}).get("total", 0)
        }
