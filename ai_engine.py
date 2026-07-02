import time
import subprocess
import webbrowser
import requests

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

SYSTEM_PROMPT = (
    "You are an expert Senior Penetration Tester and Cyber Security Analyst. "
    "Analyze the provided raw Nmap scan report. Because the target might have dozens of open ports, "
    "you MUST be concise and structured to avoid hitting maximum output token limits. "
    "Format your report into the following strict structure:\n\n"
    "1. EXECUTIVE SUMMARY: Short paragraph summarizing the posture.\n"
    "2. HOST & OS INFORMATION: Identify IP, Hostname, and OS Guess.\n"
    "3. VULNERABILITY SUMMARY TABLE: Create a Markdown table with columns: [Port, Service, Version, Estimated Severity, Known Exploits/CVE].\n"
    "4. CRITICAL & HIGH FINDINGS DETAILS: Focus ONLY on Critical/High flaws (like backdoors, RCE, anonymous access). Use 2-3 bullet points per critical flaw.\n"
    "5. REMEDIATION: Bullet points on how to fix the system.\n\n"
    "Keep the language professional, strict, and entirely in English."
)

def open_firefox_for_api():
    url = "https://aistudio.google.com/api-keys"
    print(f"\n{YELLOW}[*] Opening Firefox to: {url}{RESET}")
    
    
    try:
        subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    except Exception:
        pass

    #
    try:
        subprocess.Popen(["firefox", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    except Exception:
        pass

    
    try:
        webbrowser.open(url)
    except Exception:
        print(f"{RED}[-] Could not auto-launch browser. Please manually visit: {url}{RESET}")

def verify_gemini_key(api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": "Hello"}]}]}
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=5)
        return res.status_code == 200
    except Exception:
        return False

def start_local_ollama():
    print(f"\n{RED}[!] WARNING: Running Local LLM (Llama3) requires high hardware specs (Minimum 8GB+ RAM).{RESET}")
    print(f"{YELLOW}[*] Spawning a clean background terminal for Ollama service...{RESET}")
    
    try:
        subprocess.Popen(["qterminal", "-e", "ollama run llama3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        try:
            subprocess.Popen(["xterm", "-e", "ollama run llama3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            subprocess.Popen(["ollama", "run", "llama3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    print(f"{YELLOW}[*] Waiting 5 seconds for the LLM engine to warm up...{RESET}")
    time.sleep(5)

def analyze_with_gemini(api_key, raw_text):
    print(f"\n{GREEN}[*] Forwarding full Nmap report to Gemini Cloud AI...{RESET}")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\nRaw Scan Output:\n{raw_text}"}]}],
        "generationConfig": {
            "temperature": 0.2, 
            "maxOutputTokens": 8192  
        }
    }
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=120)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        return f"API Error (Status {res.status_code}): {res.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

def analyze_with_ollama(raw_text):
    print(f"\n{GREEN}[*] Forwarding full Nmap report to Local Ollama (Llama3)...{RESET}")
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "llama3",
        "prompt": f"{SYSTEM_PROMPT}\n\nRaw Scan Output:\n{raw_text}",
        "stream": False
    }
    try:
        res = requests.post(url, json=payload, timeout=180)
        if res.status_code == 200:
            return res.json().get("response", "")
        return f"Ollama Error: Status code {res.status_code}"
    except Exception as e:
        return f"Error connecting to local Ollama service: {str(e)}"