import os
from pydub import AudioSegment

# --- Configuration ---
# Point this to your rclone mount path
MOUNT_DIR = "/home/shay0129/Music/kollas_mount"
BITRATE = "192k"

def convert_on_mount():
    """
    Finds WAVs on the mount, converts to MP3, and saves back to the same folder.
    """
    for root, dirs, files in os.walk(MOUNT_DIR):
        for file in files:
            if file.lower().endswith(".wav"):
                wav_path = os.path.join(root, file)
                # Create the MP3 filename
                mp3_path = os.path.join(root, file.rsplit('.', 1)[0] + ".mp3")

                # Check if MP3 already exists to save time/bandwidth
                if os.path.exists(mp3_path):
                    print(f"⏭️ Skipping {file} (MP3 already exists)")
                    continue

                print(f"🎵 Processing: {file}...")

                try:
                    # pydub reads the WAV (this triggers a download from GDrive)
                    audio = AudioSegment.from_wav(wav_path)

                    # Exporting back to mount (this triggers an upload to GDrive)
                    audio.export(mp3_path, format="mp3", bitrate=BITRATE)
                    print(f"✅ Successfully converted: {file}")

                except Exception as e:
                    print(f"❌ Failed to process {file}: {e}")

if __name__ == "__main__":
    convert_on_mount()
