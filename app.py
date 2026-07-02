import os
from scanner import run_network_scan
from ai_analyser import analyze_nmap_report

def save_report_to_file(target, report_content):
    """
    Saves the generated AI analysis report into a clean Markdown (.md) file.
    """
    clean_target = target.replace(".", "_").replace("/", "_")
    filename = f"scan_report_{clean_target}.md"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"\n[+] Professional report successfully saved to: {filename}")
    except Exception as e:
        print(f"\n[-] Error saving report to file: {str(e)}")

def main():
    print("="*50)
    print("       NYXA AI-POWERED NMAP ANALYZER       ")
    print("="*50)
    
    # Step 1: Get Target IP/Domain from user
    target_host = input("[?] Enter Target IP or Domain to scan: ").strip()
    
    if not target_host:
        print("[-] Target cannot be empty! Exiting...")
        return
        
    # Step 2: Trigger the Nmap scan module
    try:
        raw_data = run_network_scan(target_host)
        
        if not raw_data or "=== TARGET:" not in raw_data:
            print("[-] No open ports or hosts found. Make sure the target is up.")
            return
            
        print("\n--- RAW NMAP SCAN RESULTS ---")
        print(raw_data)
        print("-" * 30)
        
    except Exception as e:
        print(f"[-] An error occurred during Nmap scan: {str(e)}")
        print("[!] Tip: Make sure Nmap is installed on your OS and added to PATH.")
        return

    # Step 3: Trigger the Local AI analysis module
    ai_report = analyze_nmap_report(raw_data, model_name="llama3")
    
    print("\n" + "="*50)
    print("         AI PENETRATION TESTING REPORT        ")
    print("="*50)
    print(ai_report)
    print("="*50)
    
    # Step 4: Save the final markdown report
    if "Error:" not in ai_report:
        save_report_to_file(target_host, ai_report)

if __name__ == "__main__":
    main()