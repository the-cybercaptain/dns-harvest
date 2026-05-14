#!/usr/bin/env python3
"""
Email Harvesting Module
"""

import re
import requests

REQUESTS_AVAILABLE = True

def harvest_emails_google(domain, limit=100):
    emails = set()
    if not REQUESTS_AVAILABLE:
        return list(emails)
    
    queries = [f"@{domain}", f"\"@{domain}\" email", f"site:{domain} @{domain}"]
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for query in queries[:2]:
        try:
            url = f"https://www.google.com/search?q={query}&num={min(limit, 50)}"
            response = requests.get(url, headers=headers, timeout=10)
            found = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)
            emails.update([e for e in found if domain in e])
        except:
            pass
    return list(emails)

def harvest_emails_bing(domain, limit=100):
    emails = set()
    if not REQUESTS_AVAILABLE:
        return list(emails)
    
    url = f"https://www.bing.com/search?q=%40{domain}&count={min(limit, 50)}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        found = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)
        emails.update([e for e in found if domain in e])
    except:
        pass
    return list(emails)

def harvest_emails_github(domain):
    emails = set()
    if not REQUESTS_AVAILABLE:
        return list(emails)
    
    url = f"https://api.github.com/search/code?q=@{domain}"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('items', [])[:10]:
                file_response = requests.get(item['url'], headers=headers)
                found = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', file_response.text)
                emails.update([e for e in found if domain in e])
    except:
        pass
    return list(emails)