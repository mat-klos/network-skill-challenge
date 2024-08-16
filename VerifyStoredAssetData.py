import psycopg2
import nmap
import pytest

def get_device_data_from_db():
    try:
        conn = psycopg2.connect(
            dbname="network_assets",
            user="postgres",
            password="mysecretpassword",
            host="db",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT ip_address, mac_address, vendor_name FROM assets")
        device_data = cur.fetchall()
        cur.close()
        conn.close()
        return device_data
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

def scan_device_with_nmap(ip_address):
    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=ip_address, arguments='-sP')

        scanned_ip = ip_address
        mac_address = None
        vendor_name = None

        if ip_address in nm.all_hosts():
            if 'mac' in nm[ip_address]['addresses']:
                mac_address = nm[ip_address]['addresses']['mac']
                vendor_name = nm[ip_address]['vendor'].get(mac_address)

        return scanned_ip, mac_address, vendor_name
    except nmap.PortScannerError as e:
        print(f"Nmap scan error: {e}", file=sys.stderr)
        return ip_address, None, None
    except Exception as e:
        print(f"Unexpected error during nmap scan: {e}", file=sys.stderr)
        return ip_address, None, None
    
try:
    device_data_list = get_device_data_from_db()
    test_cases = [pytest.param(data, id=data[0]) for data in device_data_list]    
except Exception as e:
    print(f"Error preparing test cases: {e}", file=sys.stderr)
    sys.exit(1)  
    
@pytest.mark.parametrize("device_data", test_cases)
def test_device_data(device_data):
    db_ip_address, db_mac_address, db_vendor_name = device_data

    scanned_ip, scanned_mac_address, scanned_vendor_name = scan_device_with_nmap(db_ip_address)

    assert db_ip_address == scanned_ip
    assert db_mac_address == scanned_mac_address
    assert db_vendor_name == scanned_vendor_name
