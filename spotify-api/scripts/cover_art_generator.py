"""
Spotify Cover Art Generator

Generates custom SVG-based cover art and uploads to Spotify playlists.

IMPORTANT: This tool is designed to be used with the LLM execution guide.
See: spotify-api/references/COVER_ART_LLM_GUIDE.md

The guide provides comprehensive instructions for:
- Analyzing playlist content to determine appropriate colors
- Applying color psychology based on genre, mood, and energy
- Creating contextually appropriate designs without preset themes
- Ensuring accessibility and professional quality

Color Selection Approaches:
1. Content-Driven (RECOMMENDED): Analyze playlist tracks/artists using the guide
2. Preset Themes (LEGACY): Use predefined theme/genre/artist colors below
3. Custom Colors: Specify exact RGB values

For best results, follow the LLM guide to analyze playlist content and 
determine colors using color psychology rather than relying on presets.
"""

import os
import base64
import requests
from io import BytesIO
from typing import Dict, List, Optional, Tuple
try:
    import cairosvg
    from PIL import Image
except ImportError as e:
    print("Missing required dependencies. Install with:")
    print("pip install cairosvg pillow")
    raise e


# ============================================================================
# LEGACY PRESETS (For backward compatibility)
# ============================================================================
# These preset color schemes are provided for quick usage, but the RECOMMENDED
# approach is to analyze playlist content using the LLM guide and determine
# colors based on:
# - Actual genres detected from tracks/artists
# - Energy level analysis (1-10 scale)
# - Mood extracted from content
# - Color psychology principles
#
# See: spotify-api/references/COVER_ART_LLM_GUIDE.md for the content-driven approach
# ============================================================================

# Preset theme color schemes (gradient_start, gradient_end, text_color)
THEME_COLORS: Dict[str, Tuple[str, str, str]] = {
    # Mood-based themes
    "summer": ("#FFD93D", "#FF6B9D", "#FFFFFF"),
    "chill": ("#4ECDC4", "#556FB5", "#FFFFFF"),
    "energetic": ("#FF6B35", "#F72C25", "#FFFFFF"),
    "dark": ("#8B5DFF", "#1A1A2E", "#FFFFFF"),
    "vintage": ("#D4A574", "#6B4423", "#F5F5DC"),
    "neon": ("#00FFF0", "#FF00FF", "#FFFFFF"),
    "minimal": ("#F5F5F5", "#2C2C2C", "#1A1A1A"),
    "warm": ("#FFAD60", "#FF6C40", "#FFFFFF"),
    "cool": ("#A8D8FF", "#3A6EA5", "#FFFFFF"),
    "sunset": ("#FF8C42", "#6A4C93", "#FFFFFF"),
    "ocean": ("#00B4D8", "#03045E", "#FFFFFF"),
    "forest": ("#90BE6D", "#2D6A4F", "#FFFFFF"),
    # Additional mood themes
    "romantic": ("#FF6B9D", "#C44569", "#FFFFFF"),
    "melancholic": ("#6C5B7B", "#355C7D", "#E8E8E8"),
    "euphoric": ("#FFC837", "#FF8008", "#FFFFFF"),
    "peaceful": ("#B2DFDB", "#80CBC4", "#2C3E50"),
    "intense": ("#C0392B", "#8E44AD", "#FFFFFF"),
    "dreamy": ("#A8E6CF", "#FFD3B6", "#FFFFFF"),
    "nostalgic": ("#E8B4B8", "#9C7A97", "#F5F5DC"),
    "party": ("#F857A6", "#FF5858", "#FFFFFF"),
}

