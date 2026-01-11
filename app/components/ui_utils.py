#app/components/ui_utils.py
import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* RTL Support for Hebrew */
        .hebrew-text {
            direction: rtl;
            text-align: right;
            font-family: 'David', 'Arial', sans-serif;
        }
        /* Container Styling */
        .stExpander {
            background-color: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        /* Audio Player Width */
        audio { width: 100%; }
        </style>
    """, unsafe_allow_html=True)

def render_header(title, icon):
    st.markdown(f"## {icon} {title}")
    st.markdown("---")
