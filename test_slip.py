"""
Castaway slip tester.

Posts the same rawHex the ESP32 posts to the live Apps Script.
Use this before deploying a script change. Delete the test rows after.

  python test_slip.py              sample bill
  python test_slip.py muffin       wrapped muffin line
  python test_slip.py extra        Extra attached to food
  python test_slip.py bbq          BBQ shack slip
  python test_slip.py charge       CHARGE slip
  python test_slip.py paste        paste a real slip, then a blank line
"""
import sys
import time
import urllib.parse
import urllib.request

URL = "https://script.google.com/macros/s/AKfycbxSySBORWg8hOuiboEEHDY_EaryuyEwuDBerK8_iqeJnE7u67xcTYWguhFqXDMx5jOe/exec"

def slip(kind):
    stamp = time.strftime("%d/%m/%Y %I:%M %p").lower()
    order = "TEST" + str(int(time.time()))[-4:]
    head = "@@t!! Castaway beach bar ! 18 Moo 6 Hinkong Koh Phangan Thailand 84280 Tel.092-420-8353 BILL Order: " + order + " Employee: Fa POS: POS 1 - - - - - - - - - - - - - - - - - - - - - - - -Dine in - - - - - - - - - - - - - - - - - - - - - - - -"
    foot = " - - - - - - - - - - - - - - - - - - - - - - - - WiFi Name : AIS CASTAWAY BEACH BAR Password: i8coconuts ********** THANK YOU ! ********** " + stamp + " dVB"
    if kind == "muffin":
        body = "Fresh Coconuts 100.001 x 100.00 Breakfast Muffins (avocado egg 250.00cheese) 1 x 250.00 Buffalo chicken wings 300.002 x 150.00 !Amount due 650.00!"
    elif kind == "extra":
        body = "Pad Thai (Chicken) 180.001 x 180.00 Extra 70.001 x 0.00 + Chicken (70.00) Soda 60.001 x 60.00 !Amount due 310.00!"
    elif kind == "bbq":
        body = "BBQ-Chimichurri dog chicken 220.001 x 220.00 BBQ-Pork rib 180.001 x 180.00 !Amount due 400.00!"
        head = head.replace("Castaway beach bar", "BBQ shack")
    elif kind == "charge":
        body = "Latte (Iced) 100.001 x 100.00 !Total 100.00! Cash 100.00"
        head = head.replace(" BILL ", " ")
    else:
        body = "Americano (hot) 80.001 x 80.00 Soda 180.003 x 60.00 Leo 270.003 x 90.00 !Amount due 530.00!"
    return head + body + foot

def send(text):
    data = urllib.parse.urlencode({"rawHex": text.encode("latin-1", "replace").hex()}).encode()
    req = urllib.request.Request(URL, data=data)
    with urllib.request.urlopen(req, timeout=90) as resp:
        print(resp.status)
        print(resp.read().decode("utf-8", "replace")[:800])

if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv) > 1 else "sample"
    if kind == "paste":
        print("Paste a slip, then a blank line.")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        text = " ".join(lines)
    else:
        text = slip(kind)
    print("Sending", kind)
    send(text)
