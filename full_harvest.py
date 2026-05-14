#!/usr/bin/env python3
"""
Complete Harvest Function Module
"""

from colorama import Fore, Style

from dns_core import lookup_domain
from email_harvest import harvest_emails_google, harvest_emails_bing, harvest_emails_github
from subdomain_discovery import discover_subdomains_crtsh, discover_subdomains_dnsdumpster, discover_subdomains_alienvault
from harvest_core import harvest_employee_names, harvest_social_media, harvest_technologies, harvest_urls

REQUESTS_AVAILABLE = True
COLORAMA_AVAILABLE = True

def print_colored(text, color=Fore.WHITE, bold=False):
    if COLORAMA_AVAILABLE:
        style = Style.BRIGHT if bold else ''
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def full_harvest(domain, sources=None, output_file=None):
    """Complete OSINT harvesting - All 54 features with IPs!"""
    
    if sources is None:
        sources = ['all']
    
    results = {
        'domain': domain,
        'timestamp': datetime.now().isoformat(),
        'main_ip': None,
        'emails': [],
        'subdomains': [],
        'subdomain_ips': {},
        'ips': [],
        'employee_names': [],
        'social_media': [],
        'technologies': [],
        'urls': [],
        'dns_records': {}
    }
    
    print_colored(f"\n{'='*70}", Fore.CYAN)
    print_colored(f"🔍 OSINT HARVESTING TARGET: {domain}", Fore.YELLOW, bold=True)
    print_colored(f"{'='*70}", Fore.CYAN)
    
    # 0. Main Domain IP
    print_colored(f"\n📍 [0/8] MAIN DOMAIN IP...", Fore.GREEN)
    main_result = lookup_domain(domain, 'A', timeout=5, use_cache=False)
    if main_result['success'] and 'has address' in main_result['output']:
        results['main_ip'] = main_result['output'].split('has address')[-1].strip().split('\n')[0]
        print_colored(f"  ✅ {domain} → {results['main_ip']}", Fore.GREEN)
    else:
        print_colored(f"  ❌ Could not resolve {domain}", Fore.RED)
    
    # 1. Email Harvesting
    if 'all' in sources or 'emails' in sources:
        print_colored(f"\n📧 [1/8] Harvesting Email Addresses...", Fore.GREEN)
        if REQUESTS_AVAILABLE:
            emails = set()
            print_colored("  → Google search...", Fore.CYAN)
            emails.update(harvest_emails_google(domain))
            print_colored("  → Bing search...", Fore.CYAN)
            emails.update(harvest_emails_bing(domain))
            print_colored("  → GitHub mining...", Fore.CYAN)
            emails.update(harvest_emails_github(domain))
            results['emails'] = list(emails)
            print_colored(f"  ✅ Found {len(results['emails'])} emails", Fore.GREEN)
            for email in list(emails)[:10]:
                print_colored(f"     • {email}", Fore.WHITE)
    
    # 2. Subdomain Discovery with IPs
    if 'all' in sources or 'subdomains' in sources:
        print_colored(f"\n🌐 [2/8] Discovering Subdomains...", Fore.GREEN)
        if REQUESTS_AVAILABLE:
            subdomains = set()
            print_colored("  → crt.sh (SSL Certificates)...", Fore.CYAN)
            subdomains.update(discover_subdomains_crtsh(domain))
            print_colored("  → DNSDumpster/HackerTarget...", Fore.CYAN)
            subdomains.update(discover_subdomains_dnsdumpster(domain))
            print_colored("  → AlienVault OTX...", Fore.CYAN)
            subdomains.update(discover_subdomains_alienvault(domain))
            results['subdomains'] = list(subdomains)
            print_colored(f"  ✅ Found {len(results['subdomains'])} subdomains", Fore.GREEN)
    
    # 3. IP Resolution for Subdomains
    if results['subdomains']:
        print_colored(f"\n🔍 [3/8] Resolving Subdomain IPs...", Fore.GREEN)
        print_colored(f"{'No.':<5} {'Subdomain':<45} {'IP Address':<20}", Fore.YELLOW)
        print_colored(f"{'-'*70}", Fore.YELLOW)
        
        count = 0
        for sub in results['subdomains'][:50]:
            count += 1
            result = lookup_domain(sub, 'A', timeout=3, use_cache=False)
            ip = "❌ Not Resolved"
            if result['success'] and 'has address' in result['output']:
                ip = result['output'].split('has address')[-1].strip().split('\n')[0]
                results['subdomain_ips'][sub] = ip
                results['ips'].append(ip)
            
            if ip != "❌ Not Resolved":
                print_colored(f"{count:<5} {sub:<45} {Fore.GREEN}{ip:<20}{Style.RESET_ALL}", Fore.WHITE)
            else:
                print_colored(f"{count:<5} {sub:<45} {Fore.RED}{ip:<20}{Style.RESET_ALL}", Fore.WHITE)
        
        results['ips'] = list(set(results['ips']))
        print_colored(f"\n  ✅ Found {len(results['ips'])} unique IPs from subdomains", Fore.GREEN)
    
    # 4. Employee Names
    if 'all' in sources or 'employees' in sources:
        print_colored(f"\n👥 [4/8] Extracting Employee Names...", Fore.GREEN)
        results['employee_names'] = harvest_employee_names(domain)
        print_colored(f"  ✅ Found {len(results['employee_names'])} potential employees", Fore.GREEN)
        for name in results['employee_names'][:10]:
            print_colored(f"     • {name}", Fore.WHITE)
    
    # 5. Social Media
    if 'all' in sources or 'social' in sources:
        print_colored(f"\n📱 [5/8] Discovering Social Media...", Fore.GREEN)
        results['social_media'] = harvest_social_media(domain)
        print_colored(f"  ✅ Found {len(results['social_media'])} platforms", Fore.GREEN)
        for item in results['social_media']:
            print_colored(f"     • {item['platform'].title()}: {item['url']}", Fore.CYAN)
    
    # 6. Technology Detection
    if 'all' in sources or 'tech' in sources:
        print_colored(f"\n💻 [6/8] Detecting Technologies...", Fore.GREEN)
        results['technologies'] = harvest_technologies(domain)
        for tech in results['technologies']:
            print_colored(f"     • {tech}", Fore.CYAN)
    
    # 7. URL Discovery
    if 'all' in sources or 'urls' in sources:
        print_colored(f"\n🔗 [7/8] Discovering URLs/Paths...", Fore.GREEN)
        results['urls'] = harvest_urls(domain)
        for url in results['urls']:
            print_colored(f"     • {url}", Fore.CYAN)
    
    # 8. DNS Records Summary
    print_colored(f"\n📊 [8/8] DNS RECORDS SUMMARY", Fore.YELLOW, bold=True)
    print_colored(f"{'='*70}", Fore.CYAN)
    for record_type in ['A', 'MX', 'NS', 'TXT']:
        result = lookup_domain(domain, record_type, use_cache=True)
        if result['success']:
            results['dns_records'][record_type] = result['output']
            print_colored(f"  {record_type}:", Fore.GREEN)
            for line in result['output'].split('\n')[:2]:
                if line.strip():
                    print_colored(f"    {line[:80]}", Fore.WHITE)
    
    # Final Summary
    print_colored(f"\n{'='*70}", Fore.CYAN)
    print_colored(f"📈 HARVESTING SUMMARY", Fore.YELLOW, bold=True)
    print_colored(f"{'='*70}", Fore.CYAN)
    print_colored(f"📍 Main Domain IP: {results['main_ip'] or 'Not Found'}", Fore.GREEN)
    print_colored(f"📧 Emails Found: {len(results['emails'])}", Fore.GREEN)
    print_colored(f"🌐 Subdomains Found: {len(results['subdomains'])}", Fore.GREEN)
    print_colored(f"🖥️  Unique IPs Found: {len(results['ips'])}", Fore.GREEN)
    print_colored(f"👥 Employee Names: {len(results['employee_names'])}", Fore.GREEN)
    print_colored(f"💻 Technologies: {len(results['technologies'])}", Fore.GREEN)
    print_colored(f"🔗 URLs Found: {len(results['urls'])}", Fore.GREEN)
    
    if output_file:
        import json
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print_colored(f"\n💾 Full results saved to {output_file}", Fore.GREEN)
    
    return results

# Import datetime for timestamp
from datetime import datetime