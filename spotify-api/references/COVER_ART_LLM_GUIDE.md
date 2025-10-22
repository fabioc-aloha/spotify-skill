# Spotify Playlist Cover Art Generator - LLM Execution Guide

## ⚠️ CRITICAL: Output Format Limitation

**The cover art is generated as SVG and immediately converted to PNG (static image) for Spotify upload.**

- ✅ **SVG features that work**: Gradients, colors, text, shapes, patterns
- ❌ **SVG features that DON'T work**: Animations (`<animate>`, `<animateTransform>`) - these are lost in PNG conversion
- 📊 **Final format**: Static PNG image (640x640 pixels)

**DO NOT use SVG animations** - they will not be visible in the final uploaded cover art.

---

## Overview

This guide enables you to create professional Spotify playlist cover art **by analyzing the playlist's actual content** (tracks, artists, genres) to determine appropriate colors, styles, and mood. You are self-contained and don't need external theme lists or color presets.

### Core Principle: Content-Driven Design

**You will determine colors and style by:**
1. Analyzing the playlist's tracks and artists using the Spotify API
2. Extracting genre, mood, and energy from the actual music
3. Applying color psychology based on the content analysis
4. Creating unique, contextually appropriate designs

This makes you truly autonomous - able to handle any playlist without needing predefined themes.

---
## Quick Reference: Complete Workflow Examples

### Example 1: High-Energy Workout Playlist

**User Request:** "Create cover art for my playlist '7i9dQZF1DXaXB8fQg7xif'"

```python
# Step 1: Get Playlist Content
playlist = client.get_playlist("7i9dQZF1DXaXB8fQg7xif")
playlist_name = playlist['name']  # "Beast Mode Gym"
tracks = playlist['tracks']['items']
artists = ["Metallica", "Rage Against the Machine", "Linkin Park"]

# Step 2: Analyze Content
# Detected: High-energy rock/metal, Energy: 9/10, Mood: Aggressive/Intense

# Step 3: Determine Colors
gradient_start = "#E63946"  # Intense red (rock/metal + high energy)
gradient_end = "#1D1D1D"    # Almost black (metal aesthetic)
text_color = "#FFFFFF"      # Maximum contrast

# Step 4: Generate
from scripts.cover_art_generator import CoverArtGenerator
generator = CoverArtGenerator(client)

png = generator.generate_cover_art(
    title="BEAST MODE GYM",
    gradient_start="#E63946",
    gradient_end="#1D1D1D",
    text_color="#FFFFFF",
    size=640
)

# Step 5: Upload
generator.upload_cover_image(playlist_id, png)
```

**Result:** Bold red-to-black gradient with large white text, perfect for gym visibility ✓

---

### Example 2: Chill Ambient Playlist

**User Request:** "Songs for getting sleepy"

```python
# Analysis: Genre=ambient, Energy: 2/10, Mood: Calm/Relaxing

# Colors (from Step 2 color psychology)
gradient_start = "#4ECDC4"  # Cool teal (chill, calming)
gradient_end = "#556FB5"    # Soft blue (peaceful)
text_color = "#FFFFFF"      # Clean contrast

# Generate
png = generator.generate_cover_art(
    title="SONGS FOR GETTING SLEEPY",
    gradient_start="#4ECDC4",
    gradient_end="#556FB5",
    text_color="#FFFFFF",
    size=640
)
```

**Result:** Soothing blue gradient with clear white text ✓

---

### Example 3: Vague Request Handling

**User Request:** "My Favorite Songs"

**Your Response:**
```
"I'd love to create cover art for your playlist! To make it perfect, could you tell me:
- What genres of music are included? (rock, pop, hip-hop, electronic, etc.)
- What's the vibe or mood? (energetic, chill, nostalgic, romantic, etc.)
- Any particular era or style you're going for? (modern, 80s, vintage, etc.)
This will help me choose the right colors, fonts, and design elements."
```

**After user responds:** "It's mostly indie rock and alternative from the 2000s, pretty chill and nostalgic vibe"

```python
# Analysis: Genre=indie/alternative, Era=2000s, Energy: 5/10, Mood: Nostalgic/Chill

# Colors (warm, vintage feel for nostalgia)
gradient_start = "#D4A574"  # Vintage gold
gradient_end = "#6B4423"    # Warm brown
text_color = "#F5F5DC"      # Cream (softer than white)

png = generator.generate_cover_art(
    title="MY FAVORITE SONGS",
    gradient_start="#D4A574",
    gradient_end="#6B4423",
    text_color="#F5F5DC",
    size=640
)
```

