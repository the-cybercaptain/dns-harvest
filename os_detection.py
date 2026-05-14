#!/usr/bin/env python3
"""
OS Detection Module
"""
import os
import subprocess
import sys
import platform
from colorama import Fore, Style

# Import print_colored from main (will be passed)
# For now, define a placeholder
COLORAMA_AVAILABLE = True

def print_colored(text, color=Fore.WHITE, bold=False):
    if COLORAMA_AVAILABLE:
        style = Style.BRIGHT if bold else ''
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def detect_os():
    """Enhanced OS detection with distribution info"""
    os_info = {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'platform': sys.platform,
        'machine': platform.machine(),
        'processor': platform.processor(),
        'hostname': platform.node(),
        'is_kali': False,
        'is_parrot': False,
        'is_ubuntu': False,
        'is_debian': False,
        'is_macos': False,
        'is_windows': False,
        'distro': 'Unknown',
        'distro_version': 'Unknown',
        'dns_tools_available': [],
        'pentesting_tools': []
    }

    if os_info['system'] == 'Linux':
        if os.path.exists('/etc/os-release'):
            try:
                with open('/etc/os-release', 'r') as f:
                    content = f.read().lower()
                    if 'kali' in content:
                        os_info['is_kali'] = True
                        os_info['distro'] = 'Kali Linux'
                    elif 'parrot' in content:
                        os_info['is_parrot'] = True
                        os_info['distro'] = 'Parrot OS'
                    elif 'ubuntu' in content:
                        os_info['is_ubuntu'] = True
                        os_info['distro'] = 'Ubuntu'
                    elif 'debian' in content:
                        os_info['is_debian'] = True
                        os_info['distro'] = 'Debian'
                    
                    try:
                        with open('/etc/os-release', 'r') as f:
                            for line in f:
                                if line.startswith('VERSION_ID='):
                                    os_info['distro_version'] = line.split('=')[1].strip().strip('"')
                                    break
                    except:
                        pass
            except:
                pass

        dns_tools = ['host', 'dig', 'nslookup']
        for tool in dns_tools:
            result = subprocess.run(['which', tool], capture_output=True)
            if result.returncode == 0:
                os_info['dns_tools_available'].append(tool)

        pentest_tools = ['nmap', 'nikto', 'sqlmap', 'metasploit', 'hydra', 'aircrack-ng', 
                        'wireshark', 'burpsuite', 'dnsrecon', 'fierce', 'dnsenum', 
                        'theharvester', 'gobuster', 'wfuzz', 'whois']
        for tool in pentest_tools:
            result = subprocess.run(['which', tool], capture_output=True)
            if result.returncode == 0:
                os_info['pentesting_tools'].append(tool)

    elif os_info['system'] == 'Darwin':
        os_info['is_macos'] = True
        os_info['distro'] = 'macOS'
    elif os_info['system'] == 'Windows':
        os_info['is_windows'] = True
        os_info['distro'] = 'Windows'

    return os_info

def print_os_info_verbose():
    """Print full OS info block (used in verbose mode)"""
    os_info = detect_os()

    print_colored(f"\n{'='*60}", Fore.CYAN)
    print_colored("🖥️  SYSTEM INFORMATION (Verbose Mode)", Fore.YELLOW, bold=True)
    print_colored(f"{'='*60}", Fore.CYAN)

    if os_info['is_kali']:
        print_colored(f"🐉 Distribution OS: {os_info['distro']} {os_info['distro_version']}", Fore.GREEN)
        print_colored("✓ Pentesting Mode: FULLY ENABLED", Fore.GREEN)
    elif os_info['is_parrot']:
        print_colored(f"🦜 Distribution OS: {os_info['distro']} {os_info['distro_version']}", Fore.GREEN)
    elif os_info['is_ubuntu']:
        print_colored(f"🐧 Distribution OS: {os_info['distro']} {os_info['distro_version']}", Fore.CYAN)
    elif os_info['is_macos']:
        print_colored(f"🍎 Distribution OS: {os_info['distro']} {os_info['distro_version']}", Fore.CYAN)
    elif os_info['is_windows']:
        print_colored(f"🪟 Distribution OS: {os_info['distro']} {os_info['distro_version']}", Fore.CYAN)
    else:
        print_colored(f"💻 Distribution OS: {os_info['system']} {os_info['release']}", Fore.WHITE)

    print_colored(f"🏷️  System: {os_info['system']}", Fore.WHITE)
    print_colored(f"📟 Release: {os_info['release']}", Fore.WHITE)
    print_colored(f"🖥️  Architecture: {os_info['machine']}", Fore.WHITE)
    print_colored(f"🌐 Hostname: {os_info['hostname']}", Fore.WHITE)
    print_colored(f"⚙️  Platform: {os_info['platform']}", Fore.WHITE)

    print_colored(f"\n📡 DNS Tools Available:", Fore.YELLOW)
    if os_info['dns_tools_available']:
        for tool in os_info['dns_tools_available']:
            result = subprocess.run(['which', tool], capture_output=True, text=True)
            path = result.stdout.strip() if result.returncode == 0 else "unknown"
            print_colored(f"  ✅ {tool} ({path})", Fore.GREEN)
    else:
        print_colored(f"  ❌ No DNS tools found! Install dnsutils", Fore.RED)

    if os_info['pentesting_tools']:
        print_colored(f"\n🔐 Pentesting Tools Available:", Fore.YELLOW)
        for tool in os_info['pentesting_tools']:
            result = subprocess.run(['which', tool], capture_output=True, text=True)
            path = result.stdout.strip() if result.returncode == 0 else "unknown"
            print_colored(f"  🛠️  {tool} ({path})", Fore.MAGENTA)

    print_colored(f"\n🐍 Python Environment:", Fore.YELLOW)
    print_colored(f"   Version: {sys.version.split()[0]}", Fore.WHITE)
    print_colored(f"   Path: {sys.executable}", Fore.WHITE)

    print_colored(f"{'='*60}\n", Fore.CYAN)
    
    return os_info

def check_system_compatibility(REQUESTS_AVAILABLE):
    """Check if system has required tools"""
    os_info = detect_os()
    print_colored("[*] Checking system compatibility...", Fore.CYAN)

    if os_info['dns_tools_available']:
        print_colored(f"[+] DNS tools found: {', '.join(os_info['dns_tools_available'])}", Fore.GREEN)
    else:
        print_colored("[-] No DNS tools found! Install dnsutils", Fore.RED)

    if REQUESTS_AVAILABLE:
        print_colored("[+] Requests library available", Fore.GREEN)
    else:
        print_colored("[-] Install: pip install requests", Fore.YELLOW)

def get_os_optimized_command(domain, record_type='A', server=None):
    """Get OS-optimized DNS command"""
    if sys.platform.startswith("win"):
        cmd = ["nslookup", "-type=" + record_type, domain]
        if server:
            cmd.extend([server])
    else:
        if record_type == 'A':
            cmd = ["host", domain]
        else:
            cmd = ["host", "-t", record_type, domain]
        if server:
            cmd.append(server)
    return cmd