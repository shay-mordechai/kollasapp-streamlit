import streamlit as st

st.set_page_config(
    page_title="KollasApp - Cochin Heritage",
    page_icon="🎵",
    layout="wide"
)

st.title("🎼 KollasApp: Cochin Jewish Digital Library")
st.markdown("""
Welcome to the community project for preserving and mapping the Piyyutim of Cochin.
This tool allows us to organize, identify, and document thousands of recordings.

### 👈 How to help:
1. **Search Library**: Browse existing recordings.
2. **Help Identify**: Listen to unverified tracks and add details about the cantor or tradition.
3. **Admin**: (For authorized users) Approve community suggestions.
""")

st.info("Choose a page from the sidebar to get started.")
