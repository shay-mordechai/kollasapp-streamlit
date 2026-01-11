import streamlit as st
import pandas as pd
from app.services.sheet_connector import SheetConnector
from app.services.local_connector import LocalConnector

st.set_page_config(page_title="Library", page_icon="🔎", layout="wide")

# Accessibility CSS
st.markdown("""
    <style>
    .streamlit-expanderHeader { font-size: 20px !important; font-weight: bold !important; }
    audio { width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("🔎 Piyyutim Library")

# Load Data from Google Sheets (Metadata)
with st.spinner("Loading library..."):
    df = SheetConnector.load_recordings()

if df.empty:
    st.warning("Library is empty. Run the indexer script first.")
    st.stop()

# Search UI
search_term = st.text_input("🔍 Search Piyyut or Cantor", placeholder="Type here...")

# Filtering logic
filtered_df = df[df['piyyut_name'].str.contains(search_term, case=False, na=False) | 
                df['cantor_name'].str.contains(search_term, case=False, na=False)]

# Results Display
for _, row in filtered_df.head(50).iterrows():
    with st.expander(f"{row['piyyut_name']} - {row['cantor_name']}"):
        col1, col2 = st.columns([3, 1])
        with col1:
            # Here we pull from your Nginx server instead of Drive
            audio_url = LocalConnector.get_audio_url(row['file_path'])
            st.audio(audio_url)
        with col2:
            st.write(f"📍 **Origin:** {row['nusach_origin']}")
            st.caption(f"Category: {row['category']}")
