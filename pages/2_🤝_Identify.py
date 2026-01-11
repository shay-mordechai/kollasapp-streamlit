import streamlit as st
import pandas as pd
from app.services.sheet_connector import SheetConnector
from app.components.tagging_form import render_tagging_form

# --- Page Config ---
st.set_page_config(page_title="Identify Recordings", page_icon="🤝")

# --- CSS Injection for Accessibility ---
st.markdown("""
    <style>
    .stButton button {
        font-size: 20px !important;
        padding: 10px 24px !important;
    }
    p, label {
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def get_drive_url(file_id):
    """Converts Drive ID to direct streamable URL."""
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def load_next_song():
    """Selects a random unverified song and stores in session state."""
    df = SheetConnector.load_recordings()

    # Filter for unverified
    if 'verification_status' in df.columns:
        unverified = df[df['verification_status'] == 'Unverified']
    else:
        # Fallback if column doesn't exist yet
        unverified = df

    if unverified.empty:
        st.session_state['current_recording'] = None
    else:
        # Sample 1 random row
        st.session_state['current_recording'] = unverified.sample(1).iloc[0].to_dict()

# --- Main Logic ---

st.title("🤝 Help Us Identify")
st.markdown("Listen to the audio clip below. If you recognize the melody, the singer, or the words, please fill out the form.")

# Initialize Session State
if 'current_recording' not in st.session_state:
    load_next_song()

current_rec = st.session_state['current_recording']

if current_rec is None:
    st.success("🎉 All recordings have been verified! Thank you for your help.")
else:
    # 1. Audio Player Section
    st.info(f"📂 File: {current_rec.get('file_name', 'Unknown')}")

    drive_id = current_rec.get('drive_file_id')
    if drive_id:
        audio_url = get_drive_url(drive_id)
        st.audio(audio_url, format='audio/mp3')
    else:
        st.error("Audio file link missing.")

    # 2. Tagging Form Component
    feedback_data = render_tagging_form(current_rec)

    # 3. Handle Form Submission
    if feedback_data:
        # Add user name (optional, could be added to form or taken from login)
        feedback_data['user_name'] = "Community Member"

        with st.spinner("Submitting your knowledge..."):
            success = SheetConnector.submit_suggestion(feedback_data)

        if success:
            st.balloons()
            st.success("Thank you! Your contribution has been recorded.")
            load_next_song() # Load next
            st.rerun()       # Refresh UI
        else:
            st.error("Something went wrong connecting to the database. Please try again.")

    # 4. Skip Button (Outside Form)
    st.markdown("---")
    if st.button("⏭️ Skip this song (I don't recognize it)"):
        load_next_song()
        st.rerun()

# --- Debugging (Optional - remove in production) ---
# st.write(st.session_state['current_recording'])
