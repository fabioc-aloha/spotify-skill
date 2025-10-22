# Spotify API Skill - Advanced Usage

## Overview

This document covers advanced features for robust application development, including error handling, fallback data, validation, and data export.

## Features for Application Development

### 1. Credential Validation

Validate credentials before making API calls:

```python
from spotify_client import validate_credentials, get_validation_errors

# Check credential status
validation = validate_credentials()

if not validation['all_valid']:
    errors = get_validation_errors()
    for error in errors:
        print(error)
    # Handle missing credentials
```

**Returns:**
```python
{
    'client_id': True/False,
    'client_secret': True/False,
    'refresh_token': True/False,
    'redirect_uri': True/False,
    'all_valid': True/False  # All required credentials present
}
```

### 2. SpotifyAPIWrapper - Graceful Error Handling

The `SpotifyAPIWrapper` provides robust error handling with optional fallback data:

```python
from spotify_client import SpotifyAPIWrapper

# Create wrapper with fallback enabled (default)
wrapper = SpotifyAPIWrapper(use_fallback=True)

# Check if API is available
if wrapper.is_available():
    print("API connected!")
else:
    print(f"Using fallback data: {wrapper.get_error()}")

# These calls return empty lists/mock data if API fails
user = wrapper.get_user_profile()
playlists = wrapper.get_user_playlists(limit=20)
tracks = wrapper.search_tracks("Beatles", limit=10)
```

**Available Methods:**
- `get_user_profile()` - Returns user data or mock profile
- `get_user_playlists(limit)` - Returns playlists or empty list
- `search_tracks(query, limit)` - Returns tracks or empty list
- `create_playlist(name, description, public)` - Returns playlist or None
- `is_available()` - Check if API is initialized
- `get_error()` - Get initialization error if any

**Use Cases:**
- **React/Web Apps**: Always have data to render, even without API access
- **Development**: Test UI without valid credentials
- **Production**: Graceful degradation when API is unavailable

### 3. Data Export for Static Apps

Export Spotify data as JSON files for apps that don't need real-time API calls:

```bash
python spotify-api/scripts/export_data.py
```

**Exports:**
- `user_profile.json` - User profile data
- `playlists.json` - All user playlists
- `top_artists_medium_term.json` - Top artists
- `top_tracks_medium_term.json` - Top tracks

**Use in React:**
```javascript
import userData from './exported_data/user_profile.json';
import playlists from './exported_data/playlists.json';

function MyComponent() {
  return (
    <div>
      <h1>Welcome, {userData.display_name}!</h1>
      <PlaylistList playlists={playlists} />
    </div>
  );
}
```

### 4. Network Detection

Automatic detection of network restrictions with helpful error messages:

```python
from spotify_client import check_network_access, NetworkAccessError

try:
    check_network_access()
    print("Network OK")
except NetworkAccessError as e:
    print(e)  # Displays setup instructions
```

**When network is blocked, users see:**
```
❌ NETWORK ACCESS BLOCKED

The Spotify API skill cannot access api.spotify.com.

🔧 FIX: Enable network egress in Claude Desktop:
   1. Open Claude Desktop → Settings → Developer
   2. Toggle 'Allow network egress' to ON (blue)
   3. Set 'Domain allowlist' to either:
      • 'All domains' (easiest), OR
      • 'Specified domains' and add 'api.spotify.com'

📖 See GETTING_STARTED.md for detailed instructions.
```

## Complete Example: React App Integration

```python
"""
Prepare data for a React application with fallback support.
"""
from spotify_client import SpotifyAPIWrapper
import json

def prepare_react_data():
    # Use wrapper with fallback
    wrapper = SpotifyAPIWrapper(use_fallback=True)

    # Build data structure
    app_data = {
        'user': wrapper.get_user_profile(),
        'playlists': wrapper.get_user_playlists(limit=20),
        'recentTracks': wrapper.search_tracks("recent", limit=10),
        'isLiveData': wrapper.is_available(),
        'dataSource': 'spotify-api' if wrapper.is_available() else 'fallback'
    }

    # Save as JSON for React app
    with open('public/spotify-data.json', 'w') as f:
        json.dump(app_data, f, indent=2)

    print(f"✅ Data prepared ({app_data['dataSource']})")
    return app_data

if __name__ == '__main__':
    prepare_react_data()
```

**In your React app:**
```javascript
import React, { useEffect, useState } from 'react';
import spotifyData from './spotify-data.json';

function SpotifyDashboard() {
  const [data, setData] = useState(spotifyData);

  useEffect(() => {
    if (data.isLiveData) {
      console.log('Using live Spotify data');
    } else {
      console.warn('Using fallback data:', data.dataSource);
    }
  }, [data]);

  return (
    <div>
      <h1>Welcome, {data.user.display_name}!</h1>
      {!data.isLiveData && (
        <div className="warning">
          Using sample data. Configure Spotify API for live data.
        </div>
      )}
      <PlaylistGrid playlists={data.playlists} />
    </div>
  );
}
```

## Error Handling Best Practices

### 1. Always Validate First

```python
from spotify_client import validate_credentials, get_validation_errors

validation = validate_credentials()
if not validation['all_valid']:
    errors = get_validation_errors()
    # Show errors to user
    return
```

### 2. Use Wrapper for User-Facing Apps

```python
# ✅ Good: Graceful degradation
wrapper = SpotifyAPIWrapper(use_fallback=True)
playlists = wrapper.get_user_playlists()  # Returns [] on error

# ❌ Avoid: Unhandled errors in production
client = create_client_from_env()
playlists = client.get_user_playlists()  # May raise exception
```

### 3. Check Network Before Critical Operations

```python
from spotify_client import check_network_access, NetworkAccessError

try:
    check_network_access()
    # Proceed with API calls
except NetworkAccessError as e:
    print(e)
    # Guide user to enable network access
```

### 4. Export Data for Static Deployments

```bash
# Generate JSON files once
python spotify-api/scripts/export_data.py

# Deploy static site with pre-generated data
# No runtime API calls needed
```

## Testing Your Integration

### Test with Valid Credentials

```bash
python spotify-api/scripts/test_credentials.py
```

### Test Wrapper Functionality

```bash
python example_wrapper_usage.py
```

### Test Data Export

```bash
python spotify-api/scripts/export_data.py
ls exported_data/
```

## Troubleshooting

### "Missing credentials" Error

```python
# Check what's missing
from spotify_client import get_validation_errors

errors = get_validation_errors()
for error in errors:
    print(error)
```

**Fix:**
1. Copy `spotify-api/.env.example` to `spotify-api/.env`
2. Add your credentials from Spotify Developer Dashboard
3. Run `python get_refresh_token.py` to get refresh token

### "Network access blocked" Error

**Fix:**
1. Open Claude Desktop → Settings → Developer
2. Enable "Allow network egress"
3. Add `api.spotify.com` to domain allowlist (or allow all domains)
4. Restart Claude Desktop

### Wrapper Returns Empty Data

```python
wrapper = SpotifyAPIWrapper(use_fallback=True)

if not wrapper.is_available():
    error = wrapper.get_error()
    print(f"API unavailable: {error}")
    # Using fallback data
```

**Common causes:**
- Missing credentials
- Network access blocked
- Invalid refresh token (re-run `get_refresh_token.py`)

## See Also

- **[GETTING_STARTED.md](../GETTING_STARTED.md)** - Initial setup
- **[USER_GUIDE.md](../USER_GUIDE.md)** - Complete API reference
- **[example_wrapper_usage.py](../example_wrapper_usage.py)** - Wrapper examples
- **[export_data.py](scripts/export_data.py)** - Data export script
