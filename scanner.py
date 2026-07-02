import subprocess
import re
import os
import sys

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def check_exit(user_input):
    """Helper function to cleanly exit if user types 'exit'."""
    if user_input.strip().lower() == 'exit':
        print(f"\n{YELLOW}[*] Exiting NYXA Engine. Goodbye!{RESET}")
        sys.exit(0)

def run_automated_nmap():
    print(f"\n{BLUE}=== Phase 1: Native Nmap Scan Automation ==={RESET}")
    print(f"{YELLOW}[i] Type 'exit' at any prompt to quit the program.{RESET}")
    
    target = input(f"{BLUE}[?] Enter Target IP or Domain (e.g., 192.168.1.1): {RESET}").strip()
    check_exit(target)
    
    if not target:
        print(f"{RED}[-] Error: Target cannot be empty!{RESET}")
        return None

    # Döngüye alıyoruz ki geçersiz girişte menü tekrar gelsin
    while True:
        print(f"\n{BLUE}[*] Select Scan Profile:")
        print(f"1. Fast Scan (Top 100 ports + Service Versions)")
        print(f"2. Comprehensive Scan (Default Scripts + OS Detection + Service Versions)")
        print(f"3. Aggressive Scan (-A -T5) (Recommended for CTFs)")
        print(f"4. Custom Arguments (Enter your own Nmap flags)")
        scan_choice = input(f"{BLUE}[?] Choice (1, 2, 3, 4 or type 'exit'): {RESET}").strip()
        
        check_exit(scan_choice)

        if scan_choice in ["1", "2", "3", "4"]:
            break
        else:
            print(f"{RED}[-] Invalid choice! Please enter a number between 1 and 4.{RESET}")

    nmap_args = ["nmap"]

    if scan_choice == "2":
        print(f"{YELLOW}[*] Configuring Comprehensive Scan (-sV -sC -O)...{RESET}")
        nmap_args.extend(["-sV", "-sC", "-O", target])
    elif scan_choice == "3":
        print(f"{YELLOW}[*] Configuring Aggressive Scan (-A -T5) for CTF environment...{RESET}")
        nmap_args.extend(["-A", "-T5", target])
    elif scan_choice == "4":
        print(f"{YELLOW}[*] Custom Scan Selected.{RESET}")
        custom_flags = input(f"{BLUE}[?] Enter your custom Nmap flags: {RESET}").strip()
        check_exit(custom_flags)
        
        cleaned_flags = re.sub(r'-o[NXGA]\s+\S+', '', custom_flags)
        cleaned_flags = re.sub(r'-o[NXGA]', '', cleaned_flags)
        flags_list = [f for f in cleaned_flags.split(" ") if f]
        
        nmap_args.extend(flags_list)
        nmap_args.append(target)
    else:
        print(f"{YELLOW}[*] Configuring Fast Scan (-sV -F)...{RESET}")
        nmap_args.extend(["-sV", "-F", target])

    clean_target = target.replace(".", "_").replace("/", "_")
    
    if not os.path.exists("results"):
        os.makedirs("results")
        
    output_filename = os.path.join("results", f"nmap_raw_{clean_target}.txt")

    print(f"{GREEN}[*] Launching native Nmap subprocess: {' '.join(nmap_args)}{RESET}")
    print(f"{YELLOW}[*] Scanning in progress. Please wait...{RESET}")

    try:
        result = subprocess.run(nmap_args, capture_output=True, text=True, check=True)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(result.stdout)
            
        print(f"{GREEN}[+] Nmap scan successfully finished!{RESET}")
        print(f"{GREEN}[+] Raw scan output saved locally to: {output_filename}{RESET}")
        return output_filename

    except subprocess.CalledProcessError as e:
        print(f"{RED}[-] Nmap process failed with exit code {e.returncode}{RESET}")
        return None
    except Exception as e:
        print(f"{RED}[-] An unexpected error occurred: {str(e)}{RESET}")
        return None