# 🕵️ Python Advanced Port Scanner

A fast, multithreaded **TCP/UDP port scanner** written in Python 3. Built for efficiency, flexibility, and ease of use — ideal for network administrators, cybersecurity researchers, and penetration testers *(for authorized environments only)*.

---

## ✨ Features

- 🚀 **Multithreaded scanning** for high performance.
- 🔍 **Supports TCP and UDP** scanning.
- 🕶️ **Stealth mode** for randomized scan timing.
- ⚡ **FAST mode** scans only common/critical ports.
- 📊 Interactive **progress bar** and colored output.
- 🧠 **Automatic service name resolution**.
- 💾 Export results to **JSON**.
- 🖥️ **Cross-platform** (Linux, macOS, Windows).

---

## 🧩 Requirements

- **Python** ≥ 3.7  
- Works best in a terminal that supports color (e.g., bash, PowerShell, or iTerm2).

---

## 📦 Installation

Clone this repository and make the script executable:

 git clone https://github.com/AndreiPaiuDev/AdvancePortScanner.git
 cd AdvancePortScanner
 chmod +x portScanner.py


---

## 🧰 Usage

Run the scanner directly:

./portScanner.py [options]


Or via the Python interpreter:

python3 portScanner.py [options]

---

## ⚙️ Command-Line Arguments

| Option | Description | Default |
|:--|:--|:--|
| `--target` | Target hostname or IP address | Local IP |
| `-s`, `--start` | Start port | `1` |
| `-e`, `--end` | End port | `65535` |
| `--fast` | Scan only common critical ports | `False` |
| `--stealth` | Randomize request timing | `False` |
| `--threads` | Max concurrent threads | `100` |
| `-t`, `--timeout` | TCP connection timeout (seconds) | `0.5` |
| `--udp-timeout` | UDP timeout (seconds) | `1.0` |
| `--quiet` | Suppress verbose output | `False` |
| `--json` | Save results to specified JSON file | `None` |
| `--version` | Show tool version and exit | — |

---

## 🧮 Examples

**Fast scan common ports on a host:**

python3 portScanner.py --target IP --fast


**Stealth TCP + UDP scan (random timing):**

python3 portScanner.py --target example.com --stealth


**Scan all ports and save to JSON:**

python3 portScanner.py --target 10.0.0.5 -s 1 -e 1024 --json results.json


---

## 🧠 Interactive Mode

When run without automatic arguments, you’ll be prompted to choose:
1. TCP  
2. UDP  
3. Both  
4. Exit  

Results are displayed in real time with progress bars and service names.

---

## 📁 JSON Output Example

{
"target": "Target IP",
"timestamp": "2025-12-19 21:37:02",
"tcp_open": ,
"udp_open":
}


---

## ⚠️ Disclaimer

This tool is for **educational and authorized testing** purposes only.  
Unauthorized scanning of networks or systems without permission **violates laws and ethical standards**.

---

## 👨‍💻 Author

**Andrei-Gabriel Paiu-Rotundu**  
*Version: 1.1*  


---

## 🌟 Inspiration

Inspired by tools like **nmap** and **masscan**, this script demonstrates how to build efficient scanners in Python using sockets and threads.

---

