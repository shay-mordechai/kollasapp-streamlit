#pages/3_🛡️_Admin.py
import streamlit as st
from app.core.database_manager import DatabaseManager
from app.components.ui_utils import load_css, render_header
from app.services.media_server import get_audio_url

st.set_page_config(page_title="Admin", page_icon="🛡️", layout="wide")
load_css()
render_header("Admin Dashboard", "🛡️")

# Simple Password Protection
pwd = st.sidebar.text_input("Password", type="password")
if pwd != "admin123":  # Change this!
    st.warning("Please verify credentials.")
    st.stop()

st.subheader("Pending Reviews")
pending = DatabaseManager.get_pending_reviews()

if not pending:
    st.success("No pending reviews. All caught up!")
else:
    for song in pending:
        with st.container():
            st.markdown(f"**{song['title']}** ({song['filename']})")

            c1, c2, c3 = st.columns([1, 2, 1])
            with c1:
                url = get_audio_url(song['file_path'])
                if url: st.audio(url)

            with c2:
                st.text_area("Lyrics Preview", song['lyrics'], height=100, disabled=True)
                st.caption(f"Cantor: {song['cantor']} | Origin: {song['origin']}")

            with c3:
                if st.button("✅ Approve", key=f"app_{song['id']}"):
                    DatabaseManager.update_song_metadata(
                        song['id'], song['title'], song['cantor'],
                        song['origin'], song['lyrics'], status="verified"
                    )
                    st.experimental_rerun()

                if st.button("❌ Reject Updates", key=f"rej_{song['id']}"):
                    # Logic to revert or mark as unverified
                    DatabaseManager.update_song_metadata(
                        song['id'], song['title'], song['cantor'],
                        song['origin'], song['lyrics'], status="unverified"
                    )
                    st.experimental_rerun()
            st.divider()
