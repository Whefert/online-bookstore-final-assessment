# Bug Report Template

## Bug Report #[ID]

**Date**: [Date Found]  
**Reporter**: [Your Name]  
**Environment**: [Browser/OS/Python Version]

---

### Summary

Brief description of the bug

### Severity

- [ ] Critical - System crash, data loss, security vulnerability
- [ ] High - Major functionality broken, workaround difficult
- [ ] Medium - Minor functionality issue, workaround available
- [ ] Low - Cosmetic issue, enhancement request

### Component

- [ ] Shopping Cart
- [ ] User Registration/Login
- [ ] Checkout Process
- [ ] Payment Processing
- [ ] User Interface
- [ ] Performance
- [ ] Security

### Steps to Reproduce

1.
2.
3.
4.

### Expected Result

What should happen

### Actual Result

What actually happens

### Screenshots/Evidence

[Attach screenshots, console logs, or other evidence]

### Additional Information

- Browser:
- Operating System:
- Screen Resolution:
- Additional Notes:

---

## Example Bug Reports

### Bug Report #001

**Date**: October 18, 2025  
**Reporter**: Test Engineer  
**Environment**: Chrome 118 / Windows 11 / Python 3.9

---

### Summary

Application crashes when entering non-numeric quantity in add to cart form

### Severity

- [x] Critical - System crash, data loss, security vulnerability
- [ ] High - Major functionality broken, workaround difficult
- [ ] Medium - Minor functionality issue, workaround available
- [ ] Low - Cosmetic issue, enhancement request

### Component

- [x] Shopping Cart
- [ ] User Registration/Login
- [ ] Checkout Process
- [ ] Payment Processing
- [ ] User Interface
- [ ] Performance
- [ ] Security

### Steps to Reproduce

1. Navigate to home page (/)
2. Find any book
3. Enter "abc" in the quantity field
4. Click "Add to Cart"

### Expected Result

Should show error message "Please enter a valid quantity" and not add item to cart

### Actual Result

Application crashes with ValueError: invalid literal for int() with base 10: 'abc'

### Screenshots/Evidence

```
File "app.py", line 46, in add_to_cart
    quantity = int(request.form.get('quantity', 1))
ValueError: invalid literal for int() with base 10: 'abc'
```

### Additional Information

- Browser: Chrome 118
- Operating System: Windows 11
- Screen Resolution: 1920x1080
- Additional Notes: Same issue occurs in update cart functionality

---

### Bug Report #002

**Date**: October 18, 2025  
**Reporter**: Test Engineer  
**Environment**: Firefox 119 / Windows 11 / Python 3.9

---

### Summary

Discount codes are case-sensitive when they should not be

### Severity

- [ ] Critical - System crash, data loss, security vulnerability
- [x] High - Major functionality broken, workaround difficult
- [ ] Medium - Minor functionality issue, workaround available
- [ ] Low - Cosmetic issue, enhancement request

### Component

- [ ] Shopping Cart
- [ ] User Registration/Login
- [x] Checkout Process
- [ ] Payment Processing
- [ ] User Interface
- [ ] Performance
- [ ] Security

### Steps to Reproduce

1. Add any item to cart
2. Navigate to checkout (/checkout)
3. Fill in all required shipping and payment information
4. Enter discount code "save10" (lowercase)
5. Submit the form

### Expected Result

10% discount should be applied successfully

### Actual Result

No discount is applied, shows "Invalid discount code" message

### Screenshots/Evidence

- "SAVE10" works correctly
- "save10" fails
- "Save10" fails
- Only exact case "SAVE10" works

### Additional Information

- Browser: Firefox 119
- Operating System: Windows 11
- Screen Resolution: 1920x1080
- Additional Notes: Same issue affects "WELCOME20" discount code

---

### Bug Report #003

**Date**: October 18, 2025  
**Reporter**: Test Engineer  
**Environment**: Chrome 118 / Windows 11 / Python 3.9

---

### Summary

Cart items with quantity 0 are not removed from cart

### Severity

- [ ] Critical - System crash, data loss, security vulnerability
- [ ] High - Major functionality broken, workaround difficult
- [x] Medium - Minor functionality issue, workaround available
- [ ] Low - Cosmetic issue, enhancement request

### Component

- [x] Shopping Cart
- [ ] User Registration/Login
- [ ] Checkout Process
- [ ] Payment Processing
- [ ] User Interface
- [ ] Performance
- [ ] Security

### Steps to Reproduce

1. Add any book to cart with quantity 2
2. Navigate to cart page (/cart)
3. Update quantity to 0
4. Click "Update Cart"

### Expected Result

Item should be removed from cart completely

### Actual Result

Item remains in cart with quantity 0, still shows in cart list

### Screenshots/Evidence

Cart shows: "The Great Gatsby - Quantity: 0 - $0.00"

### Additional Information

- Browser: Chrome 118
- Operating System: Windows 11
- Screen Resolution: 1920x1080
- Additional Notes: Workaround is to use "Remove" button instead

---

