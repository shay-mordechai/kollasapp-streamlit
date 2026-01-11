import os
import subprocess

# --- Configuration ---
# Pointing to the local temporary directory where files were downloaded
SOURCE_DIR = "/home/shay0129/Music/conversion_temp"
BITRATE = "192k"

def robust_convert():
    """
    Scans the local temporary directory for WAV files and converts them to MP3
    using a direct FFmpeg call for maximum compatibility with older formats.
    """
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Error: Source directory {SOURCE_DIR} not found.")
        return

    # Counter for statistics
    count_success = 0
    count_fail = 0

    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.lower().endswith(".wav"):
                # Full paths for input and output
                wav_path = os.path.join(root, file)
                # Replacing extension with .mp3
                mp3_path = os.path.splitext(wav_path)[0] + ".mp3"

                # Skip if already converted to save time
                if os.path.exists(mp3_path):
                    continue

                print(f"🛠️  Processing: {file}")

                # Using subprocess to call ffmpeg directly
                # This approach is more robust for ADPCM and non-standard WAVs
                command = [
                    "ffmpeg",
                    "-y",              # Overwrite output files without asking
                    "-i", wav_path,
                    "-acodec", "libmp3lame",
                    "-ab", BITRATE,
                    "-loglevel", "error",
                    mp3_path
                ]

                try:
                    # Execute the conversion
                    subprocess.run(command, check=True)
                    print(f"✅ Converted: {file}")
                    count_success += 1
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to convert {file}: {e}")
                    count_fail += 1
                except Exception as ex:
                    print(f"⚠️ Unexpected error with {file}: {ex}")
                    count_fail += 1

    print("\n" + "="*30)
    print(f"🏁 Conversion Task Completed!")
    print(f"📊 Success: {count_success}")
    print(f"📊 Failed: {count_fail}")
    print("="*30)

if __name__ == "__main__":
    robust_convert()
