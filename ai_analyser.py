import requests
import json

def analyze_nmap_report(raw_nmap_data, model_name="llama3"):
    """
    Sends raw Nmap scan output to the local Ollama (Llama 3) API
    and generates a professional, cybersecurity-focused vulnerability report.
    """
    # Local Ollama API endpoint
    url = "http://localhost:11434/api/generate"
    
    
    system_prompt = (
        "You are an expert Senior Penetration Tester and Cyber Security Analyst. "
        "Analyze the provided raw Nmap scan results thoroughly. "
        "Examine open ports, running services, and especially their respective versions. "
        "Identify known common vulnerabilities (CVEs) or exploits associated with these service versions. "
        "Provide your analysis as a professional penetration testing report using Markdown format with clear headings. "
        "The entire report MUST be written in English."
    )
    
 
    full_prompt = f"{system_prompt}\n\nRaw Nmap Output:\n{raw_nmap_data}"
    
    # Build the payload according to Ollama API specs
    payload = {
        "model": model_name,
        "prompt": full_prompt,
        "stream": False 
    }
    
    print(f"[*] Local AI ({model_name}) analysis initiated. Please wait...")
    
    try:
        # Send the POST request to the local Ollama daemon
        response = requests.post(url, json=payload, timeout=120)
        
        # Parse the JSON response if the HTTP status is OK
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("response", "Error: Received empty response from the AI model.")
        else:
            return f"Error: Ollama API returned unexpected status code ({response.status_code})"
            
    except requests.exceptions.ConnectionError:
        return (
            "Error: Could not connect to the local Ollama service!\n"
            "Please ensure that Ollama is running and 'ollama run llama3' is active in your terminal."
        )
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# test 
if __name__ == "__main__":
    sample_data = "=== TARGET: 192.168.1.5 ===\nPort 21/tcp: open | Service: ftp | Product: vsftpd 2.3.4\nPort 80/tcp: open | Service: http | Product: Apache httpd 2.4.41"
    report = analyze_nmap_report(sample_data)
    print("\n--- AI PENETRATION TESTING REPORT ---")
    print(report)