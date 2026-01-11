import streamlit as st
import urllib.parse

class LocalConnector:
    """
    Handles streaming logic from the local secure Nginx server.
    """
    @staticmethod
    def get_audio_url(relative_path):
        """
        Constructs the public URL for a file hosted on the home server.
        relative_path: The path from the root of the music folder.
        """
        base_url = st.secrets["network_config"]["home_server_url"]
        
        # Security Note: Ensure the path is URL-encoded for special characters (Hebrew)
        encoded_path = urllib.parse.quote(relative_path)
        
        # Final URL through the Cloudflare Tunnel
        return f"{base_url}/{encoded_path}"