# Genre-based color schemes
GENRE_COLORS: Dict[str, Tuple[str, str, str]] = {
    "rock": ("#E63946", "#1D1D1D", "#FFFFFF"),
    "pop": ("#FF006E", "#8338EC", "#FFFFFF"),
    "jazz": ("#FFB703", "#023047", "#FFFFFF"),
    "classical": ("#F8F9FA", "#6A040F", "#1A1A1A"),
    "electronic": ("#00F5FF", "#0077B6", "#FFFFFF"),
    "hip-hop": ("#FB5607", "#03071E", "#FFFFFF"),
    "country": ("#DDA15E", "#6A4C2A", "#FFFFFF"),
    "indie": ("#FF6B6B", "#4ECDC4", "#FFFFFF"),
    "metal": ("#ADB5BD", "#212529", "#FFFFFF"),
    "r&b": ("#9D4EDD", "#5A189A", "#FFFFFF"),
    "blues": ("#2E4057", "#048BA8", "#E8E8E8"),
    "folk": ("#A27E52", "#5D4E37", "#F5F5DC"),
    "reggae": ("#FFD700", "#228B22", "#1A1A1A"),
    "punk": ("#FF1744", "#000000", "#FFFFFF"),
    "soul": ("#8E24AA", "#D81B60", "#FFFFFF"),
}

# Artist/Band-specific moods (can be used for artist playlists)
ARTIST_MOODS: Dict[str, Tuple[str, str, str]] = {
    "beatles": ("#FFD700", "#FF6347", "#FFFFFF"),  # Sunny, British Invasion
    "pinkfloyd": ("#1A1A2E", "#8B5DFF", "#FFFFFF"),  # Dark, psychedelic
    "radiohead": ("#2C3E50", "#34495E", "#ECF0F1"),  # Moody, alternative
    "queen": ("#FFD700", "#8B0000", "#FFFFFF"),  # Regal, theatrical
    "nirvana": ("#95A5A6", "#34495E", "#ECF0F1"),  # Grunge, raw
    "davidbowie": ("#FF6B9D", "#4169E1", "#FFFFFF"),  # Glam, eclectic
    "ledzeppelin": ("#D4AF37", "#8B4513", "#FFFFFF"),  # Golden, classic rock
    "acdc": ("#FF0000", "#000000", "#FFFFFF"),  # Electric, hard rock
    "therollingstones": ("#C0392B", "#2C3E50", "#FFFFFF"),  # Raw, rebellious
    "fleetwoodmac": ("#E8B4B8", "#9C7A97", "#F5F5DC"),  # Warm, classic
}


