Assuming you have confirmed the script is working correctly by checking your logs and seeing check-ins appear in ERPNext, the final step is to make it run permanently in the background.

This way, it will run 24/7 and automatically restart if your server reboots. The best way to do this on a modern Linux server is by creating a `systemd` service.

Here’s how:

### 1\. Stop the Running Script

Go to the terminal where the script is running and press **`Ctrl+C`** to stop it.

### 2\. Get Your Full Directory Path

You need the absolute path to your script. In your `biometric-attendance-sync-tool` directory, run this command:

```bash
pwd
```

It will output something like `/home/axmed/biometric-attendance-sync-tool`. **Copy this path.**

### 3\. Create the Service File

Now, create a new service file using a text editor like `nano`:

```bash
sudo nano /etc/systemd/system/biometric-sync.service
```

### 4\. Paste the Service Configuration

Paste the following text into the editor.

**You must change** the `User` and `WorkingDirectory` lines to match your system.

```ini
[Unit]
Description=Biometric Attendance Sync Service
After=network.target

[Service]
# Change this to your username
User=axmed

# Change this to the path you copied in Step 2
WorkingDirectory=/home/axmed/biometric-attendance-sync-tool

# This is the command that runs your script
ExecStart=/usr/bin/python3 erpnext_sync.py

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

To save and exit in `nano`:

1.  Press **`Ctrl+O`** (Write Out) and then **`Enter`** to save.
2.  Press **`Ctrl+X`** to exit.

### 5\. Start and Enable the Service

Now you just need to tell `systemd` to load, start, and enable your new service.

1.  **Reload systemd:**
    ```bash
    sudo systemctl daemon-reload
    ```
2.  **Enable the service** (so it starts on boot):
    ```bash
    sudo systemctl enable biometric-sync.service
    ```
3.  **Start the service** (to run it right now):
    ```bash
    sudo systemctl start biometric-sync.service
    ```

### 6\. Check the Service Status

Your script is now running in the background. You can check its status at any time with this command:

```bash
sudo systemctl status biometric-sync.service
```

You should see a green "active (running)" status.

To see the live logs from your service (the same output you saw in your terminal before), you can run:

```bash
journalctl -u biometric-sync.service -f
```

(Press `Ctrl+C` to stop viewing the logs).

That's it\! Your integration is now complete and will run automatically.