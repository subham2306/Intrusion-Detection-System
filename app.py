from flask import Flask, render_template_string, redirect, url_for
import sqlite3
from blocker import unblock_ip, unblock_expired_ips
from db import fetch_events, fetch_blocked_ips
from config import FLASK_HOST, FLASK_PORT

app = Flask(__name__)

# =============================
# HTML Dashboard Template
# =============================
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Defence IDS Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #121212; color: #f5f5f5; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; background: #1e1e1e; }
        th, td { border: 1px solid #444; padding: 10px; text-align: left; }
        th { background: #333; }
        h1 { text-align: center; }
        .blocked { color: red; font-weight: bold; }
        .button {
            background: #e63946; color: white; padding: 5px 10px;
            text-decoration: none; border-radius: 5px; font-size: 14px;
        }
        .button:hover { background: #d62828; }
    </style>
</head>
<body>
    <h1>🚨 Defence IDS Dashboard 🚨</h1>

    <h2>📌 IDS Events (most recent)</h2>
    <table>
        <tr>
            <th>ID</th><th>Source IP</th><th>Event</th><th>Details</th><th>Timestamp (UTC)</th>
        </tr>
        {% for row in events %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td>{{ row[4] }}</td>
        </tr>
        {% endfor %}
    </table>

    <h2>🚫 Blocked IPs</h2>
    <table>
        <tr>
            <th>IP Address</th><th>Blocked At (UTC)</th><th>Action</th>
        </tr>
        {% for ip, ts in blocked_ips %}
        <tr>
            <td class="blocked">{{ ip }}</td>
            <td>{{ ts }}</td>
            <td><a class="button" href="{{ url_for('unblock', ip=ip) }}">Unblock</a></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# =============================
# Routes
# =============================
@app.route("/")
def index():
    # Auto-unblock expired IPs
    unblock_expired_ips()

    # Fetch IDS events
    events = fetch_events(limit=20)

    # Fetch blocked IPs with timestamps
    blocked_ips = fetch_blocked_ips()  # Returns list of tuples: (ip, blocked_at)
    return render_template_string(TEMPLATE, events=events, blocked_ips=blocked_ips)

@app.route("/unblock/<ip>")
def unblock(ip):
    unblock_ip(ip)
    return redirect(url_for("index"))

# =============================
# Run Flask App
# =============================
if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)