**Result:** Warm vintage aesthetic matching 2000s indie nostalgia ✓

---

## Step-by-Step Execution Process

### Step 1: Analyze Playlist Content

**FIRST: Get the actual playlist data**

```python
from scripts.spotify_client import SpotifyClient

client = SpotifyClient(access_token="...")

# Get playlist details and tracks
playlist_info = client.get_playlist(playlist_id)
playlist_name = playlist_info['name']
tracks = playlist_info['tracks']['items']

# Extract key information
artists = [track['track']['artists'][0]['name'] for track in tracks if track['track']]
track_names = [track['track']['name'] for track in tracks if track['track']]
```

**ANALYZE THE CONTENT:**
- **Genres**: What genres do these artists represent?
- **Era/Time Period**: What decades are these tracks from?
- **Energy Level**: Are these high-energy or calm tracks?
- **Mood**: Aggressive, romantic, melancholic, upbeat?
- **Common Themes**: Workout, sleep, party, focus, nostalgia?

**EXTRACT KEY CHARACTERISTICS:**
```
Based on playlist content:
- Primary Genre: [determined from artists/tracks]
- Energy Level: [1-10 scale based on track analysis]
- Dominant Mood: [extracted from track names, artists, genres]
- Era/Style: [determined from artist eras]
- Keywords: [2-3 most important words from playlist name]
```

**HANDLING VAGUE PLAYLIST NAMES:**

If the playlist name is generic (e.g., "My Favorite Songs", "My Playlist", "Good Music"), use the content analysis to understand the theme, then ASK clarifying questions:

```
"I analyzed your playlist and see it contains [genres/artists].
What vibe should the cover art convey? (energetic, chill, nostalgic, etc.)"
```

**Vague Request Indicators:**
- Generic terms: "My Favorite Songs", "My Playlist", "Good Music"
- No genre indicators: "Sunday Vibes", "Mood Music", "The Mix"
- Personal/subjective only: "Songs I Love", "Best Ever", "My Jams"
- Single ambiguous words: "Vibes", "Feels", "Energy"

**Required Clarifying Questions (ask ALL that apply):**
```
IF playlist_name_is_vague AND insufficient_context THEN
    ASK: "What genre(s) of music are in this playlist? (rock, pop, electronic, etc.)"
    ASK: "What's the mood or context? (workout, relaxation, party, study, etc.)"
    ASK: "Any specific era or style? (80s, modern, vintage, etc.)"
    WAIT: for_user_response
    THEN: proceed_with_analysis
```

---
### Step 2: Determine Colors from Content Analysis

**USE COLOR PSYCHOLOGY based on your Step 1 analysis:**

