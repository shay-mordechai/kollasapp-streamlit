#pages/1_📚_Library.py
import streamlit as st
from app.core.database_manager import DatabaseManager
from app.services.media_server import get_audio_url
from app.components.ui_utils import load_css, render_header

st.set_page_config(page_title="Library", page_icon="📚", layout="wide")
load_css()
render_header("Library Search", "📚")

# Filters
col_search, col_verified = st.columns([3, 1])
with col_search:
    query = st.text_input("🔍 Search by Title, Cantor, or Lyrics")
with col_verified:
    show_all = st.checkbox("Show Unverified", value=False)

# Fetch Data (Optimized)
songs = DatabaseManager.search_songs(
    query=query,
    limit=50,
    only_verified=not show_all
)

if not songs:
    st.warning("No recordings found.")
else:
    for song in songs:
        with st.expander(f"🎵 {song['title']} - {song['cantor']}"):
            c1, c2 = st.columns([2, 1])

            with c1:
                url = get_audio_url(song['file_path'])
                if url:
                    st.audio(url)
                else:
                    st.error("Server disconnected.")

                if song['lyrics']:
                    st.markdown(f"**Lyrics:**\n<div class='hebrew-text'>{song['lyrics']}</div>", unsafe_allow_html=True)

            with c2:
                st.caption(f"Origin: {song['origin']}")
                st.caption(f"Status: {song['status']}")
                st.caption(f"File: {song['filename']}")
