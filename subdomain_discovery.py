#!/usr/bin/env python3
"""
Subdomain Discovery Module
"""

import requests
from colorama import Fore
from dns_core import lookup_domain

# ==================== FIX: Define COLORAMA_AVAILABLE ====================
try:
    from colorama import init, Fore, Style, Back
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    class Fore:
        RED = GREEN = YELLOW = CYAN = WHITE = BLACK = MAGENTA = ''
        RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = ''
        RESET_ALL = ''
    init = lambda: None

REQUESTS_AVAILABLE = True

def print_colored(text, color=Fore.WHITE, bold=False):
    if COLORAMA_AVAILABLE:
        from colorama import Style
        style = Style.BRIGHT if bold else ''
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def discover_subdomains_crtsh(domain):
    """Discover subdomains using crt.sh"""
    subdomains = set()
    if not REQUESTS_AVAILABLE:
        return list(subdomains)
    
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                name = entry.get('name_value', '')
                if name:
                    for sub in name.split('\n'):
                        sub = sub.strip().lower()
                        if sub.endswith(domain) and sub != domain:
                            subdomains.add(sub)
    except:
        pass
    return list(subdomains)

def discover_subdomains_dnsdumpster(domain):
    """Discover subdomains using DNSDumpster via hackertarget"""
    subdomains = set()
    if not REQUESTS_AVAILABLE:
        return list(subdomains)
    
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                if line and '.' + domain in line:
                    sub = line.split(',')[0].strip()
                    if sub.endswith(domain):
                        subdomains.add(sub)
    except:
        pass
    return list(subdomains)

def discover_subdomains_alienvault(domain):
    """Discover subdomains using AlienVault OTX"""
    subdomains = set()
    if not REQUESTS_AVAILABLE:
        return list(subdomains)
    
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('passive_dns', []):
                host = item.get('hostname', '')
                if host and host.endswith(domain):
                    subdomains.add(host)
    except:
        pass
    return list(subdomains)

def harvest_subdomains_with_ips(domain):
    """Discover subdomains and show their IP addresses"""
    print_colored(f"\n{'='*70}", Fore.CYAN)
    print_colored(f"🌐 DISCOVERING SUBDOMAINS FOR: {domain}", Fore.YELLOW, bold=True)
    print_colored(f"{'='*70}", Fore.CYAN)
    
    print_colored(f"\n📍 MAIN DOMAIN INFORMATION:", Fore.GREEN)
    main_result = lookup_domain(domain, 'A', timeout=5, use_cache=False)
    if main_result['success'] and 'has address' in main_result['output']:
        main_ip = main_result['output'].split('has address')[-1].strip().split('\n')[0]
        print_colored(f"   {domain} → {main_ip}", Fore.CYAN)
    else:
        print_colored(f"   {domain} → Could not resolve", Fore.RED)
    
    print_colored(f"\n🔍 SCANNING FOR SUBDOMAINS...", Fore.GREEN)
    subs = set()
    subs.update(discover_subdomains_crtsh(domain))
    subs.update(discover_subdomains_dnsdumpster(domain))
    subs.update(discover_subdomains_alienvault(domain))
    
    if not subs:
        print_colored(f"   No subdomains found", Fore.YELLOW)
        return []
    
    print_colored(f"\n{'='*80}", Fore.CYAN)
    print_colored(f"{'No.':<5} {'Subdomain':<45} {'IP Address':<20}", Fore.YELLOW)
    print_colored(f"{'='*80}", Fore.CYAN)
    
    valid_subs = []
    count = 0
    for sub in sorted(subs)[:100]:
        count += 1
        result = lookup_domain(sub, 'A', timeout=3, use_cache=False)
        ip = "❌ Not Resolved"
        if result['success'] and 'has address' in result['output']:
            ip = result['output'].split('has address')[-1].strip().split('\n')[0]
            valid_subs.append(sub)
        
        from colorama import Style
        if ip != "❌ Not Resolved":
            print_colored(f"{count:<5} {sub:<45} {Fore.GREEN}{ip:<20}{Style.RESET_ALL}", Fore.WHITE)
        else:
            print_colored(f"{count:<5} {sub:<45} {Fore.RED}{ip:<20}{Style.RESET_ALL}", Fore.WHITE)
    
    print_colored(f"{'='*80}", Fore.CYAN)
    print_colored(f"[+] TOTAL SUBDOMAINS FOUND: {len(subs)}", Fore.GREEN)
    print_colored(f"[+] RESOLVED SUBDOMAINS: {len(valid_subs)}", Fore.GREEN)
    print_colored(f"{'='*80}\n", Fore.CYAN)
    
    return list(subs)