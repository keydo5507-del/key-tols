
#!/usr/bin/env python3
# KEY GANTENG — WiFi Nearby Scanner
# Read-only Wi-Fi discovery for Linux, Ubuntu and Windows.

import os
import re
import sys
import time
import shutil
import platform
import subprocess


class UI:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"

    @staticmethod
    def enable():
        if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
            for name in ("RESET", "BOLD", "DIM", "BLUE", "CYAN",
                         "GREEN", "YELLOW", "RED", "WHITE"):
                setattr(UI, name, "")

    @staticmethod
    def line(char="─", width=48):
        print(UI.CYAN + char * width + UI.RESET)

    @staticmethod
    def header():
        print()
        UI.line("═")
        print(f"{UI.BLUE}{UI.BOLD}  ██╗  ██╗███████╗██╗   ██╗{UI.RESET}")
        print(f"{UI.BLUE}{UI.BOLD}  ██║ ██╔╝██╔════╝╚██╗ ██╔╝{UI.RESET}")
        print(f"{UI.CYAN}{UI.BOLD}  █████╔╝ █████╗   ╚████╔╝ {UI.RESET}")
        print(f"{UI.CYAN}{UI.BOLD}  ██╔═██╗ ██╔══╝    ╚██╔╝  {UI.RESET}")
        print(f"{UI.BLUE}{UI.BOLD}  ██║  ██╗███████╗   ██║   {UI.RESET}")
        print(f"{UI.BLUE}{UI.BOLD}  ╚═╝  ╚═╝╚══════╝   ╚═╝   {UI.RESET}")
        print()
        print(f"{UI.WHITE}{UI.BOLD}       K E Y   G A N T E N G{UI.RESET}")
        print(f"{UI.CYAN}       WIFI NEARBY SCANNER{UI.RESET}")
        print(f"{UI.DIM}       NETWORK DISCOVERY TOOL{UI.RESET}")
        UI.line("═")
        print(f"  {UI.DIM}OS     : {platform.system()} {platform.release()}{UI.RESET}")
        print(f"  {UI.DIM}Python : {platform.python_version()}{UI.RESET}")
        print(f"  {UI.DIM}Mode   : Read-only Wi-Fi scan{UI.RESET}")
        UI.line()

    @staticmethod
    def status(label, value, color=None):
        print(f"  {UI.DIM}◆ {label:<11}{UI.RESET} "
              f"{color or UI.WHITE}{value}{UI.RESET}")


def run_command(args, timeout=20):
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
            check=False
        )
        return result.returncode, result.stdout or "", result.stderr or ""
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, "", str(exc)


def scan_windows():
    rc, output, error = run_command(
        ["netsh", "wlan", "show", "networks", "mode=bssid"], 25
    )
    if rc != 0:
        raise RuntimeError(error or "Gagal menjalankan pemindai Windows.")

    networks, current = [], None

    for raw in output.splitlines():
        line = raw.strip()
        match = re.match(r"SSID\s+\d+\s*:\s*(.*)", line, re.I)

        if match:
            if current:
                networks.append(current)

            current = {
                "SSID": match.group(1).strip() or "(Hidden)",
                "BSSID": [],
                "Signal": "-",
                "Security": "-",
                "Channel": "-"
            }
            continue

        if current is None:
            continue

        for pattern, key in [
            (r"BSSID\s+\d+\s*:\s*(.*)", "BSSID"),
            (r"Signal\s*:\s*(.*)", "Signal"),
            (r"Authentication\s*:\s*(.*)", "Security"),
            (r"Channel\s*:\s*(.*)", "Channel")
        ]:
            match = re.match(pattern, line, re.I)
            if match:
                value = match.group(1).strip()
                if key == "BSSID":
                    current[key].append(value)
                else:
                    current[key] = value

    if current:
        networks.append(current)

    return networks


def scan_linux_nmcli():
    rc, output, error = run_command([
        "nmcli", "-t", "-e", "yes",
        "-f", "SSID,BSSID,SIGNAL,SECURITY,CHAN",
        "device", "wifi", "list", "--rescan", "yes"
    ], 30)

    if rc != 0:
        raise RuntimeError(error or "nmcli tidak dapat memindai.")

    networks = []

    for line in output.splitlines():
        fields, buffer, escaped = [], "", False

        for char in line:
            if escaped:
                buffer += char
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == ":":
                fields.append(buffer)
                buffer = ""
            else:
                buffer += char

        fields.append(buffer)

        if len(fields) >= 5:
            ssid, bssid, signal, security, channel = fields[:5]
            networks.append({
                "SSID": ssid or "(Hidden)",
                "BSSID": bssid or "-",
                "Signal": signal + "%" if signal else "-",
                "Security": security or "Open/unknown",
                "Channel": channel or "-"
            })

    return networks


