import os
import re
import pandas as pd
import yt_dlp

INPUT_FILE = "songs.csv"  # Change to .csv if applicable
OUTPUT_FOLDER = "mp3_downloads"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def sanitize_filename(name):
    """Remove characters that are invalid in Windows/Mac/Linux filenames."""
    return re.sub(r'[\\/*?:"<>|]', "", str(name)).strip()

def download_songs(file_path):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    df['ARTIST'] = df['ARTIST'].fillna('Unknown Artist')
    df['ALBUM'] = df['ALBUM'].fillna('Unknown Album')
    df['TITLE'] = df['TITLE'].fillna('Unknown Title')

    for idx, row in df.iterrows():
        raw_url = str(row['URL']).strip()
        if not raw_url.startswith("http"):
            continue

        # Strip playlist parameters to avoid downloading entire playlists
        clean_url = raw_url.split("&list=")[0].split("?list=")[0]

        artist_str = str(row['ARTIST']).strip()
        album_str = str(row['ALBUM']).strip()
        title_str = str(row['TITLE']).strip()

        artist = sanitize_filename(artist_str)
        album = sanitize_filename(album_str)
        title = sanitize_filename(title_str)
        
        filename = f"{artist} - {album} - {title}.mp3"
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        if os.path.exists(output_path):
            print(f"[{idx + 1}/{len(df)}] Skipping (Already Exists): {filename}")
            continue

        print(f"\n[{idx + 1}/{len(df)}] Downloading: {filename}")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                # Embeds metadata directly into ID3 tags of the MP3
                {
                    'key': 'FFmpegMetadata',
                    'add_metadata': True,
                }
            ],
            # Pass custom metadata values from your spreadsheet
            'postprocessor_args': [
                '-metadata', f'artist={artist_str}',
                '-metadata', f'album={album_str}',
                '-metadata', f'title={title_str}'
            ],
            'outtmpl': os.path.splitext(output_path)[0],
            'noplaylist': True,
            'ignoreerrors': True,
            'quiet': False,
            'js_runtimes': {
                'deno': {},
                'node': {}
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['web', 'mweb', 'android']
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([clean_url])
            except Exception as e:
                print(f"Failed to download {clean_url}: {e}")

if __name__ == "__main__":
    download_songs(INPUT_FILE)