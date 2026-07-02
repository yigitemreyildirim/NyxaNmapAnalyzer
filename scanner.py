import nmap

def run_network_scan(target_ip):
    """
    Performs a fast port and service version scan on the specified target IP.
    """
    # Initialize the Nmap PortScanner object
    nm = nmap.PortScanner()
    
    # -sV: Determine service/version info (Crucial for vulnerability analysis)
    # -F: Fast mode - Scan fewer ports than the default scan (Top 100 ports)
    print(f"\n[*] Launching Nmap scan for {target_ip}...")
    nm.scan(target_ip, arguments='-sV -F')
    
    scan_results = ""
    
    # Iterate through discovered hosts
    for host in nm.all_hosts():
        scan_results += f"=== TARGET: {host} ===\n"
        scan_results += f"Status: {nm[host].state()}\n"
        
        # Check if OS detection returned any matches
        if 'osmatch' in nm[host] and nm[host]['osmatch']:
            scan_results += f"Estimated OS: {nm[host]['osmatch'][0]['name']}\n"
            
        # Iterate through scanned protocols
        for proto in nm[host].all_protocols():
            scan_results += f"\nProtocol: {proto.upper()}\n"
            ports = nm[host][proto].keys()
            
            # Extract details for each port
            for port in ports:
                port_data = nm[host][proto][port]
                state = port_data['state']
                service = port_data['name']
                product = port_data.get('product', '')
                version = port_data.get('version', '')
                
                scan_results += f"  - Port {port}/{proto}: {state} | Service: {service} | Product: {product} {version}\n"
                
    return scan_results

if __name__ == "__main__":
    # Self-test using localhost
    test_output = run_network_scan("127.0.0.1")
    print(test_output)