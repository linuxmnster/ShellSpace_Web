import subprocess
import os
import urllib.request
import stat
import platform

def download_cloudflared():
    url = "https://github.com/cloudflare/cloudflared/releases/latest/download/"
    system = platform.system().lower()
    arch = "amd64"

    if system == "windows":
        url += "cloudflared-windows-amd64.exe"
        filename = "cloudflared.exe"
    elif system == "linux":
        url += "cloudflared-linux-amd64"
        filename = "cloudflared"
    elif system == "darwin":
        url += "cloudflared-darwin-amd64"
        filename = "cloudflared"
    else:
        raise Exception("Unsupported OS")

    print("⬇️ Downloading Cloudflared...")
    urllib.request.urlretrieve(url, filename)
    os.chmod(filename, stat.S_IRWXU)
    return filename

def run_tunnel():
    print("🚇 Starting Cloudflare Tunnel...")
    bin = download_cloudflared() if not os.path.exists("cloudflared") else "cloudflared"
    proc = subprocess.Popen([bin, "tunnel", "--url", "http://localhost:5000"],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    for line in proc.stdout:
        if "trycloudflare.com" in line:
            print(f"\n🔗 Public URL: {line.strip().split(' ')[-1]}")
            break

if __name__ == "__main__":
    run_tunnel()
