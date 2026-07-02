# 🚀 NYXA: AI-Powered Nmap Analyzer & Pentest Reporter

NYXA is an automated, all-in-one cybersecurity reconnaissance tool designed for Kali Linux. It executes native Nmap scans through a robust Python infrastructure and leverages either **Google Gemini Cloud API (Gemini 2.5 Flash)** or a local **Ollama (Llama3)** engine to instantly transform raw, messy network scan text into comprehensive, executive-level Penetration Testing Reports.

This tool is purpose-built for **CTF players, Junior Penetration Testers, and security students** who want to optimize their enumeration phase and master vulnerability identification with the help of Artificial Intelligence.

---

## 🛠️ Key Features

* **Four Distinct Scan Profiles:** Fast Scan, Comprehensive Scan, **Aggressive Mode (`-A -T5`) optimized for CTFs**, and a Custom Flags mode.
* **Intelligent Input Filtering:** Advanced regex sanitization that intercepts and strips accidental output flags (`-oN`, `-oX`, etc.) in custom mode, preserving the core automated pipeline.
* **Hybrid Dual-AI Architecture:** Automatically harnesses the cloud speed of Gemini API or seamlessly drops back to local **Ollama (Llama3)** based on user credentials.
* **Automated Firefox Integration:** If you don't have an API key, NYXA automatically opens Firefox and navigates to the official Google AI Studio to let you generate a free API key on the fly.
* **Standardized Markdown Output:** Generates clean, well-formatted English `.md` penetration testing reports ready for your portfolio or client delivery.

---

## 📋 Directory Architecture

To keep the codebase modular, highly readable, and maintainable, the project is divided into three distinct scripts:

```text
/opt/NyxaNmapAnalyzer/
├── app.py             # Main Entrypoint & AI Authentication Orchestrator
├── scanner.py         # Subprocess Automation & Native Nmap Handling
├── ai_engine.py       # Cloud/Local LLM Communications & Firefox Control
└── requirements.txt   # Third-Party Python Dependencies
```

---

## 🚀 Step-by-Step Installation Guide (For Absolute Beginners)

If you are brand new to Linux or cybersecurity, follow these steps exactly. Open your Kali Linux Terminal and copy-paste the following commands line by line:

### Step 1: Navigate into the Folder
```bash
cd /opt
```

### Step 2: Clone the Repository Directly into /opt
```bash
sudo git clone https://github.com/yigitemreyildirim/NyxaNmapAnalyzer.git
```

### Step 3: Navigate into the Project Folder
```bash
cd /opt/NyxaNmapAnalyzer
```

### Step 4: Install Python Dependencies Safely
```bash
sudo pip3 install -r requirements.txt --break-system-packages
```

### Step 5: Execute the Analyzer Engine with Root Privileges
```bash
sudo python3 app.py
```

---

## 🎮 How to Use

### 1. Define Target
Enter your target domain or IP address when prompted (e.g., `192.168.1.X` or `scanme.nmap.org`).

### 2. Choose Scan Profile
Press `3` for rapid CTF enumeration or choose other options according to your scope.

### 3. AI Choice
* Type `yes` if you already have an API key and paste it.
* Type `no` to trigger the Automated Firefox Flow which will open your browser directly to the Google AI Studio page.
* Press **Enter** on an empty prompt to fall back entirely to your local environment; NYXA will spawn a brand new independent terminal window running `ollama run llama3` automatically.

### 4. Analyze Report
Check your workspace directory! A freshly generated `.md` file filled with service analyses, CVE cross-references, and remediation guidance is waiting for you.

---

## ⚠️ Legal Disclaimer

This tool is engineered strictly for educational purposes, Capture The Flag (CTF) challenges, and fully authorized infrastructure audits.

Running unauthorized scans against public infrastructure can trigger security alerts and lead to severe legal repercussions. The developer assumes absolutely no liability for misuse or damages caused by this utility.



