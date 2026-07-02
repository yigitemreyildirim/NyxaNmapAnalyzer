import subprocess
import re

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def run_automated_nmap():
    """
    Executes a native Nmap scan using subprocess based on user choice, 
    displays live status, and saves the output to a text file.
    """
    print(f"\n{BLUE}=== Phase 1: Native Nmap Scan Automation ==={RESET}")
    target = input(f"{BLUE}[?] Enter Target IP or Domain (e.g., 192.168.1.1 or scanme.nmap.org): {RESET}").strip()
    
    if not target:
        print(f"{RED}[-] Error: Target cannot be empty!{RESET}")
        return None

    print(f"\n{BLUE}[*] Select Scan Profile:")
    print(f"1. Fast Scan (Top 100 ports + Service Versions)")
    print(f"2. Comprehensive Scan (Default Scripts + OS Detection + Service Versions - Takes longer)")
    print(f"3. Aggressive Scan (-A -T5) (Recommended for CTFs - Extremely Fast & Loud)")
    print(f"4. Custom Arguments (Enter your own Nmap flags - DO NOT include output flags like -oN, -oX etc.){RESET}")
    scan_choice = input(f"{BLUE}[?] Choice (1, 2, 3 or 4): {RESET}").strip()

    nmap_args = ["nmap"]

    if scan_choice == "2":
        print(f"{YELLOW}[*] Configuring Comprehensive Scan (-sV -sC -O)...{RESET}")
        nmap_args.extend(["-sV", "-sC", "-O", target])
    elif scan_choice == "3":
        print(f"{YELLOW}[*] Configuring Aggressive Scan (-A -T5) for CTF environment...{RESET}")
        nmap_args.extend(["-A", "-T5", target])
    elif scan_choice == "4":
        print(f"{YELLOW}[*] Custom Scan Selected.{RESET}")
        custom_flags = input(f"{BLUE}[?] Enter your custom Nmap flags (e.g., -sS -sV -p 22,80,443): {RESET}").strip()
        
        # Intercept and remove any accidental output flags
        cleaned_flags = re.sub(r'-o[NXGA]\s+\S+', '', custom_flags)
        cleaned_flags = re.sub(r'-o[NXGA]', '', cleaned_flags)
        flags_list = [f for f in cleaned_flags.split(" ") if f]
        
        nmap_args.extend(flags_list)
        nmap_args.append(target)
    else:
        print(f"{YELLOW}[*] Configuring Fast Scan (-sV -F)...{RESET}")
        nmap_args.extend(["-sV", "-F", target])

    clean_target = target.replace(".", "_").replace("/", "_")
    output_filename = f"nmap_raw_{clean_target}.txt"

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
        if "requires root privileges" in e.stderr or e.returncode == 1:
            print(f"{RED}[!] Hint: Ensure you are running this script with 'sudo python3 app.py'{RESET}")
        return None
    except Exception as e:
        print(f"{RED}[-] An unexpected error occurred during Nmap execution: {str(e)}{RESET}")
        return None