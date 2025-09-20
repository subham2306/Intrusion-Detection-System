# detector.py
from utils import pkt_to_record   # ✅ now from utils, not capture
from blocker import block_ip
from config import (
    PORT_SCAN_WINDOW_SEC,
    PORT_SCAN_PORT_THRESHOLD,
    CONN_ATTEMPT_WINDOW_SEC,
    CONN_ATTEMPT_THRESHOLD,
    AUTO_BLOCK
)
from collections import defaultdict
import time

# Track recent ports and connection attempts
recent_ports = defaultdict(list)       # {ip: [(timestamp, dport), ...]}
recent_attempts = defaultdict(list)    # {ip: [timestamp, ...]}

def detect_and_block(pkt):
    rec = pkt_to_record(pkt)
    if not rec or "dport" not in rec:
        return

    src = rec['src']
    dport = rec['dport']
    ts = time.time()

    # ============================
    # Port Scan Detection
    # ============================
    recent_ports[src].append((ts, dport))
    # keep only attempts within PORT_SCAN_WINDOW_SEC
    recent_ports[src] = [(t, p) for (t, p) in recent_ports[src] if ts - t <= PORT_SCAN_WINDOW_SEC]
    unique_ports = len(set(p for (t, p) in recent_ports[src]))

    if unique_ports >= PORT_SCAN_PORT_THRESHOLD and AUTO_BLOCK:
        print(f"[DETECT] Port scan detected from {src} 🚨")
        block_ip(src, "Port Scan")
        recent_ports[src].clear()  # reset after blocking

    # ============================
    # Connection Flood Detection
    # ============================
    recent_attempts[src].append(ts)
    # keep only attempts within CONN_ATTEMPT_WINDOW_SEC
    recent_attempts[src] = [t for t in recent_attempts[src] if ts - t <= CONN_ATTEMPT_WINDOW_SEC]
    attempts = len(recent_attempts[src])

    if attempts >= CONN_ATTEMPT_THRESHOLD and AUTO_BLOCK:
        print(f"[DETECT] Connection flood/brute-force detected from {src} 🚨")
        block_ip(src, "Connection Flood / Brute-force")
        recent_attempts[src].clear()

