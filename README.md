# 🕍 KollasApp: Cochin Jewish Heritage Archive

**KollasApp** is a specialized digital library designed to preserve, catalog, and map the liturgical music (Piyyutim) of the Cochin Jewish community.

Built for efficiency and longevity, this application runs on a **high-performance, serverless architecture**. It enables community members to search the library, contribute lyrics, and identify unverified recordings, ensuring these unique musical traditions are documented for future generations.

---

## 🏗️ Architecture & Optimization

This project is engineered to run on minimal hardware (e.g., **AWS EC2 t3.micro with 1GB RAM**) while serving thousands of audio files.

* **Frontend:** [Streamlit](https://streamlit.io/) (Python) - Multi-page responsive interface.
* **Database:** **SQLite** - Replaces Pandas/CSV for memory-efficient (O(1)) data handling and persistence.
* **Storage:** **Google Drive** mounted locally via **Rclone** (VFS Cache enabled).
* **Media Streaming:** **Nginx** (running in a Rootless **Podman** container) serves audio files directly from the mount.
* **Connectivity:** **Cloudflare Tunnel** exposes the local media server securely to the web, bypassing complex firewall rules.

---

## 📂 Repository Structure

```text
KollasApp/
├── app/
│   ├── core/
│   │   ├── database_manager.py  # Singleton SQLite handler (Optimized)
│   │   └── schema.sql           # Database schema definition
│   ├── services/
│   │   ├── indexer.py           # Auto-scanner (Disk -> DB)
│   │   └── media_server.py      # Resolves dynamic Cloudflare URLs
│   └── components/
│       └── ui_utils.py          # UI helpers (RTL support, Styling)
├── pages/
│   ├── 1_📚_Library.py          # Search & Listen interface
│   ├── 2_✍️_Contribute.py       # Metadata editing & File uploads
│   └── 3_🛡️_Admin.py            # Approval dashboard
├── .streamlit/
│   ├── config.toml              # Server optimization settings
│   └── secrets.toml             # (Excluded) Passwords and Keys
├── init_db.py                   # One-time database initialization script
├── run_kollas.sh                # Main orchestration script
├── server_config.json           # Auto-generated Cloudflare URL config
├── requirements.txt             # Minimal dependencies (No Pandas)
└── Home.py                      # Application Entry Point

```

---

## ⚙️ Prerequisites

Ensure the host environment (Fedora/Ubuntu/CentOS) has the following installed:

1. **Python 3.10+**
2. **Podman** (or Docker)
3. **Rclone** (Configured with a remote named `rclone-upload`)
4. **Cloudflared** (Cloudflare Tunnel daemon)
5. **Git**

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/kollasapp-streamlit.git](https://github.com/your-username/kollasapp-streamlit.git)
cd kollasapp-streamlit

```

### 2. Install Dependencies

We use a strict minimal requirement set to save memory.

```bash
pip install -r requirements.txt

```

### 3. Configure Secrets (Critical)

You must create a secrets file to set the Admin password for the dashboard.
Create the file `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml

# Password for the Admin Dashboard (pages/3_🛡️_Admin.py)
# NOTE: Use lowercase 'admin_password' key
admin_password = "YOUR_SECURE_PASSWORD_HERE"

```

### 4. Initialize the Database

Run the initialization script to create the SQLite database file (`kollas.db`) and perform an initial scan of the mounted files.

```bash
python3 init_db.py

```

---

## 🖥️ Running the Application

We use a custom orchestration script to handle the startup sequence (Cleanup -> Mount Drive -> Start Nginx -> Start Tunnel -> Start App).

### 1. Make the script executable

```bash
chmod +x run_kollas.sh

```

### 2. Launch

```bash
./run_kollas.sh

```

**What this script does:**

1. **Cleanup:** Kills stale Podman containers or Rclone mounts.
2. **Mount:** Mounts Google Drive to `~/Music/kollas_mount`.
3. **Media Server:** Starts Nginx on port `8080`.
4. **Tunnel:** Starts Cloudflare Tunnel to expose Nginx.
5. **Config:** Updates `server_config.json` with the new Tunnel URL.
6. **App:** Launches Streamlit in the background on port `8501`.

---

## 🌐 Access

* **User Interface:** `http://<YOUR_SERVER_IP>:8501`
* **Media Server:** Handled automatically via the Cloudflare URL found in `server_config.json`.

---

**Maintained by:** Shay Mordechai

**License:** Private Community Project

```
