# Spotify API Authentication Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setting Up Your Spotify App](#setting-up-your-spotify-app)
3. [OAuth 2.0 Flow](#oauth-20-flow)
4. [Credential Management](#credential-management)
5. [Token Management](#token-management)
6. [Scopes Explained](#scopes-explained)

## Prerequisites

### Network Access (Claude Desktop Users)

⚠️ **IMPORTANT**: If using this skill in Claude Desktop, you must enable network access first:

**Required Settings:**
1. Open Claude Desktop → **Settings** → **Developer**
2. Enable **"Allow network egress"** (toggle to ON/blue)
3. Set **"Domain allowlist"** to either:
   - **"All domains"** (easiest - allows all internet access), OR
   - **"Specified domains"** and add `api.spotify.com` (more secure - Spotify only)

**Why?**
- The skill makes HTTP requests to `api.spotify.com`
- Without network egress, all API calls will be blocked
- This security feature must be explicitly enabled

**Verification:**
- Toggle should be blue/ON
- For "All domains": Message shows "Claude can access all domains on the internet"
- For "Specified domains": Verify `api.spotify.com` is in the domain list

## Setting Up Your Spotify App

### Step 1: Create a Spotify Developer Account

1. Go to https://developer.spotify.com/dashboard
2. Log in with your Spotify account (or create one)
3. Accept the terms and create your developer account

### Step 2: Create an Application

1. Click "Create an App"
2. Enter app name and description
3. Accept the terms of service
4. Click "Create"
5. Agree to Spotify API terms

### Step 3: Get Your Credentials

After creating your app, you'll have:
- **Client ID**: Unique identifier for your app
- **Client Secret**: Secret key for authentication (keep private!)
- **Redirect URI**: URL where Spotify redirects after user authorization

Example:
```
Client ID: 1234567890abcdef1234567890abcdef
Client Secret: fedcba0987654321fedcba0987654321
Redirect URI: http://localhost:8888/callback
```

### Step 4: Set Redirect URI

1. In your app settings, click "Edit Settings"
2. Add your redirect URI under "Redirect URIs"
3. Examples:
   - Development: `http://localhost:8888/callback`
   - Production: `https://yourapp.com/callback`

## OAuth 2.0 Flow

### Authorization Code Flow (User Authentication)

This is the recommended flow for accessing user data.

#### Step 1: Request User Authorization

Direct user to Spotify's authorization endpoint:

```
GET https://accounts.spotify.com/authorize
Parameters:
  - client_id: Your Client ID
  - response_type: "code"
  - redirect_uri: Your registered redirect URI
  - scope: Space-separated list of scopes
  - show_dialog: "true" (optional, forces re-authentication)
```

Example URL:
```
https://accounts.spotify.com/authorize?
client_id=1234567890abcdef1234567890abcdef&
response_type=code&
redirect_uri=http%3A%2F%2Flocalhost%3A8888%2Fcallback&
scope=playlist-modify-public%20playlist-modify-private&
show_dialog=true
```

#### Step 2: User Authorizes

User sees Spotify login and permission request screen. After authorizing, Spotify redirects to your redirect URI with authorization code:

```
http://localhost:8888/callback?code=AQBPa...&state=xyz
```

#### Step 3: Exchange Code for Access Token

Make a POST request to get access token:

```
POST https://accounts.spotify.com/api/token
Headers:
  Authorization: Basic {base64(client_id:client_secret)}
  Content-Type: application/x-www-form-urlencoded

Body:
  grant_type=authorization_code&
  code={authorization_code}&
  redirect_uri={redirect_uri}
```

Example using curl:
```bash
curl -H "Authorization: Basic $(echo -n 'YOUR_CLIENT_ID:YOUR_CLIENT_SECRET' | base64)" \
  -d "grant_type=authorization_code&code=AQBPa...&redirect_uri=http%3A%2F%2Flocalhost%3A8888%2Fcallback" \
  https://accounts.spotify.com/api/token
```

#### Step 4: Receive Access Token

Response includes:
```json
{
  "access_token": "NgCXRK...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "NgCXRK...",
  "scope": "playlist-modify-public playlist-modify-private"
}
```

Store the `refresh_token` for later token renewal.

### Client Credentials Flow (Backend Authentication)

For backend operations without user context:

```
POST https://accounts.spotify.com/api/token
Headers:
  Authorization: Basic {base64(client_id:client_secret)}
  Content-Type: application/x-www-form-urlencoded

Body:
  grant_type=client_credentials
```

Returns access token (no refresh token) valid for 1 hour.

## Credential Management

### Environment Variables

Store credentials as environment variables for security:

```bash
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
export SPOTIFY_REDIRECT_URI="http://localhost:8888/callback"
export SPOTIFY_ACCESS_TOKEN="your_access_token"
export SPOTIFY_REFRESH_TOKEN="your_refresh_token"
```

### Python Implementation

```python
import os
from spotify_client import SpotifyClient

# Load from environment
client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    access_token=os.getenv("SPOTIFY_ACCESS_TOKEN"),
    refresh_token=os.getenv("SPOTIFY_REFRESH_TOKEN")
)

# Use client for API calls
playlists = client.get_user_playlists()
```

### Secure Credential Storage

**Development:**
- Use `.env` file with python-dotenv
- Never commit credentials to version control
- Add `.env` to `.gitignore`

**Production:**
- Use environment variables
- Use secret management services (AWS Secrets Manager, HashiCorp Vault, etc.)
- Rotate refresh tokens periodically
- Implement rate limiting and monitoring

### Example: Initial OAuth Setup

```python
import os
import webbrowser
from spotify_client import SpotifyClient

# 1. Initialize client with credentials only
client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI")
)

# 2. Get authorization URL
auth_url = client.get_authorization_url()
print(f"Visit this URL to authorize: {auth_url}")
webbrowser.open(auth_url)

# 3. User visits URL, grants permissions, and is redirected
# They'll be redirected to http://localhost:8888/callback?code=...

# 4. Extract authorization code from redirect URL and exchange
auth_code = input("Enter the authorization code from the redirect URL: ")
token_data = client.get_access_token(auth_code)

print(f"Access Token: {token_data['access_token']}")
print(f"Refresh Token: {token_data['refresh_token']}")
print(f"Expires in: {token_data['expires_in']} seconds")

# 5. Store refresh token for future use
os.environ["SPOTIFY_REFRESH_TOKEN"] = token_data["refresh_token"]
```

## Token Management

### Token Expiration

- **Access Token**: Expires in 3600 seconds (1 hour)
- **Refresh Token**: Does not expire (unless revoked by user)

### Automatic Token Refresh

The SpotifyClient automatically refreshes expired tokens:

```python
# No manual refresh needed - client handles it automatically
playlists = client.get_user_playlists()  # Checks and refreshes if needed
```

### Manual Token Refresh

```python
# Manually refresh if needed
token_data = client.refresh_access_token()
print(f"New access token: {token_data['access_token']}")
```

### Checking Token Status

```python
import time

# Check if token needs refresh
if client.token_expires_at and time.time() >= client.token_expires_at - 60:
    print("Token expiring soon or already expired")
    client.refresh_access_token()
else:
    print("Token is valid")
```

## Scopes Explained

Scopes determine what data and actions are allowed for your app.

### Playlist Scopes

| Scope | Access |
|-------|--------|
| `playlist-read-private` | Read private playlists |
| `playlist-read-collaborative` | Read collaborative playlists |
| `playlist-modify-public` | Create/modify public playlists |
| `playlist-modify-private` | Create/modify private playlists |
| `ugc-image-upload` | **Upload custom playlist cover images** ⚠️ **Required for cover art generation!** |

### User Scopes

| Scope | Access |
|-------|--------|
| `user-read-private` | Read user private profile data |
| `user-read-email` | Read user email address |
| `user-read-private` | Read user's private profile information |

### Library Scopes

| Scope | Access |
|-------|--------|
| `user-library-read` | Read saved tracks/albums |
| `user-library-modify` | Save/unsave tracks/albums |

### Listening History

| Scope | Access |
|-------|--------|
| `user-top-read` | Read user's top tracks/artists |
| `user-read-recently-played` | Read recently played tracks |

### Playback Scopes

| Scope | Access |
|-------|--------|
| `user-read-currently-playing` | Read currently playing track |
| `user-read-playback-state` | Read playback state |
| `user-modify-playback-state` | Control playback |

### Recommended Scope Combinations

**For Playlist Management (without cover art):**
```
playlist-modify-public
playlist-modify-private
user-library-read
```

**For Playlist Management WITH Cover Art Generation:**
```
playlist-modify-public
playlist-modify-private
user-library-read
ugc-image-upload
```
⚠️ **Important**: The `ugc-image-upload` scope is **required** to upload custom cover art images to playlists!

**For Full User Experience:**
```
playlist-modify-public
playlist-modify-private
user-library-read
user-library-modify
user-read-private
user-read-email
user-top-read
user-read-currently-playing
user-modify-playback-state
user-read-playback-state
ugc-image-upload
```

### Requesting Specific Scopes

```python
# Request specific scopes
scopes = [
    "playlist-modify-public",
    "playlist-modify-private",
    "user-library-read"
]

auth_url = client.get_authorization_url(scope=scopes)
```

## Security Best Practices

1. **Never expose Client Secret** - Keep it secret like a password
2. **Use HTTPS** - Always use HTTPS for redirect URIs in production
3. **Rotate tokens** - Implement token rotation for long-running processes
4. **Validate redirects** - Verify redirect URI before processing auth code
5. **Rate limiting** - Implement rate limiting to prevent abuse
6. **Error handling** - Don't expose credential details in error messages
7. **Monitor access** - Log and monitor API usage for suspicious activity
8. **Secure storage** - Use encrypted storage for sensitive credentials

## Troubleshooting

### Invalid Client ID / Secret
- Verify credentials match your app settings
- Check for accidental whitespace
- Regenerate credentials if needed

### Invalid Redirect URI
- Exact match required (including http/https)
- URLs are case-sensitive
- Check URL encoding in requests

### Unauthorized (401)
- Access token may be expired - refresh it
- Token may have been revoked by user
- Check token scope has required permissions

### Forbidden (403)
- Insufficient scopes requested
- User hasn't authorized the action
- May require additional permissions

### Rate Limited (429)
- Check `Retry-After` header
- Implement exponential backoff
- Batch requests when possible
