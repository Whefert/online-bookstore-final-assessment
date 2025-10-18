"""
Security Testing with Bandit Integration
========================================

This module integrates Bandit security analysis into the test suite
to identify security vulnerabilities in the codebase.

Usage:
    pip install bandit
    python security_tests.py
"""

import subprocess
import json
import os
import sys
from pathlib import Path


class SecurityTestSuite:
    """Security testing suite using Bandit and custom security tests"""
    
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.results = {}
    
    def run_bandit_analysis(self, output_format="json"):
        """Run Bandit security analysis on the codebase"""
        print("Running Bandit Security Analysis...")
        
        try:
            # Run bandit on Python files
            cmd = [
                "bandit", 
                "-r", str(self.project_path),
                "-f", output_format,
                "-o", "bandit_report.json",
                "--exclude", "**/venv/**,**/env/**,**/test_*"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists("bandit_report.json"):
                with open("bandit_report.json", "r") as f:
                    bandit_results = json.load(f)
                
                self.results["bandit_analysis"] = bandit_results
                self.print_bandit_summary(bandit_results)
                return bandit_results
            else:
                print("Bandit report not generated")
                return None
                
        except FileNotFoundError:
            print("❌ Bandit not installed. Install with: pip install bandit")
            return None
        except Exception as e:
            print(f"Error running Bandit: {e}")
            return None
    
    def print_bandit_summary(self, results):
        """Print a summary of Bandit analysis results"""
        print("\n" + "="*60)
        print("BANDIT SECURITY ANALYSIS SUMMARY")
        print("="*60)
        
        if "results" not in results:
            print("No security issues found!")
            return
        
        issues = results["results"]
        
        # Group by severity
        severity_counts = {}
        for issue in issues:
            severity = issue.get("issue_severity", "UNKNOWN")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        print(f"Total issues found: {len(issues)}")
        for severity, count in severity_counts.items():
            print(f"  {severity}: {count}")
        
        print("\nTop Security Issues:")
        print("-" * 40)
        
        for i, issue in enumerate(issues[:10], 1):
            print(f"{i}. {issue.get('test_name', 'Unknown Test')}")
            print(f"   File: {issue.get('filename', 'Unknown')}")
            print(f"   Line: {issue.get('line_number', 'Unknown')}")
            print(f"   Severity: {issue.get('issue_severity', 'Unknown')}")
            print(f"   Confidence: {issue.get('issue_confidence', 'Unknown')}")
            print(f"   Issue: {issue.get('issue_text', 'No description')}")
            print()
    
    def custom_security_tests(self):
        """Run custom security tests specific to the bookstore application"""
        print("\nRunning Custom Security Tests...")
        
        custom_results = {
            "password_security": self.test_password_security(),
            "input_validation": self.test_input_validation(),
            "session_security": self.test_session_security(),
            "file_security": self.test_file_security(),
            "sql_injection": self.test_sql_injection_patterns()
        }
        
        self.results["custom_security_tests"] = custom_results
        return custom_results
    
    def test_password_security(self):
        """Test password security implementation"""
        print("  Testing password security...")
        
        issues = []
        
        # Check if passwords are hashed
        try:
            with open("models.py", "r") as f:
                content = f.read()
                
            if "self.password = password" in content:
                issues.append({
                    "severity": "HIGH",
                    "issue": "Passwords stored in plain text",
                    "file": "models.py",
                    "description": "User passwords are stored without hashing",
                    "recommendation": "Use bcrypt or similar hashing library"
                })
            
            # Check for hardcoded passwords
            if "demo123" in content or "password" in content.lower():
                issues.append({
                    "severity": "MEDIUM",
                    "issue": "Hardcoded credentials found",
                    "file": "models.py",
                    "description": "Demo credentials found in source code",
                    "recommendation": "Move credentials to environment variables"
                })
        
        except FileNotFoundError:
            issues.append({
                "severity": "LOW",
                "issue": "Cannot analyze models.py",
                "description": "File not found for analysis"
            })
        
        return issues
    
    def test_input_validation(self):
        """Test input validation security"""
        print("  Testing input validation...")
        
        issues = []
        
        try:
            with open("app.py", "r") as f:
                content = f.read()
            
            # Check for direct int() conversion without validation
            if "int(request.form.get(" in content:
                issues.append({
                    "severity": "MEDIUM",
                    "issue": "Unsafe type conversion",
                    "file": "app.py",
                    "description": "Direct int() conversion without error handling",
                    "recommendation": "Add try-catch blocks for type conversions"
                })
            
            # Check for SQL injection vulnerabilities (even though using in-memory storage)
            if "%" in content and "format" in content:
                issues.append({
                    "severity": "LOW",
                    "issue": "Potential string formatting vulnerability",
                    "file": "app.py",
                    "description": "String formatting detected - review for injection risks",
                    "recommendation": "Use parameterized queries for any database operations"
                })
            
            # Check for XSS protection
            if "render_template" in content and "|safe" in content:
                issues.append({
                    "severity": "HIGH",
                    "issue": "Potential XSS vulnerability",
                    "file": "app.py",
                    "description": "Use of |safe filter can lead to XSS",
                    "recommendation": "Ensure all user input is properly escaped"
                })
        
        except FileNotFoundError:
            issues.append({
                "severity": "LOW",
                "issue": "Cannot analyze app.py",
                "description": "File not found for analysis"
            })
        
        return issues
    
    def test_session_security(self):
        """Test session security configuration"""
        print("  Testing session security...")
        
        issues = []
        
        try:
            with open("app.py", "r") as f:
                content = f.read()
            
            # Check for weak secret key
            if "your_secret_key" in content:
                issues.append({
                    "severity": "HIGH",
                    "issue": "Weak secret key",
                    "file": "app.py",
                    "description": "Default/weak secret key used for sessions",
                    "recommendation": "Use a strong, randomly generated secret key"
                })
            
            # Check for session configuration
            if "SESSION_COOKIE_SECURE" not in content:
                issues.append({
                    "severity": "MEDIUM",
                    "issue": "Missing secure session configuration",
                    "file": "app.py",
                    "description": "Session cookies not configured as secure",
                    "recommendation": "Set SESSION_COOKIE_SECURE = True for HTTPS"
                })
        
        except FileNotFoundError:
            pass
        
        return issues
    
    def test_file_security(self):
        """Test file security and permissions"""
        print("  Testing file security...")
        
        issues = []
        
        # Check for sensitive files that might be exposed
        sensitive_files = [
            "requirements.txt",
            ".env",
            "config.py",
            "INSTRUCTOR_BUGS_LIST.md"
        ]
        
        for file_path in sensitive_files:
            if os.path.exists(file_path):
                if file_path.endswith(".md") and "INSTRUCTOR" in file_path:
                    issues.append({
                        "severity": "HIGH",
                        "issue": "Sensitive instructor file detected",
                        "file": file_path,
                        "description": "Instructor materials should not be in student workspace",
                        "recommendation": "Remove or restrict access to instructor files"
                    })
        
        return issues
    
    def test_sql_injection_patterns(self):
        """Test for SQL injection vulnerability patterns"""
        print("  Testing for SQL injection patterns...")
        
        issues = []
        
        # Common SQL injection patterns to look for
        sql_patterns = [
            "SELECT * FROM",
            "INSERT INTO",
            "UPDATE SET",
            "DELETE FROM",
            "DROP TABLE",
            "ALTER TABLE"
        ]
        
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r") as f:
                            content = f.read().upper()
                            
                        for pattern in sql_patterns:
                            if pattern in content and "\"" + pattern in content:
                                issues.append({
                                    "severity": "MEDIUM",
                                    "issue": f"Potential SQL query detected: {pattern}",
                                    "file": file_path,
                                    "description": "Raw SQL detected - review for injection vulnerabilities",
                                    "recommendation": "Use parameterized queries or ORM"
                                })
                    except Exception:
                        continue
        
        return issues
    
    def generate_security_report(self):
        """Generate a comprehensive security report"""
        print("\n" + "="*60)
        print("COMPREHENSIVE SECURITY REPORT")
        print("="*60)
        
        if not self.results:
            print("No security analysis has been run yet.")
            return
        
        total_issues = 0
        high_severity = 0
        medium_severity = 0
        low_severity = 0
        
        # Count issues from Bandit
        if "bandit_analysis" in self.results:
            bandit_issues = self.results["bandit_analysis"].get("results", [])
            total_issues += len(bandit_issues)
            
            for issue in bandit_issues:
                severity = issue.get("issue_severity", "").upper()
                if severity == "HIGH":
                    high_severity += 1
                elif severity == "MEDIUM":
                    medium_severity += 1
                else:
                    low_severity += 1
        
        # Count issues from custom tests
        if "custom_security_tests" in self.results:
            for test_category, issues in self.results["custom_security_tests"].items():
                total_issues += len(issues)
                
                for issue in issues:
                    severity = issue.get("severity", "").upper()
                    if severity == "HIGH":
                        high_severity += 1
                    elif severity == "MEDIUM":
                        medium_severity += 1
                    else:
                        low_severity += 1
        
        print(f"Total Security Issues: {total_issues}")
        print(f"  High Severity: {high_severity}")
        print(f"  Medium Severity: {medium_severity}")
        print(f"  Low Severity: {low_severity}")
        
        print("\nSecurity Recommendations:")
        print("1. Implement password hashing (bcrypt)")
        print("2. Add input validation and sanitization")
        print("3. Use environment variables for secrets")
        print("4. Implement CSRF protection")
        print("5. Add rate limiting")
        print("6. Configure secure session cookies")
        print("7. Implement proper error handling")
        print("8. Add security headers")
        
        # Save detailed report
        with open("security_report.json", "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\nDetailed report saved to: security_report.json")
    
    def run_all_security_tests(self):
        """Run all security tests"""
        print("Starting Comprehensive Security Analysis...")
        print("="*60)
        
        # Run Bandit analysis
        self.run_bandit_analysis()
        
        # Run custom security tests
        self.custom_security_tests()
        
        # Generate comprehensive report
        self.generate_security_report()


def main():
    """Main function to run security tests"""
    security_suite = SecurityTestSuite()
    security_suite.run_all_security_tests()


if __name__ == "__main__":
    main()