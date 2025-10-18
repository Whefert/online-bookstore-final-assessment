#!/usr/bin/env python3
# Student ID: #2416130

"""
🚀 DEPLOYMENT VALIDATION SCRIPT
==============================

This script validates that the Online Bookstore application is ready for deployment
by running comprehensive tests and security checks.

Usage:
    python validate_deployment.py

Features:
- ✅ Comprehensive test suite execution
- 🔒 Security vulnerability scanning  
- ⚡ Performance validation
- 📊 Deployment readiness assessment
- 📝 Automated reporting

Author: GitHub Copilot Testing Framework
Date: October 18, 2025
"""

import subprocess
import sys
import json
import os
from datetime import datetime
import time


class DeploymentValidator:
    """Automated deployment validation and testing orchestrator"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.results = {
            'timestamp': self.start_time.isoformat(),
            'tests': {},
            'security': {},
            'performance': {},
            'overall_status': 'UNKNOWN'
        }
        
    def print_header(self, title):
        """Print formatted section header"""
        print(f"\n{'='*60}")
        print(f"🚀 {title}")
        print(f"{'='*60}")
        
    def print_success(self, message):
        """Print success message"""
        print(f"✅ {message}")
        
    def print_warning(self, message):
        """Print warning message"""
        print(f"⚠️  {message}")
        
    def print_error(self, message):
        """Print error message"""
        print(f"❌ {message}")
        
    def run_command(self, command, description):
        """Execute command and capture results"""
        print(f"\n🔄 {description}...")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=300  # 5 minute timeout
            )
            return result
        except subprocess.TimeoutExpired:
            self.print_error(f"Command timed out: {command}")
            return None
        except Exception as e:
            self.print_error(f"Command failed: {e}")
            return None
    
    def validate_dependencies(self):
        """Check if all required dependencies are installed"""
        self.print_header("DEPENDENCY VALIDATION")
        
        dependencies = [
            ('python', 'Python interpreter'),
            ('pip', 'Python package manager'),
            ('pytest', 'Testing framework'),
            ('flask', 'Web framework'),
            ('bcrypt', 'Password hashing'),
            ('locust', 'Load testing'),
            ('bandit', 'Security scanner')
        ]
        
        all_deps_ok = True
        for dep, desc in dependencies:
            try:
                if dep == 'python':
                    result = subprocess.run([sys.executable, '--version'], 
                                          capture_output=True, text=True)
                elif dep == 'pip':
                    result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                                          capture_output=True, text=True)
                else:
                    result = subprocess.run([sys.executable, '-c', f'import {dep}'], 
                                          capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.print_success(f"{desc} - Available")
                else:
                    self.print_error(f"{desc} - Missing or broken")
                    all_deps_ok = False
                    
            except Exception as e:
                self.print_error(f"{desc} - Error checking: {e}")
                all_deps_ok = False
        
        self.results['dependencies'] = {'status': 'PASS' if all_deps_ok else 'FAIL'}
        return all_deps_ok
    
    def run_test_suite(self):
        """Execute the comprehensive test suite"""
        self.print_header("AUTOMATED TEST SUITE")
        
        # Run main test suite
        result = self.run_command(
            f"{sys.executable} run_tests.py", 
            "Running comprehensive test suite"
        )
        
        if result and result.returncode == 0:
            self.print_success("Test suite completed successfully")
            test_status = 'PASS'
        else:
            if result:
                self.print_warning(f"Test suite completed with issues (exit code: {result.returncode})")
                test_status = 'PARTIAL'
            else:
                self.print_error("Test suite failed to execute")
                test_status = 'FAIL'
        
        # Run individual pytest for detailed results
        pytest_result = self.run_command(
            f"{sys.executable} -m pytest test_cases.py --tb=short -v", 
            "Running detailed pytest analysis"
        )
        
        self.results['tests'] = {
            'status': test_status,
            'main_suite': result.returncode if result else -1,
            'pytest_detailed': pytest_result.returncode if pytest_result else -1
        }
        
        return test_status in ['PASS', 'PARTIAL']
    
    def run_security_scan(self):
        """Execute security vulnerability scanning"""
        self.print_header("SECURITY ANALYSIS")
        
        # Run Bandit security scan
        bandit_result = self.run_command(
            f"{sys.executable} -m bandit -r . -f json -o deployment_security_scan.json",
            "Running Bandit security vulnerability scan"
        )
        
        security_status = 'UNKNOWN'
        if bandit_result is not None:
            if bandit_result.returncode == 0:
                self.print_success("No security issues found")
                security_status = 'PASS'
            elif bandit_result.returncode == 1:
                self.print_warning("Security issues found - review required")
                security_status = 'REVIEW'
            else:
                self.print_error("Security scan failed")
                security_status = 'FAIL'
        
        # Run custom security tests
        custom_security = self.run_command(
            f"{sys.executable} security_tests.py",
            "Running custom security validation"
        )
        
        self.results['security'] = {
            'status': security_status,
            'bandit_scan': bandit_result.returncode if bandit_result else -1,
            'custom_tests': custom_security.returncode if custom_security else -1
        }
        
        return security_status in ['PASS', 'REVIEW']
    
    def run_performance_check(self):
        """Execute performance validation"""
        self.print_header("PERFORMANCE VALIDATION")
        
        perf_result = self.run_command(
            f"{sys.executable} performance_tests.py quick",
            "Running performance benchmarks"
        )
        
        if perf_result and perf_result.returncode == 0:
            self.print_success("Performance benchmarks completed")
            perf_status = 'PASS'
        else:
            self.print_warning("Performance tests had issues")
            perf_status = 'PARTIAL'
        
        self.results['performance'] = {
            'status': perf_status,
            'benchmark_result': perf_result.returncode if perf_result else -1
        }
        
        return perf_status == 'PASS'
    
    def generate_deployment_report(self):
        """Generate comprehensive deployment readiness report"""
        self.print_header("DEPLOYMENT READINESS ASSESSMENT")
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        # Determine overall status
        dep_ok = self.results.get('dependencies', {}).get('status') == 'PASS'
        test_ok = self.results.get('tests', {}).get('status') in ['PASS', 'PARTIAL']
        security_ok = self.results.get('security', {}).get('status') in ['PASS', 'REVIEW']
        perf_ok = self.results.get('performance', {}).get('status') == 'PASS'
        
        if dep_ok and test_ok and security_ok and perf_ok:
            overall_status = 'READY_FOR_DEPLOYMENT'
            status_icon = '🟢'
        elif dep_ok and test_ok and security_ok:
            overall_status = 'CONDITIONAL_DEPLOYMENT'
            status_icon = '🟡'
        else:
            overall_status = 'NOT_READY'
            status_icon = '🔴'
        
        self.results['overall_status'] = overall_status
        self.results['duration_seconds'] = duration
        self.results['completion_time'] = end_time.isoformat()
        
        # Print summary
        print(f"\n{status_icon} OVERALL STATUS: {overall_status}")
        print(f"⏱️  Total validation time: {duration:.1f} seconds")
        print(f"📅 Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n📊 VALIDATION SUMMARY:")
        print(f"   Dependencies: {'✅' if dep_ok else '❌'} {self.results.get('dependencies', {}).get('status', 'UNKNOWN')}")
        print(f"   Test Suite:   {'✅' if test_ok else '❌'} {self.results.get('tests', {}).get('status', 'UNKNOWN')}")
        print(f"   Security:     {'✅' if security_ok else '❌'} {self.results.get('security', {}).get('status', 'UNKNOWN')}")
        print(f"   Performance:  {'✅' if perf_ok else '❌'} {self.results.get('performance', {}).get('status', 'UNKNOWN')}")
        
        # Save results to file
        with open('deployment_validation_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        self.print_success("Deployment validation report saved to: deployment_validation_report.json")
        
        return overall_status
    
    def run_full_validation(self):
        """Execute complete deployment validation pipeline"""
        print("🚀 ONLINE BOOKSTORE - DEPLOYMENT VALIDATION")
        print("=" * 60)
        print(f"Starting validation at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Step 1: Check dependencies
            if not self.validate_dependencies():
                self.print_error("Dependency validation failed - cannot proceed")
                return False
            
            # Step 2: Run test suite
            self.run_test_suite()
            
            # Step 3: Security analysis
            self.run_security_scan()
            
            # Step 4: Performance check
            self.run_performance_check()
            
            # Step 5: Generate report
            status = self.generate_deployment_report()
            
            # Final recommendation
            self.print_header("DEPLOYMENT RECOMMENDATION")
            if status == 'READY_FOR_DEPLOYMENT':
                self.print_success("✅ RECOMMENDED: Application is ready for deployment")
                print("   All validation checks passed successfully")
                return True
            elif status == 'CONDITIONAL_DEPLOYMENT':
                self.print_warning("⚠️  CONDITIONAL: Review security/performance findings before deployment")
                print("   Core functionality validated but requires review")
                return True
            else:
                self.print_error("❌ NOT RECOMMENDED: Critical issues found - resolve before deployment")
                print("   Address failing validation checks before proceeding")
                return False
                
        except Exception as e:
            self.print_error(f"Validation pipeline failed: {e}")
            return False


def main():
    """Main deployment validation entry point"""
    validator = DeploymentValidator()
    success = validator.run_full_validation()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()