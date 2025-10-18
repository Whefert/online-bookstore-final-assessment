
# Test Execution Report
Generated: 2025-10-18 22:10:04

## Test Environment
- Python Version: 3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)]
- Operating System: nt
- Working Directory: C:\Users\jeffd\OneDrive - St Marys University\System Testing\Final Assessment\online-bookstore-final-assessment

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
