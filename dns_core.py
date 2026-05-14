#!/usr/bin/env python3
"""
DNS Core Functions Module
"""
import os
import subprocess
import time
from subprocess import PIPE
from colorama import Fore

from config import get_from_cache, add_to_cache
from os_detection import get_os_optimized_command

COLORAMA_AVAILABLE = True

def print_colored(text, color=Fore.WHITE, bold=False):
    if COLORAMA_AVAILABLE:
        from colorama import Style
        style = Style.BRIGHT if bold else ''
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def lookup_domain(domain, record_type='A', server=None, timeout=5, measure_time=False, use_cache=True):
    command = []
    start_time = None
    
    cache_key = f"{domain}:{record_type}:{server or 'default'}"
    if use_cache:
        cached_result = get_from_cache(cache_key)
        if cached_result:
            print_colored(f"[*] Using cached result for {domain}", Fore.CYAN)
            return cached_result
    
    command = get_os_optimized_command(domain, record_type, server)
    
    try:
        if measure_time:
            start_time = time.time()
        
        process = subprocess.Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout_data, stderr_data = process.communicate(timeout=timeout)
        
        response_time = None
        if measure_time and start_time:
            response_time = round((time.time() - start_time) * 1000, 2)
        
        result = {
            "success": process.returncode == 0,
            "output": stdout_data if process.returncode == 0 else stderr_data,
            "error": stderr_data if process.returncode != 0 else None,
            "response_time": response_time,
            "command": ' '.join(command)
        }
        
        if use_cache and result['success']:
            add_to_cache(cache_key, result)
        return result
    
    except subprocess.TimeoutExpired:
        process.kill()
        return {"success": False, "error": f"Timeout after {timeout} seconds"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def reverse_dns_lookup(ip_address, timeout=5):
    print_colored(f"\n[*] Reverse DNS lookup for: {ip_address}", Fore.CYAN)
    try:
        process = subprocess.Popen(["host", ip_address], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        out, err = process.communicate(timeout=timeout)
        if process.returncode == 0:
            for line in out.split('\n'):
                if 'domain name pointer' in line:
                    domain = line.split('domain name pointer')[-1].strip()
                    print_colored(f"[+] Found: {domain}", Fore.GREEN)
                    return domain
            print_colored(out, Fore.GREEN)
            return out
    except Exception as e:
        print_colored(f"[-] Error: {e}", Fore.RED)
    return None

def compare_dns_servers(domain, servers, record_type='A', timeout=5):
    print_colored(f"\n[*] Comparing DNS servers for: {domain}", Fore.CYAN)
    print_colored(f"{'Server':<20} {'Response Time':<15} {'IP Address':<15}", Fore.YELLOW)
    print_colored("-"*70, Fore.YELLOW)
    
    results = {}
    for server in servers:
        result = lookup_domain(domain, record_type, server, timeout, measure_time=True, use_cache=False)
        ip = "N/A"
        if result['success'] and 'has address' in result['output']:
            ip = result['output'].split('has address')[-1].strip().split('\n')[0]
        time_str = f"{result.get('response_time', 'N/A')} ms"
        from colorama import Style
        status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if result['success'] else f"{Fore.RED}✗{Style.RESET_ALL}"
        print_colored(f"{server:<20} {time_str:<15} {status} {ip}", Fore.WHITE)
        results[server] = {'success': result['success'], 'response_time': result.get('response_time'), 'ip': ip}
    return results

def brute_subdomains(domain, wordlist, record_type='A', timeout=3, TQDM_AVAILABLE=False):
    if not os.path.exists(wordlist):
        print_colored(f"[-] Wordlist not found: {wordlist}", Fore.RED)
        return []
    
    print_colored(f"\n[*] Brute forcing subdomains for: {domain}", Fore.CYAN)
    with open(wordlist, 'r') as f:
        subdomains = [line.strip() for line in f if line.strip()]
    
    discovered = []
    if TQDM_AVAILABLE:
        from tqdm import tqdm
        iterator = tqdm(subdomains, desc="Brute forcing")
    else:
        iterator = subdomains
    
    for sub in iterator:
        test_domain = f"{sub}.{domain}"
        result = lookup_domain(test_domain, record_type, timeout=timeout, use_cache=False)
        if result['success']:
            discovered.append(test_domain)
            ip = result['output'].split('has address')[-1].strip() if 'has address' in result['output'] else "Unknown"
            print_colored(f"[+] Found: {test_domain} → {ip}", Fore.GREEN)
    
    print_colored(f"\n[+] Found {len(discovered)} subdomains", Fore.GREEN)
    return discovered