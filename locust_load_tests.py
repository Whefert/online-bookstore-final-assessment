# Student ID: #2416130

"""
Locust Load Testing Configuration for Online Bookstore
=====================================================

This file defines load testing scenarios using Locust to simulate multiple users
interacting with the online bookstore application simultaneously.

Usage:
    pip install locust
    locust -f locust_load_tests.py --host=http://localhost:5000

Web UI available at: http://localhost:8089
"""

from locust import HttpUser, task, between
import random
import json


class BookstoreUser(HttpUser):
    """Simulates a typical user browsing and purchasing from the bookstore"""
    
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    
    def on_start(self):
        """Called when a user starts - simulate login for some users"""
        # 30% of users will register/login
        if random.random() < 0.3:
            self.register_and_login()
        
        # Initialize user session data
        self.cart_items = []
        self.books = [
            "The Great Gatsby",
            "1984", 
            "I Ching",
            "Moby Dick"
        ]
    
    def register_and_login(self):
        """Register a new user and login"""
        user_id = random.randint(1000, 9999)
        email = f"loadtest{user_id}@example.com"
        password = "testpass123"
        
        # Register user
        self.client.post("/register", data={
            "email": email,
            "password": password,
            "name": f"Load Test User {user_id}",
            "address": f"{user_id} Test Street"
        })
        
        # Login
        self.client.post("/login", data={
            "email": email,
            "password": password
        })
    
    @task(10)
    def browse_homepage(self):
        """Browse the main page - most common action"""
        self.client.get("/")
    
    @task(5)
    def view_cart(self):
        """View shopping cart"""
        self.client.get("/cart")
    
    @task(3)
    def add_book_to_cart(self):
        """Add a random book to cart"""
        book_title = random.choice(self.books)
        quantity = random.randint(1, 5)
        
        response = self.client.post("/add-to-cart", data={
            "title": book_title,
            "quantity": str(quantity)
        })
        
        if response.status_code == 302:  # Successful redirect
            self.cart_items.append({"title": book_title, "quantity": quantity})
    
    @task(2)
    def update_cart_quantity(self):
        """Update quantity of item in cart"""
        if self.cart_items:
            item = random.choice(self.cart_items)
            new_quantity = random.randint(0, 10)
            
            self.client.post("/update-cart", data={
                "title": item["title"],
                "quantity": str(new_quantity)
            })
            
            if new_quantity == 0:
                self.cart_items.remove(item)
            else:
                item["quantity"] = new_quantity
    
    @task(1)
    def remove_from_cart(self):
        """Remove item from cart"""
        if self.cart_items:
            item = random.choice(self.cart_items)
            
            self.client.post("/remove-from-cart", data={
                "title": item["title"]
            })
            
            self.cart_items.remove(item)
    
    @task(1)
    def clear_cart(self):
        """Clear entire cart"""
        if self.cart_items:
            self.client.post("/clear-cart")
            self.cart_items.clear()
    
    @task(2)
    def checkout_process(self):
        """Attempt checkout process"""
        if self.cart_items:
            # View checkout page
            response = self.client.get("/checkout")
            
            if response.status_code == 200:
                # Complete checkout with test data
                discount_codes = ["", "SAVE10", "WELCOME20", "INVALID"]
                payment_methods = ["credit_card", "paypal"]
                
                self.client.post("/process-checkout", data={
                    "name": "Load Test Customer",
                    "email": "loadtest@example.com",
                    "address": "123 Load Test Street",
                    "city": "Test City",
                    "zip_code": "12345",
                    "payment_method": random.choice(payment_methods),
                    "card_number": "4444444444444444",
                    "expiry_date": "12/25",
                    "cvv": "123",
                    "discount_code": random.choice(discount_codes)
                })
                
                # Clear cart after checkout attempt
                self.cart_items.clear()


class PowerUser(HttpUser):
    """Simulates power users who perform many operations quickly"""
    
    wait_time = between(0.5, 2)  # Faster operations
    weight = 2  # Less common than regular users
    
    def on_start(self):
        self.books = ["The Great Gatsby", "1984", "I Ching", "Moby Dick"]
    
    @task(15)
    def rapid_cart_operations(self):
        """Perform rapid cart operations to stress test"""
        book_title = random.choice(self.books)
        quantity = random.randint(10, 50)  # Larger quantities
        
        # Add to cart
        self.client.post("/add-to-cart", data={
            "title": book_title,
            "quantity": str(quantity)
        })
        
        # Immediately update quantity
        new_quantity = random.randint(1, 100)
        self.client.post("/update-cart", data={
            "title": book_title,
            "quantity": str(new_quantity)
        })
    
    @task(5)
    def stress_page_loads(self):
        """Rapidly navigate between pages"""
        pages = ["/", "/cart", "/login", "/register"]
        for _ in range(3):
            page = random.choice(pages)
            self.client.get(page)


