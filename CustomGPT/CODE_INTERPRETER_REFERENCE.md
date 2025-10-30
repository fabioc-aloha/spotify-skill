# Code Interpreter Reference Guide

## Overview

This document contains **ready-to-use Python code** for common Spotify API operations and data processing tasks. Alex DJ has Code Interpreter capabilities and can execute these patterns on-the-fly to solve user problems.

**Philosophy**: Code first, explain after. If a task involves data transformation, file processing, or analysis, write Python code immediately rather than explaining limitations.

### CRITICAL: Python vs API Separation

**⚠️ Code Interpreter CANNOT make authenticated API calls to Spotify.**

The Python environment is isolated and does NOT have access to your OAuth tokens or the ability to call Spotify APIs directly.

**Correct Workflow:**
1. **YOU (GPT)** make authenticated API calls to Spotify
2. **Python** processes the returned data (filter, transform, analyze)
3. **YOU (GPT)** use processed results to make follow-up API calls

**Example - Audio Feature Filtering:**
```
Step 1: GPT calls search API → gets 50 tracks
Step 2: GPT calls getMultipleAudioFeatures API → gets audio data
Step 3: Python filters where energy > 0.7 and tempo > 120 BPM
Step 4: GPT calls addTracksToPlaylist API → adds filtered tracks
```

**Python is for DATA PROCESSING, not API communication.**

---

## Table of Contents

