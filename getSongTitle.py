import asyncio
import os
import re
import warnings
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from pydub import AudioSegment
from shazamio import Shazam

# Ignore non-critical escape sequence warnings from pydub
warnings.filterwarnings("ignore", category=SyntaxWarning)

MP3_DIRECTORY = "./mp3_downloads"
TEMP_SLICE_PATH = "./temp_slice.mp3"


def sanitize_filename(name):
    """Remove invalid filesystem characters."""
    return re.sub(r'[\\/*?:"<>|]', "", str(name)).strip()


def write_id3_tags(file_path, artist, title, album, trackno):
    """Embed ID3 metadata tags directly into the MP3 file."""
    try:
        audio = EasyID3(file_path)
    except ID3NoHeaderError:
        audio = EasyID3()

    audio["artist"] = artist
    audio["title"] = title
    audio["album"] = album
    audio["tracknumber"] = trackno
    audio.save(file_path)


def create_middle_sample(file_path):
    """Extract a 15-second sample from the middle of the song to bypass long intros."""
    try:
        audio = AudioSegment.from_file(file_path)
        duration_ms = len(audio)

        # Skip intros: take a 15-second slice starting 30 seconds in (or halfway if short)
        start_ms = 30000 if duration_ms > 45000 else duration_ms // 2
        end_ms = min(start_ms + 15000, duration_ms)

        sample = audio[start_ms:end_ms]
        sample.export(TEMP_SLICE_PATH, format="mp3")
        return True
    except Exception:
        return False


async def recognize_and_rename_mp3s(directory_path):
    if not os.path.exists(directory_path):
        print(f"Directory non-existent: {directory_path}")
        return

    shazam = Shazam()
    mp3_files = [f for f in os.listdir(directory_path) if f.lower().endswith(".mp3")]

    print(f"Found {len(mp3_files)} MP3 file(s). Starting audio recognition...\n")

    for idx, filename in enumerate(mp3_files, start=1):
        file_path = os.path.join(directory_path, filename)

        # Extract first 2 characters as trackno (e.g. "01 Track 1.mp3" -> "01")
        trackno = filename[:2]

        print(f"[{idx}/{len(mp3_files)}] Listening to audio: '{filename}' (Track No: {trackno})...")

        try:
            # First Attempt: Full audio file
            out = await shazam.recognize(file_path)
            track = out.get("track")

            # Second Attempt: Middle audio sample if the first attempt returned no match
            if not track and create_middle_sample(file_path):
                print("  --> Retrying with middle audio sample...")
                out = await shazam.recognize(TEMP_SLICE_PATH)
                track = out.get("track")
                if os.path.exists(TEMP_SLICE_PATH):
                    os.remove(TEMP_SLICE_PATH)

            if not track:
                print(f"  --> Could not match audio signature for: {filename}")
                continue

            # Extract details from Shazam response
            artist = track.get("subtitle", "Unknown Artist")
            title = track.get("title", "Unknown Title")
            album = "Unknown Album"

            for section in track.get("sections", []):
                if section.get("type") == "SONG":
                    for metadata in section.get("metadata", []):
                        if metadata.get("title", "").lower() == "album":
                            album = metadata.get("text", "Unknown Album")
                            break

            # Write metadata to ID3 tags (including Album and Track Number)
            write_id3_tags(file_path, artist, title, album, trackno)

            # Format new filename: {trackno}-{artist}-{title}.mp3
            clean_artist = sanitize_filename(artist)
            clean_title = sanitize_filename(title)

            new_filename = f"{trackno}-{clean_artist}-{clean_title}.mp3"
            new_file_path = os.path.join(directory_path, new_filename)

            # Rename file
            if file_path != new_file_path:
                if os.path.exists(new_file_path):
                    print(f"  --> Target file already exists: {new_filename}")
                else:
                    os.rename(file_path, new_file_path)
                    print(f"  --> Matched & Renamed: '{new_filename}'")
            else:
                print(f"  --> Matched & Updated Tags: '{filename}'")

        except Exception as e:
            print(f"  --> Error processing {filename}: {e}")

    # Clean up lingering temporary files
    if os.path.exists(TEMP_SLICE_PATH):
        os.remove(TEMP_SLICE_PATH)


if __name__ == "__main__":
    asyncio.run(recognize_and_rename_mp3s(MP3_DIRECTORY))