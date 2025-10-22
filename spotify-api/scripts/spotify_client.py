"""
Spotify Web API Client Wrapper

Provides authenticated access to Spotify Web API for playlist management,
search, playback control, and user data retrieval.
"""

import os
import json
import time
import base64
import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode
from pathlib import Path
import socket

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Look for .env file in the parent directory (spotify-api folder)
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    # dotenv not available, will use system environment variables
    pass


class NetworkAccessError(Exception):
    """Raised when network access to Spotify API is blocked."""
    pass


def check_network_access():
    """
    Check if network access to Spotify API is available.
    
    Raises:
        NetworkAccessError: If connection to api.spotify.com is blocked
    """
    try:
        # Try to resolve DNS for api.spotify.com
        socket.gethostbyname('api.spotify.com')
    except socket.gaierror as e:
        raise NetworkAccessError(
            "\n❌ NETWORK ACCESS BLOCKED\n\n"
            "The Spotify API skill cannot access api.spotify.com.\n\n"
            "🔧 FIX: Enable network egress in Claude Desktop:\n"
            "   1. Open Claude Desktop → Settings → Developer\n"
            "   2. Toggle 'Allow network egress' to ON (blue)\n"
            "   3. Set 'Domain allowlist' to either:\n"
            "      • 'All domains' (easiest), OR\n"
            "      • 'Specified domains' and add 'api.spotify.com'\n\n"
            "📖 See GETTING_STARTED.md for detailed instructions.\n"
        ) from e


