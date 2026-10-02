# Python Team Project
Welcome! Please follow our Git flow guidelines.

## Python Files

| File | Description | Command |
|------|-------------|---------|
| **getYTMp3.py** | Downloads songs from YouTube/Music using yt-dlp given a CSV/Excel file with URLs and metadata. Outputs MP3 files with embedded ID3 tags (artist, album, title). | `uv run python getYTMp3.py` |
| **getSongTitle.py** | Uses Shazam to recognize MP3 songs and automatically rename them with proper artist-title format. Also writes ID3 tags (artist, title, album, track number). | `uv run python getSongTitle.py` |
| **rename_tracks.py** | Renames all MP3 files in a directory with sequential 3-digit prefixes (001-, 002-, etc.) based on sorted order. | `uv run python rename_tracks.py` |
| **rename_101_245.py** | Similar to rename_tracks but starts numbering from 101 (e.g., 101-145 for 45 tracks) and outputs to a separate directory for portable players. | `uv run python rename_101_245.py` |
| **noise_remover.py** | Applies audio processing to remove vinyl crackles, low-frequency rumble, and clicks while boosting volume. Requires input file `attached_song.mp3`. | `uv run python noise_remover.py` |
| **fix_fat_order.py** | Copies MP3 files into an output folder in strict filename order (001 → 002 → ...) so portable players/FAT32 devices list and play them correctly. | `uv run python fix_fat_order.py` |

## Git Flow Guidelines
*(Add your Git flow guidelines here)* 
