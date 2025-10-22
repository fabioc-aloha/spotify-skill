# Cover Art Upload Troubleshooting

## 401 Unauthorized Error

If you get a **401 Unauthorized** error when trying to upload cover art to Spotify, it means your access token doesn't have the required `ugc-image-upload` scope.

### The Issue

Spotify requires the `ugc-image-upload` scope to upload custom images to playlists. This is a security measure to ensure only authorized apps can modify playlist cover art.

**Error message:**
```
✗ Failed to upload cover art: 401 Unauthorized
⚠️  MISSING SCOPE: The 'ugc-image-upload' scope is required!
```

## Solutions

### Option 1: Re-authorize with Correct Scope (Recommended)

This enables automatic cover art upload directly from the skill.

**Steps:**

1. **Open your Spotify Developer Dashboard**
   - Go to https://developer.spotify.com/dashboard
   - Log in with your Spotify account
   - Select your app

2. **Verify your app settings**
   - Make sure your redirect URI is set (e.g., `http://127.0.0.1:8888/callback`)
   - Note: The scope is requested during authorization, not configured in the dashboard

3. **Re-run the OAuth flow to get a new refresh token**
   ```bash
   python get_refresh_token.py
   ```

   This script now includes `ugc-image-upload` in the requested scopes:
   - Playlist management (create, modify, read)
   - User library access
   - Playback control
   - User profile and top items
   - **🎨 ugc-image-upload** (for cover art upload!)

4. **Update your `.env` file**
   - Copy the new refresh token from the output
   - Update `SPOTIFY_REFRESH_TOKEN` in your `.env` file:
   ```
   SPOTIFY_REFRESH_TOKEN=your_new_refresh_token_here
   ```

5. **Test the upload**
   ```bash
   python spotify-api/test_cover_art.py
   ```

### Option 2: Generate Locally, Upload Manually

If you prefer not to re-authorize or want to review cover art before uploading:

**Steps:**

1. **Generate cover art locally** (doesn't require upload scope):
   ```python
   from cover_art_generator import CoverArtGenerator

   generator = CoverArtGenerator(client_id, client_secret, access_token)

   # Generate without uploading
   png_path = generator.generate_cover_art(
       title="My Playlist",
       subtitle="2024",
       theme="summer",
       output_path="my_cover.png"
   )

   print(f"Cover saved to: {png_path}")
   ```

2. **Upload manually via Spotify**:
   - Open Spotify (web or desktop app)
   - Go to your playlist
   - Click the three dots (...) → "Edit details"
   - Click "Change image"
   - Select the generated PNG file
   - Click "Save"

## Understanding Spotify Scopes

### Required Scopes for Full Functionality

```python
SCOPES = [
    # Playback control
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',

    # Playlist management
    'playlist-read-private',
    'playlist-read-collaborative',
    'playlist-modify-public',
    'playlist-modify-private',

    # Library access
    'user-library-read',
    'user-library-modify',

    # User data
    'user-top-read',
    'user-read-private',
    'user-read-email',

    # Cover art upload (NEW!)
    'ugc-image-upload',  # Required for cover art upload
]
```

### Checking Your Current Scopes

Unfortunately, Spotify doesn't provide an API endpoint to check which scopes a token has. If you're unsure:

1. Check when you last authorized (before or after `ugc-image-upload` was added to `get_refresh_token.py`)
2. Try to upload cover art - if it fails with 401, you need to re-authorize
3. Re-run `get_refresh_token.py` to be safe

## Verification

After re-authorizing with the correct scope, verify it works:

```bash
# Test cover art generation and upload
cd spotify-api
python test_cover_art.py

# Or test in your code
python -c "
from scripts.cover_art_generator import CoverArtGenerator
import os

gen = CoverArtGenerator(
    os.getenv('SPOTIFY_CLIENT_ID'),
    os.getenv('SPOTIFY_CLIENT_SECRET'),
    os.getenv('SPOTIFY_ACCESS_TOKEN')
)

# Generate test image
gen.generate_cover_art(
    title='Test',
    subtitle='Scope Check',
    theme='energetic',
    output_path='test.png'
)
print('✓ Image generated successfully!')

# Try to upload (requires playlist ID)
# gen.upload_cover_image('YOUR_PLAYLIST_ID', 'test.png')
"
```

## Common Issues

### "I re-authorized but still get 401"

1. Make sure you copied the **new** refresh token to `.env`
2. Restart any running Python processes
3. Check that `get_refresh_token.py` includes `ugc-image-upload` in the SCOPES list
4. Delete any cached tokens and re-authorize

### "The authorization page doesn't show ugc-image-upload"

The authorization page shows human-readable descriptions, not the exact scope names. Look for language like:
- "Upload images"
- "Modify playlist images"
- "Change playlist cover art"

### "I don't want to give this permission"

That's fine! You can still use all the cover art **generation** features. Just use Option 2 (generate locally, upload manually) instead of automatic upload.

## Feature Availability

| Feature | Requires ugc-image-upload? |
|---------|---------------------------|
| Generate cover art SVG | ❌ No |
| Convert SVG to PNG | ❌ No |
| Save PNG locally | ❌ No |
| Upload to Spotify API | ✅ **Yes** |

## Need Help?

If you're still having issues:

1. Check the Spotify Web API documentation: https://developer.spotify.com/documentation/web-api
2. Verify your app settings in the dashboard
3. Make sure your redirect URI exactly matches what's in your code
4. Check for any typos in your `.env` file
5. Try with a brand new Spotify app (fresh client ID/secret)

## Summary

The cover art generation skill can create images locally without any special permissions. However, to automatically upload them to Spotify via the API, you need the `ugc-image-upload` scope. Re-run `get_refresh_token.py` to get a token with this scope, or generate cover art locally and upload it manually through Spotify's interface.
