#!/usr/bin/env python3
import socket
import argparse
import sys
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

#  Color Codes
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

#  Fast scan critical ports
FAST_PORTS = [
    20, 21, 22, 23, 25, 53, 80, 110, 143, 389,
    443, 445, 465, 587, 993, 995, 1433, 1521,
    2049, 3306, 3389, 5432, 5900, 6379, 8080
]

#  ASCII Banner
def print_banner():
    banner = f"""{GREEN}                                
                                                           
                ###    ########  ##     ##    ###    ##    ##  ######  ########                                         
                ## ##   ##     ## ##     ##   ## ##   ###   ## ##    ## ##                                               
                ##   ##  ##     ## ##     ##  ##   ##  ####  ## ##       ##                                               
                ##     ## ##     ## ##     ## ##     ## ## ## ## ##       ######                                           
                ######### ##     ##  ##   ##  ######### ##  #### ##       ##                                               
                ##     ## ##     ##   ## ##   ##     ## ##   ### ##    ## ##                                               
                ##     ## ########     ###    ##     ## ##    ##  ######  ########                                         
########   #######  ########  ########     ######   ######     ###    ##    ## ##    ## ######## ########  
##     ## ##     ## ##     ##    ##       ##    ## ##    ##   ## ##   ###   ## ###   ## ##       ##     ## 
##     ## ##     ## ##     ##    ##       ##       ##        ##   ##  ####  ## ####  ## ##       ##     ## 
########  ##     ## ########     ##        ######  ##       ##     ## ## ## ## ## ## ## ######   ########  
##        ##     ## ##   ##      ##             ## ##       ######### ##  #### ##  #### ##       ##   ##   
##        ##     ## ##    ##     ##       ##    ## ##    ## ##     ## ##   ### ##   ### ##       ##    ##  
##         #######  ##     ##    ##        ######   ######  ##     ## ##    ## ##    ## ######## ##     ##                                           

                                    Python Advanced Port Scanner
                                        Author: Andrei Paiu
{RESET}"""
    print(banner)

#  Auto Detect Local IP
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

#  Service Name Lookup
def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"

#  Progress Bar
def progress_bar(current, total, bar_length=40):
    if total == 0:
        return
    percent = current / total
    filled = int(bar_length * percent)
    bar = "█" * filled + "-" * (bar_length - filled)
    print(f"\r[{bar}] {int(percent * 100)}%", end="", flush=True)

#  TCP Port Scan
def scan_tcp_port(target, port, timeout=0.5, stealth=False):
    try:
        if stealth:
            time.sleep(random.uniform(0.01, 0.15))

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        return port if result == 0 else None
    except:
        return None

def run_tcp_scan(target, ports, threads=100, timeout=0.5, stealth=False):
    open_ports = []
    total = len(ports)
    completed = 0

    def worker(p):
        return scan_tcp_port(target, p, timeout, stealth)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(worker, ports)
        for result in results:
            completed += 1
            progress_bar(completed, total)
            if result:
                open_ports.append(result)

    print()
    return open_ports

#  UDP Port Scan
def scan_udp_port(target, port, timeout=1, stealth=False):
    try:
        if stealth:
            time.sleep(random.uniform(0.01, 0.15))

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        sock.sendto(b"", (target, port))

        try:
            data, _ = sock.recvfrom(1024)
            return port
        except socket.timeout:
            return None
    except:
        return None

def run_udp_scan(target, ports, threads=50, timeout=1, stealth=False):
    open_ports = []
    total = len(ports)
    completed = 0

    def worker(p):
        return scan_udp_port(target, p, timeout, stealth)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(worker, ports)
        for result in results:
            completed += 1
            progress_bar(completed, total)
            if result:
                open_ports.append(result)

    print()
    return open_ports

#  Interactive scan type
def choose_scan_type():
    print("Select scan type:")
    print("1. TCP")
    print("2. UDP")
    print("3. TCP + UDP")
    print("4. Exit")

    choice = input("Choice (1/2/3/4): ").strip()

    if choice == "1":
        return "tcp"
    elif choice == "2":
        return "udp"
    elif choice == "3":
        return "both"
    elif choice == "4":
        return "exit"
    else:
        print("Invalid option.\n")
        return choose_scan_type()

#  Main Loop
def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Advanced TCP/UDP Port Scanner")
    parser.add_argument("-s", "--start", type=int, default=1)
    parser.add_argument("-e", "--end", type=int, default=65535)
    parser.add_argument("--target", help="Target IP or hostname")
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--stealth", action="store_true")
    parser.add_argument("--udp-timeout", type=float, default=1.0)
    parser.add_argument("-t", "--timeout", type=float, default=0.5)
    parser.add_argument("--threads", type=int, default=100)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--json", help="Save results to JSON file")
    parser.add_argument("--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print("Port Scanner v1.1 - Author: Andrei Paiu")
        sys.exit(0)

    # MAIN MENU LOOP
    while True:
        target = args.target if args.target else get_local_ip()
        print(f"{GREEN}Target: {target}{RESET}")
        print(f"Scan started at: {datetime.now()}\n")

        scan_type = choose_scan_type()

        if scan_type == "exit":
            print(f"{GREEN}Exiting...{RESET}")
            sys.exit(0)

        # Port selection
        if args.fast:
            ports = FAST_PORTS
            if not args.quiet:
                print(f"{YELLOW}FAST mode enabled (critical ports only){RESET}\n")
        else:
            ports = list(range(args.start, args.end + 1))

        tcp_open = []
        udp_open = []

        # TCP Scan
        if scan_type in ("tcp", "both"):
            if not args.quiet:
                print(f"{CYAN}Running TCP scan on {len(ports)} ports...{RESET}")
            tcp_open = run_tcp_scan(
                target, ports, threads=args.threads,
                timeout=args.timeout, stealth=args.stealth
            )
            for port in tcp_open:
                print(f"{GREEN}[TCP OPEN]{RESET} Port {port:<5} Service: {get_service_name(port)}")

        # UDP Scan
        if scan_type in ("udp", "both"):
            if not args.quiet:
                print(f"\n{GREEN}Running UDP scan on {len(ports)} ports...{RESET}")
            udp_open = run_udp_scan(
                target, ports, threads=args.threads,
                timeout=args.udp_timeout, stealth=args.stealth
            )
            for port in udp_open:
                print(f"{YELLOW}[UDP OPEN/RESP]{RESET} Port {port:<5}")

        print(f"\n{CYAN}Scan complete.{RESET}")
        print(f"Total TCP open ports: {len(tcp_open)}")
        print(f"Total UDP responsive ports: {len(udp_open)}")

        if args.json:
            import json
            data = {
                "target": target,
                "timestamp": str(datetime.now()),
                "tcp_open": tcp_open,
                "udp_open": udp_open
            }
            with open(args.json, "w") as f:
                json.dump(data, f, indent=4)
            print(f"{YELLOW}Results saved to {args.json}{RESET}")

        print(f"\n{MAGENTA}Returning to main menu...{RESET}\n")
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}Scan interrupted by user.{RESET}")
        sys.exit(1)
