# Test Plan for Online Bookstore System

## Overview

This document outlines the comprehensive testing strategy for the Online Bookstore web application. The testing approach covers functional, performance, security, and usability aspects to ensure the system meets all requirements and provides a reliable user experience.

## Test Objectives

1. **Verify Core Functionality**: Ensure all features work as expected
2. **Identify Bugs and Issues**: Find and document system defects
3. **Validate Performance**: Assess system efficiency and scalability
4. **Ensure Security**: Test for vulnerabilities and data protection
5. **Confirm Usability**: Validate user experience and accessibility

## System Under Test

- **Application**: Online Bookstore Web Application
- **Technology Stack**: Flask (Python), HTML/CSS, SQLite-equivalent in-memory storage
- **Key Features**: Shopping cart, user management, checkout process, payment processing

## Test Categories

### 1. Functional Testing

#### 1.1 Shopping Cart Operations

- **TC-CART-001 to TC-CART-009**: Test all cart operations
- Add books to cart with various quantities
- Update cart item quantities
- Remove items from cart
- Clear entire cart
- Calculate cart totals correctly

#### 1.2 User Management

- **TC-USER-001 to TC-USER-007**: Test user account operations
- User registration with validation
- Login/logout functionality
- Profile management and updates
- Password security

#### 1.3 Checkout and Payment Process

- **TC-CHECKOUT-001 to TC-CHECKOUT-007**: Test complete checkout flow
- Order processing with valid data
- Payment method handling
- Discount code application
- Order confirmation generation

### 2. Edge Case Testing

#### 2.1 Input Validation

- **TC-EDGE-001 to TC-EDGE-006**: Test boundary conditions
- Invalid data types (non-numeric quantities)
- Negative and zero values
- Empty and null inputs
- Email format validation
- Case sensitivity testing

### 3. Performance Testing

#### 3.1 Response Time Testing

- **TC-PERF-001 to TC-PERF-003**: Test system performance
- Cart calculation efficiency with large quantities
- User order history retrieval speed
- Book search performance comparison

### 4. Security Testing

#### 4.1 Data Protection

- **TC-SEC-001 to TC-SEC-003**: Test security measures
- Password storage security
- SQL injection protection
- Session management security
- Input sanitization

### 5. Integration Testing

#### 5.1 End-to-End Workflows

- **TC-INT-001 to TC-INT-004**: Test complete user journeys
- Full purchase workflow
- User registration to purchase
- Payment gateway integration
- Email service integration

### 6. Model Unit Testing

#### 6.1 Component Testing

- **TC-MODEL-001 to TC-MODEL-005**: Test individual models
- Book model functionality
- Cart and CartItem models
- User model methods
- Order model operations
- Payment and email services

### 7. Usability Testing

#### 7.1 User Experience

- **TC-UI-001 to TC-UI-003**: Test user interface
- Navigation accessibility
- Error message clarity
- Form validation feedback

## Test Environment Setup

### Prerequisites

1. Python 3.8+
2. Flask 3.0.3
3. pytest 7.0.1
4. Web browser for manual testing

### Installation Steps

```bash
# Clone/download the project
cd online-bookstore-final-assessment

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Run automated tests
pytest test_cases.py -v
```

## Test Data

### Demo User Credentials

- **Email**: demo@bookstore.com
- **Password**: demo123
- **Name**: Demo User
- **Address**: 123 Demo Street, Demo City, DC 12345

### Test Books Available

1. The Great Gatsby - Fiction - $10.99
2. 1984 - Dystopia - $8.99
3. I Ching - Traditional - $18.99
4. Moby Dick - Adventure - $12.49

### Payment Test Scenarios

- **Successful Payment**: Any card number except ending in 1111
- **Failed Payment**: Card number ending in 1111 (e.g., 4444444444441111)

### Discount Codes

- **SAVE10**: 10% discount (case-sensitive)
- **WELCOME20**: 20% discount (case-sensitive)

## Known Issues to Test For

Based on the instructor's bug list, the following issues should be discoverable through testing:

### 1. Input Validation Issues

- Missing error handling for non-numeric quantity inputs
- No validation for negative quantities in cart operations
- Missing email format validation in registration
- Case-sensitive discount code matching

### 2. Logic Errors

- Cart update quantity not removing items when set to 0
- Inefficient cart total calculation using nested loops
- Missing validation for PayPal payment method

### 3. Security Vulnerabilities

- Plain text password storage
- Case-sensitive email checking allowing duplicates
- Missing input sanitization

### 4. Performance Issues

- Inefficient algorithms in cart calculations
- Unnecessary data structures and operations
- Linear searches instead of optimized lookups

## Test Execution Strategy

### Phase 1: Automated Testing (Week 1)

- Run comprehensive pytest suite
- Document all failing tests
- Categorize issues by severity and type

### Phase 2: Manual Testing (Week 2)

- Perform exploratory testing
- Test user interface and usability
- Cross-browser compatibility testing
- Mobile responsiveness testing

### Phase 3: Performance Testing (Week 3)

- Load testing with multiple users
- Stress testing with large data sets
- Memory usage analysis
- Response time benchmarking

### Phase 4: Security Testing (Week 4)

- Penetration testing for common vulnerabilities
- Input validation testing with malicious data
- Session management testing
- Authentication and authorization testing

## Test Reporting

### Bug Report Template

For each issue found, document:

1. **Bug ID**: Unique identifier
2. **Title**: Brief description
3. **Severity**: Critical/High/Medium/Low
4. **Steps to Reproduce**: Detailed reproduction steps
5. **Expected Result**: What should happen
6. **Actual Result**: What actually happens
7. **Environment**: Browser, OS, Python version
8. **Screenshot/Evidence**: If applicable

### Test Summary Report

Include:

- Total tests executed
- Pass/fail counts
- Bug summary by category
- Performance metrics
- Security findings
- Recommendations for fixes

## Success Criteria

Testing is considered successful when:

- ✅ 95%+ of functional tests pass
- ✅ All critical and high-severity bugs are identified
- ✅ Performance benchmarks meet acceptable thresholds
- ✅ Security vulnerabilities are documented with severity levels
- ✅ Usability issues are identified and prioritized
- ✅ Test coverage includes all major user workflows

## Tools and Resources

### Automated Testing

- **pytest**: Primary testing framework
- **Flask test client**: For HTTP request testing
- **time module**: For performance measurements

### Manual Testing

- **Multiple browsers**: Chrome, Firefox, Safari, Edge
- **Mobile devices**: iOS and Android testing
- **Developer tools**: Browser debugging tools

### Performance Testing

- **Python profiling**: cProfile for performance analysis
- **Memory monitoring**: tracemalloc for memory usage
- **Load testing**: Manual simulation of concurrent users

### Security Testing

- **Input validation**: Manual injection attempts
- **Session testing**: Cookie and session manipulation
- **Authentication testing**: Brute force and bypass attempts

## Conclusion

This comprehensive test plan ensures thorough evaluation of the Online Bookstore system across all critical areas. By following this structured approach, testers can systematically identify issues, validate functionality, and provide valuable feedback for system improvement.

The combination of automated and manual testing, along with specific focus on known issue areas, provides an excellent learning experience for understanding real-world software testing challenges and best practices.
