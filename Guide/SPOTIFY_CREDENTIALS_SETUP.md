# How to Add Spotify Credentials - Complete Setup Guide

## Overview

Spotify credentials are needed to authenticate with the Spotify API. You need to store them securely and pass them to the SpotifyClient when initializing.

---

## Step 1: Get Your Spotify Credentials

### Create a Spotify Developer App

1. **Go to Spotify Developer Dashboard**
   - Visit: https://developer.spotify.com/dashboard

2. **Log In or Create Account**
   - Log in with your Spotify account (or create one free)
   - Accept the terms

3. **Create an App**
   - Click "Create an App"
   - Enter app name (e.g., "My Playlist Manager")
   - Check the terms box
   - Click "Create"

4. **Get Your Credentials**
   - You'll see your app page with:
     - **Client ID** - Copy this
     - **Client Secret** - Copy this (keep private!)

5. **Set Redirect URI**
   - Click "Edit Settings"
   - Add "Redirect URIs" section: `http://localhost:8888/callback`
   - Save

**You now have:**
```
Client ID:     1234567890abcdef1234567890abcdef
Client Secret: fedcba0987654321fedcba0987654321
Redirect URI:  http://localhost:8888/callback
```

---

## Step 2: Store Credentials Securely

### Option A: Environment Variables (Recommended for Development)

#### On macOS/Linux:

**1. Create or edit `.bashrc` or `.zshrc`:**
```bash
# Open your shell config file
nano ~/.bashrc
# or
nano ~/.zshrc
```

**2. Add these lines at the end:**
```bash
export SPOTIFY_CLIENT_ID="your_client_id_here"
export SPOTIFY_CLIENT_SECRET="your_client_secret_here"
export SPOTIFY_REDIRECT_URI="http://localhost:8888/callback"
```

**3. Save and reload:**
```bash
source ~/.bashrc
# or
source ~/.zshrc
```

**4. Verify:**
```bash
echo $SPOTIFY_CLIENT_ID
# Should print your client ID
```

#### On Windows:

**1. Open Environment Variables**
   - Search for "Environment Variables" in Start Menu
   - Click "Edit the system environment variables"
   - Click "Environment Variables" button

**2. Add New Variables**
   - Click "New" under "User variables"
   - Variable name: `SPOTIFY_CLIENT_ID`
   - Variable value: `your_client_id_here`
   - Click OK

**3. Repeat for other variables**
   - `SPOTIFY_CLIENT_SECRET` = `your_client_secret_here`
   - `SPOTIFY_REDIRECT_URI` = `http://localhost:8888/callback`

**4. Verify**
   - Open Command Prompt
   - Type: `echo %SPOTIFY_CLIENT_ID%`
   - Should print your client ID

### Option B: .env File (Alternative)

**1. Create `.env` file in your project:**
```bash
# In your project root directory
touch .env
```

**2. Add credentials:**
```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

**3. Use with python-dotenv:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
```

**4. Add `.env` to `.gitignore`:**
```bash
echo ".env" >> .gitignore
```

### Option C: Config File (For Production)

**1. Create `config.json`:**
```json
{
  "spotify": {
    "client_id": "your_client_id_here",
    "client_secret": "your_client_secret_here",
    "redirect_uri": "http://localhost:8888/callback"
  }
}
```

**2. Load in Python:**
```python
import json

with open("config.json") as f:
    config = json.load(f)
    
client_id = config["spotify"]["client_id"]
client_secret = config["spotify"]["client_secret"]
```

**3. Add `config.json` to `.gitignore`:**
```bash
echo "config.json" >> .gitignore
```

---

## Step 3: Use Credentials in Your Code

### Basic Setup

```python
import os
from spotify_client import SpotifyClient

# Load credentials from environment
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

# Initialize client
client = SpotifyClient(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri
)

# Get user playlists
playlists = client.get_user_playlists()
print(f"Found {len(playlists)} playlists")
```

### First-Time OAuth Setup

**First time you need to authenticate the user:**

```python
import os
import webbrowser
from spotify_client import SpotifyClient

# Initialize with credentials (no access token yet)
client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI")
)

# Step 1: Get authorization URL
auth_url = client.get_authorization_url()
print(f"Visit this URL to authorize:\n{auth_url}")

# Open in browser
webbrowser.open(auth_url)

# Step 2: Get authorization code from redirect
# After clicking authorize, you'll be redirected to:
# http://localhost:8888/callback?code=AQBPa...
auth_code = input("Enter the authorization code from the URL: ")

# Step 3: Exchange code for tokens
token_data = client.get_access_token(auth_code)
print(f"Access Token: {token_data['access_token']}")
print(f"Refresh Token: {token_data['refresh_token']}")

# Save refresh token for future use
os.environ["SPOTIFY_REFRESH_TOKEN"] = token_data["refresh_token"]
print("Refresh token saved! Add to environment variables for future use.")
```