1. [Image Processing](#image-processing)
2. [Batch Operations](#batch-operations)
3. [Audio Feature Analysis](#audio-feature-analysis)
4. [Playlist Analytics](#playlist-analytics)
5. [Data Export](#data-export)
6. [Smart Filtering](#smart-filtering)
7. [Deduplication](#deduplication)
8. [Data Visualization](#data-visualization)
9. [Utility Functions](#utility-functions)

---

## Image Processing

### Convert Any Image to Spotify Cover Art

Converts PNG, WebP, or other formats to square JPEG, optimized for Spotify's requirements (640x640px min, max 256KB, base64 encoded).

```python
from PIL import Image
import base64
import io

def convert_to_spotify_cover(image_path, size=640, max_size_kb=256):
    """
    Convert any image to Spotify-compatible cover art.

    Args:
        image_path: Path to input image (any format)
        size: Target dimensions (square, default 640x640)
        max_size_kb: Maximum file size in KB (default 256)

    Returns:
        tuple: (base64_string, file_size_kb)
    """
    # Open and convert to RGB (JPEG doesn't support transparency)
    img = Image.open(image_path).convert('RGB')

    # Make square by cropping to center
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    img_square = img.crop((left, top, left + min_dim, top + min_dim))

    # Resize to target dimensions
    img_resized = img_square.resize((size, size), Image.Resampling.LANCZOS)

    # Compress to JPEG under max_size_kb
    quality = 95
    while quality >= 50:
        buffer = io.BytesIO()
        img_resized.save(buffer, format='JPEG', quality=quality, optimize=True)
        size_kb = buffer.tell() / 1024

        if size_kb <= max_size_kb:
            break
        quality -= 5

    # Encode to base64 WITHOUT data URI prefix
    buffer.seek(0)
    b64_string = base64.b64encode(buffer.read()).decode('utf-8')

    print(f"✓ Converted to {size}x{size} JPEG ({size_kb:.1f} KB, quality={quality})")

    return b64_string, size_kb

# Usage
base64_image, file_size = convert_to_spotify_cover('user_uploaded.png')
# Now call uploadPlaylistCoverImage with base64_image
```

### Batch Convert Multiple Images

```python
import os
from pathlib import Path

def batch_convert_images(image_folder, output_folder='converted'):
    """Convert all images in a folder to Spotify-compatible cover art"""
    Path(output_folder).mkdir(exist_ok=True)

    results = []
    for img_file in Path(image_folder).glob('*'):
        if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp', '.gif']:
            try:
                b64_img, size_kb = convert_to_spotify_cover(str(img_file))
                output_path = Path(output_folder) / f"{img_file.stem}_spotify.jpg"

                # Save as JPEG for preview
                img = Image.open(img_file).convert('RGB')
                img.thumbnail((640, 640))
                img.save(output_path, 'JPEG', quality=90)

                results.append({
                    'original': img_file.name,
                    'size_kb': size_kb,
                    'base64': b64_img[:50] + '...',  # Preview
                    'success': True
                })
            except Exception as e:
                results.append({
                    'original': img_file.name,
                    'error': str(e),
                    'success': False
                })

    return results
```

---

## Batch Operations

### Chunk Tracks for API Limits

Split large arrays into batches of 100 for API requests.

```python
def chunk_items(items, chunk_size=100):
    """
    Split items into chunks for batch API requests.

    Args:
        items: List of track IDs, URIs, or any items
        chunk_size: Maximum items per chunk (default 100)

    Returns:
        list: List of chunked sublists
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

# Usage
track_ids = [...]  # 500 track IDs
batches = chunk_items(track_ids, 100)
print(f"Split {len(track_ids)} tracks into {len(batches)} batches")

for i, batch in enumerate(batches, 1):
    print(f"Processing batch {i}/{len(batches)} ({len(batch)} tracks)")
    # Call addTracksToPlaylist with this batch
```

### Convert Track IDs to URIs

```python
def build_track_uris(track_ids):
    """
    Convert track IDs to Spotify URI format.

    Args:
        track_ids: List of track IDs (strings)

    Returns:
        list: List of Spotify URIs (spotify:track:{id})
    """
    return [f"spotify:track:{tid}" for tid in track_ids]

# Usage
track_ids = ['4iV5W9uYEdYUVa79Axb7Rh', '1301WleyT98MSxVHPZCA6M']
uris = build_track_uris(track_ids)
# Now use with addTracksToPlaylist
```

### Extract Track IDs from API Response

```python
def extract_track_ids(api_response, response_type='search'):
    """
    Extract track IDs from various API response types.

    Args:
        api_response: API response dict
        response_type: 'search', 'playlist', 'saved_tracks', 'top_tracks'

    Returns:
        list: Track IDs
    """
    track_ids = []

    if response_type == 'search':
        # Search response: tracks.items[].id
        tracks = api_response.get('tracks', {}).get('items', [])
        track_ids = [t['id'] for t in tracks if t]

    elif response_type == 'playlist':
        # Playlist response: tracks.items[].track.id
        items = api_response.get('tracks', {}).get('items', [])
        track_ids = [item['track']['id'] for item in items if item.get('track')]

    elif response_type == 'saved_tracks':
        # User saved tracks: items[].track.id
        items = api_response.get('items', [])
        track_ids = [item['track']['id'] for item in items if item.get('track')]

    elif response_type == 'top_tracks':
        # Top tracks: items[].id
        items = api_response.get('items', [])
        track_ids = [t['id'] for t in items if t]

    return track_ids

# Usage
search_results = search(q="rock", type="track", limit=50)
track_ids = extract_track_ids(search_results, 'search')
```

### Paginate Through All Results

```python
def fetch_all_items(api_call_func, **kwargs):
    """
    Fetch all items from a paginated API endpoint.

    Args:
        api_call_func: API function to call (e.g., getCurrentUserPlaylists)
        **kwargs: Additional arguments for the API call

    Returns:
        list: All items from all pages
    """
    all_items = []
    offset = 0
    limit = kwargs.get('limit', 20)

    while True:
        response = api_call_func(offset=offset, limit=limit, **kwargs)
        items = response.get('items', [])
        all_items.extend(items)

        # Check if more pages exist
        if response.get('next') is None or len(items) == 0:
            break

        offset += limit
        print(f"Fetched {len(all_items)} items so far...")

    print(f"✓ Total: {len(all_items)} items")
    return all_items

# Usage
all_playlists = fetch_all_items(getCurrentUserPlaylists, limit=50)
all_saved_tracks = fetch_all_items(getUserSavedTracks, limit=50)
```

---

## Audio Feature Analysis

### Fetch and Analyze Audio Features

```python
import pandas as pd

def fetch_audio_features_batch(track_ids):
    """
    Fetch audio features for up to 100 tracks at once.

    Args:
        track_ids: List of track IDs (max 100)

    Returns:
        DataFrame: Audio features with track IDs
    """
    # Join IDs with commas
    ids_str = ','.join(track_ids[:100])

    # Call API
    response = getMultipleAudioFeatures(ids=ids_str)
    features = response.get('audio_features', [])

    # Convert to DataFrame
    df = pd.DataFrame(features)

    return df

def analyze_audio_features(audio_features_df):
    """
    Analyze audio features and generate statistics.

    Args:
        audio_features_df: DataFrame from fetch_audio_features_batch

    Returns:
        dict: Statistics and insights
    """
    # Remove null entries
    df = audio_features_df.dropna()

    stats = {
        'track_count': len(df),
        'avg_energy': df['energy'].mean(),
        'avg_valence': df['valence'].mean(),
        'avg_danceability': df['danceability'].mean(),
        'avg_tempo': df['tempo'].mean(),
        'energy_range': (df['energy'].min(), df['energy'].max()),
        'tempo_range': (df['tempo'].min(), df['tempo'].max()),
        'valence_range': (df['valence'].min(), df['valence'].max()),
        'high_energy_count': (df['energy'] > 0.7).sum(),
        'low_energy_count': (df['energy'] < 0.4).sum(),
        'happy_count': (df['valence'] > 0.7).sum(),
        'sad_count': (df['valence'] < 0.4).sum(),
        'instrumental_count': (df['instrumentalness'] > 0.5).sum()
    }

    return stats, df

# Usage
track_ids = extract_track_ids(playlist_response, 'playlist')
features_df = fetch_audio_features_batch(track_ids)
stats, df = analyze_audio_features(features_df)

print(f"📊 Audio Analysis:")
print(f"   Average Energy: {stats['avg_energy']:.2f}")
print(f"   Average Tempo: {stats['avg_tempo']:.0f} BPM")
print(f"   Average Mood: {stats['avg_valence']:.2f} (0=sad, 1=happy)")
print(f"   High Energy Tracks: {stats['high_energy_count']}/{stats['track_count']}")
```

### Filter Tracks by Audio Features

```python
def filter_by_audio_features(tracks, audio_features_df, criteria):
    """
    Filter tracks based on audio feature criteria.

    Args:
        tracks: List of track objects from API
        audio_features_df: DataFrame with audio features
        criteria: Dict with feature ranges, e.g.:
                  {'energy': (0.7, 1.0), 'tempo': (120, 140)}

    Returns:
        list: Filtered tracks with scores
    """
    filtered = []

    for i, (track, features) in enumerate(zip(tracks, audio_features_df.to_dict('records'))):
        if not features or pd.isna(features.get('energy')):
            continue

        # Check all criteria
        matches = True
        for feature, (min_val, max_val) in criteria.items():
            value = features.get(feature, 0)
            if not (min_val <= value <= max_val):
                matches = False
                break

        if matches:
            # Calculate composite score
            score = (
                features.get('energy', 0) * 0.4 +
                features.get('valence', 0) * 0.3 +
                features.get('danceability', 0) * 0.3
            )

            filtered.append({
                'track': track,
                'features': features,
                'score': score
            })

    # Sort by score
    filtered.sort(key=lambda x: x['score'], reverse=True)

    return filtered

# Usage
criteria = {
    'energy': (0.75, 1.0),
    'tempo': (120, 140),
    'danceability': (0.6, 1.0),
    'valence': (0.5, 1.0)
}

filtered_tracks = filter_by_audio_features(tracks, features_df, criteria)
print(f"Found {len(filtered_tracks)} tracks matching criteria")

# Get top 30 for playlist
top_30_ids = [t['track']['id'] for t in filtered_tracks[:30]]
```

---

## Playlist Analytics

### Calculate Comprehensive Playlist Statistics

```python
from collections import Counter
from datetime import datetime

def analyze_playlist_comprehensive(playlist_data):
    """
    Generate comprehensive statistics about a playlist.

    Args:
        playlist_data: Full playlist response from getPlaylist

    Returns:
        dict: Detailed statistics
    """
    tracks = playlist_data['tracks']['items']

    # Basic metrics
    total_duration_ms = sum(t['track']['duration_ms'] for t in tracks if t.get('track'))
    hours = total_duration_ms // 3600000
    minutes = (total_duration_ms % 3600000) // 60000

    # Artist analysis
    all_artists = []
    for t in tracks:
        if t.get('track'):
            all_artists.extend([a['name'] for a in t['track']['artists']])
    artist_counts = Counter(all_artists)

    # Album analysis
    albums = [t['track']['album']['name'] for t in tracks if t.get('track')]
    album_counts = Counter(albums)

    # Decade analysis
    decades = []
    for t in tracks:
        if not t.get('track'):
            continue
        year_str = t['track']['album']['release_date']
        if year_str and len(year_str) >= 4:
            year = int(year_str[:4])
            decade = (year // 10) * 10
            decades.append(f"{decade}s")
    decade_counts = Counter(decades)

    # Explicit content
    explicit_count = sum(1 for t in tracks if t.get('track') and t['track']['explicit'])

    # Popularity
    popularities = [t['track']['popularity'] for t in tracks if t.get('track')]
    avg_popularity = sum(popularities) / len(popularities) if popularities else 0

    # Track length analysis
    durations_min = [t['track']['duration_ms'] / 60000 for t in tracks if t.get('track')]
    avg_duration = sum(durations_min) / len(durations_min) if durations_min else 0

    stats = {
        'name': playlist_data['name'],
        'total_tracks': len(tracks),
        'total_duration': f"{hours}h {minutes}m",
        'total_duration_ms': total_duration_ms,
        'avg_track_length': f"{avg_duration:.1f} min",
        'longest_track': max(durations_min) if durations_min else 0,
        'shortest_track': min(durations_min) if durations_min else 0,
        'unique_artists': len(artist_counts),
        'unique_albums': len(album_counts),
        'top_10_artists': artist_counts.most_common(10),
        'decade_distribution': dict(decade_counts.most_common()),
        'explicit_tracks': explicit_count,
        'explicit_percentage': f"{explicit_count / len(tracks) * 100:.1f}%",
        'avg_popularity': f"{avg_popularity:.1f}/100",
        'high_popularity': sum(1 for p in popularities if p >= 70),
        'low_popularity': sum(1 for p in popularities if p < 30)
    }

    return stats

# Usage
playlist = getPlaylist(playlist_id)
stats = analyze_playlist_comprehensive(playlist)

print(f"📊 Playlist: {stats['name']}")
print(f"   {stats['total_tracks']} tracks • {stats['total_duration']}")
print(f"   {stats['unique_artists']} artists • {stats['unique_albums']} albums")
print(f"   Top artist: {stats['top_10_artists'][0][0]} ({stats['top_10_artists'][0][1]} tracks)")
print(f"   Avg popularity: {stats['avg_popularity']}")
print(f"   Explicit: {stats['explicit_percentage']}")
```

### Compare Two Playlists

```python
def compare_playlists(playlist1_data, playlist2_data):
    """
    Compare two playlists and find similarities/differences.

    Args:
        playlist1_data, playlist2_data: Playlist responses from getPlaylist

    Returns:
        dict: Comparison statistics
    """
    # Extract track IDs
    tracks1 = set(t['track']['id'] for t in playlist1_data['tracks']['items'] if t.get('track'))
    tracks2 = set(t['track']['id'] for t in playlist2_data['tracks']['items'] if t.get('track'))

    # Extract artists
    artists1 = set()
    artists2 = set()
    for t in playlist1_data['tracks']['items']:
        if t.get('track'):
            artists1.update(a['name'] for a in t['track']['artists'])
    for t in playlist2_data['tracks']['items']:
        if t.get('track'):
            artists2.update(a['name'] for a in t['track']['artists'])

    comparison = {
        'playlist1_name': playlist1_data['name'],
        'playlist2_name': playlist2_data['name'],
        'shared_tracks': len(tracks1 & tracks2),
        'unique_to_playlist1': len(tracks1 - tracks2),
        'unique_to_playlist2': len(tracks2 - tracks1),
        'total_unique_tracks': len(tracks1 | tracks2),
        'track_overlap_pct': len(tracks1 & tracks2) / len(tracks1 | tracks2) * 100 if tracks1 | tracks2 else 0,
        'shared_artists': len(artists1 & artists2),
        'unique_artists_1': len(artists1 - artists2),
        'unique_artists_2': len(artists2 - artists1),
        'artist_overlap_pct': len(artists1 & artists2) / len(artists1 | artists2) * 100 if artists1 | artists2 else 0
    }

    return comparison

# Usage
playlist1 = getPlaylist(playlist_id_1)
playlist2 = getPlaylist(playlist_id_2)
comp = compare_playlists(playlist1, playlist2)

print(f"Comparing: {comp['playlist1_name']} vs {comp['playlist2_name']}")
print(f"   Shared tracks: {comp['shared_tracks']}")
print(f"   Track overlap: {comp['track_overlap_pct']:.1f}%")
print(f"   Shared artists: {comp['shared_artists']}")
print(f"   Artist overlap: {comp['artist_overlap_pct']:.1f}%")
```

---

## Data Export

### Export Playlist to CSV

```python
import pandas as pd
from datetime import datetime

def export_playlist_to_csv(playlist_data, filename=None, include_audio_features=False):
    """
    Export playlist to CSV with full metadata.

    Args:
        playlist_data: Playlist response from getPlaylist
        filename: Output filename (auto-generated if None)
        include_audio_features: Fetch and include audio features (slower)

    Returns:
        str: Filename of exported CSV
    """
    tracks_data = []

    for item in playlist_data['tracks']['items']:
        if not item.get('track'):
            continue

        track = item['track']
        track_data = {
            'Track Name': track['name'],
            'Artists': ', '.join([a['name'] for a in track['artists']]),
            'Album': track['album']['name'],
            'Release Date': track['album']['release_date'],
            'Duration (min)': round(track['duration_ms'] / 60000, 2),
            'Popularity': track['popularity'],
            'Explicit': 'Yes' if track['explicit'] else 'No',
            'Track ID': track['id'],
            'Spotify URI': track['uri'],
            'Added At': item.get('added_at', '')
        }

        tracks_data.append(track_data)

    df = pd.DataFrame(tracks_data)

    # Optionally fetch audio features
    if include_audio_features and len(tracks_data) > 0:
        track_ids = [t['Track ID'] for t in tracks_data]
        features_df = fetch_audio_features_batch(track_ids)

        # Add audio features columns
        df['Energy'] = features_df['energy'].round(2)
        df['Valence'] = features_df['valence'].round(2)
        df['Danceability'] = features_df['danceability'].round(2)
        df['Tempo (BPM)'] = features_df['tempo'].round(0)

    # Generate filename
    if filename is None:
        safe_name = playlist_data['name'].replace(' ', '_').replace('/', '_')
        filename = f"{safe_name}_{datetime.now():%Y%m%d}.csv"

    df.to_csv(filename, index=False, encoding='utf-8')

    print(f"✓ Exported {len(tracks_data)} tracks to {filename}")

    return filename

# Usage
playlist = getPlaylist(playlist_id)
csv_file = export_playlist_to_csv(playlist, include_audio_features=True)
```

### Export Multiple Playlists

```python
def export_all_playlists(output_folder='playlist_exports'):
    """Export all user playlists to individual CSV files"""
    import os
    os.makedirs(output_folder, exist_ok=True)

    # Fetch all playlists
    all_playlists = fetch_all_items(getCurrentUserPlaylists, limit=50)

    exported = []
    for playlist in all_playlists:
        try:
            # Get full playlist with tracks
            full_playlist = getPlaylist(playlist['id'])

            # Export to CSV
            filename = os.path.join(
                output_folder,
                f"{full_playlist['name'].replace(' ', '_')}.csv"
            )
            export_playlist_to_csv(full_playlist, filename)

            exported.append({
                'name': full_playlist['name'],
                'tracks': full_playlist['tracks']['total'],
                'file': filename
            })
        except Exception as e:
            print(f"Error exporting {playlist['name']}: {e}")

    print(f"\n✓ Exported {len(exported)} playlists to {output_folder}/")
    return exported
```

---

## Smart Filtering

### Multi-Criteria Filter Engine

```python
def advanced_filter(tracks, audio_features_df, criteria):
    """
    Advanced filtering with multiple criteria types.

    Args:
        tracks: List of track objects
        audio_features_df: DataFrame with audio features
        criteria: Dict with various filter types:
            {
                'audio': {'energy': (0.7, 1.0), 'tempo': (120, 140)},
                'popularity': (50, 100),
                'year': (2010, 2020),
                'explicit': False,
                'duration_max_min': 10
            }

    Returns:
        list: Filtered tracks with metadata
    """
    filtered = []

    for track, features in zip(tracks, audio_features_df.to_dict('records')):
        if not features:
            continue

        # Audio feature criteria
        if 'audio' in criteria:
            audio_match = True
            for feature, (min_val, max_val) in criteria['audio'].items():
                value = features.get(feature, 0)
                if not (min_val <= value <= max_val):
                    audio_match = False
                    break
            if not audio_match:
                continue

        # Popularity criteria
        if 'popularity' in criteria:
            min_pop, max_pop = criteria['popularity']
            if not (min_pop <= track['popularity'] <= max_pop):
                continue

        # Year criteria
        if 'year' in criteria:
            year_str = track['album']['release_date']
            if year_str and len(year_str) >= 4:
                year = int(year_str[:4])
                min_year, max_year = criteria['year']
                if not (min_year <= year <= max_year):
                    continue

        # Explicit criteria
        if 'explicit' in criteria:
            if track['explicit'] != criteria['explicit']:
                continue

        # Duration criteria (in minutes)
        if 'duration_max_min' in criteria:
            duration_min = track['duration_ms'] / 60000
            if duration_min > criteria['duration_max_min']:
                continue

        # Calculate composite score
        score = (
            features.get('energy', 0.5) * 0.3 +
            features.get('valence', 0.5) * 0.25 +
            features.get('danceability', 0.5) * 0.25 +
            (track['popularity'] / 100) * 0.2
        )

        filtered.append({
            'track': track,
            'features': features,
            'score': score
        })

    # Sort by score
    filtered.sort(key=lambda x: x['score'], reverse=True)

    return filtered

# Usage Example: High-energy workout tracks from 2015-2020
criteria = {
    'audio': {
        'energy': (0.75, 1.0),
        'tempo': (120, 150),
        'danceability': (0.6, 1.0)
    },
    'popularity': (40, 100),  # Not too obscure
    'year': (2015, 2020),
    'explicit': False,  # Clean versions only
    'duration_max_min': 6  # No epic songs
}

filtered = advanced_filter(tracks, features_df, criteria)
print(f"Found {len(filtered)} tracks matching all criteria")
```

---

## Deduplication

### Find Duplicates in Single Playlist

```python
def find_duplicates_in_playlist(playlist_data):
    """
    Find duplicate tracks within a single playlist.

    Args:
        playlist_data: Playlist response from getPlaylist

    Returns:
        dict: Duplicate information
    """
    from collections import defaultdict

    track_positions = defaultdict(list)

    # Build index of track positions
    for idx, item in enumerate(playlist_data['tracks']['items']):
        if not item.get('track'):
            continue
        track_id = item['track']['id']
        track_positions[track_id].append({
            'position': idx,
            'name': item['track']['name'],
            'artists': ', '.join([a['name'] for a in item['track']['artists']]),
            'uri': item['track']['uri']
        })

    # Find duplicates (tracks appearing more than once)
    duplicates = {
        track_id: positions
        for track_id, positions in track_positions.items()
        if len(positions) > 1
    }

    # Generate report
    report = {
        'total_tracks': len(playlist_data['tracks']['items']),
        'unique_tracks': len(track_positions),
        'duplicate_count': len(duplicates),
        'total_duplicate_instances': sum(len(positions) for positions in duplicates.values()),
        'duplicates': []
    }

    for track_id, positions in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
        report['duplicates'].append({
            'track_name': positions[0]['name'],
            'artists': positions[0]['artists'],
            'occurrences': len(positions),
            'positions': [p['position'] for p in positions],
            'uris': [p['uri'] for p in positions]
        })

    return report

# Usage
playlist = getPlaylist(playlist_id)
dup_report = find_duplicates_in_playlist(playlist)

print(f"🔍 Duplicate Analysis:")
print(f"   Total tracks: {dup_report['total_tracks']}")
print(f"   Unique tracks: {dup_report['unique_tracks']}")
print(f"   Duplicates found: {dup_report['duplicate_count']}")
print(f"   Duplicate instances: {dup_report['total_duplicate_instances']}")

if dup_report['duplicates']:
    print(f"\n   Top duplicates:")
    for dup in dup_report['duplicates'][:5]:
        print(f"   • {dup['track_name']} - {dup['artists']} ({dup['occurrences']} times)")
```

### Find Duplicates Across Multiple Playlists

```python
def find_duplicates_across_playlists(playlist_ids):
    """
    Find tracks that appear in multiple playlists.

    Args:
        playlist_ids: List of playlist IDs to check

    Returns:
        dict: Cross-playlist duplicate report
    """
    from collections import defaultdict

    track_locations = defaultdict(list)

    # Fetch all playlists and index tracks
    for playlist_id in playlist_ids:
        playlist = getPlaylist(playlist_id)
        playlist_name = playlist['name']

        for item in playlist['tracks']['items']:
            if not item.get('track'):
                continue

            track = item['track']
            track_locations[track['id']].append({
                'playlist_id': playlist_id,
                'playlist_name': playlist_name,
                'track_name': track['name'],
                'artists': ', '.join([a['name'] for a in track['artists']])
            })

    # Find tracks in multiple playlists
    cross_duplicates = {
        track_id: locations
        for track_id, locations in track_locations.items()
        if len(locations) > 1
    }

    # Generate report
    report = {
        'playlists_checked': len(playlist_ids),
        'cross_playlist_duplicates': len(cross_duplicates),
        'duplicates': []
    }

    for track_id, locations in sorted(cross_duplicates.items(),
                                     key=lambda x: len(x[1]),
                                     reverse=True):
        report['duplicates'].append({
            'track_name': locations[0]['track_name'],
            'artists': locations[0]['artists'],
            'appears_in': len(locations),
            'playlists': [loc['playlist_name'] for loc in locations]
        })

    return report

# Usage
my_playlists = getCurrentUserPlaylists(limit=50)
workout_playlists = [p['id'] for p in my_playlists['items'] if 'workout' in p['name'].lower()]

cross_dup_report = find_duplicates_across_playlists(workout_playlists)

print(f"🔍 Cross-Playlist Duplicate Analysis:")
print(f"   Checked {cross_dup_report['playlists_checked']} playlists")
print(f"   Found {cross_dup_report['cross_playlist_duplicates']} tracks in multiple playlists")

for dup in cross_dup_report['duplicates'][:10]:
    print(f"   • {dup['track_name']} appears in {dup['appears_in']} playlists:")
    print(f"     {', '.join(dup['playlists'])}")
```

---

## Data Visualization

### Visualize Energy Flow

```python
import matplotlib.pyplot as plt
import numpy as np

def visualize_energy_flow(audio_features_df, playlist_name="Playlist"):
    """
    Create visualization of energy progression through playlist.

    Args:
        audio_features_df: DataFrame with audio features
        playlist_name: Name for chart title

    Returns:
        str: Filename of saved chart
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Audio Analysis: {playlist_name}', fontsize=16, fontweight='bold')

    # Energy flow over time
    axes[0, 0].plot(audio_features_df.index, audio_features_df['energy'],
                    marker='o', linewidth=2, markersize=4, color='#1DB954')
    axes[0, 0].set_title('Energy Flow', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Track Position')
    axes[0, 0].set_ylabel('Energy (0-1)')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axhline(y=0.5, color='red', linestyle='--', alpha=0.3, label='Midpoint')

    # Tempo distribution
    axes[0, 1].hist(audio_features_df['tempo'], bins=25, edgecolor='black',
                    color='#1DB954', alpha=0.7)
    axes[0, 1].set_title('Tempo Distribution', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('BPM')
    axes[0, 1].set_ylabel('Count')
    axes[0, 1].grid(True, alpha=0.3, axis='y')

    # Energy vs Valence scatter
    axes[1, 0].scatter(audio_features_df['energy'], audio_features_df['valence'],
                       alpha=0.6, s=100, c=audio_features_df['danceability'],
                       cmap='viridis', edgecolors='black', linewidth=0.5)
    axes[1, 0].set_title('Energy vs Mood (color = danceability)',
                         fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Energy')
    axes[1, 0].set_ylabel('Valence (Positivity)')
    axes[1, 0].grid(True, alpha=0.3)
    cbar = plt.colorbar(axes[1, 0].collections[0], ax=axes[1, 0])
    cbar.set_label('Danceability')

    # Feature summary radar/box plot
    features_summary = audio_features_df[['energy', 'valence', 'danceability',
                                           'acousticness', 'instrumentalness']].describe()
    axes[1, 1].boxplot([audio_features_df[col] for col in features_summary.columns],
                       labels=['Energy', 'Valence', 'Dance', 'Acoustic', 'Instrument'])
    axes[1, 1].set_title('Feature Distributions', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('Value (0-1)')
    axes[1, 1].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    filename = f"{playlist_name.replace(' ', '_')}_analysis.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ Saved visualization: {filename}")

    return filename

# Usage
track_ids = extract_track_ids(playlist_response, 'playlist')
features_df = fetch_audio_features_batch(track_ids)
chart_file = visualize_energy_flow(features_df, playlist_response['name'])
```

### Create Playlist Comparison Chart

```python
def visualize_playlist_comparison(playlists_data):
    """
    Compare multiple playlists visually.

    Args:
        playlists_data: List of tuples (playlist_name, audio_features_df)

    Returns:
        str: Filename of saved chart
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Playlist Comparison', fontsize=16, fontweight='bold')

    colors = plt.cm.Set3(np.linspace(0, 1, len(playlists_data)))

    # Energy comparison
    for idx, (name, df) in enumerate(playlists_data):
        axes[0, 0].plot(df['energy'], label=name, color=colors[idx], alpha=0.7)
    axes[0, 0].set_title('Energy Flow Comparison')
    axes[0, 0].set_xlabel('Track Position')
    axes[0, 0].set_ylabel('Energy')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Average feature comparison
    feature_names = ['Energy', 'Valence', 'Dance', 'Tempo\n(normalized)']
    x_pos = np.arange(len(feature_names))
    width = 0.8 / len(playlists_data)

    for idx, (name, df) in enumerate(playlists_data):
        avg_features = [
            df['energy'].mean(),
            df['valence'].mean(),
            df['danceability'].mean(),
            df['tempo'].mean() / 200  # Normalize tempo
        ]
        axes[0, 1].bar(x_pos + (idx * width), avg_features, width,
                       label=name, color=colors[idx], alpha=0.7)

    axes[0, 1].set_title('Average Features')
    axes[0, 1].set_xticks(x_pos + width * (len(playlists_data) - 1) / 2)
    axes[0, 1].set_xticklabels(feature_names)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3, axis='y')

    # Tempo distribution comparison
    for idx, (name, df) in enumerate(playlists_data):
        axes[1, 0].hist(df['tempo'], bins=20, alpha=0.5, label=name,
                        color=colors[idx], edgecolor='black')
    axes[1, 0].set_title('Tempo Distribution')
    axes[1, 0].set_xlabel('BPM')
    axes[1, 0].set_ylabel('Count')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3, axis='y')

    # Summary stats table
    axes[1, 1].axis('off')
    table_data = []
    for name, df in playlists_data:
        table_data.append([
            name,
            f"{len(df)}",
            f"{df['energy'].mean():.2f}",
            f"{df['valence'].mean():.2f}",
            f"{df['tempo'].mean():.0f}"
        ])

    table = axes[1, 1].table(cellText=table_data,
                            colLabels=['Playlist', 'Tracks', 'Avg Energy',
                                      'Avg Mood', 'Avg BPM'],
                            loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)

    plt.tight_layout()

    filename = "playlist_comparison.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ Saved comparison chart: {filename}")

    return filename
```

---

## Utility Functions

### Spotify URI Converters

```python
def id_to_uri(item_id, item_type='track'):
    """Convert Spotify ID to URI format"""
    return f"spotify:{item_type}:{item_id}"

def uri_to_id(uri):
    """Extract ID from Spotify URI"""
    return uri.split(':')[-1]

def uris_to_remove_format(uris):
    """Convert URIs to removal format for removeTracksFromPlaylist"""
    return [{'uri': uri} for uri in uris]

# Usage
track_uris = [id_to_uri(tid) for tid in track_ids]
removal_objects = uris_to_remove_format(track_uris)
```

### Duration Formatting

```python
def format_duration(ms):
    """Convert milliseconds to readable duration"""
    seconds = ms // 1000
    minutes = seconds // 60
    hours = minutes // 60

    if hours > 0:
        return f"{hours}h {minutes % 60}m"
    elif minutes > 0:
        return f"{minutes}m {seconds % 60}s"
    else:
        return f"{seconds}s"

def total_playlist_duration(playlist_data):
    """Calculate total duration of playlist"""
    total_ms = sum(
        item['track']['duration_ms']
        for item in playlist_data['tracks']['items']
        if item.get('track')
    )
    return format_duration(total_ms)

# Usage
print(f"Playlist duration: {total_playlist_duration(playlist)}")
```

### Safe API Caller with Retry

```python
import time

def safe_api_call(api_func, max_retries=3, retry_delay=1, **kwargs):
    """
    Call API with automatic retry on failure.

    Args:
        api_func: API function to call
        max_retries: Maximum retry attempts
        retry_delay: Seconds to wait between retries
        **kwargs: Arguments for the API function

    Returns:
        API response or None on failure
    """
    for attempt in range(max_retries):
        try:
            response = api_func(**kwargs)
            return response
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
            else:
                print(f"Failed after {max_retries} attempts")
                return None

# Usage
playlist = safe_api_call(getPlaylist, playlist_id=my_playlist_id, max_retries=3)
```

### Progress Tracker for Large Operations

```python
def process_with_progress(items, process_func, batch_size=100, description="Processing"):
    """
    Process items in batches with progress updates.

    Args:
        items: List of items to process
        process_func: Function to call for each batch
        batch_size: Items per batch
        description: Description for progress messages

    Returns:
        list: Results from each batch
    """
    batches = chunk_items(items, batch_size)
    results = []
    total_batches = len(batches)

    print(f"{description}: {len(items)} items in {total_batches} batches")

    for i, batch in enumerate(batches, 1):
        print(f"  Batch {i}/{total_batches} ({len(batch)} items)...", end='')

        try:
            result = process_func(batch)
            results.append(result)
            print(" ✓")
        except Exception as e:
            print(f" ✗ Error: {e}")
            results.append(None)

        # Small delay to avoid rate limiting
        if i < total_batches:
            time.sleep(0.5)

    successful = sum(1 for r in results if r is not None)
    print(f"✓ Completed: {successful}/{total_batches} batches successful")

    return results

# Usage
def add_batch(track_uris):
    return addTracksToPlaylist(playlist_id, uris=track_uris)

results = process_with_progress(all_track_uris, add_batch, batch_size=100,
                                description="Adding tracks")
```

---

## Quick Reference: Common Patterns

### Pattern 1: Search → Filter → Create Playlist

```python
# 1. Search for tracks
search_results = search(q="electronic workout", type="track", limit=50)
track_ids = extract_track_ids(search_results, 'search')

# 2. Get audio features
features_df = fetch_audio_features_batch(track_ids)

# 3. Filter by criteria
criteria = {'energy': (0.75, 1.0), 'tempo': (125, 140)}
filtered = filter_by_audio_features(search_results['tracks']['items'],
                                    features_df, criteria)

# 4. Create playlist
new_playlist = createPlaylist(name="⚡ High-Energy Workout", public=False)
track_uris = build_track_uris([t['track']['id'] for t in filtered[:30]])

# 5. Add tracks
addTracksToPlaylist(new_playlist['id'], uris=track_uris)
```

### Pattern 2: Analyze → Visualize → Export

```python
# 1. Get playlist
playlist = getPlaylist(playlist_id)

# 2. Analyze
stats = analyze_playlist_comprehensive(playlist)
track_ids = extract_track_ids(playlist, 'playlist')
features_df = fetch_audio_features_batch(track_ids)

# 3. Visualize
chart_file = visualize_energy_flow(features_df, playlist['name'])

# 4. Export
csv_file = export_playlist_to_csv(playlist, include_audio_features=True)

print(f"Analysis complete: {chart_file}, {csv_file}")
```

### Pattern 3: Deduplicate Playlist

```python
# 1. Get playlist
playlist = getPlaylist(playlist_id)

# 2. Find duplicates
dup_report = find_duplicates_in_playlist(playlist)

# 3. Build removal list (keep first occurrence)
tracks_to_remove = []
for dup in dup_report['duplicates']:
    # Remove all but first occurrence
    tracks_to_remove.extend(dup['uris'][1:])

# 4. Remove in batches
if tracks_to_remove:
    removal_objects = uris_to_remove_format(tracks_to_remove)
    batches = chunk_items(removal_objects, 100)

    for batch in batches:
        removeTracksFromPlaylist(playlist_id, tracks=batch)

    print(f"✓ Removed {len(tracks_to_remove)} duplicate instances")
```

---

## Remember

**You have Python code execution.** Use it liberally:

1. **Don't explain limitations** → Write code to solve the problem
2. **Don't ask users to do manual work** → Automate it
3. **Process first, explain after** → Execute, then present results
4. **Leverage pandas, matplotlib, PIL** → Full Python ecosystem available
5. **Handle errors gracefully** → Try/except with fallbacks
6. **Show results, not code** → Users want outcomes, not tutorials

**Think like a developer. Act like an assistant. Deliver like magic.**

---

*Last Updated: October 30, 2025*
*Version: 1.0*
