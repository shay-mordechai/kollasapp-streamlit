# init_db.py
import os
from app.core.database_manager import DatabaseManager
from app.services.indexer import scan_and_index

def setup():
    print("1. Initializing SQLite Database...")
    DatabaseManager.init_db()

    print("2. Scanning Mount Directory...")
    if os.path.exists("/home/shay0129/Music/kollas_mount"):
        count = scan_and_index()
        print(f"   Indexed {count} files.")
    else:
        print("   Warning: Mount directory not found. Skipping scan.")

    print("3. Done! Run 'streamlit run Home.py'")

if __name__ == "__main__":
    setup()