class MobileUser(HttpUser):
    """Simulates mobile users with different usage patterns"""
    
    wait_time = between(2, 8)  # Slower, more deliberate actions
    weight = 3
    
    def on_start(self):
        # Set mobile user agent
        self.client.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
        })
        self.books = ["The Great Gatsby", "1984", "I Ching", "Moby Dick"]
    
    @task(8)
    def mobile_browse(self):
        """Mobile browsing pattern - more homepage visits"""
        self.client.get("/")
    
    @task(3)
    def mobile_cart_add(self):
        """Mobile users typically add fewer items"""
        book_title = random.choice(self.books)
        quantity = random.randint(1, 2)  # Smaller quantities on mobile
        
        self.client.post("/add-to-cart", data={
            "title": book_title,
            "quantity": str(quantity)
        })
    
    @task(2)
    def mobile_view_cart(self):
        """Check cart frequently on mobile"""
        self.client.get("/cart")


class BotUser(HttpUser):
    """Simulates automated bot behavior - should be detected and handled"""
    
    wait_time = between(0.1, 0.5)  # Very fast, bot-like behavior
    weight = 1  # Rare
    
    @task(20)
    def bot_rapid_requests(self):
        """Make rapid requests like a bot"""
        pages = ["/", "/cart", "/login", "/register", "/checkout"]
        page = random.choice(pages)
        self.client.get(page)
    
    @task(5)
    def bot_form_spam(self):
        """Attempt form submissions with invalid data"""
        # Try to register with obviously fake data
        self.client.post("/register", data={
            "email": "bot@bot.bot",
            "password": "bot",
            "name": "Bot User"
        })


# Custom test scenarios for specific performance testing

class PerformanceStressTest(HttpUser):
    """Focused performance stress testing"""
    
    wait_time = between(0.1, 1)
    
    @task
    def stress_cart_calculation(self):
        """Stress test the inefficient cart calculation"""
        # Add many items to trigger performance issues
        for i in range(10):
            self.client.post("/add-to-cart", data={
                "title": "The Great Gatsby",
                "quantity": "100"  # Large quantity to stress calculation
            })
        
        # View cart to trigger total calculation
        self.client.get("/cart")
        
        # Clear cart
        self.client.post("/clear-cart")


class SecurityTestUser(HttpUser):
    """Tests for security vulnerabilities"""
    
    wait_time = between(1, 3)
    
    @task
    def test_input_validation(self):
        """Test various input validation scenarios"""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "<script>alert('xss')</script>",
            "../../../../etc/passwd",
            "' OR '1'='1",
            "admin'--"
        ]
        
        malicious_input = random.choice(malicious_inputs)
        
        # Test registration with malicious input
        self.client.post("/register", data={
            "email": malicious_input,
            "password": malicious_input,
            "name": malicious_input
        })
        
        # Test add to cart with malicious input
        self.client.post("/add-to-cart", data={
            "title": malicious_input,
            "quantity": malicious_input
        })


# Load testing scenarios configuration
class LoadTestConfig:
    """Configuration for different load testing scenarios"""
    
    @staticmethod
    def light_load():
        """Light load - normal usage"""
        return {
            "users": 10,
            "spawn_rate": 2,
            "run_time": "5m"
        }
    
    @staticmethod
    def medium_load():
        """Medium load - busy period"""
        return {
            "users": 50,
            "spawn_rate": 5,
            "run_time": "10m"
        }
    
    @staticmethod
    def heavy_load():
        """Heavy load - peak traffic"""
        return {
            "users": 200,
            "spawn_rate": 10,
            "run_time": "15m"
        }
    
    @staticmethod
    def stress_test():
        """Stress test - beyond normal capacity"""
        return {
            "users": 500,
            "spawn_rate": 20,
            "run_time": "20m"
        }


if __name__ == "__main__":
    print("Locust Load Testing for Online Bookstore")
    print("=" * 50)
    print()
    print("Available user types:")
    print("- BookstoreUser: Regular customer behavior")
    print("- PowerUser: Heavy usage patterns")
    print("- MobileUser: Mobile device simulation")
    print("- BotUser: Automated bot behavior")
    print("- PerformanceStressTest: Stress testing")
    print("- SecurityTestUser: Security vulnerability testing")
    print()
    print("Usage:")
    print("1. Start the Flask app: python app.py")
    print("2. Install Locust: pip install locust")
    print("3. Run load test: locust -f locust_load_tests.py --host=http://localhost:5000")
    print("4. Open web UI: http://localhost:8089")
    print()
    print("Example load test scenarios:")
    config = LoadTestConfig()
    print(f"Light load: {config.light_load()}")
    print(f"Medium load: {config.medium_load()}")
    print(f"Heavy load: {config.heavy_load()}")
    print(f"Stress test: {config.stress_test()}")