### Subsequent Calls (Using Refresh Token)

```python
import os
from spotify_client import SpotifyClient

# Initialize with refresh token
client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    refresh_token=os.getenv("SPOTIFY_REFRESH_TOKEN")
)

# Token auto-refreshes when needed
playlists = client.get_user_playlists()
```

---

## Step 4: Using the Spotify Skill

### Quick Start (5 Minutes)

**1. Set environment variables** (from Step 2 above)

**2. Go through OAuth setup** (first time only)

```bash
python3 << 'EOF'
import os
import webbrowser
from spotify_client import SpotifyClient

# Initialize
client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI")
)

# Get auth URL
auth_url = client.get_authorization_url()
print(f"Visit: {auth_url}")
webbrowser.open(auth_url)

# Paste code here
code = input("Code: ")
tokens = client.get_access_token(code)

# Save for future
print(f"Save this refresh token: {tokens['refresh_token']}")
EOF
```

**3. Add refresh token to environment**

```bash
# Add to .bashrc or .zshrc or Windows Environment Variables
export SPOTIFY_REFRESH_TOKEN="your_refresh_token_here"
```

**4. Now you can use it!**

```python
import os
from spotify_client import SpotifyClient

client = SpotifyClient(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    refresh_token=os.getenv("SPOTIFY_REFRESH_TOKEN")
)

# Ready to use!
playlists = client.get_user_playlists()
```

---

## Complete Example Script

Save as `setup_spotify.py`:

```python
#!/usr/bin/env python3
"""
Setup script for Spotify API credentials
Run this once to set up authentication
"""

import os
import sys
import webbrowser
from spotify_client import SpotifyClient


def setup_credentials():
    """Interactive setup for Spotify credentials."""
    
    print("=" * 60)
    print("Spotify API Credential Setup")
    print("=" * 60)
    
    # Check for required environment variables
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    
    if not client_id:
        print("\n❌ SPOTIFY_CLIENT_ID not set!")
        print("\nSet these environment variables first:")
        print("  export SPOTIFY_CLIENT_ID='your_client_id'")
        print("  export SPOTIFY_CLIENT_SECRET='your_client_secret'")
        print("  export SPOTIFY_REDIRECT_URI='http://localhost:8888/callback'")
        print("\nGet them from: https://developer.spotify.com/dashboard")
        return False
    
    if not client_secret:
        print("\n❌ SPOTIFY_CLIENT_SECRET not set!")
        return False
    
    if not redirect_uri:
        print("\n❌ SPOTIFY_REDIRECT_URI not set!")
        print("  export SPOTIFY_REDIRECT_URI='http://localhost:8888/callback'")
        return False
    
    print("✅ Found credentials in environment")
    print(f"   Client ID: {client_id[:10]}...")
    print(f"   Redirect URI: {redirect_uri}")
    
    # Initialize client
    client = SpotifyClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )
    
    print("\n" + "=" * 60)
    print("Step 1: Authorization")
    print("=" * 60)
    
    # Get authorization URL
    auth_url = client.get_authorization_url()
    print("\nOpening browser for authorization...")
    print(f"If browser doesn't open, visit: {auth_url}\n")
    
    webbrowser.open(auth_url)
    
    # Get authorization code
    print("After clicking 'Allow', you'll be redirected to:")
    print("  http://localhost:8888/callback?code=AQBPa...")
    print("")
    auth_code = input("Paste the authorization code: ").strip()
    
    if not auth_code:
        print("❌ No code provided")
        return False
    
    print("\n" + "=" * 60)
    print("Step 2: Getting Access Token")
    print("=" * 60)
    
    try:
        token_data = client.get_access_token(auth_code)
        print("✅ Successfully authenticated!")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False
    
    # Save refresh token
    refresh_token = token_data.get("refresh_token")
    if refresh_token:
        print("\n" + "=" * 60)
        print("Step 3: Save Refresh Token")
        print("=" * 60)
        print(f"\nRefresh Token: {refresh_token}")
        print("\nAdd this to your environment variables:")
        print(f"  export SPOTIFY_REFRESH_TOKEN='{refresh_token}'")
        print("\nOr add to .env file:")
        print(f"  SPOTIFY_REFRESH_TOKEN={refresh_token}")
        print("\nOr add to Windows Environment Variables:")
        print(f"  SPOTIFY_REFRESH_TOKEN = {refresh_token}")
        
        # Save to .env if exists
        if os.path.exists(".env"):
            response = input("\nSave to .env file? (y/n): ").strip().lower()
            if response == "y":
                with open(".env", "a") as f:
                    f.write(f"\nSPOTIFY_REFRESH_TOKEN={refresh_token}\n")
                print("✅ Saved to .env")
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print("\nYou can now use the Spotify client:")
    print("""
    from spotify_client import SpotifyClient
    import os
    
    client = SpotifyClient(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        refresh_token=os.getenv("SPOTIFY_REFRESH_TOKEN")
    )
    
    playlists = client.get_user_playlists()
    """)
    
    return True


if __name__ == "__main__":
    success = setup_credentials()
    sys.exit(0 if success else 1)
```

