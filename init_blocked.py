# init_blocked.py
import sqlite3
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create blocked_ips table
cur.execute('''
CREATE TABLE IF NOT EXISTS blocked_ips (
    ip TEXT PRIMARY KEY,
    blocked_at TEXT
)
''')

conn.commit()
conn.close()
print("blocked_ips table created (if it didn't exist)")

