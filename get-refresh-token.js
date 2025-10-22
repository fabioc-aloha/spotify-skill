#!/usr/bin/env node
/**
 * Spotify Refresh Token Generator
 * 
 * This script helps you get a Spotify refresh token for local development.
 * It uses the same OAuth flow as the MCP tool.
 */

import 'dotenv/config';
import SpotifyWebApi from 'spotify-web-api-node';
import express from 'express';

const CLIENT_ID = process.env.SPOTIFY_CLIENT_ID;
const CLIENT_SECRET = process.env.SPOTIFY_CLIENT_SECRET;
const REDIRECT_URI = 'http://127.0.0.1:8888/callback';

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error('❌ Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET in .env file');
  process.exit(1);
}

const spotifyApi = new SpotifyWebApi({
  clientId: CLIENT_ID,
  clientSecret: CLIENT_SECRET,
  redirectUri: REDIRECT_URI,
});

const scopes = [
  'user-read-playback-state',
  'user-modify-playback-state',
  'user-read-currently-playing',
  'playlist-read-private',
  'playlist-read-collaborative',
  'playlist-modify-public',
  'playlist-modify-private',
  'user-library-read',
  'user-top-read',
];

const app = express();

// Add a root route for testing
app.get('/', (req, res) => {
  res.send(`
    <h1>🎵 Spotify Refresh Token Generator</h1>
    <p>Server is running! This means the callback endpoint is working.</p>
    <h2>Next steps:</h2>
    <ol>
      <li>Make sure your Spotify app redirect URI is set to: <code>http://127.0.0.1:8888/callback</code></li>
      <li>Visit the authorization URL from the terminal</li>
      <li>Authorize the app</li>
      <li>You should be redirected back here with a code</li>
    </ol>
    <p><strong>Authorization URL:</strong><br>
    <a href="${spotifyApi.createAuthorizeURL(scopes)}" target="_blank">Click here to authorize</a></p>
  `);
});

console.log('🎵 Spotify Refresh Token Generator');
console.log('==================================');
console.log('');

// Step 1: Show authorization URL
const authorizeURL = spotifyApi.createAuthorizeURL(scopes);
console.log('📋 STEP 1: Visit this URL in your browser to authorize the app:');
console.log('');
console.log(authorizeURL);
console.log('');
console.log('📋 STEP 2: After authorization, you will be redirected to http://127.0.0.1:8888/callback');
console.log('📋 STEP 3: This script will automatically capture the code and exchange it for tokens');
console.log('');

