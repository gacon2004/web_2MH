import os
import paramiko

HOST = "103.38.236.207"
USER = "root"
PASS = "25Q*I!$SBuK&"
REMOTE_DIR = "/var/www/2mhgroup"

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = [
    ("index.html", "index.html"),
    ("logo-2mh-icon.png", "logo-2mh-icon.png"),
    ("logo-2mh-badge.png", "logo-2mh-badge.png"),
    ("logo-2mh.png", "logo-2mh.png"),
    ("hero-work.jpg", "hero-work.jpg"),
    ("team-collab.jpg", "team-collab.jpg"),
    ("ui-design.jpg", "ui-design.jpg"),
]

def main():
    print(f"Connecting to {HOST}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASS, timeout=15)
    
    sftp = ssh.open_sftp()
    for local_name, remote_name in FILES:
        local_path = os.path.join(LOCAL_DIR, local_name)
        remote_path = f"{REMOTE_DIR}/{remote_name}"
        print(f"Uploading {local_path} -> {remote_path}...")
        sftp.put(local_path, remote_path)
    
    sftp.close()
    print("Files uploaded successfully!")

    print("Reloading Nginx...")
    stdin, stdout, stderr = ssh.exec_command("systemctl reload nginx && ls -la /var/www/2mhgroup")
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    print("Output:\n", out)
    if err:
        print("Error:\n", err)
    
    ssh.close()
    print("Deployment finished!")

if __name__ == "__main__":
    main()
