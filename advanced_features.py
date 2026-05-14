#!/usr/bin/env python3
"""
Advanced DNS Features Module
"""

import subprocess
import random
import string
import requests
from subprocess import PIPE
from colorama import Fore, Back

from dns_core import lookup_domain

REQUESTS_AVAILABLE = True
COLORAMA_AVAILABLE = True

def print_colored(text, color=Fore.WHITE, bold=False):
    if COLORAMA_AVAILABLE:
        from colorama import Style
        style = Style.BRIGHT if bold else ''
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def test_zone_transfer(domain, server=None, timeout=10):
    print_colored(f"\n[*] Testing zone transfer for: {domain}", Fore.CYAN)
    dig_cmd = ["dig", "@" + (server or domain), domain, "AXFR"]
    try:
        process = subprocess.Popen(dig_cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        out, err = process.communicate(timeout=timeout)
        if "Transfer failed" not in out and "failed" not in err.lower():
            if ";" in out and len(out) > 100:
                print_colored("[+] ZONE TRANSFER SUCCESSFUL! (Vulnerable)", Fore.GREEN + Back.RED)
                print(out[:2000])
                return out
        print_colored("[-] Zone transfer failed", Fore.RED)
    except FileNotFoundError:
        print_colored("[-] 'dig' command not found", Fore.RED)
    return None

def dns_over_https(domain, record_type='A'):
    if not REQUESTS_AVAILABLE:
        print_colored("[-] Install requests: pip install requests", Fore.RED)
        return None
    
    print_colored(f"\n[*] DNS over HTTPS for: {domain}", Fore.CYAN)
    record_map = {'A': 1, 'AAAA': 28, 'MX': 15, 'TXT': 16, 'NS': 2, 'CNAME': 5}
    url = f"https://cloudflare-dns.com/dns-query?name={domain}&type={record_map.get(record_type, 1)}"
    
    try:
        response = requests.get(url, headers={'Accept': 'application/dns-json'}, timeout=10)
        data = response.json()
        if response.status_code == 200 and data.get('Answer'):
            for answer in data['Answer']:
                print(f"  {answer['data']}")
            return data
    except Exception as e:
        print_colored(f"[-] DOH Error: {e}", Fore.RED)
    return None

def whois_lookup(domain):
    print_colored(f"\n[*] WHOIS lookup for: {domain}", Fore.CYAN)
    try:
        process = subprocess.Popen(["whois", domain], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        out, err = process.communicate(timeout=15)
        if process.returncode == 0:
            print(out[:5000])
            return out
    except FileNotFoundError:
        print_colored("[-] WHOIS not found. Install: sudo apt install whois", Fore.RED)
    return None

def detect_dns_spoofing(domain):
    print_colored(f"\n[*] DNS Spoofing Detection for: {domain}", Fore.CYAN)
    servers = ['8.8.8.8', '1.1.1.1', '9.9.9.9']
    ips = []
    
    for server in servers:
        result = lookup_domain(domain, 'A', server, use_cache=False)
        if result['success'] and 'has address' in result['output']:
            ip = result['output'].split('has address')[-1].strip()
            ips.append(ip)
            print_colored(f"  {server} -> {ip}", Fore.WHITE)
    
    if len(set(ips)) > 1:
        print_colored("[!] WARNING: Multiple IPs detected - Possible spoofing!", Fore.RED)
    else:
        print_colored("[+] All servers returned same IP - No spoofing detected", Fore.GREEN)

def detect_wildcard_dns(domain):
    print_colored(f"\n[*] Wildcard DNS Detection for: {domain}", Fore.CYAN)
    random_sub = ''.join(random.choices(string.ascii_lowercase, k=15))
    test_domain = f"{random_sub}.{domain}"
    result = lookup_domain(test_domain, 'A', use_cache=False)
    
    if result['success']:
        ip = result['output'].split('has address')[-1].strip() if 'has address' in result['output'] else "Unknown"
        print_colored(f"[!] WARNING: Wildcard DNS detected! ({test_domain} resolves to {ip})", Fore.RED)
        return True
    else:
        print_colored("[+] No wildcard DNS detected", Fore.GREEN)
        return False