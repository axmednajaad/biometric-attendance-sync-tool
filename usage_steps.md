# 🚀 Biometric Attendance Sync Tool Setup and Execution

This document provides the necessary steps to set up the Python environment, install dependencies, and run the `erpnext_sync.py` script to synchronize attendance logs from a biometric device (ZK-compatible) to an ERPNext instance.

## 1. Environment Setup

It's recommended to use a virtual environment to isolate project dependencies.

```bash
python3 -m venv .venv
```

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

# ERPNext related configs
ERPNEXT_API_KEY = '393fa5b4664cad4'
ERPNEXT_API_SECRET = '84f6e23ebe02f08'
ERPNEXT_URL = 'http://104.251.212.107'
ERPNEXT_VERSION = 15


# operational configs
PULL_FREQUENCY = 10 # in minutes
LOGS_DIRECTORY = 'logs' # logs of this script is stored in this directory
IMPORT_START_DATE = None # format: '20190501'

# Biometric device configs (all keys mandatory, except latitude and longitude they are mandatory only if 'Allow Geolocation Tracking' is turned on in Frappe HR)
    #- device_id - must be unique, strictly alphanumerical chars only. no space allowed.
    #- ip - device IP Address
    #- punch_direction - 'IN'/'OUT'/'AUTO'/None
    #- clear_from_device_on_fetch: if set to true then attendance is deleted after fetch is successful.
                                    #(Caution: this feature can lead to data loss if used carelessly.)
    #- latitude - float, latitude of the location of the device
    #- longitude - float, longitude of the location of the device
devices = [
    {
        'device_id': 'zkt_office',
        # 'ip': '172.20.1.222',
        'ip': '192.168.100.178',
        'punch_direction': 'AUTO',
        'clear_from_device_on_fetch': False,
        'latitude': 0.0000,
        'longitude': 0.0000
    }
]


# Configs updating sync timestamp in the Shift Type DocType
# please, read this thread to know why this is necessary https://discuss.erpnext.com/t/v-12-hr-auto-attendance-purpose-of-last-sync-of-checkin-in-shift-type/52997
shift_type_device_mapping = [
    {
        'shift_type_name': ['Full Time'],
        'related_device_id': ['zkt_office']
    }
]


# Ignore following exceptions thrown by ERPNext and continue importing punch logs.
# Note: All other exceptions will halt the punch log import to erpnext.
#       1. No Employee found for the given employee User ID in the Biometric device.
#       2. Employee is inactive for the given employee User ID in the Biometric device.
#       3. Duplicate Employee Checkin found. (This exception can happen if you have cleared the logs/status.json of this script)
# Use the corresponding number to ignore the above exceptions. (Default: Ignores all the listed exceptions)
allowed_exceptions = [1,2,3]
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
