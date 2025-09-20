# =============================
# config.py
# Tune thresholds and configuration here
# =============================

# Database
DB_PATH = "ids_events.db"

# Detection thresholds
PORT_SCAN_WINDOW_SEC = 20        # sliding window to observe ports
PORT_SCAN_PORT_THRESHOLD = 20    # unique ports from one IP within window = port scan

CONN_ATTEMPT_WINDOW_SEC = 60     # window for connection attempts
CONN_ATTEMPT_THRESHOLD = 50      # connections in window => brute-force-like behavior

# Auto-block settings
AUTO_BLOCK = True
BLOCK_COMMAND_TEMPLATE = "iptables -A INPUT -s {ip} -j DROP"  # uses subprocess; requires sudo

# Dashboard
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

# Whitelist (trusted IPs never blocked)
WHITELIST = ["127.0.0.1"]

# Block duration (seconds) before auto-unblock
BLOCK_DURATION = 300  # 5 minutes

# =============================
# Email Alert Configuration
# =============================
ADMIN_EMAIL = "subhamsahoo2306@gmail.com"
APP_PASSWORD = "zavknrclesowqofg"   # no spaces!
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587



