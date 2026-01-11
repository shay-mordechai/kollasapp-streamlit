#!/bin/bash
# manage_mount.sh - Enhanced Version

MOUNT_PATH="$HOME/Music/kollas_mount"

case "$1" in
    start)
        echo "🛡️ Cleaning up old mount points..."
        # Force unmount if something is stuck
        fusermount -uz $MOUNT_PATH 2>/dev/null
        
        echo "🚀 Mounting Cochin Archive..."
        mkdir -p $MOUNT_PATH
        rclone mount rclone-upload:Cochin_Archive $MOUNT_PATH \
        --vfs-cache-mode full \
        --vfs-read-chunk-size 16M \
        --vfs-read-chunk-size-limit 1G \
        --dir-cache-time 5s \
        --buffer-size 32M \
        --daemon
        
        # Wait a second and check if it actually worked
        sleep 2
        if mountpoint -q $MOUNT_PATH; then
            echo "✅ Mounted successfully to $MOUNT_PATH"
        else
            echo "❌ Failed to mount. Check 'rclone config' or logs."
        fi
        ;;
    stop)
        echo "🛑 Stopping mount..."
        fusermount -u $MOUNT_PATH
        echo "✅ Safe to remove folder."
        ;;
    status)
        if mountpoint -q $MOUNT_PATH; then
            echo "🟢 Mount is ACTIVE"
            df -h $MOUNT_PATH
        else
            echo "🔴 Mount is INACTIVE"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        ;;
esac
