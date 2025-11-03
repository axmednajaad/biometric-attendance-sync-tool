import socket
from zk import ZK, const
import requests

def comprehensive_device_test(ip, port=4370):
    print(f"🔍 Testing biometric device at {ip}:{port}")
    print("=" * 50)
    
    # Test 1: Basic network connectivity
    print("1. Testing network connectivity...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            print("   ✅ Port 4370 is open and accessible")
        else:
            print("   ❌ Port 4370 is closed or blocked")
            return False
    except Exception as e:
        print(f"   ❌ Network test failed: {e}")
        return False
    
    # Test 2: ZK Protocol connection
    print("2. Testing ZK protocol connection...")
    zk = ZK(ip, port=port, timeout=10)
    conn = None
    try:
        conn = zk.connect()
        print("   ✅ ZK protocol connection successful")
        
        # Test 3: Device information
        print("3. Fetching device information...")
        try:
            device_name = conn.get_device_name()
            print(f"   ✅ Device Name: {device_name}")
        except:
            print("   ⚠️  Could not fetch device name")
        
        # Test 4: Firmware version
        try:
            firmware = conn.get_firmware_version()
            print(f"   ✅ Firmware Version: {firmware}")
        except:
            print("   ⚠️  Could not fetch firmware version")
        
        # Test 5: Platform info
        try:
            platform = conn.get_platform()
            print(f"   ✅ Platform: {platform}")
        except:
            print("   ⚠️  Could not fetch platform info")
        
        # Test 6: Serial number
        try:
            serial = conn.get_serialnumber()
            print(f"   ✅ Serial Number: {serial}")
        except:
            print("   ⚠️  Could not fetch serial number")
        
        # Test 7: Attendance data
        print("4. Testing attendance data access...")
        try:
            attendances = conn.get_attendance()
            print(f"   ✅ Found {len(attendances)} attendance records")
            
            if attendances:
                # Show recent records
                recent = sorted(attendances, key=lambda x: x.timestamp, reverse=True)[:3]
                print("   Recent records:")
                for att in recent:
                    print(f"     - User: {att.user_id}, Time: {att.timestamp}, Punch: {att.punch}")
        except Exception as e:
            print(f"   ⚠️  Attendance access issue: {e}")
        
        # Test 8: User data
        print("5. Testing user data access...")
        try:
            users = conn.get_users()
            print(f"   ✅ Found {len(users)} users")
            
            if users:
                # Show some users
                sample_users = users[:3]
                print("   Sample users:")
                for user in sample_users:
                    print(f"     - ID: {user.user_id}, Name: {user.name}")
        except Exception as e:
            print(f"   ⚠️  User access issue: {e}")
        
        conn.disconnect()
        print("\n🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ ZK connection failed: {e}")
        return False

def test_erpnext_connection():
    print("\n🔍 Testing ERPNext connection...")
    print("=" * 50)
    
    try:
        # Test ERPNext API connectivity
        url = "http://104.251.212.107/api/method/version"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ ERPNext API is accessible")
            return True
        else:
            print(f"❌ ERPNext API returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERPNext connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Biometric Device Diagnostic Tool")
    print("=" * 50)
    
    # Test biometric device
    device_ok = comprehensive_device_test('172.20.1.222')
    
    # Test ERPNext
    erpnext_ok = test_erpnext_connection()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Biometric Device: {'✅ OK' if device_ok else '❌ FAILED'}")
    print(f"ERPNext Connection: {'✅ OK' if erpnext_ok else '❌ FAILED'}")
    
    if device_ok and erpnext_ok:
        print("\n🎉 All systems are ready for integration!")
    else:
        print("\n⚠️  Some components need attention")