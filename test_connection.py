from zk import ZK, const

device_ip = '192.168.100.178' # The IP of your device
device_port = 4370             # The port you provided

zk = ZK(device_ip, port=device_port, timeout=10)
conn = None
try:
    print(f"Attempting to connect to {device_ip}:{device_port}...")
    conn = zk.connect()
    print("\nConnection SUCCESSFUL!")

    # Get some info to confirm it's working
    serial_number = conn.get_serialnumber()
    print(f"Device Serial Number: {serial_number}")

except Exception as e:
    print(f"\nConnection FAILED: {e}")
finally:
    if conn:
        conn.disconnect()
        print("Disconnected.")