# utils.py
from scapy.all import IP, TCP, UDP
from datetime import datetime

def pkt_to_record(pkt):
    rec = {}
    if IP in pkt:
        rec['src'] = pkt[IP].src
        rec['dst'] = pkt[IP].dst
        rec['proto'] = pkt[IP].proto
        rec['ts'] = datetime.utcnow().isoformat()
        if TCP in pkt:
            rec['sport'] = pkt[TCP].sport
            rec['dport'] = pkt[TCP].dport
            flags = pkt[TCP].flags
            rec['flags'] = str(flags)
        elif UDP in pkt:
            rec['sport'] = pkt[UDP].sport
            rec['dport'] = pkt[UDP].dport
        else:
            rec['sport'] = None
            rec['dport'] = None
    else:
        return None
    return rec

