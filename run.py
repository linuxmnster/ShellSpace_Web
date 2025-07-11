import os
import sys
import subprocess
import threading
import time
import webbrowser
import urllib.request
import platform
import stat
import argparse

# === CLI Argument ===
parser = argparse.ArgumentParser(description="ShellSpace Chatroom Launcher")
parser.add_argument('--key', help="Set or override the Flask secret key")
args = parser.parse_args()

SECRET_FILE = "secret_key.txt"

# === Secret Key Handling ===
def get_or_set_secret():
    if args.key:
        with open(SECRET_FILE, "w") as f:
            f.write(args.key)
        print(f"✅ Secret key overridden and saved to {SECRET_FILE}")
        return args.key

    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "r") as f:
            return f.read().strip()

    key = input("🔑 Enter a new Flask secret key (one-time setup): ").strip()
    with open(SECRET_FILE, "w") as f:
        f.write(key)
    return key

# === Install required packages ===
required = ["flask", "flask_socketio", "eventlet"]
for pkg in required:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

from app import create_app, socketio

# === Launch Flask App ===
def run_server(secret_key):
    app = create_app()
    app.secret_key = secret_key
    socketio.run(app, host="0.0.0.0", port=5000)

# === Cloudflare Tunnel Setup ===
def download_cloudflared():
    system = platform.system().lower()
    url = "https://github.com/cloudflare/cloudflared/releases/latest/download/"
    arch = "amd64"

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

    print("⬇️ Downloading cloudflared...")
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

# === Main ===
if __name__ == "__main__":
    secret_key = get_or_set_secret()
    threading.Thread(target=lambda: run_server(secret_key), daemon=True).start()
    time.sleep(2)
    run_cloudflare()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Exiting ShellSpace.")
