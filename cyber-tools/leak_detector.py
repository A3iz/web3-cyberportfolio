#!/usr/bin/env python3
"""
Leak Detector - Cybersecurity Tool for Data Breach Detection
Author: Abdulaziz Althari
Description: Scans text files for potential leaked emails, passwords, and sensitive data
"""

import re
import sys
import os
from pathlib import Path
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    print("Warning: colorama not installed. Install with: pip install colorama")

class LeakDetector:
    def __init__(self):
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.password_patterns = {
            'weak_password': re.compile(r'\b(?:password|pass|pwd|secret)\s*[:=]\s*(\w+)', re.IGNORECASE),
            'hash_md5': re.compile(r'\b[a-f0-9]{32}\b'),
            'hash_sha1': re.compile(r'\b[a-f0-9]{40}\b'),
            'hash_sha256': re.compile(r'\b[a-f0-9]{64}\b'),
            'api_key': re.compile(r'\b(?:api[_-]?key|apikey|access[_-]?token)\s*[:=]\s*[\'"]?([a-zA-Z0-9_-]{20,})[\'"]?', re.IGNORECASE),
            'jwt_token': re.compile(r'\beyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\b'),
            'private_key': re.compile(r'-----BEGIN (?:RSA )?PRIVATE KEY-----'),
        }
        self.credit_card_pattern = re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b')
        self.ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
        self.phone_pattern = re.compile(r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b')
        
        self.findings = {
            'emails': [],
            'passwords': [],
            'credit_cards': [],
            'ssns': [],
            'phones': [],
            'api_keys': [],
            'hashes': [],
            'tokens': []
        }

    def colorize(self, text, color_code):
        """Apply color to text if colorama is available"""
        if COLORAMA_AVAILABLE:
            return f"{color_code}{text}{Style.RESET_ALL}"
        return text

    def scan_file(self, filepath):
        """Scan a file for potential data leaks"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                lines = content.split('\n')
                
            print(f"\n{self.colorize('='*60, Fore.CYAN)}")
            print(f"{self.colorize(f'SCANNING: {filepath}', Fore.CYAN)}")
            print(f"{self.colorize('='*60, Fore.CYAN)}")
            
            # Scan for emails
            emails = self.email_pattern.findall(content)
            if emails:
                self.findings['emails'].extend(emails)
                print(f"\n{self.colorize('[EMAIL] EMAIL ADDRESSES FOUND:', Fore.YELLOW)}")
                for email in set(emails):
                    print(f"  {self.colorize('->', Fore.RED)} {email}")
            
            # Scan for passwords and secrets
            for pattern_name, pattern in self.password_patterns.items():
                matches = pattern.findall(content)
                if matches:
                    if pattern_name == 'weak_password':
                        self.findings['passwords'].extend(matches)
                        print(f"\n{self.colorize('[PASSWORD] POTENTIAL PASSWORDS:', Fore.RED)}")
                        for match in set(matches):
                            print(f"  {self.colorize('->', Fore.RED)} {match}")
                    elif pattern_name in ['hash_md5', 'hash_sha1', 'hash_sha256']:
                        self.findings['hashes'].extend(matches)
                        print(f"\n{self.colorize(f'[HASH] {pattern_name.upper()} HASHES:', Fore.MAGENTA)}")
                        for match in set(matches):
                            print(f"  {self.colorize('->', Fore.RED)} {match[:20]}...")
                    elif pattern_name == 'api_key':
                        self.findings['api_keys'].extend(matches)
                        print(f"\n{self.colorize('[API] API KEYS/TOKENS:', Fore.RED)}")
                        for match in set(matches):
                            print(f"  {self.colorize('->', Fore.RED)} {match}")
                    elif pattern_name == 'jwt_token':
                        self.findings['tokens'].extend(matches)
                        print(f"\n{self.colorize('[JWT] JWT TOKENS:', Fore.RED)}")
                        for match in set(matches):
                            print(f"  {self.colorize('->', Fore.RED)} {match[:30]}...")
                    elif pattern_name == 'private_key':
                        print(f"\n{self.colorize('[PRIVATE] PRIVATE KEY DETECTED!', Fore.RED)}")
                        print(f"  {self.colorize('-> CRITICAL SECURITY RISK', Fore.RED)}")
            
            # Scan for credit cards
            credit_cards = self.credit_card_pattern.findall(content)
            if credit_cards:
                self.findings['credit_cards'].extend(credit_cards)
                print(f"\n{self.colorize('[CREDIT] POTENTIAL CREDIT CARDS:', Fore.RED)}")
                for cc in set(credit_cards):
                    print(f"  {self.colorize('->', Fore.RED)} {cc}")
            
            # Scan for SSNs
            ssns = self.ssn_pattern.findall(content)
            if ssns:
                self.findings['ssns'].extend(ssns)
                print(f"\n{self.colorize('[SSN] SOCIAL SECURITY NUMBERS:', Fore.RED)}")
                for ssn in set(ssns):
                    print(f"  {self.colorize('->', Fore.RED)} {ssn}")
            
            # Scan for phone numbers
            phones = self.phone_pattern.findall(content)
            if phones:
                formatted_phones = [f"({match[0]}) {match[1]}-{match[2]}" for match in phones]
                self.findings['phones'].extend(formatted_phones)
                print(f"\n{self.colorize('[PHONE] PHONE NUMBERS:', Fore.YELLOW)}")
                for phone in set(formatted_phones):
                    print(f"  {self.colorize('->', Fore.YELLOW)} {phone}")
                    
        except Exception as e:
            print(f"{self.colorize(f'Error scanning {filepath}: {str(e)}', Fore.RED)}")

    def generate_report(self):
        """Generate a summary report of findings"""
        print(f"\n{self.colorize('='*60, Fore.GREEN)}")
        print(f"{self.colorize('LEAK DETECTION SUMMARY REPORT', Fore.GREEN)}")
        print(f"{self.colorize('='*60, Fore.GREEN)}")
        
        total_findings = sum(len(v) for v in self.findings.values())
        
        if total_findings == 0:
            print(f"{self.colorize('[OK] No potential data leaks detected!', Fore.GREEN)}")
        else:
            print(f"{self.colorize(f'[WARNING] Total potential leaks found: {total_findings}', Fore.YELLOW)}")
            
            for category, items in self.findings.items():
                if items:
                    print(f"\n{self.colorize(f'{category.upper()}:', Fore.CYAN)} {len(items)} found")
            
            # Risk assessment
            risk_level = "LOW"
            if self.findings['passwords'] or self.findings['api_keys'] or self.findings['credit_cards']:
                risk_level = "HIGH"
            elif self.findings['emails'] or self.findings['hashes']:
                risk_level = "MEDIUM"
                
            color = Fore.GREEN if risk_level == "LOW" else Fore.YELLOW if risk_level == "MEDIUM" else Fore.RED
            print(f"\n{self.colorize(f'[RISK] RISK LEVEL: {risk_level}', color)}")
            
            # Recommendations
            print(f"\n{self.colorize('[SECURITY] SECURITY RECOMMENDATIONS:', Fore.CYAN)}")
            if self.findings['passwords']:
                print("  • Remove hardcoded passwords immediately")
            if self.findings['api_keys']:
                print("  • Rotate all exposed API keys")
            if self.findings['credit_cards']:
                print("  • Remove credit card data from files")
            if self.findings['emails']:
                print("  • Consider if email exposure is necessary")
            print("  • Use environment variables for secrets")
            print("  • Implement proper secret management")
            print("  • Add files to .gitignore if needed")

def main():
    detector = LeakDetector()
    
    print(f"{detector.colorize('LEAK DETECTOR - Cybersecurity Tool', Fore.CYAN)}")
    print(f"{detector.colorize('Author: Abdulaziz Althari', Fore.CYAN)}")
    print(f"{detector.colorize('-' * 50, Fore.CYAN)}")
    
    # Check if file argument provided
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        # Default to leaks.txt in same directory
        filepath = Path(__file__).parent / "leaks.txt"
    
    if not os.path.exists(filepath):
        print(f"{detector.colorize(f'[ERROR] File not found: {filepath}', Fore.RED)}")
        print(f"Usage: python {sys.argv[0]} <filepath>")
        print(f"Or create a 'leaks.txt' file in the same directory")
        return
    
    detector.scan_file(filepath)
    detector.generate_report()

if __name__ == "__main__":
    main()
