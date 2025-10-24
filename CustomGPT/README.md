# Spotify Custom GPT Action

This directory contains an OpenAPI specification that allows OpenAI Custom GPTs to **directly call the Spotify Web API** using OAuth 2.0 authentication.

## 📋 Overview

This Custom GPT Action enables your GPT to:
- ✅ Create, read, update, and delete playlists
- ✅ Add and remove tracks from playlists
- ✅ Search for tracks, artists, albums, and playlists
- ✅ Get artist information and top tracks
- ✅ Get music recommendations
- ✅ Control playback (play, pause, skip)
- ✅ Get current playback state

**No API server required!** The GPT talks directly to Spotify using built-in OAuth 2.0.

### 🤖 Designed for GPT-5 Success

This action is optimized for AI comprehension with:
- **Clear decision trees** for operation selection
- **Explicit format examples** (URI conversion, object notation)
- **Step-by-step workflows** with sample API responses
- **Batching vs pagination** guidance
- **Error recovery patterns** with user-friendly messages
- **Comprehensive knowledge base** (511 lines) with 6 detailed workflows

---

## 🚀 Quick Setup (5 Minutes)

### 1️⃣ Create Spotify App (2 minutes)

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click **Create app**
3. Fill in:
   - **App name:** "My Custom GPT"
   - **App description:** "Custom GPT for Spotify"
   - **Redirect URI:** `https://chat.openai.com/aip/plugin-YOUR_GPT_ID/oauth/callback`
     _(We'll update this later)_
4. Click **Save**
5. **Copy your Client ID and Client Secret** (you'll need these!)

### 2️⃣ Create Custom GPT (2 minutes)

1. Go to [ChatGPT](https://chat.openai.com) → **Explore GPTs** → **Create**
2. Fill in the **Configure** tab:

   **Name:**
   ```
   Alex METHOD DJ
   ```

   **Description:**
   ```
   Your personal Spotify music manager - create playlists, search music, and control playback
   ```

   **Instructions:** (copy-paste this)
   ```
   You are Alex METHOD DJ, a Spotify assistant that helps users manage their Spotify music library.

   IMPORTANT: Follow the detailed workflows and guidelines in your knowledge base document "SPOTIFY_GPT_INSTRUCTIONS.md"

   CORE CAPABILITIES:
   - Search and discover music
   - Create and manage playlists
   - Add/remove tracks (use spotify:track:{id} format)
   - Get personalized recommendations
   - Control playback
   - Create custom cover art (square JPEG, user uploads manually)

   **KEY REMINDERS:**
   - Convert track IDs to URIs: spotify:track:{id}
   - Confirm before destructive actions
   - Provide external_urls.spotify links
   - Respect API limits (100 tracks, 50 results)
   - Cover art: Create square JPEG image and provide it for user to upload
   - Removal format: {"tracks": [{"uri": "..."}]}

   Refer to SPOTIFY_GPT_INSTRUCTIONS.md for complete workflows, pagination, batching, and error handling.
   ```

   **Knowledge Base:**
   - Upload `SPOTIFY_GPT_INSTRUCTIONS.md` from the CustomGPT folder

   **Conversation Starters:**
   ```
   Create a chill evening playlist with 20 songs
   Find tracks by Pink Floyd and add them to my Rock Classics playlist
   Generate cover art for my Workout Mix playlist
   What's currently playing on my Spotify?
   ```

### 3️⃣ Add the Action (1 minute)

1. In the **Configure** tab, scroll to **Actions**
2. Click **Create new action**
3. **Import from URL:** (paste this)
   ```
   https://raw.githubusercontent.com/fabioc-aloha/spotify-skill/main/CustomGPT/spotify-playlist-action.json
   ```

   **OR** manually copy the contents of `spotify-playlist-action.json` and paste it

4. Click **Save** (at bottom)

### 4️⃣ Configure OAuth Authentication (2 minutes)

After saving your action, you'll see the **Authentication** section.

**Fill out the form as follows:**

| Field | Value | Notes |
|-------|-------|-------|
| **Authentication Type** | OAuth | Select the third radio button |
| **Client ID** | `<your_spotify_client_id>` | From Spotify Dashboard |
| **Client Secret** | `<your_spotify_client_secret>` | From Spotify Dashboard |
| **Authorization URL** | `https://accounts.spotify.com/authorize` | Copy exactly |
| **Token URL** | `https://accounts.spotify.com/api/token` | Copy exactly |
| **Scope** | *(see below)* | Should auto-populate from spec |
| **Token Exchange Method** | Default (POST request) | Keep the default selected |

**Step-by-step:**

1. **Authentication Type:** Select **OAuth** (the third radio button)

2. **Client ID:** Paste your Spotify Client ID from Step 1

3. **Client Secret:** Paste your Spotify Client Secret from Step 1

4. **Authorization URL:** Enter exactly:
   ```
   https://accounts.spotify.com/authorize
   ```

5. **Token URL:** Enter exactly:
   ```
   https://accounts.spotify.com/api/token
   ```

6. **Scope:** ChatGPT should auto-populate this from the OpenAPI spec. If it's empty, manually enter (space-separated):
   ```
   user-read-private user-read-email playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-read user-top-read user-read-playback-state user-modify-playback-state user-read-currently-playing ugc-image-upload
   ```

   **Note:** The `ugc-image-upload` scope is required for uploading custom playlist cover art. All other scopes are for standard playlist and playback operations.

7. **Token Exchange Method:** Keep **"Default (POST request)"** selected

8. **IMPORTANT - Update Spotify Redirect URI:**
   - ChatGPT will show you a callback URL at the top (looks like: `https://chat.openai.com/aip/g-xxxxx/oauth/callback`)
   - **Copy this URL**
   - Go back to your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Open your app → Click **Settings**
   - Under **Redirect URIs**, click **Edit**
   - **Add** the callback URL you copied
   - Click **Add** then **Save**

9. Back in ChatGPT, click **Save** at the bottom of the Authentication section

> **📝 Note:** This setup uses the OAuth 2.0 Authorization Code flow, which is the standard for web applications. ChatGPT will:
> 1. Redirect users to Spotify for authentication
> 2. Exchange the authorization code for access/refresh tokens
> 3. Automatically refresh tokens when they expire
> 4. Securely store tokens per user

### 5️⃣ Test Your GPT! (30 seconds)

1. Click **Test** in the top right of the GPT builder
2. Try: "Search for songs by Queen"
3. Click **Allow** when prompted to authenticate with Spotify
4. Try: "Create a playlist called 'My Awesome Mix'"

🎉 **Done!** Your Spotify Custom GPT is ready!

---

## 🎵 What You Can Do

Try these commands:

### Search Music
- "Find tracks by Coldplay"
- "Search for chill indie music"
- "Show me The Weeknd's top songs"

### Create Playlists
- "Create a workout playlist"
- "Make a 90s hip-hop playlist"
- "Create a playlist called 'Road Trip'"

### Manage Playlists
- "Add Bohemian Rhapsody to my Rock Classics playlist"
- "Show me my playlists"
- "Remove duplicates from my playlist"

### Control Playback (requires Spotify Premium)
- "Play my workout playlist"
- "Skip to the next song"
- "What's currently playing?"

### Cover Art
- "Create a cover art for my Road Trip playlist"
- "Design a minimalist cover for my Chill Vibes playlist"

---

## 📖 Available Operations

### Playlist Management
- `GET /me/playlists` - List your playlists
- `POST /me/playlists` - Create new playlist
- `GET /playlists/{id}` - Get playlist details
- `PUT /playlists/{id}` - Update playlist name/description
- `DELETE /playlists/{id}/followers` - Unfollow/delete playlist

### Track Management
- `GET /playlists/{id}/tracks` - Get playlist tracks
- `POST /playlists/{id}/tracks` - Add tracks (use Spotify URIs: `spotify:track:xxx`)
- `DELETE /playlists/{id}/tracks` - Remove tracks

### Search & Discovery
- `GET /search` - Search for tracks, artists, albums, playlists
- `GET /artists/{id}` - Get artist info
- `GET /artists/{id}/top-tracks` - Get artist's top tracks
- `GET /recommendations` - Get personalized recommendations

### Playback Control
- `GET /me/player` - Get current playback state
- `PUT /me/player/play` - Start/resume playback
- `PUT /me/player/pause` - Pause playback
- `POST /me/player/next` - Skip to next track
- `POST /me/player/previous` - Skip to previous track

## 💡 Usage Examples

### Create a Themed Playlist
```
User: "Create a chill indie playlist with 20 songs"

GPT will:
1. Search: GET /search?q=chill indie&type=track&limit=20
2. Create playlist: POST /me/playlists (name: "Chill Indie Vibes")
3. Add tracks: POST /playlists/{id}/tracks (body: {uris: ["spotify:track:xxx", ...]})
4. Return the playlist link
```

### Add Songs by Artist
```
User: "Add The Beatles top songs to my 'Classics' playlist"

GPT will:
1. Search artist: GET /search?q=The Beatles&type=artist
2. Get top tracks: GET /artists/{id}/top-tracks
3. Find your playlist: GET /me/playlists (filter for "Classics")
4. Add tracks: POST /playlists/{id}/tracks
```

### Control Playback
```
User: "Play my workout playlist"

GPT will:
1. Find playlist: GET /me/playlists (filter for "workout")
2. Start playback: PUT /me/player/play (body: {context_uri: "spotify:playlist:xxx"})
```

## 🔒 Security & Privacy

- **OAuth 2.0:** Users authenticate directly with Spotify
- **Token Management:** ChatGPT handles token refresh automatically
- **Permissions:** Only requested scopes are granted
- **Privacy:** No third-party servers involved - direct Spotify API calls

## 🐛 Troubleshooting

### OAuth Authentication Issues

**"Authentication failed" or "Invalid client"**
- Verify your Client ID and Client Secret are correct (no extra spaces)
- Make sure you're using credentials from the correct Spotify app
- Check that the redirect URI in Spotify matches exactly what ChatGPT shows

**"Redirect URI mismatch" error**
- The callback URL must **exactly match** between ChatGPT and Spotify
- Format: `https://chat.openai.com/aip/g-xxxxx/oauth/callback`
- After adding to Spotify, click **Save** in the Spotify Dashboard
- Wait a few seconds, then try authenticating again

**Scope configuration**
- ChatGPT should auto-populate scopes from the OpenAPI spec's `securitySchemes` section
- If the Scope field is empty, manually enter the required scopes (space-separated)
- Required scopes: `user-read-private user-read-email playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-read user-top-read user-read-playback-state user-modify-playback-state user-read-currently-playing`
- Do NOT leave the scope field blank - authentication will fail without proper scopes

**Token Exchange Method**
- Use **"Default (POST request)"** (recommended)
- Only use "Basic authorization header" if you have specific requirements

### API Usage Issues

**"Invalid URI" errors when adding tracks**
- Spotify requires URIs in format: `spotify:track:{track_id}`
- Not just the track ID: ❌ `7qiZfU4dY1lWllzX7mPBI`
- Correct format: ✅ `spotify:track:7qiZfU4dY1lWllzX7mPBI`

**"Forbidden" or "Insufficient scope" errors**
- The OAuth token may not have required permissions
- Try re-authenticating (start a new conversation with the GPT)
- Some operations require Spotify Premium (e.g., playback control)

**GPT not finding playlists**
- The GPT needs to search through your playlists first with GET /me/playlists
- For large libraries, may need pagination (offset parameter)

## 📚 Help & Support

### Documentation Files

- **`SPOTIFY_GPT_INSTRUCTIONS.md`** (511 lines) - Complete knowledge base with:
  - 6 detailed workflows (create playlist, search & add, remove tracks, cover art, recommendations, playback)
  - API limits and pagination strategies
  - Batching patterns for 100+ items
  - Error handling and troubleshooting
  - Complete examples and best practices
  - **Upload this as knowledge file when creating your GPT**

- **`spotify-playlist-action.json`** - OpenAPI 3.1 specification (16 endpoints, 15 scopes)

### Additional Resources

- [Spotify Web API Reference](https://developer.spotify.com/documentation/web-api)
- [OpenAI GPT Actions Documentation](https://platform.openai.com/docs/actions)
- [OAuth 2.0 Authorization](https://developer.spotify.com/documentation/web-api/concepts/authorization)
- Main project repository: [Spotify Skills for Claude](https://github.com/fabioc-aloha/spotify-skill)

### Need More Help?

- **API Issues:** Check [Spotify API Status](https://developer.spotify.com/status)
- **OAuth Problems:** Review the Authentication section in Step 4 above
- **GPT Configuration:** See OpenAI's [Actions documentation](https://platform.openai.com/docs/actions)
- **Feature Requests:** Open an issue on the main repository

---

---

## 🎯 Advanced Customization

### Add More Endpoints

Edit `spotify-playlist-action.json` to add more Spotify API endpoints:

```json
"/me/top/tracks": {
  "get": {
    "operationId": "getMyTopTracks",
    "summary": "Get user's top tracks",
    ...
  }
}
```

### Custom Instructions

Enhance your GPT's behavior by refining instructions:

```
When creating playlists:
- Default to public playlists unless user specifies private
- Add 20-30 songs for a good mix
- Include variety (different artists/albums)
- Add a descriptive playlist description

When searching:
- Show top 5 results with artist names
- Include Spotify links for easy access
- Offer to add tracks to existing or new playlists
```

---

## 📁 Files in This Directory

- **`spotify-playlist-action.json`** - OpenAPI 3.1 specification for direct Spotify API integration (16 endpoints, 644 lines)
- **`SPOTIFY_GPT_INSTRUCTIONS.md`** - Comprehensive knowledge base for LLM (511 lines) - Upload when creating GPT
- **`README.md`** - Complete setup and usage documentation (this file)

---

## 📄 License

This project is licensed under the Apache 2.0 License - see the LICENSE file in the root directory.
