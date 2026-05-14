#!/usr/bin/env python3
"""
Output Handlers Module
"""

import csv
import json
import os
from datetime import datetime
from colorama import Fore
from tqdm import tqdm

from dns_core import lookup_domain

TQDM_AVAILABLE = True
COLORAMA_AVAILABLE = True

def print_colored(text, color=Fore.WHITE, bold=False):
    if COLORAMA_AVAILABLE:
        from colorama import Style
        style = Style.BRIGHT if bold else ''
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['domain', 'record_type', 'ip_address', 'response_time_ms', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    print_colored(f"[+] Results exported to {filename}", Fore.GREEN)

def save_results_to_file(results, filename):
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode) as f:
        for result in results:
            f.write(f"Domain: {result.get('domain', 'N/A')}\n")
            f.write(f"Output: {result.get('output', 'N/A')}\n")
            f.write("-"*40 + "\n")
    print_colored(f"[+] Results saved to {filename}", Fore.GREEN)

def batch_lookup(domains, record_type, server, timeout, verbose, output_file, measure_time, use_cache=True):
    results = []
    csv_data = []
    iterator = tqdm(domains, desc="Looking up") if TQDM_AVAILABLE and len(domains) > 1 else domains
    
    for domain in iterator:
        if verbose:
            print_colored(f"\n{'='*50}", Fore.CYAN)
            print_colored(f"[*] Looking up: {domain}", Fore.CYAN)
        
        result = lookup_domain(domain, record_type, server, timeout, measure_time, use_cache)
        result['domain'] = domain
        results.append(result)
        
        ip = "N/A"
        if result['success'] and 'has address' in result['output']:
            ip = result['output'].split('has address')[-1].strip().split('\n')[0]
        csv_data.append({'domain': domain, 'record_type': record_type, 'ip_address': ip,
                        'response_time_ms': result.get('response_time', 'N/A'), 'timestamp': datetime.now().isoformat()})
        
        if result['success']:
            print_colored(f"\n[+] Output for {domain} ({ip}):", Fore.GREEN)
            print(result['output'])
        else:
            print_colored(f"\n[-] Failed: {result.get('error')}", Fore.RED)
    
    if output_file:
        save_results_to_file(results, output_file)
    return results, csv_data

def read_domains_from_file(filename):
    if not os.path.exists(filename):
        print_colored(f"[-] File not found: {filename}", Fore.RED)
        return []
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]