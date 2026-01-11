#Home.py
import streamlit as st
from app.services.indexer import scan_and_index
from app.core.database_manager import DatabaseManager
from app.components.ui_utils import load_css

st.set_page_config(page_title="KollasApp", page_icon="🕍", layout="wide")
load_css()

# Initialize DB on first run
if "db_init" not in st.session_state:
    DatabaseManager.init_db()
    st.session_state["db_init"] = True

st.title("🕍 KollasApp: Cochin Heritage Archive")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    **Welcome to the Digital Library of Cochin Jewish Piyyutim.**

    This platform preserves our heritage by cataloging thousands of recordings.
    The system runs on a highly optimized, community-driven architecture.

    **Features:**
    * 🔍 **Search**: Instantly find songs by title, cantor, or lyrics.
    * ✍️ **Contribute**: Add lyrics or correct metadata.
    * ☁️ **Cloud**: Direct streaming via secure tunnel.
    """)

with col2:
    st.info("System Status")
    if st.button("🔄 Scan for New Files"):
        with st.spinner("Indexing filesystem..."):
            count = scan_and_index()
            if count > 0:
                st.success(f"Found {count} new recordings!")
            else:
                st.info("Library is up to date.")

    # Quick Stats
    with DatabaseManager.get_connection() as conn:
        cursor = conn.cursor()
        total = cursor.execute("SELECT COUNT(*) FROM songs").fetchone()[0]
        verified = cursor.execute("SELECT COUNT(*) FROM songs WHERE status='verified'").fetchone()[0]

    st.metric("Total Recordings", total)
    st.metric("Verified Metadata", verified)
