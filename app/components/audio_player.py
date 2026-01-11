# app/components/audio_player.py
import streamlit as st

def play_drive_audio(file_id):
    # Construct a direct streaming link
    # Note: Large files might buffer. Ideally, convert to OGG/MP3 low bitrate for web.
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    st.audio(url, format="audio/mp3")
