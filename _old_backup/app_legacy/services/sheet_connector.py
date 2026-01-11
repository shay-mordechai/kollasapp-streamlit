import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime

# Scopes required for the API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

class SheetConnector:
    """
    Handles interactions with the Google Sheet database.
    Assumes a Google Sheet exists with tabs: 'recordings_master' and 'community_feedback'.
    """

    @staticmethod
    @st.cache_resource
    def _get_client():
        """
        Authenticates with Google Cloud using st.secrets.
        Cached as a resource to persist the connection object.
        """
        try:
            # Construct credentials from the TOML secrets
            creds_dict = st.secrets["gcp_service_account"]
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
            client = gspread.authorize(creds)
            return client
        except Exception as e:
            st.error(f"Failed to authenticate with Google Services: {e}")
            return None

    @staticmethod
    def _get_worksheet(worksheet_name):
        """Helper to get a specific worksheet object."""
        client = SheetConnector._get_client()
        sheet_id = st.secrets["spreadsheet_config"]["sheet_key"] # Store ID in secrets
        try:
            sheet = client.open_by_key(sheet_id)
            return sheet.worksheet(worksheet_name)
        except Exception as e:
            st.error(f"Error accessing worksheet '{worksheet_name}': {e}")
            return None

    @staticmethod
    @st.cache_data(ttl=600)  # Cache for 10 minutes
    def load_recordings():
        """
        Fetches all data from 'recordings_master'.
        Returns: pd.DataFrame
        """
        worksheet = SheetConnector._get_worksheet("recordings_master")
        if not worksheet:
            return pd.DataFrame()

        data = worksheet.get_all_records()
        return pd.DataFrame(data)

    @staticmethod
    def submit_suggestion(feedback_data: dict):
        """
        Appends a user suggestion to 'community_feedback'.
        Args:
            feedback_data (dict): Dictionary containing feedback details.
        """
        worksheet = SheetConnector._get_worksheet("community_feedback")
        if not worksheet:
            return False

        try:
            # Ensure timestamp is added
            feedback_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            feedback_data['status'] = 'New'

            # Convert dict values to list based on headers (assuming specific order or append)
            # For robustness, we simply append the values.
            # Ideally, map keys to header columns here.
            worksheet.append_row(list(feedback_data.values()))
            return True
        except Exception as e:
            st.error(f"Failed to submit suggestion: {e}")
            return False

    @staticmethod
    def update_recording(rec_id: str, updated_data: dict, row_index: int):
        """
        Updates the master record. Used by Admin.
        Args:
            rec_id: The ID of the recording.
            updated_data: Dict of columns to update.
            row_index: The specific row number in the sheet (2-based index for gspread).
        """
        worksheet = SheetConnector._get_worksheet("recordings_master")
        if not worksheet:
            return False

        try:
            # This is a simplified update. In production, find the cell by header name.
            # Example: Update status to Verified
            # worksheet.update_cell(row_index, col_index, value)
            st.warning("Update logic requires mapping column names to indices. Implementation pending schema finalization.")

            # Force cache clear so changes reflect immediately
            SheetConnector.load_recordings.clear()
            return True
        except Exception as e:
            st.error(f"Failed to update recording: {e}")
            return False

    @staticmethod
    def clear_cache():
        """Manually clear the data cache."""
        SheetConnector.load_recordings.clear()
