#!/usr/bin/env python3
"""
simulate_attack.py
------------------
Append fake attack log lines to the monitored log file.
Run while the SOC server is live to see real-time detection.

Usage:
  python simulate_attack.py all
  python simulate_attack.py brute_force
  python simulate_attack.py impossible_login
  python simulate_attack.py high_volume
"""
import sys
import time
import random

LOG_FILE = "logs/sample_auth.log"
USERS    = ["admin", "root", "ubuntu", "deploy", "git", "postgres"]


def log(line: str) -> None:
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    print(f"  >> {line}")
    time.sleep(0.25)


def brute_force(ip: str = "203.0.113.42", n: int = 8) -> None:
    print(f"\n[*] Brute-force from {ip}")
    for _ in range(n):
        user = random.choice(USERS)
        log(f"Failed password for invalid user {user} from {ip} port 22 ssh2")


def impossible_login(ip: str = "198.51.100.7") -> None:
    print(f"\n[*] Impossible login from {ip}")
    for _ in range(6):
        log(f"Failed password for root from {ip} port 22 ssh2")
    time.sleep(0.5)
    log(f"Accepted password for root from {ip} port 22 ssh2")


def high_volume(ip: str = "192.0.2.100", n: int = 12) -> None:
    print(f"\n[*] High-volume from {ip}")
    for _ in range(n):
        user = random.choice(USERS)
        port = random.randint(1024, 65535)
        log(f"Failed password for invalid user {user} from {ip} port {port} ssh2")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("brute_force",    "all"): brute_force()
    if mode in ("impossible_login","all"): impossible_login()
    if mode in ("high_volume",    "all"): high_volume()
    print("\n[+] Done — check the SOC dashboard.")