import subprocess
import requests

# For the iPhone
def send_ntfy(message, topic="daily-paperwatch"):
    # Make sure you subscribe to topic
    requests.post(f"https://ntfy.sh/{topic}", data=message.encode())

# For the Mac
def mac_notify(title, message):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])

