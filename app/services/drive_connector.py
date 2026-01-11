import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

SCOPES = ["https://www.googleapis.com/auth/drive"]

class DriveConnector:
    @staticmethod
    @st.cache_resource
    def _get_drive_service():
        try:
            creds_dict = st.secrets["gcp_service_account"]
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
            return build('drive', 'v3', credentials=creds)
        except Exception as e:
            st.error(f"Failed to connect to Google Drive: {e}")
            return None

    @staticmethod
    def upload_file_to_drive(uploaded_file, folder_id=None):
        service = DriveConnector._get_drive_service()
        if not service or not folder_id:
            folder_id = st.secrets["drive_config"].get("inbox_folder_id")
        
        try:
            file_metadata = {'name': uploaded_file.name, 'parents': [folder_id]}
            fh = io.BytesIO(uploaded_file.getvalue())
            media = MediaIoBaseUpload(fh, mimetype=uploaded_file.type, resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return file.get('id')
        except Exception as e:
            st.error(f"Error uploading to Drive: {e}")
            return None
