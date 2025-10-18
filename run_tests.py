#!/usr/bin/env python3
"""
Test Execution Script for Online Bookstore System
================================================

This script provides an easy way to run all test suites and generate reports.
It includes automated tests, performance tests, and generates comprehensive reports.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --quick      # Run quick tests only
    python run_tests.py --performance # Run performance tests only
    python run_tests.py --manual     # Show manual testing checklist
"""

import argparse
import subprocess
import sys
import os
import time
from datetime import datetime

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")
    
    required_packages = ['flask', 'pytest', 'requests']
    optional_packages = ['locust', 'bandit']
    missing_packages = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed (optional)")
        except ImportError:
            missing_optional.append(package)
            print(f"⚠️  {package} is missing (optional for advanced testing)")
    
    if missing_packages:
        print(f"\nMissing required packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    if missing_optional:
        print(f"\nMissing optional packages: {', '.join(missing_optional)}")
        print("Install with: pip install locust bandit")
        print("These are needed for load testing and security analysis")
    
    return True

def run_automated_tests():
    """Run the automated pytest suite"""
    print("\n" + "="*60)
    print("RUNNING AUTOMATED TESTS")
    print("="*60)
    
    if not os.path.exists("test_cases.py"):
        print("❌ test_cases.py not found!")
        return False
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "test_cases.py", 
            "-v", 
            "--tb=short",
            "--color=yes"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✅ All automated tests passed!")
        else:
            print("❌ Some automated tests failed!")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running automated tests: {e}")
        return False

def run_performance_tests():
    """Run performance tests"""
    print("\n" + "="*60)
    print("RUNNING PERFORMANCE TESTS")
    print("="*60)
    
    if not os.path.exists("performance_tests.py"):
        print("❌ performance_tests.py not found!")
        return False
    
    try:
        # Try quick performance test first
        result = subprocess.run([
            sys.executable, "performance_tests.py", "quick"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return True
        
    except Exception as e:
        print(f"❌ Error running performance tests: {e}")
        return False

def run_security_tests():
    """Run Bandit security analysis"""
    print("\n" + "="*60)
    print("RUNNING SECURITY TESTS (BANDIT)")
    print("="*60)
    
    if not os.path.exists("security_tests.py"):
        print("❌ security_tests.py not found!")
        return False
    
    try:
        result = subprocess.run([
            sys.executable, "security_tests.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return True
        
    except Exception as e:
        print(f"❌ Error running security tests: {e}")
        return False

def run_load_tests():
    """Information about running Locust load tests"""
    print("\n" + "="*60)
    print("LOAD TESTING WITH LOCUST")
    print("="*60)
    
    if not os.path.exists("locust_load_tests.py"):
        print("❌ locust_load_tests.py not found!")
        return False
    
    try:
        # Check if locust is available
        import locust
        print("✅ Locust is available")
        print("\nTo run load tests:")
        print("1. Ensure Flask app is running: python app.py")
        print("2. Run Locust: locust -f locust_load_tests.py --host=http://localhost:5000")
        print("3. Open web UI: http://localhost:8089")
        print("\nLoad test scenarios available:")
        print("- BookstoreUser: Regular customer behavior")
        print("- PowerUser: Heavy usage patterns") 
        print("- MobileUser: Mobile device simulation")
        print("- SecurityTestUser: Security testing")
        print("- PerformanceStressTest: Performance stress testing")
        
        return True
        
    except ImportError:
        print("⚠️  Locust not installed")
        print("Install with: pip install locust")
        print("Then run: locust -f locust_load_tests.py --host=http://localhost:5000")
        return False
    """Run performance tests"""
    print("\n" + "="*60)
    print("RUNNING PERFORMANCE TESTS")
    print("="*60)
    
    if not os.path.exists("performance_tests.py"):
        print("❌ performance_tests.py not found!")
        return False
    
    try:
        # Try quick performance test first
        result = subprocess.run([
            sys.executable, "performance_tests.py", "quick"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return True
        
    except Exception as e:
        print(f"❌ Error running performance tests: {e}")
        return False

def show_manual_testing_guide():
    """Show manual testing instructions"""
    print("\n" + "="*60)
    print("MANUAL TESTING GUIDE")
    print("="*60)
    
    print("""
Manual Testing Steps:

1. START THE APPLICATION
   python app.py

2. OPEN BROWSER AND NAVIGATE TO
   http://localhost:5000

3. FOLLOW THE CHECKLIST
   See MANUAL_TESTING_CHECKLIST.md for detailed steps

4. KEY AREAS TO TEST:
   • Shopping cart operations (add, update, remove)
   • User registration and login
   • Checkout process with different payment methods
   • Discount code functionality
   • Error handling and validation
   • Performance with large quantities
   • Security testing (try malicious inputs)

5. KNOWN ISSUES TO LOOK FOR:
   • App crashes with non-numeric quantity input
   • Case-sensitive discount codes
   • Cart items with 0 quantity not removed
   • No email format validation
   • Passwords stored in plain text
   • Performance issues with large cart quantities

6. DOCUMENT BUGS USING:
   See BUG_REPORT_TEMPLATE.md for format

7. TEST BROWSERS:
   • Chrome, Firefox, Safari, Edge
   • Mobile and tablet views
   • Different screen resolutions
""")

def check_app_server():
    """Check if the Flask app is running"""
    try:
        import requests
        response = requests.get("http://localhost:5000", timeout=5)
        return response.status_code == 200
    except:
        return False

def generate_test_report():
    """Generate a comprehensive test report"""
    print("\n" + "="*60)
    print("GENERATING TEST REPORT")
    print("="*60)
    
    report_content = f"""
# Test Execution Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Test Environment
- Python Version: {sys.version}
- Operating System: {os.name}
- Working Directory: {os.getcwd()}

## Test Categories Executed

### 1. Automated Tests (pytest)
- **Location**: test_cases.py
- **Categories**: 
  - Functional Testing (Cart, User, Checkout)
  - Edge Case Testing
  - Performance Testing
  - Security Testing
  - Integration Testing
  - Model Unit Testing

### 2. Performance Tests
- **Location**: performance_tests.py
- **Focus Areas**:
  - Cart calculation performance
  - User operations performance
  - Page load times
  - Memory usage analysis

### 3. Manual Testing
- **Guide**: MANUAL_TESTING_CHECKLIST.md
- **Bug Reports**: BUG_REPORT_TEMPLATE.md
- **Areas Covered**:
  - User interface testing
  - Cross-browser compatibility
  - Accessibility testing
  - Usability evaluation

## Known Issues to Verify

Based on code analysis, the following issues should be discoverable:

### High Priority Issues
1. **Input Validation Crash** - App crashes on non-numeric quantity input
2. **Case-Sensitive Discount Codes** - Only exact case works for discount codes
3. **Email Validation Missing** - Accepts invalid email formats
4. **Security Vulnerability** - Passwords stored in plain text

### Medium Priority Issues
1. **Cart Quantity Bug** - Items with 0 quantity not removed
2. **Performance Issues** - Inefficient cart calculation algorithm
3. **Duplicate User Registration** - Case-insensitive email checking allows duplicates

### Low Priority Issues
1. **Code Quality** - Unused variables and inefficient algorithms
2. **Missing Validations** - PayPal payment method not properly validated

## Testing Recommendations

1. **Start with Automated Tests**
   ```bash
   python run_tests.py
   ```

2. **Run Performance Analysis**
   ```bash
   python performance_tests.py quick
   ```

3. **Conduct Manual Testing**
   - Follow MANUAL_TESTING_CHECKLIST.md
   - Test on multiple browsers
   - Document bugs using BUG_REPORT_TEMPLATE.md

4. **Focus Areas for Bug Discovery**
   - Input validation edge cases
   - Error handling scenarios
   - Performance with large datasets
   - Security testing with malicious inputs

## Expected Outcomes

Students should be able to:
- ✅ Identify 80%+ of intentional bugs through systematic testing
- ✅ Create comprehensive bug reports with reproduction steps
- ✅ Propose appropriate fixes for identified issues
- ✅ Evaluate system performance and suggest optimizations
- ✅ Assess security vulnerabilities and recommend improvements

## Next Steps

1. Execute all test categories
2. Document findings thoroughly
3. Prioritize issues by severity
4. Propose fixes and improvements
5. Validate fixes through re-testing

---
*This report provides a foundation for comprehensive system testing education.*
"""
    
    # Save report
    with open("TEST_EXECUTION_REPORT.md", "w") as f:
        f.write(report_content)
    
    print("✅ Test report generated: TEST_EXECUTION_REPORT.md")

def main():
    """Main test execution function"""
    parser = argparse.ArgumentParser(description="Run Online Bookstore Test Suite")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests only")
    parser.add_argument("--manual", action="store_true", help="Show manual testing guide")
    parser.add_argument("--report", action="store_true", help="Generate test report only")
    
    args = parser.parse_args()
    
    print("🧪 ONLINE BOOKSTORE TEST SUITE")
    print("="*60)
    print(f"Test execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    success = True
    
    if args.manual:
        show_manual_testing_guide()
        return
    
    if args.report:
        generate_test_report()
        return
    
    if args.performance:
        success &= run_performance_tests()
    elif args.quick:
        success &= run_performance_tests()  # Quick performance test
    else:
        # Run all tests
        print("\n🎯 Running comprehensive test suite...")
        
        # Check if app server is running for integration tests
        if check_app_server():
            print("✅ Flask app is running - full integration testing available")
        else:
            print("⚠️  Flask app not detected - run 'python app.py' for full testing")
        
        # Run automated tests
        success &= run_automated_tests()
        
        # Run performance tests
        success &= run_performance_tests()
        
        # Run security tests
        success &= run_security_tests()
        
        # Show load testing information
        run_load_tests()
        
        # Show manual testing guide
        show_manual_testing_guide()
    
    # Generate final report
    generate_test_report()
    
    print("\n" + "="*60)
    print("TEST EXECUTION SUMMARY")
    print("="*60)
    
    if success:
        print("✅ All automated tests completed successfully!")
    else:
        print("❌ Some tests failed or had issues!")
    
    print(f"\nTest execution completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n📋 NEXT STEPS:")
    print("1. Review test results and any failures")
    print("2. Start Flask app: python app.py")
    print("3. Perform manual testing using MANUAL_TESTING_CHECKLIST.md")
    print("4. Document bugs using BUG_REPORT_TEMPLATE.md")
    print("5. Analyze performance results")
    print("6. Review security findings") 
    print("7. Run load tests: locust -f locust_load_tests.py --host=http://localhost:5000")
    print("8. Check advanced profiling data (timeit, cProfile results)")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())