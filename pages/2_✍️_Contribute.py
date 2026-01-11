#pages/2_✍️_Contribute.py
import streamlit as st
import os
import shutil
from app.core.database_manager import DatabaseManager
from app.services.indexer import scan_and_index
from app.components.ui_utils import load_css, render_header

MOUNT_DIR = "/home/shay0129/Music/kollas_mount"
UPLOAD_DIR = os.path.join(MOUNT_DIR, "community_uploads")

st.set_page_config(page_title="Contribute", page_icon="✍️", layout="wide")
load_css()
render_header("Contribute", "✍️")

tab1, tab2 = st.tabs(["Upload New", "Edit Metadata"])

# --- TAB 1: UPLOAD ---
with tab1:
    st.info(f"Files upload to: `{UPLOAD_DIR}`")
    uploaded_files = st.file_uploader("Upload MP3s", type=['mp3', 'wav', 'm4a'], accept_multiple_files=True)

    if uploaded_files:
        if st.button("🚀 Start Upload"):
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            progress_bar = st.progress(0)

            for i, file in enumerate(uploaded_files):
                dest_path = os.path.join(UPLOAD_DIR, file.name)
                with open(dest_path, "wb") as f:
                    shutil.copyfileobj(file, f)
                progress_bar.progress((i + 1) / len(uploaded_files))

            st.success("Upload complete! Indexing...")
            scan_and_index()

# --- TAB 2: EDIT METADATA ---
with tab2:
    st.write("Search for a song to edit details or add lyrics.")
    edit_query = st.text_input("Find song", key="edit_search")

    if edit_query:
        results = DatabaseManager.search_songs(edit_query, limit=10, only_verified=False)

        selected_song_id = st.selectbox(
            "Select Song",
            options=[s['id'] for s in results],
            format_func=lambda x: next((s['title'] for s in results if s['id'] == x), x)
        )

        if selected_song_id:
            song = DatabaseManager.get_song_by_id(selected_song_id)

            with st.form("edit_form"):
                st.markdown(f"**Editing:** {song['filename']}")
                new_title = st.text_input("Title", value=song['title'])
                new_cantor = st.text_input("Cantor", value=song['cantor'])
                new_origin = st.selectbox("Origin", ["Unknown", "Ernakulam", "Parur", "Cochin", "Mala"], index=0)
                new_lyrics = st.text_area("Lyrics (Hebrew supported)", value=song['lyrics'] or "")

                submitted = st.form_submit_button("Submit for Review")

                if submitted:
                    DatabaseManager.update_song_metadata(
                        selected_song_id, new_title, new_cantor, new_origin, new_lyrics, status="pending"
                    )
                    st.success("Changes submitted for Admin approval!")
