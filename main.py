#!/usr/bin/env python3
"""
Professional DNS & OSINT Harvesting Tool - Ultimate Edition
Main Entry Point - Calls all modules
"""

import sys
import argparse
import json
import os

# Import all modules
from config import clear_cache
from os_detection import detect_os, print_os_info_verbose, check_system_compatibility, get_os_optimized_command
from dns_core import lookup_domain, reverse_dns_lookup, compare_dns_servers, brute_subdomains
from email_harvest import harvest_emails_google, harvest_emails_bing, harvest_emails_github
from subdomain_discovery import harvest_subdomains_with_ips, discover_subdomains_crtsh, discover_subdomains_dnsdumpster, discover_subdomains_alienvault
from advanced_features import test_zone_transfer, dns_over_https, whois_lookup, detect_dns_spoofing, detect_wildcard_dns
from harvest_core import harvest_employee_names, harvest_social_media, harvest_technologies, harvest_urls
from full_harvest import full_harvest
from output_handlers import export_to_csv, batch_lookup, read_domains_from_file

# Import colorama for banner
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
    class Back:
        RED = GREEN = YELLOW = CYAN = WHITE = BLACK = ''
        RESET = ''
    init = lambda: None

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
    BS4_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    BS4_AVAILABLE = False

init()

# ==================== UI BANNER ====================

def show_banner():
    banner = f"""
{Fore.CYAN}{'='*70}{Style.RESET_ALL}
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.YELLOW}║{Style.RESET_ALL}          {Fore.GREEN}🔍 DNS & OSINT HARVESTING TOOL - ULTIMATE EDITION{Style.RESET_ALL}          {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║{Style.RESET_ALL}                   {Fore.CYAN}70+ Professional Features{Style.RESET_ALL}                         {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
{Fore.CYAN}{'='*70}{Style.RESET_ALL}
{Fore.WHITE}📧 Email Harvesting    🌐 Subdomain Discovery    👥 Employee Names{Style.RESET_ALL}
{Fore.WHITE}📱 Social Media        💻 Technology Detection   🔗 URL Discovery{Style.RESET_ALL}
{Fore.WHITE}🔍 DNS Records         🛡️  Security Features     📊 Data Export{Style.RESET_ALL}
{Fore.CYAN}{'='*70}{Style.RESET_ALL}
"""
    print(banner)

def print_colored(text, color=Fore.WHITE, bold=False):
    if COLORAMA_AVAILABLE:
        style = Style.BRIGHT if bold else ''
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

# ==================== MAIN FUNCTION ====================