### Bug Report #004

**Date**: October 18, 2025  
**Reporter**: Test Engineer  
**Environment**: Chrome 118 / Windows 11 / Python 3.9

---

### Summary

No email format validation allows registration with invalid email addresses

### Severity

- [ ] Critical - System crash, data loss, security vulnerability
- [x] High - Major functionality broken, workaround difficult
- [ ] Medium - Minor functionality issue, workaround available
- [ ] Low - Cosmetic issue, enhancement request

### Component

- [ ] Shopping Cart
- [x] User Registration/Login
- [ ] Checkout Process
- [ ] Payment Processing
- [ ] User Interface
- [ ] Performance
- [x] Security

### Steps to Reproduce

1. Navigate to registration page (/register)
2. Enter invalid email format: "notanemail"
3. Enter valid password and name
4. Submit registration form

### Expected Result

Should show error message "Please enter a valid email address"

### Actual Result

Registration succeeds with invalid email format

### Screenshots/Evidence

Successfully registered users with emails like:

- "notanemail"
- "@domain.com"
- "user@"
- "user space@domain.com"

### Additional Information

- Browser: Chrome 118
- Operating System: Windows 11
- Screen Resolution: 1920x1080
- Additional Notes: This could cause issues with order confirmations and password resets

---

### Bug Report #005

**Date**: October 18, 2025  
**Reporter**: Test Engineer  
**Environment**: All Browsers / Windows 11 / Python 3.9

---

### Summary

Passwords stored in plain text (Security Vulnerability)

### Severity

- [x] Critical - System crash, data loss, security vulnerability
- [ ] High - Major functionality broken, workaround difficult
- [ ] Medium - Minor functionality issue, workaround available
- [ ] Low - Cosmetic issue, enhancement request

### Component

- [ ] Shopping Cart
- [x] User Registration/Login
- [ ] Checkout Process
- [ ] Payment Processing
- [ ] User Interface
- [ ] Performance
- [x] Security

### Steps to Reproduce

1. Register a new user account
2. Examine user object in application memory/debug
3. Check password storage method

### Expected Result

Passwords should be hashed using bcrypt or similar secure hashing algorithm

### Actual Result

Passwords are stored as plain text in User objects

### Screenshots/Evidence

```python
# In models.py User class
def __init__(self, email, password, name="", address=""):
    self.password = password  # Plain text storage!
```

### Additional Information

- Browser: All Browsers
- Operating System: Windows 11
- Screen Resolution: N/A
- Additional Notes: Major security vulnerability - passwords visible to anyone with access to application memory or database

---

### Bug Report #006

**Date**: October 18, 2025  
**Reporter**: Test Engineer  
**Environment**: Chrome 118 / Windows 11 / Python 3.9

---

### Summary

Performance issue: Inefficient cart total calculation algorithm

### Severity

- [ ] Critical - System crash, data loss, security vulnerability
- [ ] High - Major functionality broken, workaround difficult
- [x] Medium - Minor functionality issue, workaround available
- [ ] Low - Cosmetic issue, enhancement request

### Component

- [x] Shopping Cart
- [ ] User Registration/Login
- [ ] Checkout Process
- [ ] Payment Processing
- [ ] User Interface
- [x] Performance
- [ ] Security

### Steps to Reproduce

1. Add large quantities of items to cart (100+ of each item)
2. Add multiple different books
3. Navigate to cart page
4. Observe page load time

### Expected Result

Cart total should calculate quickly regardless of quantities

### Actual Result

Noticeable delay when calculating totals with large quantities due to inefficient nested loop

### Screenshots/Evidence

```python
# Current inefficient implementation in models.py
def get_total_price(self):
    total = 0
    for item in self.items.values():
        for i in range(item.quantity):  # Unnecessary loop!
            total += item.book.price
    return total
```

### Additional Information

- Browser: Chrome 118
- Operating System: Windows 11
- Screen Resolution: 1920x1080
- Additional Notes: Should use multiplication instead of loops: `total += item.book.price * item.quantity`

---

## Bug Severity Guidelines

### Critical

- Application crashes or becomes unusable
- Data corruption or loss
- Security vulnerabilities that expose user data
- Financial calculation errors

### High

- Major features don't work as intended
- Significant user experience impact
- Difficult workarounds required
- Business logic errors

### Medium

- Minor features don't work correctly
- Moderate user experience impact
- Easy workarounds available
- Performance issues

### Low

- Cosmetic issues
- Minor user experience improvements
- Enhancement requests
- Documentation issues

## Testing Notes

When testing for bugs, pay special attention to:

1. **Input Validation**: Try invalid, empty, null, and edge case inputs
2. **Error Handling**: Look for unhandled exceptions and crashes
3. **Business Logic**: Verify calculations, workflows, and data integrity
4. **Security**: Test for common vulnerabilities (XSS, injection, etc.)
5. **Performance**: Monitor response times and resource usage
6. **Usability**: Evaluate user experience and accessibility
7. **Cross-browser**: Test on different browsers and devices
