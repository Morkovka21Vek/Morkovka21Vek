from qtile_extras.popup import (
    PopupRelativeLayout,
    PopupImage,
    PopupText
)
import subprocess
import os

def get_wifi_status():
    try:
        wifi = subprocess.check_output("iwgetid -r", shell=True).decode().strip()
        return f"📶 {wifi}"
    except:
        return "❌ Wi-Fi"

def show_wifi_con(qtile):
    try:
        wifi = subprocess.check_output("iwgetid -r", shell=True).decode().strip()
        strength = subprocess.check_output(
            "awk 'NR==3 {print $3}' /proc/net/wireless", shell=True
        ).decode().strip()
        os.system(f"notify-send  -t 2000 -u normal \"📶 Wi-Fi\" \"strength: {strength}\"")
    except:
        os.system(f"notify-send  -t 2000 -u normal \"❌ Wi-Fi\"")
