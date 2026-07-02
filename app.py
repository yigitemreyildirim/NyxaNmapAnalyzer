import os
from scanner import run_automated_nmap
import ai_engine

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_banner():
    print(f"{BLUE}" + "="*50)
    print("    NYXA AUTOMATED NMAP & AI REPORTING ENGINE     ")
    print("="*50 + f"{RESET}")

def main():
    print_banner()
    
    scan_file = run_automated_nmap()
    if not scan_file:
        print(f"{RED}[-] Automation pipeline broken. Exiting script execution.{RESET}")
        return

    with open(scan_file, "r", encoding="utf-8") as f:
        scan_data = f.read()

    print(f"\n{BLUE}=== Phase 2: Artificial Intelligence Authentication Flow ==={RESET}")
    choice = input(f"{BLUE}[?] Do you have a Google Gemini API Key? (yes / no): {RESET}").strip().lower()
    
    api_key = None
    use_cloud = False
    
    if choice in ['yes', 'y']:
        api_key = input(f"{BLUE}[?] Enter your Gemini API Key: {RESET}").strip()
        print(f"{YELLOW}[*] Validating your API Key...{RESET}")
        if ai_engine.verify_gemini_key(api_key):
            print(f"{GREEN}[+] API Key verified successfully! Proceeding with Cloud Analysis...{RESET}")
            use_cloud = True
        else:
            print(f"{RED}[-] Invalid API Key! Exiting safely.{RESET}")
            return
            
    elif choice in ['no', 'n', 'create']:
        ai_engine.open_firefox_for_api()
        
        api_key = input(f"\n{BLUE}[?] Paste your newly created Gemini API Key here (or press Enter to fallback to Local Ollama): {RESET}").strip()
        if api_key:
            print(f"{YELLOW}[*] Validating your new API Key...{RESET}")
            if ai_engine.verify_gemini_key(api_key):
                print(f"{GREEN}[+] API Key verified successfully!{RESET}")
                use_cloud = True
            else:
                print(f"{RED}[-] Invalid API Key entered. Exiting loop safely.{RESET}")
                return
        else:
            print(f"{YELLOW}[*] No key entered. Diverting stream to Local Engine setup...{RESET}")
            ai_engine.start_local_ollama()
    else:
        print(f"{YELLOW}[*] Unknown option. Defaulting to local environment automation...{RESET}")
        ai_engine.start_local_ollama()

    if use_cloud and api_key:
        final_report = ai_engine.analyze_with_gemini(api_key, scan_data)
    else:
        final_report = ai_engine.analyze_with_ollama(scan_data)

    print(f"\n{GREEN}==================================================")
    print("         AI PENETRATION TESTING REPORT        ")
    print(f"=================================================={RESET}")
    print(final_report)
    print(f"{GREEN}=================================================={RESET}")
    
    # MD raporunu results klasörüne kaydediyoruz
    pure_filename = os.path.basename(scan_file).split('.')[0]
    output_report_name = os.path.join("results", f"analysis_report_{pure_filename}.md")
    
    with open(output_report_name, "w", encoding="utf-8") as out_f:
        out_f.write(final_report)
    print(f"\n{GREEN}[+] Full analytical report generated and saved as: {output_report_name}{RESET}")

if __name__ == "__main__":
    main()