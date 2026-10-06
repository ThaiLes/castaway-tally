import socket
import time
from datetime import datetime

ESP32_IP = "192.168.1.100"
ESP32_PORT = 9100

# Dynamically generate current timestamp (e.g. "01/10/2026 11:15 am")
now_timestamp = datetime.now().strftime("%d/%m/%Y %I:%M %p").lower()

ESC_INIT = b'\x1b\x40'
ESC_ALIGN_CENTER = b'\x1b\x61\x01'
ESC_ALIGN_LEFT = b'\x1b\x61\x00'
ESC_CUT = b'\x1d\x56\x42\x00'

# CHARGE Receipt (Paid)
CHARGE_STREAM = (
    ESC_INIT + ESC_ALIGN_CENTER +
    b"RECEIPT\n\n"
    b"Castaway beach bar\n"
    b"18 Moo 6 Hinkong Koh Phangan Thailand 84280\n"
    b"Tel.092-420-8353\n\n" +
    ESC_ALIGN_LEFT +
    b"Order: 01\n"
    b"Employee: Fa\n"
    b"POS: POS 1\n"
    b"------------------------------------------\n"
    b"Dine in\n"
    b"------------------------------------------\n"
    b"Cappucino (hot)                          B180.00\n"
    b"2 x B90.00\n"
    b"Water                                     B40.00\n"
    b"1 x B40.00\n"
    b"Pancake,Scrambled eggs and bacon          B500.00\n"
    b"2 x B250.00\n"
    b"Orange Espresso                           B120.00\n"
    b"1 x B120.00\n"
    b"------------------------------------------\n"
    b"Total                                    B840.00\n"
    b"Cash                                     B840.00\n"
    b"------------------------------------------\n" +
    ESC_ALIGN_CENTER +
    b"WiFi Name : AIS CASTAWAY BEACH BAR\n"
    b"Password: i8coconuts\n"
    b"********** THANK YOU ! **********\n\n" +
    ESC_ALIGN_LEFT +
    f"{now_timestamp}                     #6-9014\n".encode('utf-8') +
    ESC_CUT
)

# BILL Receipt (Pre-Bill)
BILL_STREAM = (
    ESC_INIT + ESC_ALIGN_CENTER +
    b"RECEIPT\n\n"
    b"Castaway beach bar\n"
    b"18 Moo 6 Hinkong Koh Phangan Thailand 84280\n"
    b"Tel.092-420-8353\n\n"
    b"BILL\n\n" +
    ESC_ALIGN_LEFT +
    b"Order: Ticket - 9:48 am\n"
    b"Employee: Fa\n"
    b"POS: POS 1\n"
    b"------------------------------------------\n"
    b"Dine in\n"
    b"------------------------------------------\n"
    b"Leo                           B240.00\n"
    b"3 x B80.00\n"
    b"------------------------------------------\n"
    b"Amount due                               B140.00\n"
    b"------------------------------------------\n" +
    ESC_ALIGN_CENTER +
    b"WiFi Name : AIS CASTAWAY BEACH BAR\n"
    b"Password: i8coconuts\n"
    b"********** THANK YOU ! **********\n\n" +
    ESC_ALIGN_LEFT +
    f"{now_timestamp}\n".encode('utf-8') +
    ESC_CUT
)

def send_pos_burst(job_name, data_buffer):
    print(f"\n[Simulator] Connecting to ESP32 at {ESP32_IP}:{ESP32_PORT}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ESP32_IP, ESP32_PORT))
        
        print(f"[Simulator] Sending '{job_name}' stream ({len(data_buffer)} bytes)...")
        sock.sendall(data_buffer)
        
        time.sleep(0.2)
        sock.close()
        print(f"[Simulator] SUCCESS: Sent '{job_name}' burst.\n")
        
    except Exception as e:
        print(f"[Simulator Error] {e}\n")

if __name__ == "__main__":
    print("=== LOYVERSE TEST SIMULATOR ===")
    print("1. Send CHARGE Receipt (Paid - B840.00)")
    print("2. Send BILL Receipt   (Pre-bill - B140.00)")
    
    choice = input("\nSelect (1 or 2): ").strip()
    
    if choice == '1':
        send_pos_burst("CHARGE", CHARGE_STREAM)
    elif choice == '2':
        send_pos_burst("BILL", BILL_STREAM)
    else:
        print("Invalid selection.")