def scan_linux_iwlist():
    if not shutil.which("iwlist"):
        raise RuntimeError(
            "nmcli/iwlist tidak tersedia. Adapter Wi-Fi harus "
            "terlihat oleh sistem operasi."
        )

    rc, output, error = run_command(["iwlist", "scan"], 30)

    if rc != 0:
        raise RuntimeError(error or "iwlist gagal melakukan pemindaian.")

    networks, current = [], None

    for raw in output.splitlines():
        line = raw.strip()

        if "Cell " in line and "Address:" in line:
            if current:
                networks.append(current)

            current = {
                "SSID": "(Hidden)",
                "BSSID": line.split("Address:", 1)[1].strip(),
                "Signal": "-",
                "Security": "Unknown",
                "Channel": "-"
            }

        elif current is not None:
            match = re.search(r'ESSID:"(.*)"', line)
            if match:
                current["SSID"] = match.group(1) or "(Hidden)"

            match = re.search(r"Quality[=:]([^ ]+)", line)
            if match:
                current["Signal"] = match.group(1)

            match = re.search(r"Channel[:=](\d+)", line)
            if match:
                current["Channel"] = match.group(1)

            if "WPA2" in line or "WPA" in line:
                current["Security"] = "WPA/WPA2"
            elif "Encryption key:off" in line:
                current["Security"] = "Open"

    if current:
        networks.append(current)

    return networks


def scan_macos():
    candidates = [
        "/System/Library/PrivateFrameworks/Apple80211.framework/"
        "Versions/Current/Resources/airport",
        "/System/Library/PrivateFrameworks/Apple80211.framework/"
        "Versions/A/Resources/airport"
    ]

    airport = next((p for p in candidates if os.path.exists(p)), None)

    if not airport:
        raise RuntimeError(
            "Pemindai airport tidak tersedia pada versi macOS ini."
        )

    rc, output, error = run_command([airport, "-s"], 25)

    if rc != 0:
        raise RuntimeError(error or "Pemindaian macOS gagal.")

    networks = []

    for line in output.splitlines()[1:]:
        parts = line.split()

        if len(parts) >= 7:
            networks.append({
                "SSID": parts[0],
                "BSSID": parts[1],
                "Signal": parts[2] + " dBm",
                "Channel": parts[3],
                "Security": " ".join(parts[6:])
            })

    return networks


def show_results(networks, elapsed):
    print()
    UI.line("═")
    print(f"{UI.WHITE}{UI.BOLD}  SCAN RESULTS{UI.RESET}")
    UI.line("═")

    UI.status("Duration", f"{elapsed:.2f} seconds", UI.CYAN)
    UI.status(
        "Networks",
        str(len(networks)),
        UI.GREEN if networks else UI.YELLOW
    )
    UI.line()

    if not networks:
        print(f"  {UI.YELLOW}No networks reported.{UI.RESET}")
        print("  Check Wi-Fi adapter, driver and OS permissions.")
        UI.line("═")
        return

    for index, net in enumerate(networks, 1):
        ssid = str(net.get("SSID") or "(Hidden)")
        ssid = ssid.replace("\n", " ")[:40]

        bssid = net.get("BSSID", "-")
        if isinstance(bssid, list):
            bssid = ", ".join(bssid) or "-"

        print(
            f"  {UI.CYAN}{UI.BOLD}[{index:02d}]{UI.RESET} "
            f"{UI.WHITE}{UI.BOLD}{ssid}{UI.RESET}"
        )
        print(f"       BSSID    : {bssid}")
        print(f"       Signal   : {net.get('Signal', '-')}")
        print(f"       Channel  : {net.get('Channel', '-')}")
        print(f"       Security : {net.get('Security', '-')}")
        UI.line("·", 36)

    print(f"{UI.DIM}  KEY GANTENG • WIFI SCANNER{UI.RESET}")
    print(f"{UI.DIM}  Scan only; no password testing or disconnection.{UI.RESET}")
    UI.line("═")


def main():
    UI.enable()
    UI.header()

    system = platform.system()
    UI.status("Status", "Starting scan...", UI.YELLOW)
    started = time.monotonic()

    try:
        if system == "Windows":
            networks = scan_windows()

        elif system == "Linux":
            if shutil.which("nmcli"):
                try:
                    networks = scan_linux_nmcli()
                except RuntimeError:
                    networks = scan_linux_iwlist()
            else:
                networks = scan_linux_iwlist()

        elif system == "Darwin":
            networks = scan_macos()

        else:
            raise RuntimeError(
                f"Operating system {system} is not supported."
            )

        elapsed = time.monotonic() - started
        UI.status("Status", "Scan completed", UI.GREEN)
        show_results(networks, elapsed)

    except RuntimeError as error:
        print()
        UI.line("═")
        UI.status("Status", "Scan failed", UI.RED)
        print(f"  {UI.RED}{error}{UI.RESET}")
        print("  Check Wi-Fi adapter, driver, permissions and OS tools.")

        if system == "Linux":
            print("  Linux: NetworkManager/nmcli or iwlist is required.")
        elif system == "Windows":
            print("  Windows: check Wi-Fi adapter and WLAN AutoConfig.")

        print("  A normal VPS/container usually has no physical Wi-Fi radio.")
        UI.line("═")
        sys.exit(1)


if __name__ == "__main__":
    main()
