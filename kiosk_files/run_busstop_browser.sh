#!/bin/sh
SITE="http://127.0.0.1:8000"
UPDATE_INTERVAL="31536000" # 31536000 seconds = 1 year
/usr/bin/chromium-browser --app="${SITE}" \
    --kiosk \
    --noerrdialogs \
    --disable-session-crashed-bubble \
    --disable-restore-session-state \
    --disable-infobars \
    --check-for-update-interval="${UPDATE_INTERVAL}" \
    --disable-pinch
