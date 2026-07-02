import os
import sys
import ai_engine
from scanner import run_automated_nmap, check_exit

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
    try:
        print_banner()
        
        # Step 1: Run Nmap Scan Automation
        scan_file = run_automated_nmap()
        if not scan_file:
            print(f"{RED}[-] Automation pipeline broken. Exiting script execution.{RESET}")
            return

        with open(scan_file, "r", encoding="utf-8") as f:
            scan_data = f.read()

        # Step 2: Artificial Intelligence Authentication Flow
        print(f"\n{BLUE}=== Phase 2: Artificial Intelligence Authentication Flow ==={RESET}")
        choice = input(f"{BLUE}[?] Do you have a Google Gemini API Key? (yes / no) [Or press Enter to use Gemini]: {RESET}").strip().lower()
        
        check_exit(choice)
        
        api_key = None
        use_cloud = False
        
        # Kullanıcı 'yes', 'y' dediyse veya doğrudan enter'a basıp bulut modunu seçtiyse
        if choice in ['yes', 'y', '']:
            api_key = input(f"{BLUE}[?] Enter your Gemini API Key: {RESET}").strip()
            check_exit(api_key)
            
            if not api_key:
                print(f"{YELLOW}[*] No key entered. Diverting stream to Local Ollama Engine...{RESET}")
                ai_engine.start_local_ollama()
            else:
                print(f"{YELLOW}[*] Validating your API Key...{RESET}")
                if ai_engine.verify_gemini_key(api_key):
                    print(f"{GREEN}[+] API Key verified successfully! Proceeding with Cloud Analysis...{RESET}")
                    use_cloud = True
                else:
                    print(f"{RED}[-] Invalid API Key! Exiting safely.{RESET}")
                    return
                
        elif choice in ['no', 'n', 'create']:
            # Firefox'u güvenli modlarla tetikleyen yeni fonksiyonu çağırır
            ai_engine.open_firefox_for_api()
            
            api_key = input(f"\n{BLUE}[?] Paste your newly created Gemini API Key here (or type 'local' to fallback to Ollama): {RESET}").strip()
            check_exit(api_key)
            
            if api_key and api_key.lower() != 'local':
                print(f"{YELLOW}[*] Validating your new API Key...{RESET}")
                if ai_engine.verify_gemini_key(api_key):
                    print(f"{GREEN}[+] API Key verified successfully! Proceeding with Cloud Analysis...{RESET}")
                    use_cloud = True
                else:
                    print(f"{RED}[-] Invalid API Key entered. Exiting safely.{RESET}")
                    return
            else:
                print(f"{YELLOW}[*] Fallback triggered. Diverting stream to Local Ollama Engine setup...{RESET}")
                ai_engine.start_local_ollama()
        else:
            # Kullanıcı doğrudan geçersiz bir şey girdiyse ya da 'local' yazdıysa
            print(f"{YELLOW}[*] Local mode triggered. Starting Local Ollama workflow...{RESET}")
            ai_engine.start_local_ollama()

        # Step 3: Run Selected AI Engine
        if use_cloud and api_key:
            print(f"\n{YELLOW}[*] Forwarding full Nmap report to Gemini Cloud AI...{RESET}")
            final_report = ai_engine.analyze_with_gemini(api_key, scan_data)
        else:
            print(f"\n{YELLOW}[*] Forwarding full Nmap report to Local Ollama Engine (Llama3)...{RESET}")
            final_report = ai_engine.analyze_with_ollama(scan_data)

        # Step 4: Output Rendering & Display
        print(f"\n{GREEN}==================================================")
        print("         AI PENETRATION TESTING REPORT        ")
        print(f"=================================================={RESET}")
        print(final_report)
        print(f"{GREEN}=================================================={RESET}")
        
        # Step 5: Save Generated Report to Local Workspace
        pure_filename = os.path.basename(scan_file).split('.')[0]
        output_report_name = os.path.join("results", f"analysis_report_{pure_filename}.md")
        
        with open(output_report_name, "w", encoding="utf-8") as out_f:
            out_f.write(final_report)
        print(f"\n{GREEN}[+] Full analytical report generated and saved as: {output_report_name}{RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Operational interruption detected (Ctrl+C). Shutting down NYXA safely...{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()