class CoverArtGenerator:
    """
    Generate and upload custom cover art for Spotify playlists.
    
    Attributes:
        client_id: Spotify application client ID
        client_secret: Spotify application client secret
        access_token: Valid Spotify user access token
    """
    
    def __init__(self, client_id: str, client_secret: str, access_token: str):
        """
        Initialize cover art generator.
        
        Args:
            client_id: Spotify application client ID
            client_secret: Spotify application client secret
            access_token: Valid Spotify user access token with playlist-modify scope
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.base_url = "https://api.spotify.com/v1"
    
    def create_and_upload_cover(
        self,
        playlist_id: str,
        title: str,
        subtitle: str = "",
        theme: Optional[str] = None,
        genre: Optional[str] = None,
        artist: Optional[str] = None,
        gradient_start: Optional[str] = None,
        gradient_end: Optional[str] = None,
        text_color: Optional[str] = None
    ) -> bool:
        """
        Generate cover art and upload to Spotify playlist in one step.
        
        Args:
            playlist_id: Spotify playlist ID
            title: Main title text (large font, readable at thumbnail size)
            subtitle: Subtitle text (smaller font, optional)
            theme: Preset theme name (e.g., 'summer', 'chill', 'dark', 'romantic')
            genre: Genre-based color scheme (e.g., 'rock', 'jazz', 'pop', 'blues')
            artist: Artist/band name for artist-specific moods (e.g., 'beatles', 'pinkfloyd')
            gradient_start: Custom gradient start color (hex, e.g., '#FF6B6B')
            gradient_end: Custom gradient end color (hex)
            text_color: Custom text color (hex)
        
        Returns:
            True if successful, False otherwise
        
        Example:
            >>> generator = CoverArtGenerator(client_id, client_secret, token)
            >>> generator.create_and_upload_cover(
            ...     playlist_id="37i9dQZF1DXcBWIGoYBM5M",
            ...     title="Summer Vibes",
            ...     subtitle="Feel Good Hits",
            ...     theme="summer"
            ... )
            True
        """
        try:
            # Generate cover art PNG
            png_path = self.generate_cover_art(
                title=title,
                subtitle=subtitle,
                theme=theme,
                genre=genre,
                artist=artist,
                gradient_start=gradient_start,
                gradient_end=gradient_end,
                text_color=text_color,
                output_path=None  # Use temp file
            )
            
            # Upload to Spotify
            success = self.upload_cover_image(playlist_id, png_path)
            
            # Clean up temp file
            if os.path.exists(png_path):
                os.remove(png_path)
            
            return success
            
        except Exception as e:
            print(f"Error creating and uploading cover: {e}")
            return False
    
    def generate_cover_art(
        self,
        title: str,
        subtitle: str = "",
        theme: Optional[str] = None,
        genre: Optional[str] = None,
        artist: Optional[str] = None,
        gradient_start: Optional[str] = None,
        gradient_end: Optional[str] = None,
        text_color: Optional[str] = None,
        output_path: Optional[str] = None,
        size: int = 600
    ) -> str:
        """
        Generate cover art image (SVG → PNG).
        Typography optimized for thumbnail readability at 80% width.
        
        RECOMMENDED WORKFLOW:
        1. Use COVER_ART_LLM_GUIDE.md to analyze playlist content
        2. Determine colors from actual tracks/artists/genres
        3. Apply color psychology based on energy and mood
        4. Pass custom colors (gradient_start, gradient_end, text_color)
        
        This method supports three approaches:
        - Content-Driven (RECOMMENDED): Use guide to analyze and pass custom colors
        - Legacy Presets: Use theme/genre/artist parameters for preset colors
        - Direct Colors: Specify exact gradient_start, gradient_end, text_color
        
        Args:
            title: Main title text (will be large and readable)
            subtitle: Subtitle text (optional)
            theme: Preset theme name (mood-based)
            genre: Genre-based color scheme
            artist: Artist/band name for artist-specific moods
            gradient_start: Custom gradient start color
            gradient_end: Custom gradient end color
            text_color: Custom text color
            output_path: Output PNG file path (None = temp file)
            size: Output size in pixels (default 600x600)
        
        Returns:
            Path to generated PNG file
        
        Raises:
            ValueError: If no color scheme is specified
        """
        # Determine colors - prioritize artist mood, then genre, then theme
        if artist:
            # Normalize artist name (remove spaces, lowercase)
            artist_key = artist.lower().replace(" ", "").replace("the", "")
            if artist_key in ARTIST_MOODS:
                gradient_start, gradient_end, text_color = ARTIST_MOODS[artist_key]
            elif theme and theme in THEME_COLORS:
                gradient_start, gradient_end, text_color = THEME_COLORS[theme]
            elif genre and genre in GENRE_COLORS:
                gradient_start, gradient_end, text_color = GENRE_COLORS[genre]
            else:
                # Default to energetic theme if artist not found
                gradient_start, gradient_end, text_color = THEME_COLORS["energetic"]
        elif theme and theme in THEME_COLORS:
            gradient_start, gradient_end, text_color = THEME_COLORS[theme]
        elif genre and genre in GENRE_COLORS:
            gradient_start, gradient_end, text_color = GENRE_COLORS[genre]
        elif not (gradient_start and gradient_end and text_color):
            raise ValueError(
                "Must specify theme, genre, artist, or custom colors "
                "(gradient_start, gradient_end, text_color)"
            )
        
        # Generate SVG
        svg_content = self._create_svg(
            title=title,
            subtitle=subtitle,
            gradient_start=gradient_start,
            gradient_end=gradient_end,
            text_color=text_color,
            size=size
        )
        
        # Convert SVG to PNG
        png_data = cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            output_width=size,
            output_height=size
        )
        
        # Save to file or temp file
        if output_path is None:
            output_path = "temp_cover.png"
        
        with open(output_path, 'wb') as f:
            f.write(png_data)
        
        # Optimize image size
        self._optimize_image(output_path, max_size_kb=256)
        
        return output_path
    
    def _create_svg(
        self,
        title: str,
        subtitle: str,
        gradient_start: str,
        gradient_end: str,
        text_color: str,
        size: int = 600
    ) -> str:
        """
        Create SVG content with gradient background and text.
        Optimized for thumbnail readability with large typography at 80% width.
        Automatically wraps long titles across multiple lines.
        
        Args:
            title: Main title text
            subtitle: Subtitle text
            gradient_start: Gradient start color (hex)
            gradient_end: Gradient end color (hex)
            text_color: Text color (hex)
            size: Canvas size in pixels
        
        Returns:
            SVG content as string
        """
        center = size // 2
        text_width = size * 0.8  # 80% of cover width for text
        
        # Calculate dynamic font sizes based on text length for optimal thumbnail readability
        # Larger fonts for shorter text, scaled down for longer text
        title_length = len(title)
        if title_length <= 10:
            title_font_size = 96  # Very large for short titles
        elif title_length <= 15:
            title_font_size = 84
        elif title_length <= 20:
            title_font_size = 72
        else:
            title_font_size = 60  # Still large for longer titles
        
        subtitle_font_size = title_font_size * 0.45  # Subtitle is 45% of title size
        
        # Word wrap title if too long (more than 20 characters)
        title_lines = self._wrap_text(title, max_chars_per_line=20)
        num_title_lines = len(title_lines)
        
        # Calculate vertical positioning based on number of lines
        line_height = title_font_size * 1.1  # 110% of font size for line spacing
        total_title_height = line_height * num_title_lines
        
        # Vertical spacing to prevent overlap
        if subtitle:
            # Start title higher to make room for subtitle
            title_start_y = center - (total_title_height / 2) - (subtitle_font_size * 0.5)
            subtitle_y = title_start_y + total_title_height + (subtitle_font_size * 1.2)
        else:
            # Center the title
            title_start_y = center - (total_title_height / 2)
            subtitle_y = 0
        
        svg = f'''<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="grad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:{gradient_start};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{gradient_end};stop-opacity:1" />
    </radialGradient>
  </defs>
  
  <!-- Background gradient -->
  <rect width="{size}" height="{size}" fill="url(#grad)" />
  
  <!-- Decorative shapes (positioned to avoid text) -->
  <circle cx="{size * 0.85}" cy="{size * 0.15}" r="{size * 0.12}" 
          fill="{text_color}" opacity="0.08" />
  <circle cx="{size * 0.15}" cy="{size * 0.85}" r="{size * 0.08}" 
          fill="{text_color}" opacity="0.12" />
  
  <!-- Title text with multi-line support -->
'''
        
        # Add each line of the title
        for i, line in enumerate(title_lines):
            line_y = title_start_y + (i * line_height)
            svg += f'''  <text x="{center}" y="{line_y}" 
        font-family="Arial Black, Arial Bold, Arial, sans-serif" 
        font-size="{title_font_size}" 
        font-weight="900" 
        fill="{text_color}" 
        text-anchor="middle" 
        dominant-baseline="middle">
    {self._escape_xml(line)}
  </text>
'''
        
        # Add subtitle if provided (with proper spacing)
        if subtitle:
            svg += f'''  
  <!-- Subtitle text -->
  <text x="{center}" y="{subtitle_y}" 
        font-family="Arial, sans-serif" 
        font-size="{subtitle_font_size}" 
        font-weight="600"
        fill="{text_color}" 
        text-anchor="middle" 
        opacity="0.95">
    {self._escape_xml(subtitle)}
  </text>
'''
        
        svg += '</svg>'
        return svg
    
    def _wrap_text(self, text: str, max_chars_per_line: int = 20) -> List[str]:
        """
        Wrap text into multiple lines, trying to break at word boundaries.
        
        Args:
            text: Text to wrap
            max_chars_per_line: Maximum characters per line
        
        Returns:
            List of text lines
        """
        if len(text) <= max_chars_per_line:
            return [text]
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            # +1 for space
            if current_length + word_length + (1 if current_line else 0) <= max_chars_per_line:
                current_line.append(word)
                current_length += word_length + (1 if len(current_line) > 1 else 0)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _escape_xml(self, text: str) -> str:
        """
        Escape special XML characters.
        
        Args:
            text: Input text
        
        Returns:
            XML-safe text
        """
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))
    
    def _optimize_image(self, image_path: str, max_size_kb: int = 256) -> None:
        """
        Optimize PNG image to meet Spotify's size requirements.
        
        Args:
            image_path: Path to PNG image
            max_size_kb: Maximum file size in KB (default 256 for Spotify)
        """
        max_size_bytes = max_size_kb * 1024
        
        # Check current size
        current_size = os.path.getsize(image_path)
        if current_size <= max_size_bytes:
            return  # Already meets requirements
        
        # Load image
        img = Image.open(image_path)
        
        # Try reducing quality
        quality = 95
        while quality > 20:
            output = BytesIO()
            img.save(output, format='PNG', optimize=True, quality=quality)
            
            if output.tell() <= max_size_bytes:
                # Save optimized image
                with open(image_path, 'wb') as f:
                    f.write(output.getvalue())
                return
            
            quality -= 5
        
        # If still too large, resize
        scale = 0.9
        while os.path.getsize(image_path) > max_size_bytes and scale > 0.5:
            new_size = (int(img.width * scale), int(img.height * scale))
            resized = img.resize(new_size, Image.Resampling.LANCZOS)
            
            output = BytesIO()
            resized.save(output, format='PNG', optimize=True)
            
            if output.tell() <= max_size_bytes:
                with open(image_path, 'wb') as f:
                    f.write(output.getvalue())
                return
            
            scale -= 0.1
    
    def upload_cover_image(self, playlist_id: str, image_path: str) -> bool:
        """
        Upload cover image to Spotify playlist.
        
        Args:
            playlist_id: Spotify playlist ID
            image_path: Path to image file (JPEG or PNG)
        
        Returns:
            True if successful, False otherwise
        
        Example:
            >>> generator.upload_cover_image(
            ...     "37i9dQZF1DXcBWIGoYBM5M",
            ...     "my_cover.png"
            ... )
            True
        """
        try:
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Base64 encode
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            
            # Upload to Spotify
            url = f"{self.base_url}/playlists/{playlist_id}/images"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "image/jpeg"
            }
            
            response = requests.put(url, headers=headers, data=encoded_image)
            
            if response.status_code == 202:
                print(f"✓ Cover art uploaded successfully to playlist {playlist_id}")
                return True
            elif response.status_code == 401:
                print(f"✗ Failed to upload cover art: 401 Unauthorized")
                print(f"  Response: {response.text}")
                print("\n⚠️  MISSING SCOPE: The 'ugc-image-upload' scope is required!")
                print("\nTo fix this:")
                print("1. Go to https://developer.spotify.com/dashboard")
                print("2. Select your app and ensure it has the 'ugc-image-upload' scope")
                print("3. Re-run the OAuth flow to get a new refresh token with this scope")
                print("4. Update your .env file with the new refresh token")
                print("\nAlternatively, you can:")
                print("- Generate cover art locally (it will save as PNG)")
                print("- Manually upload it to Spotify via the web/mobile app")
                return False
            else:
                print(f"✗ Failed to upload cover art: {response.status_code}")
                print(f"  Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error uploading cover image: {e}")
            return False


# Example usage
if __name__ == "__main__":
    # Load credentials from environment
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")
    
    if not all([CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN]):
        print("Error: Missing Spotify credentials in environment variables")
        print("Set SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and SPOTIFY_ACCESS_TOKEN")
        exit(1)
    
    # Initialize generator
    generator = CoverArtGenerator(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN)
    
    # Example: Generate cover art with 'summer' theme
    print("Generating sample cover art with 'summer' theme...")
    png_path = generator.generate_cover_art(
        title="Summer Vibes",
        subtitle="Feel Good Hits",
        theme="summer",
        output_path="sample_cover.png"
    )
    print(f"✓ Cover art saved to: {png_path}")
    
    # To upload to a playlist:
    # generator.create_and_upload_cover(
    #     playlist_id="your_playlist_id",
    #     title="My Playlist",
    #     subtitle="2024",
    #     theme="summer"
    # )
