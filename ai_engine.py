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
    "Analyze the provided raw comprehensive Nmap scan report text file thoroughly. "
    "Identify open ports, running services, operating systems, and service versions. "
    "Thoroughly cross-reference versions with known common vulnerabilities (CVEs) or exploits. "
    "Provide your analysis as a highly professional penetration testing report using Markdown format with clear headings. "
    "The entire report MUST be written in English."
)

def open_firefox_for_api():
    url = "https://aistudio.google.com/api-keys"
    print(f"\n{YELLOW}[*] Opening Firefox to: {url}{RESET}")
    try:
        subprocess.Popen(["firefox", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        webbrowser.open(url)

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
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 3000}
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