class SpotifyClient:
    """Authenticated Spotify Web API client."""
    
    BASE_URL = "https://api.spotify.com/v1"
    AUTH_URL = "https://accounts.spotify.com/api/token"
    AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str = None,
                 access_token: str = None, refresh_token: str = None):
        """
        Initialize Spotify client.
        
        Args:
            client_id: Spotify app client ID
            client_secret: Spotify app client secret
            redirect_uri: OAuth redirect URI
            access_token: Existing access token (optional)
            refresh_token: Refresh token for token renewal (optional)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires_at = None
        
    def get_authorization_url(self, scope: List[str] = None) -> str:
        """
        Generate OAuth authorization URL.
        
        Args:
            scope: List of Spotify API scopes
            
        Returns:
            Authorization URL for user to visit
        """
        if not scope:
            scope = [
                "playlist-modify-public",
                "playlist-modify-private",
                "user-library-read",
                "user-library-modify",
                "user-read-private",
                "user-read-email",
                "user-top-read",
                "user-read-currently-playing",
                "user-modify-playback-state",
                "user-read-playback-state"
            ]
        
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(scope),
            "show_dialog": "true"
        }
        
        return f"{self.AUTHORIZE_URL}?{urlencode(params)}"
    
    def get_access_token(self, auth_code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            auth_code: Authorization code from OAuth callback
            
        Returns:
            Token response with access_token, refresh_token, expires_in
        """
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = base64.b64encode(auth_str.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_bytes}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self.redirect_uri
        }
        
        response = requests.post(self.AUTH_URL, headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data["access_token"]
        self.refresh_token = token_data.get("refresh_token")
        self.token_expires_at = time.time() + token_data.get("expires_in", 3600)
        
        return token_data
    
    def refresh_access_token(self, refresh_token: str = None) -> Dict[str, Any]:
        """
        Refresh expired access token using refresh token.
        
        Args:
            refresh_token: Refresh token (uses stored if not provided)
            
        Returns:
            New token response
        """
        token = refresh_token or self.refresh_token
        if not token:
            raise ValueError("No refresh token available")
        
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = base64.b64encode(auth_str.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_bytes}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": token
        }
        
        response = requests.post(self.AUTH_URL, headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data["access_token"]
        if "refresh_token" in token_data:
            self.refresh_token = token_data["refresh_token"]
        self.token_expires_at = time.time() + token_data.get("expires_in", 3600)
        
        return token_data
    
    def _check_token_expiry(self):
        """Refresh token if expired."""
        if self.token_expires_at and time.time() >= self.token_expires_at - 60:
            self.refresh_access_token()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authorization headers."""
        self._check_token_expiry()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, 
                     params: Dict = None, **kwargs) -> Dict[str, Any]:
        """
        Make API request with error handling.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            data: Request body data
            params: Query parameters
            
        Returns:
            Response JSON
        """
        url = f"{self.BASE_URL}/{endpoint}"
        headers = self._get_headers()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                **kwargs
            )
        except requests.exceptions.ConnectionError as e:
            # Check if it's a network access issue
            check_network_access()
            # If check passes, it's some other connection error
            raise
        
        if response.status_code == 204:
            return {}
        
        response.raise_for_status()
        return response.json()
    
    # Playlist Operations
    
    def get_user_playlists(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get user's playlists."""
        data = self._make_request(
            "GET", "me/playlists",
            params={"limit": limit, "offset": offset}
        )
        return data.get("items", [])
    
    def create_playlist(self, name: str, description: str = "", 
                       public: bool = True) -> Dict[str, Any]:
        """Create new playlist for current user."""
        user = self.get_current_user()
        user_id = user["id"]
        
        return self._make_request(
            "POST", f"users/{user_id}/playlists",
            data={
                "name": name,
                "description": description,
                "public": public
            }
        )
    
    def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """Get playlist details."""
        return self._make_request("GET", f"playlists/{playlist_id}")
    
    def update_playlist(self, playlist_id: str, name: str = None, 
                       description: str = None, public: bool = None) -> Dict:
        """Update playlist details."""
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if public is not None:
            data["public"] = public
        
        return self._make_request("PUT", f"playlists/{playlist_id}", data=data)
    
    def delete_playlist(self, playlist_id: str) -> None:
        """Delete (unfollow) playlist."""
        self._make_request("DELETE", f"playlists/{playlist_id}")
    
    def get_playlist_tracks(self, playlist_id: str, limit: int = 50, 
                           offset: int = 0) -> List[Dict]:
        """Get tracks from a playlist."""
        data = self._make_request(
            "GET", f"playlists/{playlist_id}/tracks",
            params={"limit": limit, "offset": offset}
        )
        return data.get("items", [])
    
    def add_tracks_to_playlist(self, playlist_id: str, track_ids: List[str], 
                              position: int = None) -> Dict[str, Any]:
        """Add tracks to playlist."""
        # Spotify has a limit of 100 tracks per request
        if len(track_ids) > 100:
            raise ValueError("Maximum 100 tracks per request")
        
        uris = [f"spotify:track:{track_id}" for track_id in track_ids]
        
        data = {"uris": uris}
        if position is not None:
            data["position"] = position
        
        return self._make_request(
            "POST", f"playlists/{playlist_id}/tracks",
            data=data
        )
    
    def remove_tracks_from_playlist(self, playlist_id: str, 
                                   track_ids: List[str]) -> Dict[str, Any]:
        """Remove tracks from playlist."""
        uris = [f"spotify:track:{track_id}" for track_id in track_ids]
        
        return self._make_request(
            "DELETE", f"playlists/{playlist_id}/tracks",
            data={"uris": uris}
        )
    
    # Search Operations
    
    def search_tracks(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for tracks."""
        data = self._make_request(
            "GET", "search",
            params={"q": query, "type": "track", "limit": limit}
        )
        return data.get("tracks", {}).get("items", [])
    
    def search_artists(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for artists."""
        data = self._make_request(
            "GET", "search",
            params={"q": query, "type": "artist", "limit": limit}
        )
        return data.get("artists", {}).get("items", [])
    
    def search_albums(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for albums."""
        data = self._make_request(
            "GET", "search",
            params={"q": query, "type": "album", "limit": limit}
        )
        return data.get("albums", {}).get("items", [])
    
    def search_playlists(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for playlists."""
        data = self._make_request(
            "GET", "search",
            params={"q": query, "type": "playlist", "limit": limit}
        )
        return data.get("playlists", {}).get("items", [])
    
    def search(self, query: str, types: List[str] = None, 
               limit: int = 20) -> Dict[str, Any]:
        """Search across multiple types."""
        if not types:
            types = ["track", "artist", "album", "playlist"]
        
        return self._make_request(
            "GET", "search",
            params={"q": query, "type": ",".join(types), "limit": limit}
        )
    
    # Artist Operations
    
    def get_artist(self, artist_id: str) -> Dict[str, Any]:
        """Get artist details."""
        return self._make_request("GET", f"artists/{artist_id}")
    
    def get_artist_top_tracks(self, artist_id: str, market: str = "US") -> List[Dict]:
        """
        Get artist's top tracks (returns up to 10 tracks).
        
        Note: Spotify API returns up to 10 top tracks per artist.
        The limit parameter is not supported by this endpoint.
        """
        data = self._make_request(
            "GET", f"artists/{artist_id}/top-tracks",
            params={"market": market}
        )
        return data.get("tracks", [])
    
    def get_related_artists(self, artist_id: str, limit: int = 50) -> List[Dict]:
        """Get related artists."""
        data = self._make_request(
            "GET", f"artists/{artist_id}/related-artists"
        )
        return data.get("artists", [])[:limit]
    
    def get_artist_albums(self, artist_id: str, limit: int = 50, 
                         offset: int = 0) -> List[Dict]:
        """Get artist's albums."""
        data = self._make_request(
            "GET", f"artists/{artist_id}/albums",
            params={"limit": limit, "offset": offset}
        )
        return data.get("items", [])
    
    # User Operations
    
    def get_current_user(self) -> Dict[str, Any]:
        """Get current user profile."""
        return self._make_request("GET", "me")
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user profile by ID."""
        return self._make_request("GET", f"users/{user_id}")
    
    def get_top_items(self, item_type: str = "tracks", limit: int = 20,
                     offset: int = 0, time_range: str = "medium_term") -> List[Dict]:
        """
        Get user's top tracks or artists.
        
        Args:
            item_type: "tracks" or "artists"
            limit: Number of items (max 50)
            offset: Pagination offset
            time_range: "long_term", "medium_term", or "short_term"
        """
        endpoint = f"me/top/{item_type}"
        data = self._make_request(
            "GET", endpoint,
            params={"limit": min(limit, 50), "offset": offset, 
                   "time_range": time_range}
        )
        return data.get("items", [])
    
    # Library Operations
    
    def get_saved_tracks(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get user's saved tracks."""
        data = self._make_request(
            "GET", "me/tracks",
            params={"limit": limit, "offset": offset}
        )
        return data.get("items", [])
    
    def save_tracks(self, track_ids: List[str]) -> None:
        """Save tracks to library."""
        self._make_request(
            "PUT", "me/tracks",
            params={"ids": ",".join(track_ids)}
        )
    
    def remove_saved_tracks(self, track_ids: List[str]) -> None:
        """Remove tracks from library."""
        self._make_request(
            "DELETE", "me/tracks",
            params={"ids": ",".join(track_ids)}
        )
    
    def check_saved_tracks(self, track_ids: List[str]) -> List[bool]:
        """Check if tracks are in user's library."""
        data = self._make_request(
            "GET", "me/tracks/contains",
            params={"ids": ",".join(track_ids)}
        )
        return data if isinstance(data, list) else []
    
    # Recommendations
    
    def get_recommendations(self, seed_artists: List[str] = None,
                           seed_tracks: List[str] = None,
                           seed_genres: List[str] = None,
                           limit: int = 20, **kwargs) -> List[Dict]:
        """
        Get track recommendations based on seeds.
        
        Args:
            seed_artists: Artist IDs (max 5)
            seed_tracks: Track IDs (max 5)
            seed_genres: Genres (max 5)
            limit: Number of recommendations
            **kwargs: Additional audio feature parameters
        """
        params = {"limit": limit}
        
        seeds = []
        if seed_artists:
            params["seed_artists"] = ",".join(seed_artists[:5])
            seeds.extend(seed_artists[:5])
        if seed_tracks:
            params["seed_tracks"] = ",".join(seed_tracks[:5])
            seeds.extend(seed_tracks[:5])
        if seed_genres:
            params["seed_genres"] = ",".join(seed_genres[:5])
            seeds.extend(seed_genres[:5])
        
        if len(seeds) > 5:
            raise ValueError("Maximum 5 seeds total (artists + tracks + genres)")
        
        params.update(kwargs)
        
        data = self._make_request("GET", "recommendations", params=params)
        return data.get("tracks", [])
    
    def get_available_genres(self) -> List[str]:
        """Get list of available seed genres."""
        data = self._make_request("GET", "recommendations/available-genre-seeds")
        return data.get("genres", [])
    
    # Playback Operations
    
    def get_currently_playing(self) -> Dict[str, Any]:
        """Get currently playing track."""
        return self._make_request("GET", "me/player/currently-playing") or {}
    
    def get_available_devices(self) -> List[Dict]:
        """Get available playback devices."""
        data = self._make_request("GET", "me/player/devices")
        return data.get("devices", [])
    
    def start_playback(self, device_id: str = None, context_uri: str = None,
                      track_uris: List[str] = None, offset: int = 0) -> None:
        """Start playback on device."""
        params = {}
        if device_id:
            params["device_id"] = device_id
        
        data = {}
        if context_uri:
            data["context_uri"] = context_uri
        if track_uris:
            data["uris"] = track_uris
        if offset:
            data["offset"] = {"position": offset}
        
        self._make_request(
            "PUT", "me/player/play",
            data=data if data else None,
            params=params if params else None
        )
    
    def pause_playback(self, device_id: str = None) -> None:
        """Pause playback."""
        params = {"device_id": device_id} if device_id else None
        self._make_request("PUT", "me/player/pause", params=params)
    
    def next_track(self, device_id: str = None) -> None:
        """Skip to next track."""
        params = {"device_id": device_id} if device_id else None
        self._make_request("POST", "me/player/next", params=params)
    
    def previous_track(self, device_id: str = None) -> None:
        """Skip to previous track."""
        params = {"device_id": device_id} if device_id else None
        self._make_request("POST", "me/player/previous", params=params)
    
    def seek_to_position(self, position_ms: int, device_id: str = None) -> None:
        """Seek to position in track (milliseconds)."""
        params = {"position_ms": position_ms}
        if device_id:
            params["device_id"] = device_id
        
        self._make_request("PUT", "me/player/seek", params=params)
    
    def set_repeat_mode(self, state: str, device_id: str = None) -> None:
        """Set repeat mode (off, context, track)."""
        params = {"state": state}
        if device_id:
            params["device_id"] = device_id
        
        self._make_request("PUT", "me/player/repeat", params=params)
    
    def set_shuffle(self, state: bool, device_id: str = None) -> None:
        """Enable/disable shuffle."""
        params = {"state": str(state).lower()}
        if device_id:
            params["device_id"] = device_id
        
        self._make_request("PUT", "me/player/shuffle", params=params)
    
    def set_volume(self, volume_percent: int, device_id: str = None) -> None:
        """Set playback volume (0-100)."""
        if not 0 <= volume_percent <= 100:
            raise ValueError("Volume must be between 0 and 100")
        
        params = {"volume_percent": volume_percent}
        if device_id:
            params["device_id"] = device_id
        
        self._make_request("PUT", "me/player/volume", params=params)
    
    # Track Operations
    
    def get_track(self, track_id: str) -> Dict[str, Any]:
        """Get track details."""
        return self._make_request("GET", f"tracks/{track_id}")
    
    def get_tracks(self, track_ids: List[str]) -> List[Dict]:
        """Get multiple tracks (max 50)."""
        data = self._make_request(
            "GET", "tracks",
            params={"ids": ",".join(track_ids[:50])}
        )
        return data.get("tracks", [])
    
    def get_track_audio_features(self, track_id: str) -> Dict[str, Any]:
        """Get audio features for a track."""
        return self._make_request("GET", f"audio-features/{track_id}")
    
    # Album Operations
    
    def get_album(self, album_id: str) -> Dict[str, Any]:
        """Get album details."""
        return self._make_request("GET", f"albums/{album_id}")
    
    def get_album_tracks(self, album_id: str, limit: int = 50,
                        offset: int = 0) -> List[Dict]:
        """Get tracks from album."""
        data = self._make_request(
            "GET", f"albums/{album_id}/tracks",
            params={"limit": limit, "offset": offset}
        )
        return data.get("items", [])


# Helper function to create client from environment variables
def create_client_from_env() -> SpotifyClient:
    """
    Create SpotifyClient from environment variables.
    
    Loads credentials from .env file (if available) or system environment.
    Required environment variables:
    - SPOTIFY_CLIENT_ID
    - SPOTIFY_CLIENT_SECRET
    
    Optional environment variables:
    - SPOTIFY_REDIRECT_URI (default: http://localhost:8888/callback)
    - SPOTIFY_ACCESS_TOKEN
    - SPOTIFY_REFRESH_TOKEN
    
    Returns:
        Configured SpotifyClient instance
        
    Raises:
        ValueError: If required credentials are missing
    """
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
    access_token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')
    
    if not client_id or not client_secret:
        raise ValueError(
            "Missing required Spotify credentials. "
            "Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables."
        )
    
    return SpotifyClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        access_token=access_token,
        refresh_token=refresh_token
    )


def validate_credentials() -> Dict[str, bool]:
    """
    Validate that all required Spotify credentials are available.
    
    Returns:
        Dictionary with validation results for each credential
    """
    return {
        'client_id': bool(os.getenv('SPOTIFY_CLIENT_ID')),
        'client_secret': bool(os.getenv('SPOTIFY_CLIENT_SECRET')),
        'refresh_token': bool(os.getenv('SPOTIFY_REFRESH_TOKEN')),
        'redirect_uri': bool(os.getenv('SPOTIFY_REDIRECT_URI')),
        'all_valid': all([
            os.getenv('SPOTIFY_CLIENT_ID'),
            os.getenv('SPOTIFY_CLIENT_SECRET'),
            os.getenv('SPOTIFY_REFRESH_TOKEN')
        ])
    }


def get_validation_errors() -> List[str]:
    """
    Get list of missing credential errors.
    
    Returns:
        List of error messages for missing credentials
    """
    errors = []
    
    if not os.getenv('SPOTIFY_CLIENT_ID'):
        errors.append("❌ SPOTIFY_CLIENT_ID is not set")
    
    if not os.getenv('SPOTIFY_CLIENT_SECRET'):
        errors.append("❌ SPOTIFY_CLIENT_SECRET is not set")
    
    if not os.getenv('SPOTIFY_REFRESH_TOKEN'):
        errors.append("❌ SPOTIFY_REFRESH_TOKEN is not set (run get_refresh_token.py)")
    
    if errors:
        errors.append("\n💡 TIP: Copy spotify-api/.env.example to spotify-api/.env and add your credentials")
    
    return errors


class SpotifyAPIWrapper:
    """
    High-level wrapper for Spotify API with error handling and fallback support.
    
    Use this for applications that need graceful degradation when API is unavailable.
    """
    
    def __init__(self, client: SpotifyClient = None, use_fallback: bool = True):
        """
        Initialize wrapper.
        
        Args:
            client: SpotifyClient instance (auto-created if None)
            use_fallback: Return mock data on errors if True
        """
        self.use_fallback = use_fallback
        self.client = client
        self._initialized = False
        self._init_error = None
        
        # Try to initialize client
        if not self.client:
            try:
                self.client = create_client_from_env()
                if self.client.refresh_token:
                    self.client.refresh_access_token()
                self._initialized = True
            except Exception as e:
                self._init_error = str(e)
                if not use_fallback:
                    raise
    
    def _handle_error(self, error: Exception, fallback_data: Any = None) -> Any:
        """Handle API errors with optional fallback."""
        if self.use_fallback and fallback_data is not None:
            return fallback_data
        raise error
    
    def get_user_playlists(self, limit: int = 20) -> List[Dict]:
        """
        Get user's playlists with error handling.
        
        Returns:
            List of playlist dictionaries, or empty list on error (if use_fallback=True)
        """
        if not self._initialized:
            return self._handle_error(
                Exception(self._init_error or "Client not initialized"),
                fallback_data=[]
            )
        
        try:
            return self.client.get_user_playlists(limit=limit)
        except Exception as e:
            return self._handle_error(e, fallback_data=[])
    
    def search_tracks(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for tracks with error handling.
        
        Returns:
            List of track dictionaries, or empty list on error (if use_fallback=True)
        """
        if not self._initialized:
            return self._handle_error(
                Exception(self._init_error or "Client not initialized"),
                fallback_data=[]
            )
        
        try:
            results = self.client.search(query, types=["track"], limit=limit)
            return results.get("tracks", {}).get("items", [])
        except Exception as e:
            return self._handle_error(e, fallback_data=[])
    
    def get_user_profile(self) -> Dict:
        """
        Get user profile with error handling.
        
        Returns:
            User profile dictionary, or mock data on error (if use_fallback=True)
        """
        if not self._initialized:
            return self._handle_error(
                Exception(self._init_error or "Client not initialized"),
                fallback_data={
                    'display_name': 'Unknown User',
                    'id': 'unknown',
                    'email': 'unknown@example.com'
                }
            )
        
        try:
            return self.client.get_current_user()
        except Exception as e:
            return self._handle_error(e, fallback_data={
                'display_name': 'Unknown User',
                'id': 'unknown',
                'email': 'unknown@example.com'
            })
    
    def create_playlist(self, name: str, description: str = "", public: bool = True) -> Optional[Dict]:
        """
        Create playlist with error handling.
        
        Returns:
            Playlist dictionary, or None on error (if use_fallback=True)
        """
        if not self._initialized:
            return self._handle_error(
                Exception(self._init_error or "Client not initialized"),
                fallback_data=None
            )
        
        try:
            user = self.client.get_current_user()
            return self.client.create_playlist(
                user_id=user['id'],
                name=name,
                description=description,
                public=public
            )
        except Exception as e:
            return self._handle_error(e, fallback_data=None)
    
    def is_available(self) -> bool:
        """Check if API is available and initialized."""
        return self._initialized
    
    def get_error(self) -> Optional[str]:
        """Get initialization error if any."""
        return self._init_error
