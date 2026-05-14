#!/usr/bin/env python3
"""
Core Harvesting Functions Module (Employee, Social, Technology, URLs)
"""

import re
import requests
from colorama import Fore

REQUESTS_AVAILABLE = True
COLORAMA_AVAILABLE = True

def print_colored(text, color=Fore.WHITE, bold=False):
    if COLORAMA_AVAILABLE:
        from colorama import Style
        style = Style.BRIGHT if bold else ''
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def harvest_employee_names(domain):
    employees = set()
    if not REQUESTS_AVAILABLE:
        return list(employees)
    
    url = f"https://www.google.com/search?q=site:linkedin.com+company+{domain}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        names = re.findall(r'([A-Z][a-z]+ [A-Z][a-z]+)', response.text)
        employees.update(names[:20])
    except:
        pass
    return list(employees)

def harvest_social_media(domain):
    social_media = []
    platforms = {
        'twitter': f'https://twitter.com/search?q={domain}',
        'linkedin': f'https://www.linkedin.com/search/results/companies/?keywords={domain}',
        'github': f'https://github.com/search?q={domain}',
        'facebook': f'https://www.facebook.com/search/top/?q={domain}'
    }
    for platform, url in platforms.items():
        social_media.append({'platform': platform, 'url': url})
    return social_media

def harvest_technologies(domain):
    technologies = []
    if not REQUESTS_AVAILABLE:
        return technologies
    
    try:
        response = requests.get(f'http://{domain}', timeout=5)
        if 'Server' in response.headers:
            technologies.append(f"Web Server: {response.headers['Server']}")
        if 'X-Powered-By' in response.headers:
            technologies.append(f"Powered By: {response.headers['X-Powered-By']}")
        if 'wp-content' in response.text:
            technologies.append("WordPress")
        if 'django' in response.text.lower():
            technologies.append("Django")
        if 'rails' in response.text.lower():
            technologies.append("Ruby on Rails")
    except:
        pass
    return technologies

def harvest_urls(domain):
    urls = set()
    if not REQUESTS_AVAILABLE:
        return list(urls)
    
    common_paths = ['/robots.txt', '/sitemap.xml', '/.git/config', '/admin', '/login', '/api', '/wp-admin', '/backup', '/config']
    
    for path in common_paths[:5]:
        try:
            url = f'http://{domain}{path}'
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                urls.add(url)
        except:
            pass
    return list(urls)