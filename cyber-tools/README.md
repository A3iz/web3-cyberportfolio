# Cyber Tools - Data Leak Detection

## Overview
This directory contains cybersecurity tools for detecting potential data breaches and sensitive information exposure. The primary tool is `leak_detector.py`, which scans text files for various types of leaked credentials and sensitive data.

## Tools

### leak_detector.py
A comprehensive Python script that scans files for:
- **Email addresses** - Identifies potential email leaks
- **Passwords** - Detects hardcoded passwords and secrets
- **API Keys & Tokens** - Finds exposed API keys and access tokens
- **Cryptographic Hashes** - Identifies MD5, SHA1, and SHA256 hashes
- **JWT Tokens** - Detects JSON Web Tokens
- **Credit Card Numbers** - Identifies potential credit card data
- **Social Security Numbers** - Finds SSN patterns
- **Phone Numbers** - Detects phone number patterns
- **Private Keys** - Identifies RSA private key headers

## Installation

### Dependencies
```bash
pip install colorama  # For colored output (optional but recommended)
```

### Requirements File
Create a `requirements.txt` if needed:
```
colorama>=0.4.4
```

## Usage

### Basic Usage
```bash
# Scan the default leaks.txt file
python leak_detector.py

# Scan a specific file
python leak_detector.py /path/to/suspicious_file.txt

# Scan multiple files
python leak_detector.py file1.txt
python leak_detector.py file2.log
```

### Sample Output
```
🔍 LEAK DETECTOR - Cybersecurity Tool
Author: Abdulaziz Althari
--------------------------------------------------

============================================================
SCANNING: leaks.txt
============================================================

📧 EMAIL ADDRESSES FOUND:
  → admin@example.com
  → support@company.org

🔑 POTENTIAL PASSWORDS:
  → admin123
  → secretpass

🔐 API KEYS/TOKENS:
  → sk_test_4eC39HqLyjWDarjtT1zdp7dc

============================================================
LEAK DETECTION SUMMARY REPORT
============================================================
⚠️  Total potential leaks found: 15

🚨 RISK LEVEL: HIGH

🛡️  SECURITY RECOMMENDATIONS:
  • Remove hardcoded passwords immediately
  • Rotate all exposed API keys
  • Use environment variables for secrets
```

## Features

### Detection Capabilities
- **Pattern Matching**: Uses regex patterns to identify various data types
- **Risk Assessment**: Automatically categorizes findings by risk level
- **Colored Output**: Visual highlighting of different threat types
- **Comprehensive Reporting**: Detailed summary with security recommendations

### Security Best Practices
- **No Data Storage**: Tool doesn't store or transmit found data
- **Local Processing**: All scanning happens locally
- **Privacy Focused**: Designed for internal security audits

## Integration

### CI/CD Pipeline
```yaml
# Example GitHub Actions integration
- name: Run Leak Detection
  run: |
    python cyber-tools/leak_detector.py logs/
    python cyber-tools/leak_detector.py config/
```

### Pre-commit Hook
```bash
#!/bin/sh
# Add to .git/hooks/pre-commit
python cyber-tools/leak_detector.py $(git diff --cached --name-only)
```

## Testing

### Test File Structure
The included `leaks.txt` contains sample data for testing:
- Fake credentials (never use real data)
- Various data formats and patterns
- Common vulnerability examples

### Validation
```bash
# Run against test file to verify functionality
python leak_detector.py leaks.txt

# Expected: Multiple findings across all categories
# Risk Level: HIGH (due to passwords and API keys)
```

## Security Considerations

### Data Handling
- Never commit real credentials to test files
- Use fake/example data for testing only
- Regularly update detection patterns
- Consider false positive rates

### Production Use
- Run in secure environments only
- Limit access to scan results
- Implement proper logging and audit trails
- Consider legal implications of data scanning

## Customization

### Adding New Patterns
```python
# Add to LeakDetector class
new_pattern = re.compile(r'your_pattern_here')
self.custom_patterns = {'custom_type': new_pattern}
```

### Output Formats
- Console output (default)
- JSON format (for automation)
- CSV export (for reporting)

## Roadmap
- [ ] JSON/CSV output formats
- [ ] Directory scanning capability
- [ ] Custom pattern configuration files
- [ ] Integration with security scanners
- [ ] Real-time monitoring features

## Contributing
1. Fork the repository
2. Add new detection patterns
3. Improve risk assessment logic
4. Add tests for new features
5. Submit pull request

## License
MIT License - Use responsibly for security auditing purposes only.
