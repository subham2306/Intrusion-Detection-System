# db.py
import sqlite3
from config import DB_PATH
from datetime import datetime

# =============================
# Initialize Database
# =============================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Events table (already existing)
    cur.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        src_ip TEXT,
        event_type TEXT,
        details TEXT,
        ts TEXT
    )
    ''')

    # New: blocked IPs table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS blocked_ips (
        ip TEXT PRIMARY KEY,
        blocked_at TEXT
    )
    ''')

    conn.commit()
    conn.close()

# =============================
# Insert IDS event
# =============================
def insert_event(src_ip, event_type, details):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO events (src_ip, event_type, details, ts) VALUES (?, ?, ?, ?)',
        (src_ip, event_type, details, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

# =============================
# Insert blocked IP
# =============================
def insert_blocked_ip(ip):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        'INSERT OR IGNORE INTO blocked_ips (ip, blocked_at) VALUES (?, ?)',
        (ip, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

# =============================
# Remove blocked IP
# =============================
def remove_blocked_ip(ip):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('DELETE FROM blocked_ips WHERE ip=?', (ip,))
    conn.commit()
    conn.close()

# =============================
# Fetch recent events
# =============================
def fetch_events(limit=200):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, src_ip, event_type, details, ts FROM events ORDER BY id DESC LIMIT ?', (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

# =============================
# Fetch blocked IPs
# =============================
def fetch_blocked_ips():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT ip, blocked_at FROM blocked_ips ORDER BY blocked_at DESC')
    rows = cur.fetchall()
    conn.close()
    return rows

# =============================
# Run initialization
# =============================
if __name__ == "__main__":
    init_db()
    print("DB initialized:", DB_PATH)

