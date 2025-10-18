# Manual Testing Checklist

## Pre-Testing Setup

- [ ] Application is running on localhost
- [ ] All dependencies are installed
- [ ] Demo user account is available
- [ ] Test data is properly loaded

## 1. Shopping Cart Testing

### Add to Cart Functionality

- [ ] Add single book with default quantity (1)
- [ ] Add single book with custom quantity (3)
- [ ] Add same book multiple times (quantities should accumulate)
- [ ] Add different books to cart
- [ ] Verify cart icon/counter updates correctly
- [ ] Test with maximum quantity values
- [ ] Test with zero quantity (should not add)
- [ ] Test with negative quantity (should handle gracefully)
- [ ] Test with non-numeric quantity (abc, special characters)

### Cart Management

- [ ] View cart page with items
- [ ] Update quantity of existing items
- [ ] Set quantity to zero (should remove item)
- [ ] Remove individual items from cart
- [ ] Clear entire cart
- [ ] Verify cart total calculation is accurate
- [ ] Test cart persistence during session

### Edge Cases

- [ ] Add non-existent book (should show error)
- [ ] Access cart page when empty
- [ ] Navigate between pages with items in cart

## 2. User Registration and Authentication

### Registration

- [ ] Register new user with all required fields
- [ ] Register with missing name field
- [ ] Register with missing email field
- [ ] Register with missing password field
- [ ] Register with existing email address
- [ ] Register with invalid email formats:
  - [ ] notanemail
  - [ ] @domain.com
  - [ ] user@
  - [ ] user space@domain.com
  - [ ] user@domain
- [ ] Register with same email in different cases (test@example.com vs TEST@EXAMPLE.COM)
- [ ] Verify user is automatically logged in after registration

### Login/Logout

- [ ] Login with valid demo credentials (demo@bookstore.com / demo123)
- [ ] Login with valid registered user credentials
- [ ] Login with incorrect password
- [ ] Login with non-existent email
- [ ] Login with empty fields
- [ ] Verify redirect to intended page after login
- [ ] Logout and verify session is cleared
- [ ] Access protected pages after logout (should redirect to login)

### Profile Management

- [ ] Access account page when logged in
- [ ] Update profile name
- [ ] Update profile address
- [ ] Update password
- [ ] Verify changes are saved
- [ ] Verify old password still works if not changed

## 3. Checkout Process

### Checkout Access

- [ ] Access checkout with items in cart
- [ ] Try to access checkout with empty cart (should redirect)
- [ ] Verify cart contents display correctly on checkout page

### Shipping Information

- [ ] Fill all required shipping fields
- [ ] Submit with missing name field
- [ ] Submit with missing email field
- [ ] Submit with missing address field
- [ ] Submit with missing city field
- [ ] Submit with missing zip code field
- [ ] Test with very long input values
- [ ] Test with special characters in fields

### Payment Information

- [ ] Select credit card payment method
- [ ] Fill all credit card fields
- [ ] Submit with missing card number
- [ ] Submit with missing expiry date
- [ ] Submit with missing CVV
- [ ] Select PayPal payment method
- [ ] Submit PayPal payment (should work without card details)

### Discount Codes

- [ ] Apply valid discount code "SAVE10" (exact case)
- [ ] Apply valid discount code "WELCOME20" (exact case)
- [ ] Apply invalid discount code
- [ ] Apply discount codes in different cases:
  - [ ] save10 (lowercase)
  - [ ] Save10 (mixed case)
  - [ ] SAVE10 (uppercase - should work)
- [ ] Apply multiple discount codes
- [ ] Verify discount calculation is correct

### Payment Processing

- [ ] Complete checkout with successful payment (card not ending in 1111)
- [ ] Complete checkout with failed payment (card ending in 1111)
- [ ] Verify order is created on successful payment
- [ ] Verify cart is cleared after successful payment
- [ ] Verify no order is created on payment failure

## 4. Order Confirmation

### Order Creation

- [ ] Verify order confirmation page displays after successful payment
- [ ] Verify order details are accurate (items, quantities, total)
- [ ] Verify shipping information is correct
- [ ] Verify order ID is generated
- [ ] Check that order appears in user's order history (if logged in)

### Email Confirmation

- [ ] Verify email confirmation is "sent" (check console output)
- [ ] Verify email contains correct order details