// Step 2: Handle the callback
app.get('/callback', async (req, res) => {
  const code = req.query.code;
  const error = req.query.error;
  
  console.log('📥 Callback received:');
  console.log('   URL:', req.url);
  console.log('   Query params:', req.query);
  console.log('   Authorization code:', code ? '✅ Present' : '❌ Missing');
  console.log('   Error:', error || 'None');

  if (error) {
    console.error('❌ Authorization failed:', error);
    res.send(`
      <h1>❌ Authorization Failed</h1>
      <p>Error: ${error}</p>
      <p>You can close this window and try again.</p>
      <h3>Common solutions:</h3>
      <ul>
        <li>Make sure you clicked "Agree" on the authorization page</li>
        <li>Check that the redirect URI in your Spotify app matches exactly: <code>http://127.0.0.1:8888/callback</code></li>
        <li>Try running the script again</li>
      </ul>
    `);
    setTimeout(() => process.exit(1), 5000);
    return;
  }

  if (!code) {
    console.error('❌ No authorization code received');
    console.log('');
    console.log('🔧 TROUBLESHOOTING:');
    console.log('1. Make sure your Spotify app redirect URI is exactly: http://127.0.0.1:8888/callback');
    console.log('2. Go to https://developer.spotify.com/dashboard');
    console.log('3. Select your app > Edit Settings > Redirect URIs');
    console.log('4. Add or update to: http://127.0.0.1:8888/callback');
    console.log('5. Save and try again');
    console.log('');
    
    res.send(`
      <h1>❌ No Authorization Code</h1>
      <p>The authorization process didn't complete properly.</p>
      <h3>Please check your Spotify app settings:</h3>
      <ol>
        <li>Go to <a href="https://developer.spotify.com/dashboard" target="_blank">Spotify Developer Dashboard</a></li>
        <li>Select your app</li>
        <li>Click "Edit Settings"</li>
        <li>Under "Redirect URIs", make sure you have exactly: <code>http://127.0.0.1:8888/callback</code></li>
        <li>Save the settings</li>
        <li>Run this script again: <code>npm run get-token</code></li>
      </ol>
      <p>Current request details:</p>
      <pre>URL: ${req.url}
Query params: ${JSON.stringify(req.query, null, 2)}</pre>
    `);
    setTimeout(() => process.exit(1), 10000);
    return;
  }

  try {
    console.log('✅ Authorization code received! Exchanging for tokens...');
    
    const data = await spotifyApi.authorizationCodeGrant(code);
    const accessToken = data.body.access_token;
    const refreshToken = data.body.refresh_token;
    const expiresIn = data.body.expires_in;

    console.log('');
    console.log('🎉 SUCCESS! Here are your tokens:');
    console.log('=====================================');
    console.log('');
    console.log('🔑 Access Token:', accessToken);
    console.log('♻️  Refresh Token:', refreshToken);
    console.log('⏰ Expires In:', expiresIn, 'seconds');
    console.log('');
    console.log('📝 NEXT STEPS:');
    console.log('1. Copy the refresh token above');
    console.log('2. Add it to your .env file:');
    console.log(`   SPOTIFY_REFRESH_TOKEN=${refreshToken}`);
    console.log('3. Restart your server: npm start');
    console.log('4. All Spotify tools will now work!');
    console.log('');

    res.send(`
      <h1>🎉 Success!</h1>
      <h2>Your Spotify Refresh Token:</h2>
      <p style="background: #f0f0f0; padding: 10px; font-family: monospace; word-break: break-all;">
        ${refreshToken}
      </p>
      <h3>Next Steps:</h3>
      <ol>
        <li>Copy the refresh token above</li>
        <li>Add it to your .env file as: <code>SPOTIFY_REFRESH_TOKEN=${refreshToken}</code></li>
        <li>Restart your server: <code>npm start</code></li>
        <li>All Spotify tools will now work!</li>
      </ol>
      <p>You can close this window now.</p>
    `);

    // Auto-shutdown after showing results
    setTimeout(() => {
      console.log('🔄 Shutting down server...');
      process.exit(0);
    }, 2000);

  } catch (error) {
    console.error('❌ Failed to exchange authorization code:', error.message);
    
    let helpText = 'Make sure the authorization code is valid and hasn\'t been used already.';
    if (error.message.includes('invalid_grant')) {
      helpText = 'The authorization code has expired or been used already. Please get a new code by visiting the authorization URL again.';
    } else if (error.message.includes('invalid_client')) {
      helpText = 'Invalid client credentials. Please check your Client ID and Client Secret in .env file.';
    }

    res.send(`
      <h1>❌ Error</h1>
      <p>Failed to exchange authorization code: ${error.message}</p>
      <p>${helpText}</p>
      <p>You can close this window and try again.</p>
    `);
    
    setTimeout(() => process.exit(1), 2000);
  }
});

// Start the server
const server = app.listen(8888, '127.0.0.1', () => {
  console.log('🌐 Server running on http://127.0.0.1:8888');
  console.log('🔄 Waiting for authorization...');
  console.log('');
  console.log('💡 TIP: If nothing happens after clicking "Agree", check if the browser');
  console.log('    redirected you to 127.0.0.1:8888. The page might load slowly.');
  console.log('');
});

// Handle process termination
process.on('SIGINT', () => {
  console.log('\n\n🛑 Process interrupted. Shutting down...');
  server.close();
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n\n🛑 Process terminated. Shutting down...');
  server.close();
  process.exit(0);
});
