#!/bin/bash

# ==========================================
# KollasApp Production Launcher (1GB RAM Optimized)
# ==========================================

# 1. Cleanup Environment
# Remove old containers and unmount drive to prevent stale handles
echo "Step 1: Cleaning up environment..."
podman rm -f kollas-media-server 2>/dev/null
killall -9 rclone 2>/dev/null
killall -9 streamlit 2>/dev/null
fusermount -uz ~/Music/kollas_mount 2>/dev/null

# 2. Mount Storage (Google Drive)
# --vfs-cache-mode writes: Essential for stability when uploading files
echo "Step 2: Mounting Google Drive..."
mkdir -p ~/Music/kollas_mount
rclone mount rclone-upload:Cochin_Archive ~/Music/kollas_mount \
  --daemon --allow-other --vfs-cache-mode writes

# Wait for mount to stabilize
sleep 3

# 3. Start Nginx Media Server (Rootless Podman)
# Serves MP3s via HTTP on port 8080. Low memory footprint.
echo "Step 3: Starting Nginx Media Server..."
podman run -d \
  --name kollas-media-server \
  --network host \
  -v /home/shay0129/Music/kollas_mount:/usr/share/nginx/html:ro \
  nginx:alpine sh -c "echo 'server { listen 8080; charset utf-8; location / { root /usr/share/nginx/html; autoindex on; } }' > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"

# 4. Initialize Database
# Scans the mount and registers files in SQLite
echo "Step 4: Initializing Database & Indexing..."
python3 init_db.py

# 5. Start Streamlit UI (Background Process)
# Running on port 8501. Using nohup to keep it alive if session disconnects.
echo "Step 5: Starting Streamlit App..."
nohup streamlit run Home.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  > streamlit.log 2>&1 &

PID=$!
echo "   Streamlit started with PID $PID. Logs at streamlit.log"

# 6. Establish Cloudflare Tunnel (Media Server)
# This exposes Nginx (8080) to the internet so the Streamlit app can play audio.
echo "Step 6: Establishing Cloudflare Media Tunnel..."

~/.local/bin/cloudflared tunnel --url http://127.0.0.1:8080 2>&1 | tee /tmp/cloudflared.log | while read -r line; do
    # Print line to console so we see status
    echo "$line"

    # Logic to capture the TryCloudflare URL
    if [[ "$line" == *"https://"*".trycloudflare.com"* ]]; then
        TUNNEL_URL=$(echo "$line" | grep -o "https://.*\.trycloudflare\.com" | head -n 1)

        echo -e "\n\e[32m[MEDIA SERVER LIVE]: $TUNNEL_URL\e[0m"

        # Update server_config.json so Python knows where to find MP3s
        echo "{\"MUSIC_SERVER_URL\": \"$TUNNEL_URL\"}" > server_config.json

        # Git Update Logic (Push new URL to repo if using GitOps)
        # Note: Ensure ~/.ssh/id_rsa exists and has permissions
        git add server_config.json
        git commit -m "Auto-update: Media Server URL to $TUNNEL_URL"
        git push origin main

        echo -e "\n\e[32m****************************************************"
        echo -e "SYSTEM ONLINE"
        echo -e "UI: http://$(curl -s ifconfig.me):8501"
        echo -e "Media: $TUNNEL_URL"
        echo -e "****************************************************\e[0m\n"
    fi
done
