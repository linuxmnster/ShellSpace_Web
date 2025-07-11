import os
import sys
import subprocess
import threading
import time
import webbrowser
import urllib.request
import platform
import stat

# --- Auto install required packages ---
required = ["flask", "flask_socketio", "eventlet"]
for pkg in required:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

from app import create_app, socketio

# --- Launch Flask app ---
def run_server():
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=5000)

# --- Download + Run Cloudflared ---
def download_cloudflared():
    system = platform.system().lower()
    arch = "amd64"
    url = "https://github.com/cloudflare/cloudflared/releases/latest/download/"

    if "win" in system:
        url += "cloudflared-windows-amd64.exe"
        filename = "cloudflared.exe"
    elif "linux" in system:
        url += "cloudflared-linux-amd64"
        filename = "cloudflared"
    elif "darwin" in system:
        url += "cloudflared-darwin-amd64"
        filename = "cloudflared"
    else:
        print("Unsupported OS")
        sys.exit(1)

    print("📡 Downloading cloudflared...")
    urllib.request.urlretrieve(url, filename)
    os.chmod(filename, stat.S_IRWXU)
    return filename

def run_cloudflare():
    exe = "./cloudflared" if os.path.exists("cloudflared") else download_cloudflared()
    proc = subprocess.Popen([exe, "tunnel", "--url", "http://localhost:5000"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True)

    for line in proc.stdout:
        if "trycloudflare.com" in line:
            public_url = line.strip().split()[-1]
            print(f"\n🌐 Public Chat URL: {public_url}")
            webbrowser.open(public_url)
            break

# --- Main Startup ---
if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    time.sleep(2)
    run_cloudflare()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
