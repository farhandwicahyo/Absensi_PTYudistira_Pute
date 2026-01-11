"""
Utility untuk mendapatkan informasi perangkat
"""
from flask import request
import re

def get_browser_info():
    """Mendapatkan informasi browser dari user agent"""
    user_agent = request.headers.get('User-Agent', '')
    
    # Detect browser
    if 'Chrome' in user_agent and 'Edg' not in user_agent:
        browser = 'Chrome'
    elif 'Firefox' in user_agent:
        browser = 'Firefox'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        browser = 'Safari'
    elif 'Edg' in user_agent:
        browser = 'Edge'
    elif 'Opera' in user_agent:
        browser = 'Opera'
    else:
        browser = 'Unknown'
    
    return browser

def get_os_info():
    """Mendapatkan informasi OS dari user agent"""
    user_agent = request.headers.get('User-Agent', '')
    
    # Detect OS
    if 'Windows' in user_agent:
        os_name = 'Windows'
    elif 'Mac' in user_agent:
        os_name = 'macOS'
    elif 'Linux' in user_agent:
        os_name = 'Linux'
    elif 'Android' in user_agent:
        os_name = 'Android'
    elif 'iOS' in user_agent:
        os_name = 'iOS'
    else:
        os_name = 'Unknown'
    
    return os_name

def get_device_info():
    """Mendapatkan semua informasi perangkat"""
    return {
        'browser': get_browser_info(),
        'os': get_os_info(),
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', '')
    }
