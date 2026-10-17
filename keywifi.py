#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KEY GANTENG - Multi Tools (Lengkap)
Support: VPS • Termux • Linux • Android
"""

import os
import sys
import time
import socket
import concurrent.futures
import urllib.request
import ssl
import subprocess
from datetime import datetime

# ==================== COLORS ====================
class Col:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    R = RED + BOLD
    G = GREEN + BOLD
    Y = YELLOW + BOLD
    C = CYAN + BOLD

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def banner():
    print(f"""{Col.R}
  _  __          ____             _                   
 | |/ /___ _   _/ ___| __ _ _ __ | |_ ___ _ __   __ _ 
 | ' // _ \ | | | |  _ / _` | '_ \| __/ _ \ '_ \ / _` |
 | . \  __/ |_| | |_| | (_| | | | | ||  __/ | | | (_| |
 |_|\_\___|\__, |\____|\__,_|_| |_|\__\___|_| |_|\__, |
           |___/                                   |___/ 
{Col.C}              KEY GANTENG - Multi Tools
{Col.Y}        Support VPS • Termux • Linux • Android
{Col.RESET}""")

def enter():
    input(f"\n{Col.Y}[ Tekan Enter untuk kembali ke menu ]{Col.RESET}")

# ==================== TOOLS ====================

def port_scanner():
    clear()
    banner()
    print(f"{Col.C}[01] Port Scanner{Col.RESET}\n")
    target = input(f"{Col.Y}Target (IP/Domain): {Col.RESET}").strip()
    if not target:
        return

    try:
        ip = socket.gethostbyname(target)
    except:
        print(f"{Col.R}[!] Gagal resolve domain{Col.RESET}")
        enter()
        return

    print(f"\n{Col.G}[*] Mengscan {target} ({ip})...{Col.RESET}\n")

    ports = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,8443,8888,9090]

    def scan(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            s.close()
            return port if result == 0 else None
        except:
            return None

    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as exe:
        for port in exe.map(scan, ports):
            if port:
                open_ports.append(port)
                print(f"{Col.G}[+] Port {port} OPEN{Col.RESET}")

    if not open_ports:
        print(f"{Col.R}Tidak ada port terbuka dari daftar umum.{Col.RESET}")
    enter()

def subdomain_finder():
    clear()
    banner()
    print(f"{Col.C}[02] Subdomain Finder{Col.RESET}\n")
    domain = input(f"{Col.Y}Domain (contoh: example.com): {Col.RESET}").strip()
    if not domain:
        return

    wordlist = [
        "www","mail","ftp","localhost","webmail","smtp","pop","ns1","webdisk","ns2",
        "cpanel","whm","autodiscover","autoconfig","m","imap","test","ns","blog","pop3",
        "dev","www2","admin","forum","news","vpn","ns3","mail2","new","mysql","old",
        "lists","support","mobile","mx","static","docs","beta","shop","sql","secure",
        "demo","cp","calendar","wiki","web","api","cdn","img","static","media","app"
    ]

    print(f"\n{Col.G}[*] Mencari subdomain {domain}...{Col.RESET}\n")
    found = 0
    for sub in wordlist:
        host = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(host)
            print(f"{Col.G}[+] {host:<35} → {ip}{Col.RESET}")
            found += 1
        except:
            pass

    if found == 0:
        print(f"{Col.R}Tidak menemukan subdomain.{Col.RESET}")
    enter()

def http_checker():
    clear()
    banner()
    print(f"{Col.C}[03] HTTP Status Checker{Col.RESET}\n")
    print("Masukkan URL (bisa banyak, pisahkan spasi)")
    raw = input(f"{Col.Y}URL: {Col.RESET}").strip()
    if not raw:
        return

    urls = raw.split()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print()
    for url in urls:
        if not url.startswith("http"):
            url = "http://" + url
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "KeyGanteng/2.0"})
            with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
                code = resp.getcode()
                color = Col.G if code < 400 else Col.Y if code < 500 else Col.R
                print(f"{color}[{code}] {url}{Col.RESET}")
        except Exception as e:
            print(f"{Col.R}[ERR] {url} → {str(e)[:60]}{Col.RESET}")
    enter()

def dns_lookup():
    clear()
    banner()
    print(f"{Col.C}[04] DNS Lookup{Col.RESET}\n")
    domain = input(f"{Col.Y}Domain: {Col.RESET}").strip()
    if not domain:
        return

    print(f"\n{Col.G}Hasil untuk {domain}:{Col.RESET}\n")
    try:
        ip = socket.gethostbyname(domain)
        print(f"A Record    : {ip}")
    except:
        print("A Record    : Tidak ditemukan")

    for cmd in [["dig", "+short", domain], ["nslookup", domain]]:
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True, timeout=5)
            if out.strip():
                print(f"\n{Col.Y}{cmd[0]} output:{Col.RESET}")
                print(out)
                break
        except:
            continue
    enter()

def network_info():
    clear()
    banner()
    print(f"{Col.C}[05] Network Information{Col.RESET}\n")

    try:
        ip = urllib.request.urlopen("https://api.ipify.org", timeout=5).read().decode()
        print(f"{Col.G}IP Publik     : {ip}{Col.RESET}")
    except:
        print(f"{Col.R}IP Publik     : Gagal mengambil{Col.RESET}")

    try:
        print(f"{Col.G}Hostname      : {socket.gethostname()}{Col.RESET}")
    except:
        pass

    print(f"\n{Col.Y}Interface:{Col.RESET}")
    try:
        out = subprocess.check_output(["ip", "-brief", "addr"], text=True, stderr=subprocess.DEVNULL)
        print(out)
    except:
        try:
            out = subprocess.check_output(["ifconfig"], text=True, stderr=subprocess.DEVNULL)
            print(out[:2000])
        except:
            print("Tidak bisa mengambil info interface")
    enter()

def whois_lookup():
    clear()
    banner()
    print(f"{Col.C}[06] Whois Lookup{Col.RESET}\n")
    target = input(f"{Col.Y}Domain / IP: {Col.RESET}").strip()
    if not target:
        return
    print()
    try:
        out = subprocess.check_output(["whois", target], text=True, stderr=subprocess.STDOUT, timeout=10)
        print(out[:3500])
    except FileNotFoundError:
        print(f"{Col.R}[!] Perintah whois tidak ditemukan.{Col.RESET}")
        print("Termux  : pkg install whois")
        print("Ubuntu  : sudo apt install whois")
    except Exception as e:
        print(f"{Col.R}Error: {e}{Col.RESET}")
    enter()

def dir_fuzzer():
    clear()
    banner()
    print(f"{Col.C}[07] Directory Fuzzer (Basic){Col.RESET}\n")
    url = input(f"{Col.Y}Target URL (contoh: https://example.com): {Col.RESET}").strip()
    if not url:
        return
    if not url.startswith("http"):
        url = "http://" + url
    if not url.endswith("/"):
        url += "/"

    wordlist = [
        "admin","login","dashboard","panel","cp","cpanel","administrator","wp-admin",
        "uploads","images","img","css","js","assets","static","media","files",
        "backup","bak","old","test","dev","api","config","includes","tmp",
        "robots.txt","sitemap.xml",".env","wp-config.php","config.php","admin.php"
    ]

    print(f"\n{Col.G}[*] Mulai fuzzing {url}...{Col.RESET}\n")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    found = 0
    for word in wordlist:
        target = url + word
        try:
            req = urllib.request.Request(target, headers={"User-Agent": "KeyGanteng/2.0"})
            with urllib.request.urlopen(req, timeout=6, context=ctx) as resp:
                code = resp.getcode()
                if code < 400:
                    print(f"{Col.G}[{code}] {target}{Col.RESET}")
                    found += 1
        except:
            pass

    if found == 0:
        print(f"{Col.R}Tidak menemukan directory/file dari wordlist dasar.{Col.RESET}")
    enter()

def banner_grabber():
    clear()
    banner()
    print(f"{Col.C}[08] Banner Grabber{Col.RESET}\n")
    target = input(f"{Col.Y}IP / Domain: {Col.RESET}").strip()
    port = input(f"{Col.Y}Port (default 80): {Col.RESET}").strip() or "80"

    try:
        port = int(port)
        ip = socket.gethostbyname(target)
        print(f"\n{Col.G}[*] Mengambil banner dari {ip}:{port}...{Col.RESET}\n")

        s = socket.socket()
        s.settimeout(5)
        s.connect((ip, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner_data = s.recv(1024).decode(errors="ignore")
        s.close()
        print(banner_data)
    except Exception as e:
        print(f"{Col.R}Gagal: {e}{Col.RESET}")
    enter()

def reverse_ip():
    clear()
    banner()
    print(f"{Col.C}[09] Reverse IP (Basic){Col.RESET}\n")
    ip = input(f"{Col.Y}Masukkan IP: {Col.RESET}").strip()
    if not ip:
        return

    print(f"\n{Col.G}[*] Mencoba reverse lookup...{Col.RESET}\n")
    try:
        host = socket.gethostbyaddr(ip)
        print(f"{Col.G}Hostname: {host[0]}{Col.RESET}")
        if host[1]:
            print(f"Aliases : {', '.join(host[1])}")
    except Exception as e:
        print(f"{Col.R}Tidak ditemukan / Error: {e}{Col.RESET}")
    enter()

def wifi_menu():
    clear()
    banner()
    print(f"{Col.C}[10] WiFi Tools{Col.RESET}\n")
    print(f"{Col.R}PERINGATAN PENTING:{Col.RESET}")
    print("• Membutuhkan WiFi Adapter yang support Monitor Mode")
    print("• Tidak berfungsi di VPS")
    print("• Di Termux hampir pasti tidak support\n")

    print(f"{Col.Y}[1]{Col.RESET} Jalankan Key WiFi Deauth")
    print(f"{Col.Y}[0]{Col.RESET} Kembali")

    pilihan = input(f"\n{Col.Y}Pilih: {Col.RESET}").strip()
    if pilihan == "1":
        if os.path.exists("keywifi.py"):
            os.system("sudo python3 keywifi.py")
        else:
            print(f"\n{Col.R}[!] File keywifi.py tidak ditemukan!{Col.RESET}")
            enter()

def about():
    clear()
    banner()
    print(f"""{Col.C}
KEY GANTENG - Multi Tools
Version : 2.0 (Lengkap)

Tools yang tersedia:
 01. Port Scanner
 02. Subdomain Finder
 03. HTTP Status Checker
 04. DNS Lookup
 05. Network Information
 06. Whois Lookup
 07. Directory Fuzzer
 08. Banner Grabber
 09. Reverse IP Lookup
 10. WiFi Tools

Support Platform:
• VPS / Cloud Server
• Termux (Android)
• Kali Linux / Ubuntu / Debian
• Windows (sebagian)

Hanya gunakan pada sistem milik sendiri
atau yang memiliki izin.
{Col.RESET}""")
    enter()

# ==================== MAIN MENU ====================

def main_menu():
    while True:
        clear()
        banner()
        print(f"""{Col.C}
[01] Port Scanner
[02] Subdomain Finder
[03] HTTP Status Checker
[04] DNS Lookup
[05] Network Information
[06] Whois Lookup
[07] Directory Fuzzer
[08] Banner Grabber
[09] Reverse IP Lookup
[10] WiFi Tools
[11] About
[00] Keluar
{Col.RESET}""")

        choice = input(f"{Col.Y}Pilih menu: {Col.RESET}").strip()

        if choice in ["1", "01"]:
            port_scanner()
        elif choice in ["2", "02"]:
            subdomain_finder()
        elif choice in ["3", "03"]:
            http_checker()
        elif choice in ["4", "04"]:
            dns_lookup()
        elif choice in ["5", "05"]:
            network_info()
        elif choice in ["6", "06"]:
            whois_lookup()
        elif choice in ["7", "07"]:
            dir_fuzzer()
        elif choice in ["8", "08"]:
            banner_grabber()
        elif choice in ["9", "09"]:
            reverse_ip()
        elif choice in ["10"]:
            wifi_menu()
        elif choice in ["11"]:
            about()
        elif choice in ["0", "00"]:
            print(f"\n{Col.G}Terima kasih telah memakai KEY GANTENG!{Col.RESET}\n")
            sys.exit(0)
        else:
            print(f"{Col.R}Pilihan tidak valid!{Col.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Col.R}[!] Dibatalkan{Col.RESET}\n")
        sys.exit(0)
