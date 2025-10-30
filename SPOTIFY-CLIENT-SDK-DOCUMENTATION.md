# Spotify Client-Side SDK Documentation

*Complete guide to client-side Spotify integration across web, mobile, and desktop platforms*

## Table of Contents

1. [Overview](#overview)
2. [Web Playback SDK (JavaScript)](#web-playback-sdk-javascript)
3. [iOS SDK](#ios-sdk)
4. [Android SDK](#android-sdk)
5. [Authentication Methods](#authentication-methods)
6. [Scopes & Permissions](#scopes--permissions)
7. [Platform Comparison](#platform-comparison)
8. [Implementation Examples](#implementation-examples)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Overview

This documentation covers Spotify's client-side SDKs that enable direct integration with the Spotify app and streaming capabilities within your applications. Unlike server-side Web API integration, these SDKs provide:

- **Direct streaming capabilities** (Web Playback SDK)
- **Integration with the main Spotify app** (iOS/Android SDKs)
- **Client-side authentication** (PKCE flow)
- **Real-time playback control** and state management
- **Offline support** (mobile SDKs)

### Key Differences from Server-Side API

| Feature | Client-Side SDKs | Server-Side Web API |
|---------|------------------|-------------------|
| **Streaming** | ✅ Direct playback in browser/app | ❌ Control only |
| **Authentication** | PKCE, App Remote | OAuth 2.0 Authorization Code |
| **Offline Support** | ✅ (Mobile SDKs) | ❌ |
| **Client Secret** | ❌ Not required | ✅ Required |
| **Platform** | Browser, iOS, Android | Any platform with HTTP |

---

## Web Playback SDK (JavaScript)

### Overview

The **Web Playback SDK** is a client-side JavaScript library that creates a Spotify Connect device in your browser, enabling:

- Direct music streaming (requires **Spotify Premium**)
- Playback control (play, pause, skip, volume)
- Real-time player state updates
- Integration with Spotify Connect ecosystem

### Key Features

- **Lightweight** client-side only library
- **Real-time streaming** with Spotify Premium accounts
- **Cross-browser support** (Chrome, Firefox, Safari, Microsoft Edge)
- **Mobile compatibility** (Android and iOS browsers)
- **No client secret required** (uses implicit grant flow)

### Requirements

- **Spotify Premium subscription** (mobile-only plans excluded)
- Modern web browser with JavaScript enabled
- HTTPS connection (required for production)

### Basic Implementation

#### 1. Load the SDK

```html
<script src="https://sdk.scdn.co/spotify-player.js"></script>
```

#### 2. Initialize Player

```javascript
window.onSpotifyWebPlaybackSDKReady = () => {
    const token = 'BQA...'; // Your access token

    const player = new Spotify.Player({
        name: 'My Web Player',
        getOAuthToken: cb => { cb(token); },
        volume: 0.5
    });

    // Ready
    player.addListener('ready', ({ device_id }) => {
        console.log('Ready with Device ID', device_id);
    });

    // Not Ready
    player.addListener('not_ready', ({ device_id }) => {
        console.log('Device ID has gone offline', device_id);
    });

    // Player State Changed
    player.addListener('player_state_changed', (state) => {
        console.log('Currently Playing', state.track_window.current_track);
        console.log('Position', state.position);
        console.log('Duration', state.duration);
    });

    // Connect to the player!
    player.connect();
};
```

#### 3. Playback Controls

```javascript
// Toggle play/pause
player.togglePlay();

// Skip to next track
player.nextTrack();

// Skip to previous track
player.previousTrack();

// Set volume (0.0 to 1.0)
player.setVolume(0.8);

// Get current state
player.getCurrentState().then(state => {
    if (!state) {
        console.error('User is not playing music through the Web Playback SDK');
        return;
    }

    console.log('Currently Playing', state.track_window.current_track);
    console.log('Position in Song', state.position);
    console.log('Duration of Song', state.duration);
});
```

### Required Scopes

For Web Playback SDK integration:

```javascript
const scopes = [
    'streaming',                    // Required for Web Playback SDK
    'user-read-email',             // Read user email
    'user-read-private',           // Read user subscription details
    'user-read-playback-state',    // Read current playback state
    'user-modify-playback-state'   // Control playback
];
```

### Complete Example with React

```jsx
import React, { useState, useEffect } from 'react';

function WebPlayer({ token }) {
    const [player, setPlayer] = useState(undefined);
    const [is_paused, setPaused] = useState(false);
    const [is_active, setActive] = useState(false);
    const [current_track, setTrack] = useState({
        name: "",
        album: { images: [{ url: "" }] },
        artists: [{ name: "" }]
    });

    useEffect(() => {
        const script = document.createElement("script");
        script.src = "https://sdk.scdn.co/spotify-player.js";
        script.async = true;
        document.body.appendChild(script);

        window.onSpotifyWebPlaybackSDKReady = () => {
            const player = new window.Spotify.Player({
                name: 'Web Playback SDK Player',
                getOAuthToken: cb => { cb(token); },
                volume: 0.5
            });

            setPlayer(player);

            player.addListener('ready', ({ device_id }) => {
                console.log('Ready with Device ID', device_id);
            });

            player.addListener('not_ready', ({ device_id }) => {
                console.log('Device ID has gone offline', device_id);
            });

            player.addListener('player_state_changed', (state => {
                if (!state) return;

                setTrack(state.track_window.current_track);
                setPaused(state.paused);

                player.getCurrentState().then(state => {
                    (!state) ? setActive(false) : setActive(true)
                });
            }));

            player.connect();
        };
    }, []);

    return (
        <div className="container">
            <div className="main-wrapper">
                <img src={current_track.album.images[0]?.url}
                     className="now-playing__cover" alt="" />

                <div className="now-playing__side">
                    <div className="now-playing__name">
                        {current_track.name}
                    </div>
                    <div className="now-playing__artist">
                        {current_track.artists[0]?.name}
                    </div>
                </div>

                <div className="controls">
                    <button onClick={() => { player.previousTrack() }}>
                        ⏮️
                    </button>
                    <button onClick={() => { player.togglePlay() }}>
                        {is_paused ? "▶️" : "⏸️"}
                    </button>
                    <button onClick={() => { player.nextTrack() }}>
                        ⏭️
                    </button>
                </div>
            </div>
        </div>
    );
}

export default WebPlayer;
```

---

## iOS SDK

### Overview

The **Spotify iOS SDK** allows your iOS application to interact with the Spotify app running on the same device. It provides:

- **App Remote control** of Spotify playback
- **Always-in-sync playback** with the main Spotify app
- **Offline support** for cached content
- **Built-in networking** and track relinking
- **Lightweight implementation** with authentication support

### Key Features

- **Lightweight SDK** with minimal overhead
- **Authentication** handling with built-in support
- **Always-in-sync playback** via the main Spotify application
- **Offline support** (excludes Web API calls)
- **Built-in networking**, track relinking, and caching

### Requirements

- **iOS 12+** deployment target
- **Architectures**: arm64 (device), arm64 + x86_64 (simulator)
- **Physical iOS device** needed for Spotify app integration
- **Spotify app** installed on target device

### Installation

#### CocoaPods

```ruby
# Podfile
pod 'SpotifyiOS'
```

#### Swift Package Manager

```swift
// Package.swift dependencies
.package(url: "https://github.com/spotify/ios-sdk", from: "2.1.0")
```

### Basic Implementation

#### 1. Configure App

```swift
// AppDelegate.swift
import SpotifyiOS

class AppDelegate: UIResponder, UIApplicationDelegate {

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {

        SpotifyiOS.setClientID("your-client-id")
        SpotifyiOS.setRedirectURL(URL(string: "your-redirect-url")!)

        return true
    }

    func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey : Any] = [:]) -> Bool {
        SpotifyiOS.application(app, open: url, options: options)
        return true
    }
}
```

#### 2. Authentication

```swift
import SpotifyiOS

class ViewController: UIViewController {

    private let spotifyClientID = "your-client-id"
    private let spotifyRedirectURL = URL(string: "your-redirect-url")!

    override func viewDidLoad() {
        super.viewDidLoad()

        // Configure
        SpotifyiOS.setClientID(spotifyClientID)
        SpotifyiOS.setRedirectURL(spotifyRedirectURL)
    }

    @IBAction func authorizeButtonTapped(_ sender: Any) {
        let scope: SPTScope = [.appRemoteControl, .userReadEmail, .userReadPrivate]

        SpotifyiOS.authorization.authorize(from: self, scopes: scope) { [weak self] result in
            switch result {
            case .success(let session):
                print("Authorized successfully: \(session.accessToken)")
                self?.connectToSpotifyAppRemote()
            case .failure(let error):
                print("Authorization failed: \(error)")
            }
        }
    }
}
```

#### 3. App Remote Integration

```swift
import SpotifyiOS

class SpotifyManager: NSObject, ObservableObject {

    private let appRemote = SPTAppRemote.sharedInstance()
    @Published var isConnected = false
    @Published var currentTrack: SPTAppRemoteTrack?

    override init() {
        super.init()
        appRemote.connectionParameters.accessToken = SpotifyiOS.session?.accessToken
        appRemote.delegate = self
    }

    func connect() {
        guard let _ = SpotifyiOS.session?.accessToken else {
            print("No access token available")
            return
        }

        appRemote.connect()
    }

    func disconnect() {
        appRemote.disconnect()
    }

    // Playback controls
    func play() {
        appRemote.playerAPI?.resume(nil)
    }

    func pause() {
        appRemote.playerAPI?.pause(nil)
    }

    func skipNext() {
        appRemote.playerAPI?.skip(toNext: nil)
    }

    func skipPrevious() {
        appRemote.playerAPI?.skip(toPrevious: nil)
    }

    func playURI(_ uri: String) {
        appRemote.playerAPI?.play(uri, callback: nil)
    }
}

// MARK: - SPTAppRemoteDelegate
extension SpotifyManager: SPTAppRemoteDelegate {
    func appRemoteDidEstablishConnection(_ appRemote: SPTAppRemote) {
        print("App remote connected")
        isConnected = true

        // Subscribe to player state
        appRemote.playerAPI?.subscribe(toPlayerState: { [weak self] result, error in
            if let error = error {
                print("Failed to subscribe to player state: \(error)")
                return
            }
            print("Successfully subscribed to player state")
        })
    }

    func appRemote(_ appRemote: SPTAppRemote, didDisconnectWithError error: Error?) {
        print("App remote disconnected")
        isConnected = false
    }

    func appRemote(_ appRemote: SPTAppRemote, didFailConnectionAttemptWithError error: Error?) {
        print("Failed to connect: \(error?.localizedDescription ?? "Unknown error")")
        isConnected = false
    }
}

// MARK: - SPTAppRemotePlayerStateDelegate
extension SpotifyManager: SPTAppRemotePlayerStateDelegate {
    func playerStateDidChange(_ playerState: SPTAppRemotePlayerState) {
        currentTrack = playerState.track
        print("Track: \(playerState.track.name) by \(playerState.track.artist.name)")
    }
}
```

### Required Scopes

```swift
let scope: SPTScope = [
    .appRemoteControl,      // Required for iOS SDK
    .userReadEmail,         // Read user email
    .userReadPrivate,       // Read user subscription details
    .playlistReadPrivate,   // Read private playlists
    .playlistModifyPrivate, // Modify private playlists
    .userLibraryRead,       // Read user's library
    .userLibraryModify      // Modify user's library
]
```

---

## Android SDK

### Overview

The **Spotify Android SDK** allows your Android application to interact with the Spotify app, providing:

- **App Remote control** for playback management
- **Always-in-sync playback** with the main Spotify app
- **Lightweight library** (less than 300KB)
- **Offline/online support** with automatic handling
- **System integration** (audio focus, lockscreen, calls)

### Key Features

- **Lightweight** (less than 300KB, no native dependencies)
- **Always-in-sync** playback with Spotify app
- **Handles system integration** (audio focus, lockscreen controls, calls)
- **Automatic track relinking** for different regions
- **Works offline and online** without Web API calls for metadata
- **Automatic processing** of playback, caching, and network traffic

### Requirements

- **Minimum Android SDK Version 14** (Android 4.0+)
- **Gson dependency** (version 2.6.1 or later)
- **Spotify app** installed on target device

### Installation

#### Gradle

```gradle
// app/build.gradle
dependencies {
    implementation 'com.spotify.android:auth:2.1.1'
    implementation 'com.spotify.android:app-remote:0.8.0'
    implementation 'com.google.code.gson:gson:2.8.9'
}
```

### Basic Implementation

#### 1. Configure Authentication

```java
// MainActivity.java
import com.spotify.sdk.android.auth.AuthorizationClient;
import com.spotify.sdk.android.auth.AuthorizationRequest;
import com.spotify.sdk.android.auth.AuthorizationResponse;

public class MainActivity extends AppCompatActivity {

    private static final String CLIENT_ID = "your-client-id";
    private static final String REDIRECT_URI = "your-app://callback";
    private static final int REQUEST_CODE = 1337;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        authenticateSpotify();
    }

    private void authenticateSpotify() {
        AuthorizationRequest.Builder builder =
            new AuthorizationRequest.Builder(CLIENT_ID, AuthorizationResponse.Type.TOKEN, REDIRECT_URI);

        builder.setScopes(new String[]{
            "app-remote-control",
            "user-read-email",
            "user-read-private"
        });

        AuthorizationRequest request = builder.build();
        AuthorizationClient.openLoginActivity(this, REQUEST_CODE, request);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
        super.onActivityResult(requestCode, resultCode, intent);

        if (requestCode == REQUEST_CODE) {
            AuthorizationResponse response = AuthorizationClient.getResponse(resultCode, intent);

            switch (response.getType()) {
                case TOKEN:
                    // Handle successful response
                    String accessToken = response.getAccessToken();
                    connectToAppRemote(accessToken);
                    break;

                case ERROR:
                    // Handle error response
                    Log.e("Auth", "Authorization error: " + response.getError());
                    break;

                default:
                    // Most likely auth flow was cancelled
                    Log.d("Auth", "Authorization cancelled");
            }
        }
    }
}
```

#### 2. App Remote Integration

```java
import com.spotify.android.appremote.api.ConnectionParams;
import com.spotify.android.appremote.api.Connector;
import com.spotify.android.appremote.api.SpotifyAppRemote;

public class SpotifyManager {

    private static final String CLIENT_ID = "your-client-id";
    private static final String REDIRECT_URI = "your-app://callback";

    private SpotifyAppRemote mSpotifyAppRemote;

    public void connectToAppRemote(String accessToken) {
        ConnectionParams connectionParams =
            new ConnectionParams.Builder(CLIENT_ID)
                .setRedirectUri(REDIRECT_URI)
                .showAuthView(true)
                .build();

        SpotifyAppRemote.connect(context, connectionParams,
            new Connector.ConnectionListener() {

                @Override
                public void onConnected(SpotifyAppRemote spotifyAppRemote) {
                    mSpotifyAppRemote = spotifyAppRemote;
                    Log.d("SpotifyManager", "Connected! Yay!");

                    // Subscribe to PlayerState
                    subscribeToPlayerState();
                }

                @Override
                public void onFailure(Throwable throwable) {
                    Log.e("SpotifyManager", throwable.getMessage(), throwable);
                }
            });
    }

    private void subscribeToPlayerState() {
        mSpotifyAppRemote.getPlayerApi()
            .subscribeToPlayerState()
            .setEventCallback(playerState -> {
                final Track track = playerState.track;
                if (track != null) {
                    Log.d("SpotifyManager", track.name + " by " + track.artist.name);
                }
            });
    }

    // Playback controls
    public void play() {
        mSpotifyAppRemote.getPlayerApi().resume();
    }

    public void pause() {
        mSpotifyAppRemote.getPlayerApi().pause();
    }

    public void skipNext() {
        mSpotifyAppRemote.getPlayerApi().skipNext();
    }

    public void skipPrevious() {
        mSpotifyAppRemote.getPlayerApi().skipPrevious();
    }

    public void playUri(String uri) {
        mSpotifyAppRemote.getPlayerApi().play(uri);
    }

    public void disconnect() {
        SpotifyAppRemote.disconnect(mSpotifyAppRemote);
    }
}
```

#### 3. Kotlin Implementation

```kotlin
// SpotifyManager.kt
import com.spotify.android.appremote.api.ConnectionParams
import com.spotify.android.appremote.api.Connector
import com.spotify.android.appremote.api.SpotifyAppRemote

class SpotifyManager(private val context: Context) {

    companion object {
        private const val CLIENT_ID = "your-client-id"
        private const val REDIRECT_URI = "your-app://callback"
    }

    private var spotifyAppRemote: SpotifyAppRemote? = null

    fun connect() {
        val connectionParams = ConnectionParams.Builder(CLIENT_ID)
            .setRedirectUri(REDIRECT_URI)
            .showAuthView(true)
            .build()

        SpotifyAppRemote.connect(context, connectionParams, object : Connector.ConnectionListener {
            override fun onConnected(appRemote: SpotifyAppRemote) {
                spotifyAppRemote = appRemote
                Log.d("SpotifyManager", "Connected to Spotify!")

                // Subscribe to player state changes
                appRemote.playerApi.subscribeToPlayerState().setEventCallback { playerState ->
                    val track = playerState.track
                    Log.d("SpotifyManager", "Currently playing: ${track.name} by ${track.artist.name}")
                }
            }

            override fun onFailure(throwable: Throwable) {
                Log.e("SpotifyManager", "Failed to connect", throwable)
            }
        })
    }

    fun play() = spotifyAppRemote?.playerApi?.resume()
    fun pause() = spotifyAppRemote?.playerApi?.pause()
    fun skipNext() = spotifyAppRemote?.playerApi?.skipNext()
    fun skipPrevious() = spotifyAppRemote?.playerApi?.skipPrevious()
    fun playUri(uri: String) = spotifyAppRemote?.playerApi?.play(uri)

    fun disconnect() {
        spotifyAppRemote?.let {
            SpotifyAppRemote.disconnect(it)
        }
    }
}
```

### Required Scopes

```java
String[] scopes = {
    "app-remote-control",       // Required for Android SDK
    "user-read-email",          // Read user email
    "user-read-private",        // Read user subscription details
    "playlist-read-private",    // Read private playlists
    "playlist-modify-private",  // Modify private playlists
    "user-library-read",        // Read user's library
    "user-library-modify"       // Modify user's library
};
```

---

## Authentication Methods

### PKCE Flow (Recommended for Client-Side)

The **Authorization Code with PKCE (Proof Key for Code Exchange)** flow is the recommended method for client-side applications where the client secret cannot be safely stored.

#### Why PKCE?

- **No client secret required** - safer for public clients
- **Protection against authorization code interception**
- **Recommended for SPAs, mobile apps, and desktop apps**
- **Required for Web Playback SDK** in production environments

#### Implementation

```javascript
// 1. Generate code verifier and challenge
const generateRandomString = (length) => {
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const values = crypto.getRandomValues(new Uint8Array(length));
    return values.reduce((acc, x) => acc + possible[x % possible.length], "");
}

const sha256 = async (plain) => {
    const encoder = new TextEncoder();
    const data = encoder.encode(plain);
    return window.crypto.subtle.digest('SHA-256', data);
}

const base64encode = (input) => {
    return btoa(String.fromCharCode(...new Uint8Array(input)))
        .replace(/=/g, '')
        .replace(/\+/g, '-')
        .replace(/\//g, '_');
}

// Generate PKCE parameters
const codeVerifier = generateRandomString(64);
const hashed = await sha256(codeVerifier);
const codeChallenge = base64encode(hashed);

// Store code verifier for later use
localStorage.setItem('code_verifier', codeVerifier);
```

```javascript
// 2. Request authorization
const clientId = 'your-client-id';
const redirectUri = 'http://localhost:3000/callback';
const scope = 'streaming user-read-email user-read-private';

const authUrl = new URL("https://accounts.spotify.com/authorize");
const params = {
    response_type: 'code',
    client_id: clientId,
    scope: scope,
    code_challenge_method: 'S256',
    code_challenge: codeChallenge,
    redirect_uri: redirectUri,
    state: generateRandomString(16) // Optional but recommended
};

authUrl.search = new URLSearchParams(params).toString();
window.location.href = authUrl.toString();
```

```javascript
// 3. Exchange code for token
const getToken = async (code) => {
    const codeVerifier = localStorage.getItem('code_verifier');

    const payload = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            client_id: clientId,
            grant_type: 'authorization_code',
            code: code,
            redirect_uri: redirectUri,
            code_verifier: codeVerifier,
        }),
    };

    const response = await fetch("https://accounts.spotify.com/api/token", payload);
    const data = await response.json();

    if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        return data.access_token;
    }

    throw new Error('Failed to get access token');
};

// Parse authorization code from callback URL
const urlParams = new URLSearchParams(window.location.search);
const code = urlParams.get('code');
if (code) {
    getToken(code).then(token => {
        console.log('Access token:', token);
        // Initialize Web Playback SDK or make API calls
    });
}
```

### Implicit Grant Flow (Deprecated)

⚠️ **Warning**: The Implicit Grant flow is deprecated and should not be used for new applications. Use PKCE flow instead.

```javascript
// Legacy - DO NOT USE
const authUrl = `https://accounts.spotify.com/authorize?` +
    `client_id=${clientId}&` +
    `response_type=token&` +
    `redirect_uri=${encodeURIComponent(redirectUri)}&` +
    `scope=${encodeURIComponent(scope)}`;
```

### Token Refresh

```javascript
const refreshToken = async () => {
    const refreshToken = localStorage.getItem('refresh_token');

    const payload = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            grant_type: 'refresh_token',
            refresh_token: refreshToken,
            client_id: clientId
        })
    };

    const response = await fetch("https://accounts.spotify.com/api/token", payload);
    const data = await response.json();

    if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
        if (data.refresh_token) {
            localStorage.setItem('refresh_token', data.refresh_token);
        }
        return data.access_token;
    }

    throw new Error('Failed to refresh token');
};
```

---

## Scopes & Permissions

### Core Streaming Scopes

| Scope | Description | Required For |
|-------|-------------|--------------|
| `streaming` | Control playback of Spotify tracks | **Web Playback SDK** |
| `app-remote-control` | Remote control playback of Spotify | **iOS/Android SDKs** |
| `user-read-playback-state` | Read user's player state | Playback information |
| `user-modify-playback-state` | Control user's playback | Playback controls |

### User Data Scopes

| Scope | Description | Use Case |
|-------|-------------|----------|
| `user-read-email` | Read user's email address | User identification |
| `user-read-private` | Read user's subscription details | Premium validation |
| `user-read-currently-playing` | Read currently playing content | Now playing display |
| `user-read-recently-played` | Read recently played tracks | History features |

### Playlist & Library Scopes

| Scope | Description | Use Case |
|-------|-------------|----------|
| `playlist-read-private` | Read private playlists | Playlist browsing |
| `playlist-modify-private` | Modify private playlists | Playlist editing |
| `playlist-modify-public` | Modify public playlists | Public playlist editing |
| `user-library-read` | Read user's saved content | Library browsing |
| `user-library-modify` | Modify user's saved content | Save/unsave tracks |

### Common Scope Combinations

#### Web Playback SDK
```javascript
const scopes = [
    'streaming',
    'user-read-email',
    'user-read-private',
    'user-read-playback-state',
    'user-modify-playback-state'
];
```

#### Mobile SDK (iOS/Android)
```javascript
const scopes = [
    'app-remote-control',
    'user-read-email',
    'user-read-private',
    'user-read-currently-playing',
    'playlist-read-private',
    'user-library-read'
];
```

#### Full-Featured App
```javascript
const scopes = [
    'streaming',                     // Web playback
    'app-remote-control',           // Mobile control
    'user-read-email',              // User info
    'user-read-private',            // Subscription details
    'user-read-playback-state',     // Current playback
    'user-modify-playback-state',   // Playback control
    'user-read-currently-playing',  // Now playing
    'user-read-recently-played',    // Listening history
    'playlist-read-private',        // Private playlists
    'playlist-modify-private',      // Edit private playlists
    'playlist-modify-public',       // Edit public playlists
    'user-library-read',            // Saved content
    'user-library-modify',          // Save/unsave
    'user-top-read',               // Top artists/tracks
    'user-follow-read',            // Following info
    'user-follow-modify'           // Follow/unfollow
];
```

---

## Platform Comparison

| Feature | Web Playback SDK | iOS SDK | Android SDK |
|---------|------------------|---------|-------------|
| **Platform** | Web browsers | iOS 12+ | Android 4.0+ |
| **Streaming** | ✅ Direct | ❌ Via Spotify app | ❌ Via Spotify app |
| **Premium Required** | ✅ Yes | ❌ No | ❌ No |
| **Offline Support** | ❌ No | ✅ Yes | ✅ Yes |
| **Installation Size** | ~100KB | Lightweight | <300KB |
| **Client Secret** | ❌ Not needed | ❌ Not needed | ❌ Not needed |
| **Background Play** | ❌ Tab dependent | ✅ System integration | ✅ System integration |
| **Device Integration** | Limited | ✅ Full | ✅ Full |

### When to Use Each SDK

#### Web Playback SDK
- **Web applications** requiring direct streaming
- **Premium user experiences** with in-browser playback
- **Single-page applications** (SPAs)
- **Desktop web apps** with Electron

#### iOS SDK
- **Native iOS applications**
- **Offline music experiences**
- **Background playback** requirements
- **System-integrated** music apps

#### Android SDK
- **Native Android applications**
- **Lightweight integration** needs
- **Offline support** requirements
- **System audio focus** handling

---

## Implementation Examples

### Complete Web Player with PKCE

```html
<!DOCTYPE html>
<html>
<head>
    <title>Spotify Web Player</title>
</head>
<body>
    <div id="login">
        <button onclick="authenticateUser()">Login with Spotify</button>
    </div>

    <div id="player" style="display:none;">
        <div id="current-track"></div>
        <div id="controls">
            <button onclick="previousTrack()">⏮️</button>
            <button id="play-pause" onclick="togglePlay()">⏸️</button>
            <button onclick="nextTrack()">⏭️</button>
        </div>
        <input type="range" id="volume" min="0" max="100" value="50"
               onchange="setVolume(this.value)">
    </div>

    <script src="https://sdk.scdn.co/spotify-player.js"></script>
    <script>
        const CLIENT_ID = 'your-client-id';
        const REDIRECT_URI = 'http://localhost:3000';
        const SCOPES = 'streaming user-read-email user-read-private user-read-playback-state user-modify-playback-state';

        let player;
        let device_id;

        // PKCE Authentication
        const generateRandomString = (length) => {
            const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            const values = crypto.getRandomValues(new Uint8Array(length));
            return values.reduce((acc, x) => acc + possible[x % possible.length], "");
        }

        const sha256 = async (plain) => {
            const encoder = new TextEncoder();
            const data = encoder.encode(plain);
            return window.crypto.subtle.digest('SHA-256', data);
        }

        const base64encode = (input) => {
            return btoa(String.fromCharCode(...new Uint8Array(input)))
                .replace(/=/g, '')
                .replace(/\+/g, '-')
                .replace(/\//g, '_');
        }

        async function authenticateUser() {
            const codeVerifier = generateRandomString(64);
            const hashed = await sha256(codeVerifier);
            const codeChallenge = base64encode(hashed);

            localStorage.setItem('code_verifier', codeVerifier);

            const authUrl = new URL("https://accounts.spotify.com/authorize");
            const params = {
                response_type: 'code',
                client_id: CLIENT_ID,
                scope: SCOPES,
                code_challenge_method: 'S256',
                code_challenge: codeChallenge,
                redirect_uri: REDIRECT_URI,
            };

            authUrl.search = new URLSearchParams(params).toString();
            window.location.href = authUrl.toString();
        }

        async function getToken(code) {
            const codeVerifier = localStorage.getItem('code_verifier');

            const payload = {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    client_id: CLIENT_ID,
                    grant_type: 'authorization_code',
                    code: code,
                    redirect_uri: REDIRECT_URI,
                    code_verifier: codeVerifier,
                }),
            };

            const response = await fetch("https://accounts.spotify.com/api/token", payload);
            const data = await response.json();

            if (data.access_token) {
                localStorage.setItem('access_token', data.access_token);
                return data.access_token;
            }
            throw new Error('Failed to get token');
        }

        // Initialize Web Playback SDK
        window.onSpotifyWebPlaybackSDKReady = () => {
            const token = localStorage.getItem('access_token');
            if (!token) return;

            player = new Spotify.Player({
                name: 'My Web Player',
                getOAuthToken: cb => { cb(token); },
                volume: 0.5
            });

            player.addListener('ready', ({ device_id: id }) => {
                console.log('Ready with Device ID', id);
                device_id = id;
                document.getElementById('login').style.display = 'none';
                document.getElementById('player').style.display = 'block';
            });

            player.addListener('not_ready', ({ device_id }) => {
                console.log('Device ID has gone offline', device_id);
            });

            player.addListener('player_state_changed', (state) => {
                if (!state) return;

                updateTrackInfo(state.track_window.current_track);
                updatePlayButton(state.paused);
            });

            player.connect();
        };

        function updateTrackInfo(track) {
            document.getElementById('current-track').innerHTML = `
                <img src="${track.album.images[0]?.url}" width="100">
                <div>
                    <h3>${track.name}</h3>
                    <p>${track.artists.map(a => a.name).join(', ')}</p>
                </div>
            `;
        }

        function updatePlayButton(paused) {
            document.getElementById('play-pause').textContent = paused ? '▶️' : '⏸️';
        }

        function togglePlay() {
            player.togglePlay();
        }

        function nextTrack() {
            player.nextTrack();
        }

        function previousTrack() {
            player.previousTrack();
        }

        function setVolume(volume) {
            player.setVolume(volume / 100);
        }

        // Handle callback
        window.addEventListener('DOMContentLoaded', async () => {
            const urlParams = new URLSearchParams(window.location.search);
            const code = urlParams.get('code');

            if (code) {
                try {
                    await getToken(code);
                    window.history.replaceState({}, document.title, "/");
                } catch (error) {
                    console.error('Authentication failed:', error);
                }
            }

            // Check if already authenticated
            const token = localStorage.getItem('access_token');
            if (token && !code) {
                // SDK will auto-initialize
            }
        });
    </script>
</body>
</html>
```

### React Native Spotify Integration

```jsx
// SpotifyModule.js
import {
    authorize,
    refresh,
    revoke
} from 'react-native-app-auth';

const config = {
    issuer: 'https://accounts.spotify.com',
    clientId: 'your-client-id',
    redirectUrl: 'com.yourapp://oauth/callback',
    scopes: [
        'streaming',
        'user-read-email',
        'user-read-private',
        'user-read-playback-state',
        'user-modify-playback-state'
    ],
    additionalParameters: {},
    customHeaders: {}
};

export const SpotifyAuth = {
    async login() {
        try {
            const result = await authorize(config);
            return result.accessToken;
        } catch (error) {
            throw new Error(`Authentication failed: ${error.message}`);
        }
    },

    async refreshToken(refreshToken) {
        try {
            const result = await refresh(config, {
                refreshToken: refreshToken
            });
            return result.accessToken;
        } catch (error) {
            throw new Error(`Token refresh failed: ${error.message}`);
        }
    },

    async logout() {
        await revoke(config, {
            tokenToRevoke: token,
            sendClientId: true
        });
    }
};
```

### SwiftUI iOS Implementation

```swift
// ContentView.swift
import SwiftUI
import SpotifyiOS

struct ContentView: View {
    @StateObject private var spotifyManager = SpotifyManager()
    @State private var isShowingLogin = true

    var body: some View {
        Group {
            if isShowingLogin {
                LoginView(spotifyManager: spotifyManager, isShowingLogin: $isShowingLogin)
            } else {
                PlayerView(spotifyManager: spotifyManager)
            }
        }
        .onOpenURL { url in
            SpotifyiOS.setAccessToken(from: url)
        }
    }
}

struct LoginView: View {
    let spotifyManager: SpotifyManager
    @Binding var isShowingLogin: Bool

    var body: some View {
        VStack {
            Text("Spotify Player")
                .font(.largeTitle)
                .padding()

            Button("Login with Spotify") {
                spotifyManager.authenticate { success in
                    if success {
                        isShowingLogin = false
                    }
                }
            }
            .buttonStyle(.borderedProminent)
        }
    }
}

struct PlayerView: View {
    @ObservedObject var spotifyManager: SpotifyManager

    var body: some View {
        VStack {
            if let track = spotifyManager.currentTrack {
                AsyncImage(url: URL(string: track.imageIdentifier.stringRepresentation)) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                } placeholder: {
                    Rectangle()
                        .fill(Color.gray.opacity(0.3))
                }
                .frame(width: 200, height: 200)
                .cornerRadius(12)

                Text(track.name)
                    .font(.title)
                    .fontWeight(.bold)

                Text(track.artist.name)
                    .font(.title2)
                    .foregroundColor(.secondary)
            }

            HStack(spacing: 40) {
                Button(action: spotifyManager.skipPrevious) {
                    Image(systemName: "backward.fill")
                        .font(.title)
                }

                Button(action: spotifyManager.togglePlayPause) {
                    Image(systemName: spotifyManager.isPlaying ? "pause.fill" : "play.fill")
                        .font(.title)
                }

                Button(action: spotifyManager.skipNext) {
                    Image(systemName: "forward.fill")
                        .font(.title)
                }
            }
            .padding()
        }
        .onAppear {
            spotifyManager.connect()
        }
    }
}

// SpotifyManager.swift
class SpotifyManager: NSObject, ObservableObject {
    private let appRemote = SPTAppRemote.sharedInstance()

    @Published var isConnected = false
    @Published var currentTrack: SPTAppRemoteTrack?
    @Published var isPlaying = false

    func authenticate(completion: @escaping (Bool) -> Void) {
        let scope: SPTScope = [.appRemoteControl, .userReadEmail, .userReadPrivate]

        SpotifyiOS.authorization.authorize(from: UIApplication.shared.windows.first!.rootViewController!, scopes: scope) { result in
            switch result {
            case .success(_):
                completion(true)
            case .failure(_):
                completion(false)
            }
        }
    }

    func connect() {
        guard let accessToken = SpotifyiOS.session?.accessToken else { return }

        appRemote.connectionParameters.accessToken = accessToken
        appRemote.delegate = self
        appRemote.connect()
    }

    func togglePlayPause() {
        if isPlaying {
            appRemote.playerAPI?.pause(nil)
        } else {
            appRemote.playerAPI?.resume(nil)
        }
    }

    func skipNext() {
        appRemote.playerAPI?.skip(toNext: nil)
    }

    func skipPrevious() {
        appRemote.playerAPI?.skip(toPrevious: nil)
    }
}

extension SpotifyManager: SPTAppRemoteDelegate {
    func appRemoteDidEstablishConnection(_ appRemote: SPTAppRemote) {
        isConnected = true

        appRemote.playerAPI?.subscribe(toPlayerState: { _, _ in })
        appRemote.playerAPI?.delegate = self
    }

    func appRemote(_ appRemote: SPTAppRemote, didDisconnectWithError error: Error?) {
        isConnected = false
    }

    func appRemote(_ appRemote: SPTAppRemote, didFailConnectionAttemptWithError error: Error?) {
        isConnected = false
    }
}

extension SpotifyManager: SPTAppRemotePlayerStateDelegate {
    func playerStateDidChange(_ playerState: SPTAppRemotePlayerState) {
        currentTrack = playerState.track
        isPlaying = !playerState.isPaused
    }
}
```

---

## Best Practices

### Security

1. **Never expose client secrets** in client-side code
2. **Use PKCE flow** for all client-side authentication
3. **Implement token refresh** to handle expiration
4. **Store tokens securely** (never in localStorage for production)
5. **Validate token scope** before API calls

```javascript
// Good: Secure token storage (example with secure storage)
const secureStorage = {
    setToken(token) {
        // Use secure storage mechanism
        // For web: consider httpOnly cookies
        // For mobile: use Keychain/Keystore
    },
    getToken() {
        // Retrieve from secure storage
    }
};
```

### Performance

1. **Initialize SDKs only when needed**
2. **Implement connection retry logic**
3. **Handle network failures gracefully**
4. **Cache frequently accessed data**
5. **Debounce user interactions**

```javascript
// Connection retry with exponential backoff
async function connectWithRetry(maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            await player.connect();
            return;
        } catch (error) {
            if (i === maxRetries - 1) throw error;

            const delay = Math.pow(2, i) * 1000; // Exponential backoff
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
}
```

### User Experience

1. **Provide clear loading states**
2. **Handle Premium requirements gracefully**
3. **Implement offline indicators**
4. **Show meaningful error messages**
5. **Maintain playback state across sessions**

```jsx
// React component with proper loading states
function SpotifyPlayer() {
    const [connectionState, setConnectionState] = useState('disconnected'); // disconnected, connecting, connected, error
    const [error, setError] = useState(null);

    const renderConnectionState = () => {
        switch (connectionState) {
            case 'connecting':
                return <div>Connecting to Spotify...</div>;
            case 'connected':
                return <PlayerControls />;
            case 'error':
                return <div>Error: {error}. <button onClick={retry}>Retry</button></div>;
            default:
                return <button onClick={connect}>Connect to Spotify</button>;
        }
    };

    return <div>{renderConnectionState()}</div>;
}
```

### Error Handling

1. **Implement comprehensive error handling**
2. **Provide fallback functionality**
3. **Log errors for debugging**
4. **Show user-friendly error messages**

```javascript
// Comprehensive error handling
class SpotifyService {
    async handlePlayback(action) {
        try {
            await action();
        } catch (error) {
            switch (error.name) {
                case 'SpotifyApi.PremiumRequiredError':
                    this.showPremiumUpgradeDialog();
                    break;
                case 'SpotifyApi.DeviceNotFoundError':
                    this.showDeviceSelectionDialog();
                    break;
                case 'SpotifyApi.RateLimitError':
                    this.handleRateLimit(error.retryAfter);
                    break;
                default:
                    this.showGenericError(error.message);
                    console.error('Spotify error:', error);
            }
        }
    }
}
```

### Cross-Platform Considerations

1. **Feature detection** for platform capabilities
2. **Graceful degradation** when features unavailable
3. **Consistent UI/UX** across platforms
4. **Platform-specific optimizations**

```javascript
// Feature detection and fallback
const SpotifyCapabilities = {
    hasWebPlayback: () => window.Spotify && window.Spotify.Player,
    hasAppRemote: () => /* detect mobile app availability */,

    getOptimalStrategy() {
        if (this.hasWebPlayback()) return 'web-playback';
        if (this.hasAppRemote()) return 'app-remote';
        return 'web-api-only';
    }
};
```

---

## Troubleshooting

### Common Issues

#### Web Playback SDK

**Issue**: Player not initializing
```javascript
// Solution: Check Premium subscription and token scopes
const troubleshootWebPlayback = {
    checkPremium: async (token) => {
        const response = await fetch('https://api.spotify.com/v1/me', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const user = await response.json();
        return user.product === 'premium';
    },

    checkScopes: (token) => {
        // Decode JWT token to check scopes
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.scope.includes('streaming');
    }
};
```

**Issue**: HTTPS requirement
```javascript
// Solution: Ensure HTTPS in production
if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
    console.error('Web Playback SDK requires HTTPS');
    // Redirect to HTTPS or show error
}
```

**Issue**: Cross-origin iframe problems
```html
<!-- Solution: Set proper iframe permissions -->
<iframe src="your-app-url"
        allow="encrypted-media; autoplay">
</iframe>
```

#### iOS SDK

**Issue**: Connection failures
```swift
// Solution: Check app installation and permissions
func troubleshootConnection() {
    // Check if Spotify app is installed
    if UIApplication.shared.canOpenURL(URL(string: "spotify:")!) {
        print("Spotify app is installed")
    } else {
        print("Spotify app not installed - redirect to App Store")
    }

    // Check authentication
    if let session = SpotifyiOS.session {
        print("Authenticated with token: \(session.accessToken)")
    } else {
        print("Not authenticated - need to login")
    }
}
```

#### Android SDK

**Issue**: Build configuration problems
```gradle
// Solution: Ensure proper dependencies and proguard rules
android {
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

// proguard-rules.pro
-keep class com.spotify.** { *; }
-keep interface com.spotify.** { *; }
```

### Debugging Tools

#### Web Console Debugging
```javascript
// Enable SDK debugging
window.localStorage.setItem('spotify-sdk-debug', 'true');

// Monitor player events
player.addListener('ready', (data) => console.log('Ready:', data));
player.addListener('not_ready', (data) => console.log('Not Ready:', data));
player.addListener('player_state_changed', (state) => console.log('State:', state));

// Check connection status
player.getCurrentState().then(state => {
    if (!state) {
        console.log('User is not playing music through the Web Playback SDK');
    } else {
        console.log('Current state:', state);
    }
});
```

#### Network Monitoring
```javascript
// Monitor API requests
const originalFetch = window.fetch;
window.fetch = function(...args) {
    if (args[0].includes('spotify')) {
        console.log('Spotify API call:', args[0]);
    }
    return originalFetch.apply(this, args);
};
```

#### Error Logging Service
```javascript
// Comprehensive error logging
class SpotifyErrorLogger {
    static log(error, context) {
        const errorData = {
            timestamp: new Date().toISOString(),
            error: error.message,
            stack: error.stack,
            context: context,
            userAgent: navigator.userAgent,
            url: window.location.href
        };

        // Send to logging service
        console.error('Spotify Error:', errorData);

        // Optional: Send to external service
        // this.sendToLoggingService(errorData);
    }
}
```

### Performance Monitoring

```javascript
// Track SDK performance
const performanceMonitor = {
    trackConnectionTime: () => {
        const start = performance.now();

        player.addListener('ready', () => {
            const connectionTime = performance.now() - start;
            console.log(`Connection established in ${connectionTime}ms`);
        });
    },

    trackPlaybackLatency: () => {
        const playStart = performance.now();

        player.togglePlay().then(() => {
            const latency = performance.now() - playStart;
            console.log(`Playback command latency: ${latency}ms`);
        });
    }
};
```

---

## Resources & Links

### Official Documentation
- [Web Playback SDK Guide](https://developer.spotify.com/documentation/web-playback-sdk)
- [iOS SDK Documentation](https://developer.spotify.com/documentation/ios)
- [Android SDK Documentation](https://developer.spotify.com/documentation/android)
- [PKCE Authorization Guide](https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow)
- [Scopes Reference](https://developer.spotify.com/documentation/web-api/concepts/scopes)

### Example Projects
- [Web Playback SDK Example](https://github.com/spotify/web-playback-sdk-example)
- [iOS SDK Examples](https://github.com/spotify/ios-sdk)
- [Android SDK Examples](https://github.com/spotify/android-sdk)
- [PKCE Flow Example](https://github.com/spotify/web-api-examples/tree/master/authorization/authorization_code_pkce)

### Community & Support
- [Spotify Developer Community](https://community.spotify.com/t5/Spotify-for-Developers/bd-p/Spotify_Developer)
- [Developer Terms of Service](https://developer.spotify.com/terms)
- [Developer Policy](https://developer.spotify.com/policy)
- [Rate Limiting Guidelines](https://developer.spotify.com/documentation/web-api/concepts/rate-limits)

---

*This documentation covers comprehensive client-side integration with Spotify's ecosystem. For server-side Web API integration, refer to our [Spotify API Documentation](SPOTIFY-API-DOCUMENTATION.md).*
