# capture.py
from scapy.all import sniff
import json
from detector import detect_and_block
from utils import pkt_to_record   # ✅ now imported from utils

def process_pkt(pkt):
    rec = pkt_to_record(pkt)
    if rec:
        # Print packet JSON (for logging/debug)
        print(json.dumps(rec), flush=True)
        # Pass packet to detector for analysis/blocking
        detect_and_block(pkt)

if __name__ == "__main__":
    print("[INFO] Starting packet capture for IDS...")
    # sniff all interfaces; on Linux you might need sudo
    sniff(prn=process_pkt, store=False)

