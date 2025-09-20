import subprocess
import time
import smtplib
from email.mime.text import MIMEText
from config import (
    WHITELIST,
    BLOCK_DURATION,
    ADMIN_EMAIL,
    APP_PASSWORD,
    SMTP_SERVER,
    SMTP_PORT,
    DB_PATH
)
from db import insert_blocked_ip, remove_blocked_ip

# Track blocked IPs in memory (still useful for quick checks)
BLOCKED_IPS = {}

# =============================
# Email Alert
# =============================
def send_alert(ip, event):
    """
    Send email alert when suspicious activity is detected.
    """
    msg = MIMEText(f"🚨 IDS Alert 🚨\n\nEvent: {event}\nSource IP: {ip}")
    msg['Subject'] = f"IDS Alert - {event} from {ip}"
    msg['From'] = ADMIN_EMAIL
    msg['To'] = ADMIN_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(ADMIN_EMAIL, APP_PASSWORD)
            server.sendmail(ADMIN_EMAIL, ADMIN_EMAIL, msg.as_string())
        print(f"[EMAIL] Alert sent for {ip} ({event})")
    except Exception as e:
        print(f"[ERROR] Failed to send email alert: {e}")

# =============================
# Block IP
# =============================
def block_ip(ip, event="Unknown Event"):
    """
    Block an IP using iptables, unless it's whitelisted.
    """
    if ip in WHITELIST:
        print(f"[INFO] Skipping whitelist IP: {ip}")
        return

    if ip not in BLOCKED_IPS:
        try:
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
            BLOCKED_IPS[ip] = time.time()
            print(f"[BLOCK] {ip} has been blocked for {event}!")

            # Save to DB
            insert_blocked_ip(ip)

            # Send email alert
            send_alert(ip, event)

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to block {ip}: {e}")

# =============================
# Unblock IP
# =============================
def unblock_ip(ip):
    """
    Remove IP from iptables and database
    """
    try:
        subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        if ip in BLOCKED_IPS:
            del BLOCKED_IPS[ip]

        # Remove from DB
        remove_blocked_ip(ip)

        print(f"[UNBLOCK] {ip} manually unblocked")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to unblock {ip}: {e}")

# =============================
# Auto-unblock expired IPs
# =============================
def unblock_expired_ips():
    """
    Unblock IPs after BLOCK_DURATION seconds.
    """
    now = time.time()
    expired_ips = [ip for ip, t in BLOCKED_IPS.items() if now - t > BLOCK_DURATION]

    for ip in expired_ips:
        unblock_ip(ip)

# =============================
# Get currently blocked IPs
# =============================
def get_blocked_ips():
    """
    Returns list of blocked IPs from DB
    """
    from db import fetch_blocked_ips
    rows = fetch_blocked_ips()
    return [row[0] for row in rows]