**Run it:**
```bash
python3 setup_spotify.py
```

---

## Troubleshooting

### "SPOTIFY_CLIENT_ID not found"

**Problem:** Environment variable not set

**Solution:**
```bash
# Check if set
echo $SPOTIFY_CLIENT_ID

# If empty, set it
export SPOTIFY_CLIENT_ID="your_id"

# Or add to .bashrc/.zshrc and reload
source ~/.bashrc
```

### "Invalid Client ID or Secret"

**Problem:** Wrong credentials or typo

**Solution:**
- Double-check from https://developer.spotify.com/dashboard
- No extra spaces or quotes
- Copy-paste to avoid typos

### "Invalid Redirect URI"

**Problem:** Redirect URI doesn't match what's registered

**Solution:**
- Must match exactly in Spotify Dashboard
- Case-sensitive
- Must include `http://` or `https://`
- Default: `http://localhost:8888/callback`

### "Authorization code expired"

**Problem:** Code was valid for only 10 minutes

**Solution:**
- Run setup script again
- Go through OAuth flow again
- Use refresh token for subsequent calls

### "Token expired"

**Problem:** Access token expired (normally happens after 1 hour)

**Solution:**
- Client auto-refreshes with refresh token
- No action needed - happens automatically
- Make sure `SPOTIFY_REFRESH_TOKEN` is set

---

## Security Best Practices

### ✅ DO

1. **Use environment variables** - Keep secrets out of code
2. **Add to .gitignore** - Never commit credentials
   ```bash
   echo ".env" >> .gitignore
   echo "config.json" >> .gitignore
   ```
3. **Use refresh tokens** - Reuse without re-authentication
4. **Rotate credentials** - Periodically update
5. **Regenerate secret** - If compromised (in Spotify Dashboard)
6. **Use HTTPS** - In production only

### ❌ DON'T

1. **Hard-code credentials** - Never in source code
2. **Commit .env files** - Add to .gitignore
3. **Share credentials** - Keep private
4. **Use access token** - Use refresh token instead
5. **Log credentials** - Remove from logs
6. **Send over HTTP** - Use HTTPS in production

---

## Quick Reference

### Check Credentials are Set

```bash
# Linux/Mac
echo "Client ID: $SPOTIFY_CLIENT_ID"
echo "Client Secret: $SPOTIFY_CLIENT_SECRET"
echo "Redirect URI: $SPOTIFY_REDIRECT_URI"
echo "Refresh Token: $SPOTIFY_REFRESH_TOKEN"

# Windows (Command Prompt)
echo Client ID: %SPOTIFY_CLIENT_ID%
echo Client Secret: %SPOTIFY_CLIENT_SECRET%
echo Redirect URI: %SPOTIFY_REDIRECT_URI%
echo Refresh Token: %SPOTIFY_REFRESH_TOKEN%
```

### Update Credentials

```bash
# Linux/Mac - edit ~/.bashrc or ~/.zshrc
nano ~/.bashrc

# Windows - Use GUI Environment Variables
# Search "Environment Variables" in Start Menu
```

### Remove Credentials

```bash
# Linux/Mac
unset SPOTIFY_CLIENT_ID
unset SPOTIFY_CLIENT_SECRET
unset SPOTIFY_REDIRECT_URI
unset SPOTIFY_REFRESH_TOKEN

# Or edit ~/.bashrc to remove the lines
```

---

## Summary

1. **Get credentials** from https://developer.spotify.com/dashboard
2. **Add Redirect URI** in Spotify Dashboard settings
3. **Set environment variables** (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, etc.)
4. **Run OAuth setup** first time to get refresh token
5. **Save refresh token** in environment
6. **Use SpotifyClient** in your code

**That's it!** You're ready to use the Spotify API. 🎵
