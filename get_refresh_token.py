#!/usr/bin/env python3
"""
Spotify Refresh Token Generator (Python)

This script helps you get a Spotify refresh token for local development.
It uses OAuth 2.0 Authorization Code Flow.

Usage:
    python get_refresh_token.py
"""

import os
import sys
import webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, urlencode
import json

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / 'spotify-api' / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        # Try loading from current directory
        load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Using system environment variables.")

# Add the spotify-api/scripts directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'spotify-api' / 'scripts'))

try:
    from spotify_client import SpotifyClient
except ImportError:
    print("❌ Could not import spotify_client. Make sure you're running from the project root.")
    sys.exit(1)


# Configuration
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://127.0.0.1:8888/callback'

# Scopes needed for the Spotify API skill
SCOPES = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'playlist-read-private',
    'playlist-read-collaborative',
    'playlist-modify-public',
    'playlist-modify-private',
    'user-library-read',
    'user-library-modify',
    'user-top-read',
    'user-read-private',
    'user-read-email',
    'ugc-image-upload',  # Required for cover art upload!
]

# Global variable to store the authorization code
auth_code = None
auth_error = None


class SpotifyCallbackHandler(BaseHTTPRequestHandler):
    """HTTP request handler for OAuth callback."""
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def do_GET(self):
        """Handle GET requests."""
        global auth_code, auth_error
        
        # Parse the URL
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            # Root page - show instructions
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            auth_url = client.get_authorization_url(scope=SCOPES)
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Spotify Refresh Token Generator</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                    h1 {{ color: #1DB954; }}
                    code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
                    .button {{ display: inline-block; padding: 10px 20px; background: #1DB954; 
                              color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
                    .button:hover {{ background: #1ed760; }}
                </style>
            </head>
            <body>
                <h1>🎵 Spotify Refresh Token Generator</h1>
                <p>Server is running! This means the callback endpoint is working.</p>
                
                <h2>Next steps:</h2>
                <ol>
                    <li>Make sure your Spotify app redirect URI is set to: <code>{REDIRECT_URI}</code></li>
                    <li>Click the button below to authorize the app</li>
                    <li>Authorize the app in the Spotify page</li>
                    <li>You'll be redirected back here with your token</li>
                </ol>
                
                <a href="{auth_url}" class="button">🔐 Authorize with Spotify</a>
                
                <h3>Or copy this URL:</h3>
                <p style="word-break: break-all; background: #f4f4f4; padding: 10px; border-radius: 5px;">
                    {auth_url}
                </p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif parsed_path.path == '/callback':
            # OAuth callback
            params = parse_qs(parsed_path.query)
            
            print('📥 Callback received:')
            print(f'   URL: {self.path}')
            print(f'   Query params: {params}')
            
            if 'error' in params:
                auth_error = params['error'][0]
                print(f'❌ Authorization failed: {auth_error}')
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Authorization Failed</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        h1 {{ color: #e22134; }}
                    </style>
                </head>
                <body>
                    <h1>❌ Authorization Failed</h1>
                    <p>Error: {auth_error}</p>
                    <p>You can close this window and try again.</p>
                    
                    <h3>Common solutions:</h3>
                    <ul>
                        <li>Make sure you clicked "Agree" on the authorization page</li>
                        <li>Check that the redirect URI in your Spotify app matches exactly: <code>{REDIRECT_URI}</code></li>
                        <li>Try running the script again</li>
                    </ul>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
                return
            
            if 'code' not in params:
                print('❌ No authorization code received')
                print('')
                print('🔧 TROUBLESHOOTING:')
                print(f'1. Make sure your Spotify app redirect URI is exactly: {REDIRECT_URI}')
                print('2. Go to https://developer.spotify.com/dashboard')
                print('3. Select your app > Edit Settings > Redirect URIs')
                print(f'4. Add or update to: {REDIRECT_URI}')
                print('5. Save and try again')
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>No Authorization Code</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        h1 {{ color: #e22134; }}
                        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
                    </style>
                </head>
                <body>
                    <h1>❌ No Authorization Code</h1>
                    <p>The authorization process didn't complete properly.</p>
                    
                    <h3>Please check your Spotify app settings:</h3>
                    <ol>
                        <li>Go to <a href="https://developer.spotify.com/dashboard" target="_blank">Spotify Developer Dashboard</a></li>
                        <li>Select your app</li>
                        <li>Click "Edit Settings"</li>
                        <li>Under "Redirect URIs", make sure you have exactly: <code>{REDIRECT_URI}</code></li>
                        <li>Save the settings</li>
                        <li>Run this script again: <code>python get_refresh_token.py</code></li>
                    </ol>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
                return
            
            # Got the authorization code!
            auth_code = params['code'][0]
            print(f'✅ Authorization code received: {auth_code[:20]}...')
            
            try:
                print('🔄 Exchanging authorization code for tokens...')
                
                # Exchange code for tokens
                token_data = client.get_access_token(auth_code)
                
                access_token = token_data.get('access_token')
                refresh_token = token_data.get('refresh_token')
                expires_in = token_data.get('expires_in')
                
                print('')
                print('🎉 SUCCESS! Here are your tokens:')
                print('=' * 60)
                print('')
                print(f'🔑 Access Token:  {access_token}')
                print(f'♻️  Refresh Token: {refresh_token}')
                print(f'⏰ Expires In:    {expires_in} seconds')
                print('')
                print('📝 NEXT STEPS:')
                print('1. Copy the refresh token above')
                print('2. Add it to your spotify-api/.env file:')
                print(f'   SPOTIFY_REFRESH_TOKEN={refresh_token}')
                print('3. Test with: python spotify-api/scripts/test_credentials.py')
                print('4. All Spotify API functions will now work!')
                print('')
                
                # Send success page
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Success!</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        h1 {{ color: #1DB954; }}
                        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; 
                               font-family: 'Courier New', monospace; }}
                        .token {{ background: #f4f4f4; padding: 15px; border-radius: 5px; 
                                 word-break: break-all; font-family: 'Courier New', monospace; 
                                 margin: 10px 0; }}
                        .copy-btn {{ padding: 5px 10px; background: #1DB954; color: white; 
                                     border: none; border-radius: 3px; cursor: pointer; margin-left: 10px; }}
                        .copy-btn:hover {{ background: #1ed760; }}
                    </style>
                    <script>
                        function copyToken() {{
                            const token = document.getElementById('refresh-token').textContent;
                            navigator.clipboard.writeText(token).then(() => {{
                                alert('Refresh token copied to clipboard!');
                            }});
                        }}
                    </script>
                </head>
                <body>
                    <h1>🎉 Success!</h1>
                    
                    <h2>Your Spotify Refresh Token:</h2>
                    <div class="token" id="refresh-token">{refresh_token}</div>
                    <button class="copy-btn" onclick="copyToken()">📋 Copy Token</button>
                    
                    <h3>Next Steps:</h3>
                    <ol>
                        <li>Copy the refresh token above</li>
                        <li>Open <code>spotify-api/.env</code> file</li>
                        <li>Update or add: <code>SPOTIFY_REFRESH_TOKEN={refresh_token}</code></li>
                        <li>Test with: <code>python spotify-api/scripts/test_credentials.py</code></li>
                        <li>All Spotify API functions will now work!</li>
                    </ol>
                    
                    <p><strong>You can close this window now.</strong></p>
                    <p style="color: #666; font-size: 0.9em;">The server will shut down automatically in 3 seconds...</p>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
                
            except Exception as e:
                print(f'❌ Failed to exchange authorization code: {e}')
                
                help_text = 'Make sure the authorization code is valid and hasn\'t been used already.'
                error_msg = str(e)
                
                if 'invalid_grant' in error_msg.lower():
                    help_text = 'The authorization code has expired or been used already. Please get a new code by visiting the authorization URL again.'
                elif 'invalid_client' in error_msg.lower():
                    help_text = 'Invalid client credentials. Please check your Client ID and Client Secret in .env file.'
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Error</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        h1 {{ color: #e22134; }}
                    </style>
                </head>
                <body>
                    <h1>❌ Error</h1>
                    <p>Failed to exchange authorization code: {error_msg}</p>
                    <p>{help_text}</p>
                    <p>You can close this window and try again.</p>
                </body>
                </html>
                """
                self.wfile.write(html.encode())


def main():
    """Main function to run the OAuth flow."""
    global client
    
    print('=' * 60)
    print('🎵 Spotify Refresh Token Generator (Python)')
    print('=' * 60)
    print('')
    
    # Validate credentials
    if not CLIENT_ID or not CLIENT_SECRET:
        print('❌ Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET')
        print('')
        print('Please make sure you have a .env file in spotify-api/ with:')
        print('  SPOTIFY_CLIENT_ID=your_client_id')
        print('  SPOTIFY_CLIENT_SECRET=your_client_secret')
        print('')
        print('Get these from: https://developer.spotify.com/dashboard')
        sys.exit(1)
    
    print(f'✅ Client ID found: {CLIENT_ID[:15]}...')
    print(f'✅ Client Secret found: {CLIENT_SECRET[:15]}...')
    print('')
    
    # Initialize Spotify client
    client = SpotifyClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI
    )
    
    # Get authorization URL
    auth_url = client.get_authorization_url(scope=SCOPES)
    
    print('📋 STEP 1: Authorization URL generated')
    print('')
    print('📝 SCOPES REQUESTED:')
    print('   - Playlist management (create, modify, read)')
    print('   - User library access (saved tracks, albums)')
    print('   - Playback control')
    print('   - User profile and top items')
    print('   - 🎨 ugc-image-upload (for cover art generation!)')
    print('')
    print('🌐 Opening your browser to authorize the app...')
    print('   If the browser doesn\'t open, visit this URL manually:')
    print('')
    print(f'   {auth_url}')
    print('')
    
    # Start HTTP server
    server = HTTPServer(('127.0.0.1', 8888), SpotifyCallbackHandler)
    
    print('🌐 Server running on http://127.0.0.1:8888')
    print('🔄 Waiting for authorization...')
    print('')
    print('💡 TIP: After authorizing on Spotify, you\'ll be redirected back here.')
    print('   If nothing happens, check if the redirect URI in your Spotify app')
    print('   settings matches: http://127.0.0.1:8888/callback')
    print('')
    
    # Open browser
    try:
        webbrowser.open(auth_url)
    except:
        print('⚠️  Could not open browser automatically. Please visit the URL above manually.')
    
    # Handle requests until we get the token
    try:
        while auth_code is None and auth_error is None:
            server.handle_request()
        
        # Give time to display the success page
        if auth_code:
            import time
            time.sleep(3)
            print('🔄 Shutting down server...')
            print('✅ Done! Your refresh token is ready to use.')
        
    except KeyboardInterrupt:
        print('\n\n🛑 Process interrupted. Shutting down...')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
