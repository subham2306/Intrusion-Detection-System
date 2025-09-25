Intrusion Detection System (IDS)
A Python-based Intrusion Detection System (IDS) that monitors network/system activity, detects suspicious behavior, and alerts users of potential security threats. This project is designed for learning, cybersecurity practice, and lightweight real-world monitoring.
🔥 Features
📡 Traffic Monitoring – Capture and analyze packets/logs.
🛡️ Anomaly Detection – Identify unusual or suspicious activities.
⚡ Signature-Based Detection – Match patterns against known attack signatures.
🔍 Log Analysis – Parse system and application logs for intrusion attempts.
📈 Visualization – Generate reports and charts for detected threats.
🔔 Alerts – Get notified when malicious activity is found.

🛠️ Tech Stack
Programming: Python
Libraries: Scapy, Pandas, Matplotlib, Regex
Database: SQLite (for storing detected events)
OS Support: Linux / Windows


# Intrusion Detection & Threat Intelligence (lab)

## Prereqs
- Ubuntu/Kali VM (has pip3, sudo)
- Run as root for capture and iptables actions.
- Install requirements: pip3 install -r requirements.txt

## Steps to run
1. Initialize DB (optional): python3 db.py
2. Start the capture + detector pipeline (in a terminal with sudo): sudo python3 capture.py
3. Run the Project: python3 app.py
4. View the Result: localhost:5000/

## Step to attack from a attacker machine
1. nmap -p- -T4 server ip adreess (ex- nnmap -p- -T4 192.168.150.163)


   