#### Energy Level Mapping:
- **High Energy (8-10)**: Bright, saturated colors
  - Examples: Bright red (#E63946), electric orange (#FF6B35), hot pink (#FF6B9D)
- **Medium Energy (4-7)**: Balanced, clear colors
  - Examples: Deep blue (#0369A1), vibrant purple (#8B5DFF), teal (#4ECDC4)
- **Low Energy (1-3)**: Muted, soft colors
  - Examples: Soft blue (#A8D8FF), pale green (#B2DFDB), light gray (#E8E8E8)

#### Genre-to-Color Mapping:

Use these associations when you detect genres from the playlist:

| Genre Detected | Color Scheme (gradient_start, gradient_end, text_color) |
|----------------|--------------------------------------------------------|
| Rock/Metal     | Intense red + Black (#E63946, #1D1D1D, #FFFFFF)       |
| Electronic/EDM | Neon colors (#00FFF0, #8B5DFF, #FFFFFF)               |
| Hip-Hop/Rap    | Purple + Gold (#6A4C93, #FFD93D, #FFFFFF)              |
| Jazz/Blues     | Brown + Cream (#6B4423, #F5F5DC, #2C2C2C)             |
| Classical      | Gold + Navy (#D4A574, #2C3E50, #F5F5DC)               |
| Pop            | Pink + Yellow (#FF6B9D, #FFD93D, #FFFFFF)              |
| Country        | Earth tones (#D4A574, #8B4513, #F5F5DC)               |
| Reggae         | Green + Yellow (#90BE6D, #FFD93D, #1A1A1A)            |
| Indie/Alt      | Muted pastels (#B2DFDB, #E8B4B8, #2C3E50)             |
| Ambient/Chill  | Cool blues (#4ECDC4, #556FB5, #FFFFFF)                |

#### Mood-to-Color Mapping:

| Mood Detected   | Color Temperature | Saturation | Example Scheme            |
|----------------|-------------------|------------|---------------------------|
| Aggressive     | Warm              | High       | Red + Black               |
| Calm/Peaceful  | Cool              | Low        | Soft blue + Light purple  |
| Happy/Upbeat   | Warm              | High       | Yellow + Orange           |
| Melancholic    | Cool              | Low        | Gray + Deep blue          |
| Romantic       | Warm              | Medium     | Pink + Rose               |
| Nostalgic      | Warm              | Low        | Sepia + Vintage gold      |
| Energetic      | Warm/Bright       | High       | Orange + Red              |
| Focus/Study    | Cool              | Low        | Light blue + White        |

#### Color Psychology Reference:

**Color Temperature:**
- **Warm** (energetic, passionate): Reds, oranges, yellows
- **Cool** (calm, focused): Blues, teals, purples
- **Neutral** (balanced): Grays, beige, muted tones

**Saturation:**
- **High saturation**: Energetic, bold, attention-grabbing
- **Medium saturation**: Balanced, professional
- **Low saturation**: Calm, sophisticated, subtle

**Contrast:**
- **High contrast**: Dramatic, easier to read (rock, workout, party)
- **Low contrast**: Softer, more subtle (ambient, classical, sleep)

**Common Color Meanings:**
- **Red**: Energy, passion, intensity, aggression
- **Orange**: Enthusiasm, creativity, warmth
- **Yellow**: Happiness, optimism, attention
- **Green**: Nature, calm, growth, balance
- **Blue**: Trust, calm, focus, professionalism
- **Purple**: Creativity, luxury, electronic/synthetic
- **Pink**: Romance, softness, pop music
- **Brown**: Earth, vintage, acoustic, organic
- **Black**: Power, sophistication, mystery
- **White**: Clean, minimal, modern, space

#### SYNTHESIZE YOUR COLOR SCHEME:

1. Determine primary mood from playlist content
2. Select base colors from genre/mood mappings
3. Adjust saturation based on energy level
4. Ensure high contrast for text readability (minimum 4.5:1 ratio)

**Example Analysis:**
```
Playlist: "Ultimate Workout Mix"
Content Analysis:
- Artists: Eminem, Metallica, Linkin Park, Rage Against the Machine
- Genres Detected: Rock, Metal, Hip-Hop
- Energy Level: 9/10 (very high energy)
- Mood: Aggressive, Intense, Motivational

Color Decision:
gradient_start = "#E63946"  # Intense red (high energy, aggressive)
gradient_end = "#1D1D1D"    # Almost black (metal/rock aesthetic)
text_color = "#FFFFFF"      # Maximum contrast

Reasoning: High-energy rock/metal requires bold, aggressive colors
with maximum contrast for workout/gym visibility.
```

#### Multi-Genre Playlists:

For playlists with mixed genres, blend color schemes:

```python
# Example: Playlist with Electronic (60%) + Chill (40%) tracks
# Electronic = bright neon colors
# Chill = cool, muted tones
# Blend = Teal to Purple gradient

gradient_start = "#4ECDC4"  # Cool teal (chill influence)
gradient_end = "#8B5DFF"    # Electric purple (electronic influence)
text_color = "#FFFFFF"      # Clean contrast
```

#### Era-Specific Colors:

If tracks are primarily from specific eras:

**80s/90s Detected:**
- Neon colors (cyan, magenta, yellow)
- High saturation
- Example: "#00FFF0" to "#FF00FF"

**Modern/Contemporary:**
- Clean, simple gradients
- Muted or monochrome
- Example: "#F5F5F5" to "#2C2C2C"

**Classic/Vintage (pre-1980):**
- Warm, faded tones
- Lower saturation
- Example: "#D4A574" to "#6B4423"

---

### Step 3: Typography Rules (CRITICAL - NON-NEGOTIABLE)

#### Font Sizes for Thumbnail Readability:
1. **Primary word**: 70-90px (LARGE)
2. **Secondary word**: 60-80px
3. **Supporting words**: 40-60px
4. **NEVER** use fonts smaller than 40px

#### Text Wrapping (for long titles):

Long playlist names must wrap properly to maintain readability. The `cover_art_generator.py` script includes automatic text wrapping:

```python
# Automatic text wrapping at word boundaries
def wrap_text(text, max_chars=20):
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + len(current_line) > max_chars:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)

    if current_line:
        lines.append(' '.join(current_line))
    return lines
```

**Text Wrapping Strategy:**
- **Max characters per line**: 20 (for readability)
- **Break at word boundaries**: Never split words
- **Line height**: 110% of font size (font_size * 1.1)
- **Example**: "My Ultimate Workout Power Hour" → ["My Ultimate Workout", "Power Hour"]

#### Text Layout:
- Text occupies **80% of canvas width**
- Line height: **110%** of font size (font_size * 1.1)
- Vertical spacing: **20px between elements**
- Center alignment (both horizontal and vertical)

#### Font Weight:
- Titles: **Bold** (weight: 700-900)
- Subtitles: **Semi-bold** (weight: 600)

#### Edge Cases:

**Very Long Titles (>25 characters):**

**Strategy 1: Multi-line wrapping** (primary method)
```python
title_lines = wrap_text("My Ultimate Workout Power Hour", max_chars=20)
# Result: ["My Ultimate Workout", "Power Hour"]
```

**Strategy 2: Abbreviate common words** (if still too long)
```python
title = title.replace("The ", "").replace(" and ", " & ")
# "The Best Songs and More" → "Best Songs & More"
```

**Strategy 3: Focus on keywords** (last resort)
```python
# "My Favorite Classic Rock Songs" → "CLASSIC ROCK"
keywords = extract_keywords(title)
```

**Special Characters:**
- **Emojis**: Replace with text or remove (e.g., "🎵 Music" → "Music")
- **Symbols** (&, @, #): Keep if part of title, encode properly for SVG
- **Non-English**: Ensure font supports character set

---
### Step 4: Generate the Cover Art

**EXECUTE THIS CODE:**

```python
from scripts.cover_art_generator import CoverArtGenerator
from scripts.spotify_client import SpotifyClient

# Initialize
client = SpotifyClient(access_token="...")
generator = CoverArtGenerator(client)

# Generate with colors determined from Step 2
png_path = generator.generate_cover_art(
    title="Workout Power",  # From playlist name
    subtitle="",  # Optional
    gradient_start="#E63946",  # Determined from Step 2
    gradient_end="#1D1D1D",    # Determined from Step 2
    text_color="#FFFFFF",      # High contrast
    output_path="workout_cover.png",
    size=640  # Spotify recommended
)

print(f"✓ Cover art created: {png_path}")

# Upload to playlist
success = generator.upload_cover_image(
    playlist_id="37i9dQZF1DXaXB8fQg7xif",
    image_path=png_path
)

if success:
    print("✓ Cover art uploaded to Spotify!")
else:
    print("✗ Upload failed - check authentication and permissions")
```

**Key Parameters:**
- `title`: The main text (required)
- `subtitle`: Optional secondary text
- `gradient_start`: Top gradient color from Step 2 analysis
- `gradient_end`: Bottom gradient color from Step 2 analysis
- `text_color`: Text color ensuring 4.5:1 contrast ratio
- `output_path`: Where to save the PNG file
- `size`: Image dimensions (640x640 recommended for Spotify)

---
### Step 5: Quality Assurance Checklist

Before finalizing, verify:

**Readability:**
- [ ] Can you read the title at 100x100px (thumbnail size)?
- [ ] Is there sufficient contrast between text and background (≥4.5:1 ratio)?
- [ ] Does text wrap properly (no cutoffs)?
- [ ] Are all words clearly visible?

**Design Quality:**
- [ ] Do colors match the playlist content/mood?
- [ ] Is the gradient direction visually appealing?
- [ ] Does it look professional and polished?
- [ ] Would you click on this in Spotify?

**Technical Requirements:**
- [ ] Image is 640x640px or larger
- [ ] File size < 256KB (Spotify limit)
- [ ] Format is JPEG or PNG
- [ ] Colors are vibrant but not oversaturated

**Accessibility (WCAG 2.1 AA):**
- [ ] Contrast ratio ≥ 4.5:1 for normal text
- [ ] Contrast ratio ≥ 3:1 for large text (>24px)
- [ ] Readable for colorblind users (test with grayscale)

**Content Alignment:**
- [ ] Colors reflect the actual music genres in the playlist
- [ ] Energy level matches the track content
- [ ] Mood is appropriate for the use case (workout, sleep, party, etc.)

---
## Advanced Techniques

### Empty or Private Playlists

If you cannot access playlist tracks:

1. **Ask for genre/mood**: "I can't access the playlist tracks. What genre and mood should the cover art convey?"
2. **Use playlist name only**: Extract clues from the name itself
3. **Default to universal design**: Use balanced, professional colors

### Error Recovery

**If generation fails:**
1. Check that all color codes are valid hex format (#RRGGBB)
2. Ensure title is not empty
3. Verify gradient_start and gradient_end are different colors
4. Confirm text_color has sufficient contrast with both gradient colors

**If upload fails:**
1. Verify the `ugc-image-upload` scope is included in OAuth token
2. Check that image is <256KB
3. Ensure playlist is owned by the authenticated user
4. Confirm image is valid PNG or JPEG format

### Template Fallback (Alternative Method)

If content analysis is unavailable, use these predefined templates:

**Rock/Metal Template:**
```python
gradient_start = "#E63946"  # Intense red
gradient_end = "#1D1D1D"    # Almost black
text_color = "#FFFFFF"      # White
```

**Electronic/EDM Template:**
```python
gradient_start = "#00FFF0"  # Neon cyan
gradient_end = "#8B5DFF"    # Electric purple
text_color = "#FFFFFF"      # White
```

**Chill/Ambient Template:**
```python
gradient_start = "#4ECDC4"  # Cool teal
gradient_end = "#556FB5"    # Soft blue
text_color = "#FFFFFF"      # White
```

**Pop/Upbeat Template:**
```python
gradient_start = "#FF6B9D"  # Hot pink
gradient_end = "#FFD93D"    # Bright yellow
text_color = "#FFFFFF"      # White
```

**Classical/Jazz Template:**
```python
gradient_start = "#D4A574"  # Gold
gradient_end = "#2C3E50"    # Navy
text_color = "#F5F5DC"      # Cream
```

---
## Summary

**You are now self-contained and autonomous for cover art generation.** You don't need preset theme lists - instead, you:

1. **Analyze** the playlist's actual content (tracks, artists, genres)
2. **Extract** genre, mood, and energy from the music
3. **Apply** color psychology based on your analysis
4. **Generate** contextually appropriate cover art
5. **Verify** quality and accessibility

This approach makes you adaptive to any playlist - past, present, or future - by analyzing the actual content rather than relying on predefined themes.

### Decision Tree

```
START
├─ Can access playlist tracks?
│  ├─ YES → Analyze content (Step 1) → Determine colors (Step 2)
│  └─ NO → Ask user for genre/mood → Use template fallback
│
├─ Is playlist name vague?
│  ├─ YES → Ask clarifying questions → Wait for response
│  └─ NO → Extract keywords from name
│
├─ Colors determined?
│  ├─ YES → Apply typography rules (Step 3)
│  └─ NO → Use template fallback
│
├─ Title > 25 characters?
│  ├─ YES → Apply text wrapping
│  └─ NO → Use title as-is
│
├─ Generate cover art (Step 4)
│
├─ Quality checks pass? (Step 5)
│  ├─ YES → Upload to Spotify
│  └─ NO → Adjust colors/typography → Regenerate
│
END
```

### Success Metrics

**Good Cover Art:**
- ✓ Colors derived from actual playlist content
- ✓ Readable at thumbnail size (100x100px)
- ✓ Colors match playlist mood/energy
- ✓ Professional, polished appearance
- ✓ High contrast for accessibility (≥4.5:1 ratio)
- ✓ Unique and contextually appropriate

**Poor Cover Art:**
- ✗ Generic colors not based on content
- ✗ Text too small or cramped
- ✗ Low contrast (hard to read)
- ✗ Colors don't match genre/mood
- ✗ Looks amateurish or cluttered

### Final Checklist

Before delivering cover art to the user:

1. [ ] Analyzed playlist content (tracks, artists, genres)
2. [ ] Extracted energy level and mood from content
3. [ ] Determined colors using color psychology
4. [ ] Applied proper typography (fonts 40-90px)
5. [ ] Implemented text wrapping for long titles
6. [ ] Verified readability at thumbnail size
7. [ ] Checked contrast ratios (WCAG 2.1 AA ≥4.5:1)
8. [ ] Generated image at 640x640px
9. [ ] Uploaded to Spotify successfully
10. [ ] Confirmed visual quality matches content

---

## Troubleshooting

### Common Issues

**"401 Unauthorized" when uploading:**
- Missing `ugc-image-upload` scope in OAuth token
- Solution: Re-run `get_refresh_token.py` to get new token with all scopes

**"Image too large" error:**
- File size exceeds 256KB
- Solution: Reduce image size or quality

**Text is unreadable in thumbnail:**
- Font size too small (<40px)
- Solution: Increase font size or use text wrapping

**Colors don't match playlist mood:**
- Insufficient content analysis
- Solution: Review Step 1 and Step 2 more carefully

**Text gets cut off:**
- Title too long without wrapping
- Solution: Apply text wrapping (Step 3)

---

**Remember**: The primary method is content-driven analysis (Steps 1-2). Only use template fallback when content is unavailable. Always prioritize readability and accessibility over artistic complexity.