## 5. Navigation and UI

### General Navigation

- [ ] Navigate to home page
- [ ] Navigate to cart page
- [ ] Navigate to login page
- [ ] Navigate to registration page
- [ ] Navigate to account page (when logged in)
- [ ] Test all navigation links work correctly

### Responsive Design

- [ ] Test on desktop browser (1920x1080)
- [ ] Test on tablet size (768px width)
- [ ] Test on mobile size (320px width)
- [ ] Verify all elements are visible and accessible
- [ ] Test touch interactions on mobile

### Error Messages

- [ ] Verify flash messages appear for successful actions
- [ ] Verify error messages appear for failed actions
- [ ] Verify messages are clear and helpful
- [ ] Verify messages disappear appropriately

## 6. Performance Testing

### Response Time

- [ ] Measure page load times for all major pages
- [ ] Test with large quantities in cart (100+ items)
- [ ] Test cart total calculation speed with many items
- [ ] Test user with many orders in history

### Browser Performance

- [ ] Monitor browser memory usage during extended session
- [ ] Test for memory leaks during repeated operations
- [ ] Check browser console for JavaScript errors

## 7. Security Testing

### Input Validation

- [ ] Try SQL injection in form fields: `'; DROP TABLE users; --`
- [ ] Try XSS in form fields: `<script>alert('xss')</script>`
- [ ] Try path traversal: `../../../etc/passwd`
- [ ] Test with very long input strings (1000+ characters)

### Authentication Security

- [ ] Verify passwords are not visible in browser
- [ ] Check if passwords are stored securely (check source/debug)
- [ ] Test session timeout behavior
- [ ] Try to access other users' data

### Session Management

- [ ] Test session persistence across browser tabs
- [ ] Test session handling with multiple browser windows
- [ ] Verify logout clears all session data

## 8. Cross-Browser Testing

### Browser Compatibility

- [ ] Test on Chrome (latest version)
- [ ] Test on Firefox (latest version)
- [ ] Test on Safari (if available)
- [ ] Test on Edge (latest version)
- [ ] Compare functionality across browsers
- [ ] Note any browser-specific issues

## 9. Accessibility Testing

### Basic Accessibility

- [ ] Test navigation using only keyboard
- [ ] Verify all interactive elements are focusable
- [ ] Check form labels are properly associated
- [ ] Verify error messages are announced
- [ ] Test with screen reader (if available)

## 10. Data Integrity Testing

### Data Persistence

- [ ] Add items to cart, close browser, reopen (items should persist during session)
- [ ] Create user account, logout, login (data should persist)
- [ ] Create order, verify it appears in order history

### Data Validation

- [ ] Verify prices are calculated correctly
- [ ] Verify quantities are handled as integers
- [ ] Verify order totals match cart totals
- [ ] Verify discount calculations are accurate

## Bug Reporting

For each issue found, document:

1. **Bug ID**: Unique identifier (BUG-001, BUG-002, etc.)
2. **Severity**: Critical/High/Medium/Low
3. **Component**: Cart/User/Checkout/Payment/UI
4. **Summary**: Brief description
5. **Steps to Reproduce**: Detailed steps
6. **Expected Result**: What should happen
7. **Actual Result**: What actually happens
8. **Browser/Environment**: Testing environment details
9. **Screenshot**: If applicable

## Expected Issues to Find

Based on the application analysis, look for these specific issues:

### High Priority Issues

- [ ] Application crashes when entering non-numeric quantity
- [ ] Cart items with 0 quantity are not removed
- [ ] Discount codes don't work with different capitalization
- [ ] No email format validation allows invalid emails
- [ ] Duplicate user registration with different email cases

### Medium Priority Issues

- [ ] Missing validation for PayPal payment method
- [ ] No input sanitization for form fields
- [ ] Performance issues with large cart quantities
- [ ] Passwords stored in plain text (security issue)

### Low Priority Issues

- [ ] Inefficient cart total calculation
- [ ] Unused variables and data structures
- [ ] Missing helper function usage in some routes

## Testing Completion Checklist

- [ ] All manual test cases executed
- [ ] All bugs documented with proper details
- [ ] Screenshots captured for UI issues
- [ ] Performance metrics recorded
- [ ] Cross-browser results documented
- [ ] Final test report prepared
