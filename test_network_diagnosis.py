import socket
import requests
import subprocess
import os

def network_diagnosis(ip):
    print(f"🔍 Comprehensive Network Diagnosis for {ip}")
    print("=" * 60)
    
    # Test 1: Basic ping
    print("1. Testing basic connectivity (ping)...")
    try:
        result = subprocess.run(['ping', '-c', '3', ip], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("   ✅ Device is reachable via ping")
        else:
            print("   ❌ Device is not reachable via ping")
            print(f"   Ping output: {result.stdout}")
    except Exception as e:
        print(f"   ❌ Ping test failed: {e}")
    
    # Test 2: Port scan for common biometric ports
    print("\n2. Scanning common biometric device ports...")
    common_ports = [4370, 80, 8080, 5005, 5006, 5010]
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                print(f"   ✅ Port {port} is OPEN")
            else:
                print(f"   ❌ Port {port} is closed")
        except Exception as e:
            print(f"   ❌ Port {port} test failed: {e}")
    
    # Test 3: Check local network configuration
    print("\n3. Checking local network configuration...")
    try:
        # Get default gateway
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        print(f"   Network routes:\n{result.stdout}")
    except Exception as e:
        print(f"   ❌ Network config check failed: {e}")
    
    # Test 4: Check if IP is in same subnet
    print("\n4. Checking subnet compatibility...")
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
        print(f"   Your IP: {host_ip}")
        print(f"   Device IP: {ip}")
        
        # Simple subnet check (first 2 octets)
        host_subnet = '.'.join(host_ip.split('.')[:2])
        device_subnet = '.'.join(ip.split('.')[:2])
        
        if host_subnet == device_subnet:
            print("   ✅ IP addresses appear to be in same subnet")
        else:
            print("   ⚠️  IP addresses may be in different subnets")
    except Exception as e:
        print(f"   ❌ Subnet check failed: {e}")

def test_erpnext_detailed():
    print("\n🔍 Detailed ERPNext Connection Test")
    print("=" * 60)
    
    erpnext_url = "http://104.251.212.107"
    
    # Test different endpoints
    endpoints = [
        "/api/method/version",
        "/",
        "/api/method/frappe.auth.get_logged_user"
    ]
    
    for endpoint in endpoints:
        url = erpnext_url + endpoint
        print(f"\nTesting: {url}")
        
        try:
            response = requests.get(url, timeout=10, verify=False)
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Endpoint accessible")
                if "version" in endpoint:
                    try:
                        data = response.json()
                        print(f"   ERPNext Version: {data.get('message', {}).get('version', 'Unknown')}")
                    except:
                        print("   ✅ Endpoint working (could not parse version)")
            elif response.status_code == 417:
                print("   ⚠️  Status 417 - Expectation Failed (API might need specific headers)")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.ConnectTimeout:
            print("   ❌ Connection timeout")
        except requests.exceptions.ConnectionError:
            print("   ❌ Connection refused - server might be down or URL incorrect")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def check_firewall_and_permissions():
    print("\n🔍 Checking System Configuration")
    print("=" * 60)
    
    # Check if we can bind to sockets (permission test)
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(('0.0.0.0', 0))
        test_socket.close()
        print("✅ Socket binding test passed")
    except PermissionError:
        print("❌ Permission denied for socket operations")
    except Exception as e:
        print(f"⚠️  Socket test issue: {e}")
    
    # Check current directory and permissions
    print(f"Current directory: {os.getcwd()}")
    print(f"Directory writable: {os.access('.', os.W_OK)}")

if __name__ == "__main__":
    print("COMPREHENSIVE DIAGNOSTIC TOOL")
    print("=" * 60)
    
    device_ip = "172.20.1.222"
    
    # Run diagnostics
    network_diagnosis(device_ip)
    test_erpnext_detailed()
    check_firewall_and_permissions()
    
    print("\n" + "=" * 60)
    print("RECOMMENDED NEXT STEPS:")
    print("1. If device is not pingable: Check physical network connection")
    print("2. If all ports are closed: Device might be on different VLAN/network")
    print("3. For ERPNext 417 error: Verify API credentials and URL")
    print("4. Contact network administrator for device accessibility")