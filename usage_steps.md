````markdown
# 🚀 Biometric Attendance Sync Tool Setup and Execution

This document provides the necessary steps to set up the Python environment, install dependencies, and run the `erpnext_sync.py` script to synchronize attendance logs from a biometric device (ZK-compatible) to an ERPNext instance.

## 1. Environment Setup

### A. Create the Virtual Environment

It's recommended to use a virtual environment to isolate project dependencies.

```bash
python3 -m venv .venv
```
````

### B. Activate the Virtual Environment

You must activate the environment before installing packages or running the script.

```bash
source .venv/bin/activate
```

---

## 2\. Dependency Installation

Install the required Python packages using `pip`. The `pyzk` package is used for communicating with ZK biometric devices, and `requests` is used for the ERPNext API calls.

```bash
pip install requests pickledb pyzk
```

---

## 3\. Configuration and Pre-Requisites

### A. Create and Configure `local_config.py`

You **must** create a file named **`local_config.py`** in the same directory as `erpnext_sync.py`. This file holds all your ERPNext credentials and device details.

**Example `local_config.py` Content:**

```python
# --- Example of necessary settings in local_config.py ---

# ERPNext API Credentials
ERPNEXT_URL = "[http://your-erpnext-site.com](http://your-erpnext-site.com)"
ERPNEXT_API_KEY = "YOUR_API_KEY"
ERPNEXT_API_SECRET = "YOUR_API_SECRET"

# Sync Settings
PULL_FREQUENCY = 5  # Time in minutes to wait between full sync cycles
LOGS_DIRECTORY = "logs"  # Directory to store logs and status files
IMPORT_START_DATE = "20240101" # Start date for historical import (Format YYYYMMDD)
ERPNEXT_VERSION = 14 # Adjust if you are using ERPNext v15 or later

# Device Configuration
devices = [
    {
        'device_id': 'HO1',
        'ip': '192.168.100.178',
        'clear_from_device_on_fetch': False, # Set to True to delete logs from device after successful pull
        'punch_direction': 'AUTO', # 'AUTO', 'IN', or 'OUT'
        'latitude': None, # Set for geo-location check-in (ERPNext v15+)
        'longitude': None
    },
    # Add more devices here...
]

# Optional: List of errors to ignore when pushing to ERPNext
# 1: Not Found, 2: Inactive, 3: Duplicate
allowed_exceptions = [1, 2, 3]
```

### B. Network Connectivity Test

Ensure your machine can reach the biometric device before attempting to run the script:

```bash
ping 192.168.100.178
```

---

## 4\. Execution

Run the script while your virtual environment (`.venv`) is active.

```bash
python erpnext_sync.py
```

The script will run in an infinite loop, performing synchronization based on the `PULL_FREQUENCY` defined in `local_config.py`.

---

## 5\. Script Termination

### A. Primary Termination ($\text{Ctrl} + \text{C}$)

Press **$\text{Ctrl} + \text{C}$** (Control + C) to send an interrupt signal and gracefully stop the running script.

### B. Suspend and Kill ($\text{Ctrl} + \text{Z}$)

If $\text{Ctrl} + \text{C}$ does not work, you can suspend the script and then terminate it:

1.  Press **$\text{Ctrl} + \text{Z}$** to **suspend** the process and send it to the background.

2.  Once suspended (you'll see a message like `[1] + Stopped`), run the following command to kill the background job:

    ```bash
    kill %1
    ```

    > **Note:** `%1` refers to the job ID of the process that was most recently stopped/suspended.

---

## 6\. Optional: Deactivate the Virtual Environment

When you are finished working in this environment:

```bash
deactivate
```

```

```