def main():
    parser = argparse.ArgumentParser(
        description="Professional DNS & OSINT Harvesting Tool - 70+ Features",
        epilog="""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              COMPLETE FEATURES                                ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ DNS LOOKUP:          -domain d1 d2 d3    -type A/MX/TXT/NS    -server IP      ║
║ HARVESTING:          --harvest           --harvest-emails     --harvest-sub   ║
║                     --harvest-employees  --harvest-social     --harvest-tech  ║
║                     --harvest-urls                                            ║
║ ADVANCED DNS:        -reverse IP         -axfr                -compare s1 s2  ║
║                     --whois              --doh                --detect-spoof  ║
║                     --detect-wildcard    -brute wordlist                       ║
║ OUTPUT:              -j JSON             -csv CSV             -o FILE         ║
║                     --time               -v verbose (shows OS info auto)      ║
║ SYSTEM:              --check-system      --no-color           --no-cache      ║
║                     --clear-cache        -f FILE                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Main DNS options
    parser.add_argument("-domain", dest="domains", nargs='+', help="Domains to resolve/harvest")
    parser.add_argument("-f", "--file", dest="input_file", help="Read domains from file")
    parser.add_argument("-reverse", dest="reverse_ip", help="Reverse DNS lookup")
    parser.add_argument("-type", dest="record_type", choices=['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME'], default='A')
    parser.add_argument("-server", dest="server", help="DNS server to query")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Timeout in seconds")

    # Harvesting options
    parser.add_argument("--harvest", action="store_true", help="Full OSINT harvest")
    parser.add_argument("--harvest-emails", action="store_true", help="Harvest emails only")
    parser.add_argument("--harvest-subdomains", action="store_true", help="Discover subdomains with IPs")
    parser.add_argument("--harvest-employees", action="store_true", help="Extract employee names only")
    parser.add_argument("--harvest-social", action="store_true", help="Social media discovery only")
    parser.add_argument("--harvest-tech", action="store_true", help="Technology detection only")
    parser.add_argument("--harvest-urls", action="store_true", help="URL discovery only")
    parser.add_argument("--save-harvest", dest="harvest_output", help="Save harvest results to JSON")

    # Advanced DNS features
    parser.add_argument("-brute", dest="wordlist", help="Subdomain brute force")
    parser.add_argument("-axfr", "--zone-transfer", action="store_true", help="Test zone transfer")
    parser.add_argument("-compare", dest="compare_servers", nargs='+', help="Compare DNS servers")
    parser.add_argument("--whois", action="store_true", help="WHOIS lookup")
    parser.add_argument("--doh", action="store_true", help="DNS over HTTPS")
    parser.add_argument("--detect-spoof", action="store_true", help="DNS spoofing detection")
    parser.add_argument("--detect-wildcard", action="store_true", help="Wildcard detection")

    # Output options
    parser.add_argument("-o", "--output", dest="output_file", help="Save to text file")
    parser.add_argument("-csv", dest="csv_file", help="Export to CSV")
    parser.add_argument("-j", "--json", action="store_true", help="JSON output")
    parser.add_argument("--time", action="store_true", help="Measure response time")

    # System options
    parser.add_argument("--check-system", action="store_true", help="Check system compatibility")
    parser.add_argument("--no-color", action="store_true", help="Disable colors")
    parser.add_argument("--no-cache", action="store_true", help="Disable cache")
    parser.add_argument("--clear-cache", action="store_true", help="Clear cache")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Show banner
    show_banner()

    if args.no_color and COLORAMA_AVAILABLE:
        global Fore, Style, Back
        Fore = Style = Back = type('Dummy', (), {'RESET_ALL': '', 'RED': '', 'GREEN': '', 'YELLOW': '', 'CYAN': '', 'MAGENTA': '', 'WHITE': ''})()

    # ==================== VERBOSE MODE ====================
    if args.verbose:
        print_os_info_verbose()

    # System checks
    if args.check_system:
        check_system_compatibility(REQUESTS_AVAILABLE)
        sys.exit(0)
    if args.clear_cache:
        cleared = clear_cache()
        print_colored("[+] Cache cleared" if cleared else "[-] No cache found", Fore.GREEN if cleared else Fore.YELLOW)
        sys.exit(0)

    # File input
    if args.input_file:
        domains = read_domains_from_file(args.input_file)
        if domains:
            args.domains = domains

    # ==================== HARVESTING HANDLERS ====================

    if args.harvest:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        for domain in args.domains:
            full_harvest(domain, ['all'], args.harvest_output)
        sys.exit(0)

    if args.harvest_emails:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        for domain in args.domains:
            print_colored(f"\n📧 Emails for {domain}:", Fore.GREEN)
            emails = set()
            emails.update(harvest_emails_google(domain))
            emails.update(harvest_emails_bing(domain))
            emails.update(harvest_emails_github(domain))
            for email in emails:
                print_colored(f"  • {email}", Fore.WHITE)
            print_colored(f"\n[+] Total: {len(emails)} emails", Fore.CYAN)
        sys.exit(0)

    if args.harvest_subdomains:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        for domain in args.domains:
            harvest_subdomains_with_ips(domain)
        sys.exit(0)

    if args.harvest_employees:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        for domain in args.domains:
            print_colored(f"\n👥 Employees for {domain}:", Fore.GREEN)
            for name in harvest_employee_names(domain):
                print_colored(f"  • {name}", Fore.WHITE)
        sys.exit(0)

    if args.harvest_social:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        for domain in args.domains:
            print_colored(f"\n📱 Social Media for {domain}:", Fore.GREEN)
            for item in harvest_social_media(domain):
                print_colored(f"  • {item['platform'].title()}: {item['url']}", Fore.CYAN)
        sys.exit(0)

    if args.harvest_tech:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        for domain in args.domains:
            print_colored(f"\n💻 Technologies for {domain}:", Fore.GREEN)
            for tech in harvest_technologies(domain):
                print_colored(f"  • {tech}", Fore.CYAN)
        sys.exit(0)

    if args.harvest_urls:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        for domain in args.domains:
            print_colored(f"\n🔗 URLs for {domain}:", Fore.GREEN)
            for url in harvest_urls(domain):
                print_colored(f"  • {url}", Fore.CYAN)
        sys.exit(0)

    # ==================== ADVANCED DNS HANDLERS ====================

    if args.reverse_ip:
        reverse_dns_lookup(args.reverse_ip, args.timeout)
        sys.exit(0)

    if args.zone_transfer:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        test_zone_transfer(args.domains[0], args.server, args.timeout)
        sys.exit(0)

    if args.compare_servers:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        compare_dns_servers(args.domains[0], args.compare_servers, args.record_type, args.timeout)
        sys.exit(0)

    if args.whois:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        for domain in args.domains:
            whois_lookup(domain)
        sys.exit(0)

    if args.doh:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        for domain in args.domains:
            dns_over_https(domain, args.record_type)
        sys.exit(0)

    if args.detect_spoof:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        detect_dns_spoofing(args.domains[0])
        sys.exit(0)

    if args.detect_wildcard:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        detect_wildcard_dns(args.domains[0])
        sys.exit(0)

    if args.wordlist:
        if not args.domains:
            print_colored("[-] Please specify a domain", Fore.RED)
            sys.exit(1)
        brute_subdomains(args.domains[0], args.wordlist, args.record_type, args.timeout, TQDM_AVAILABLE)
        sys.exit(0)

    # ==================== DNS LOOKUP ====================

    if args.domains:
        use_cache = not args.no_cache
        results, csv_data = batch_lookup(args.domains, args.record_type, args.server,
                                         args.timeout, args.verbose, args.output_file, args.time, use_cache)

        if args.csv_file and csv_data:
            export_to_csv(csv_data, args.csv_file)
        if args.json:
            print(json.dumps(results, indent=2, default=str))

        successful = sum(1 for r in results if r['success'])
        print_colored(f"\n{'='*50}", Fore.CYAN)
        print_colored(f"[+] Summary: {successful}/{len(results)} successful", Fore.GREEN)
        print_colored(f"{'='*50}", Fore.CYAN)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n[-] Interrupted by user", Fore.RED)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n[-] Unexpected error: {e}", Fore.RED)
        sys.exit(1)