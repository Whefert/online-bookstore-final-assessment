# Performance Testing Scripts

"""
Performance testing utilities for the Online Bookstore application.
These scripts help measure and analyze system performance under various conditions.
"""

import time
import sys
import os
import threading
from concurrent.futures import ThreadPoolExecutor
import statistics
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Cart, Book, User, Order

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Note: 'requests' module not available. Web testing will be skipped.")

try:
    from app import BOOKS
except ImportError:
    # Create sample books if app import fails
    BOOKS = [
        Book("The Great Gatsby", "Fiction", 10.99, "/images/books/the_great_gatsby.jpg"),
        Book("1984", "Dystopia", 8.99, "/images/books/1984.jpg"),
        Book("I Ching", "Traditional", 18.99, "/images/books/I-Ching.jpg"),
        Book("Moby Dick", "Adventure", 12.49, "/images/books/moby_dick.jpg")
    ]


class PerformanceTestSuite:
    """Performance testing suite for the bookstore application"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
        else:
            self.session = None
        self.results = {}
    
    def measure_execution_time(self, func, *args, **kwargs):
        """Measure execution time of a function"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    
    def test_cart_performance(self):
        """Test cart operations performance"""
        print("Testing Cart Performance...")
        
        # Test 1: Cart total calculation with many items
        cart = Cart()
        book = Book("Performance Test Book", "Test", 10.99, "/test.jpg")
        
        # Add many items to cart
        quantities = [10, 50, 100, 500, 1000]
        results = {}
        
        for qty in quantities:
            cart.clear()
            cart.add_book(book, qty)
            
            _, execution_time = self.measure_execution_time(cart.get_total_price)
            results[f"cart_total_{qty}_items"] = execution_time
            print(f"Cart total calculation ({qty} items): {execution_time:.6f} seconds")
        
        self.results["cart_performance"] = results
        
        # Test 2: Multiple cart operations
        operations_count = 1000
        cart.clear()
        
        start_time = time.time()
        for i in range(operations_count):
            cart.add_book(book, 1)
        end_time = time.time()
        
        add_time = (end_time - start_time) / operations_count
        print(f"Average add operation time: {add_time:.6f} seconds")
        
        return results
    
    def test_user_operations_performance(self):
        """Test user-related operations performance"""
        print("Testing User Operations Performance...")
        
        user = User("test@example.com", "password", "Test User")
        
        # Test order history with many orders
        order_counts = [10, 50, 100, 500, 1000]
        results = {}
        
        for count in order_counts:
            # Clear previous orders
            user.orders = []
            
            # Add many orders
            for i in range(count):
                order = Order(
                    order_id=f"ORDER{i:06d}",
                    user_email="test@example.com",
                    items=[],
                    shipping_info={},
                    payment_info={},
                    total_amount=10.99
                )
                user.add_order(order)
            
            # Measure order history retrieval
            _, execution_time = self.measure_execution_time(user.get_order_history)
            results[f"order_history_{count}_orders"] = execution_time
            print(f"Order history retrieval ({count} orders): {execution_time:.6f} seconds")
        
        self.results["user_performance"] = results
        return results
    
    def test_page_load_performance(self):
        """Test web page load performance"""
        if not REQUESTS_AVAILABLE:
            print("Skipping page load tests - requests module not available")
            return {}
            
        print("Testing Page Load Performance...")
        
        pages = {
            "home": "/",
            "cart": "/cart",
            "login": "/login",
            "register": "/register",
            "checkout": "/checkout"
        }
        
        results = {}
        
        for page_name, url in pages.items():
            response_times = []
            
            # Test each page multiple times
            for _ in range(10):
                try:
                    start_time = time.time()
                    response = self.session.get(f"{self.base_url}{url}")
                    end_time = time.time()
                    
                    if response.status_code in [200, 302]:  # Success or redirect
                        response_times.append(end_time - start_time)
                except requests.exceptions.RequestException as e:
                    print(f"Error accessing {page_name}: {e}")
                    continue
            
            if response_times:
                avg_time = statistics.mean(response_times)
                min_time = min(response_times)
                max_time = max(response_times)
                
                results[page_name] = {
                    "average": avg_time,
                    "min": min_time,
                    "max": max_time,
                    "samples": len(response_times)
                }
                
                print(f"{page_name.capitalize()} page - Avg: {avg_time:.3f}s, Min: {min_time:.3f}s, Max: {max_time:.3f}s")
        
        self.results["page_load_performance"] = results
        return results
    
    def test_concurrent_users(self, num_users=10, requests_per_user=5):
        """Test performance with concurrent users"""
        if not REQUESTS_AVAILABLE:
            print("Skipping concurrent user tests - requests module not available")
            return {}
            
        print(f"Testing Concurrent Users Performance ({num_users} users, {requests_per_user} requests each)...")
        
        def simulate_user():
            """Simulate a single user's actions"""
            if not REQUESTS_AVAILABLE:
                return []
                
            user_session = requests.Session()
            response_times = []
            
            for _ in range(requests_per_user):
                try:
                    # Simulate browsing behavior
                    start_time = time.time()
                    
                    # Home page
                    response = user_session.get(f"{self.base_url}/")
                    if response.status_code != 200:
                        continue
                    
                    # Cart page
                    response = user_session.get(f"{self.base_url}/cart")
                    
                    end_time = time.time()
                    response_times.append(end_time - start_time)
                    
                except requests.exceptions.RequestException:
                    continue
            
            return response_times
        
        # Run concurrent user simulation
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [executor.submit(simulate_user) for _ in range(num_users)]
            all_response_times = []
            
            for future in futures:
                user_times = future.result()
                all_response_times.extend(user_times)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        if all_response_times:
            avg_response_time = statistics.mean(all_response_times)
            total_requests = len(all_response_times)
            requests_per_second = total_requests / total_time
            
            results = {
                "concurrent_users": num_users,
                "total_requests": total_requests,
                "total_time": total_time,
                "average_response_time": avg_response_time,
                "requests_per_second": requests_per_second,
                "successful_requests": total_requests
            }
            
            print(f"Total requests: {total_requests}")
            print(f"Total time: {total_time:.2f} seconds")
            print(f"Average response time: {avg_response_time:.3f} seconds")
            print(f"Requests per second: {requests_per_second:.2f}")
            
            self.results["concurrent_performance"] = results
            return results
        
        return None
    
    def test_memory_usage(self):
        """Test memory usage patterns"""
        print("Testing Memory Usage...")
        
        import tracemalloc
        
        # Start memory tracing
        tracemalloc.start()
        
        # Simulate heavy cart usage
        cart = Cart()
        book = Book("Memory Test Book", "Test", 10.99, "/test.jpg")
        
        # Baseline memory
        baseline = tracemalloc.get_traced_memory()
        
        # Add many items
        for i in range(1000):
            cart.add_book(book, 10)
        
        # Memory after operations
        after_ops = tracemalloc.get_traced_memory()
        
        # Clear cart
        cart.clear()
        
        # Memory after cleanup
        after_cleanup = tracemalloc.get_traced_memory()
        
        tracemalloc.stop()
        
        results = {
            "baseline_memory_mb": baseline[0] / 1024 / 1024,
            "peak_memory_mb": baseline[1] / 1024 / 1024,
            "after_operations_mb": after_ops[0] / 1024 / 1024,
            "after_cleanup_mb": after_cleanup[0] / 1024 / 1024,
            "memory_increase_mb": (after_ops[0] - baseline[0]) / 1024 / 1024
        }
        
        print(f"Baseline memory: {results['baseline_memory_mb']:.2f} MB")
        print(f"After operations: {results['after_operations_mb']:.2f} MB")
        print(f"After cleanup: {results['after_cleanup_mb']:.2f} MB")
        print(f"Memory increase: {results['memory_increase_mb']:.2f} MB")
        
        self.results["memory_usage"] = results
        return results
    
    def run_all_tests(self):
        """Run all performance tests"""
        print("=" * 60)
        print("ONLINE BOOKSTORE PERFORMANCE TEST SUITE")
        print("=" * 60)
        print()
        
        # Run all test categories
        self.test_cart_performance()
        print()
        
        self.test_user_operations_performance()
        print()
        
        self.test_page_load_performance()
        print()
        
        self.test_concurrent_users()
        print()
        
        self.test_memory_usage()
        print()
        
        # Generate summary report
        self.generate_performance_report()
    
    def generate_performance_report(self):
        """Generate a comprehensive performance report"""
        print("=" * 60)
        print("PERFORMANCE TEST SUMMARY REPORT")
        print("=" * 60)
        
        # Performance thresholds
        thresholds = {
            "cart_total_calculation": 0.001,  # 1ms for cart total
            "page_load_average": 0.1,  # 100ms for page loads
            "requests_per_second": 50,  # Minimum RPS
            "memory_increase": 10  # Max 10MB increase
        }
        
        issues_found = []
        
        # Analyze cart performance
        if "cart_performance" in self.results:
            cart_results = self.results["cart_performance"]
            for test_name, time_taken in cart_results.items():
                if time_taken > thresholds["cart_total_calculation"] * 1000:  # Scale with items
                    issues_found.append(f"Slow cart calculation: {test_name} took {time_taken:.6f}s")
        
        # Analyze page load performance
        if "page_load_performance" in self.results:
            page_results = self.results["page_load_performance"]
            for page_name, metrics in page_results.items():
                if metrics["average"] > thresholds["page_load_average"]:
                    issues_found.append(f"Slow page load: {page_name} avg {metrics['average']:.3f}s")
        
        # Analyze concurrent performance
        if "concurrent_performance" in self.results:
            concurrent_results = self.results["concurrent_performance"]
            if concurrent_results["requests_per_second"] < thresholds["requests_per_second"]:
                issues_found.append(f"Low throughput: {concurrent_results['requests_per_second']:.2f} RPS")
        
        # Analyze memory usage
        if "memory_usage" in self.results:
            memory_results = self.results["memory_usage"]
            if memory_results["memory_increase_mb"] > thresholds["memory_increase"]:
                issues_found.append(f"High memory usage: {memory_results['memory_increase_mb']:.2f} MB increase")
        
        # Print summary
        if issues_found:
            print("PERFORMANCE ISSUES FOUND:")
            for issue in issues_found:
                print(f"  ⚠️  {issue}")
        else:
            print("✅ All performance tests passed!")
        
        print()
        print("RECOMMENDATIONS:")
        print("  • Optimize cart total calculation algorithm")
        print("  • Implement database indexing for large datasets")
        print("  • Add caching for frequently accessed data")
        print("  • Consider pagination for large result sets")
        print("  • Monitor memory usage in production")
        
        # Save detailed results
        with open("performance_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print()
        print("Detailed results saved to: performance_test_results.json")


def run_quick_performance_test():
    """Run a quick performance test without web server dependency"""
    print("Quick Performance Test (No Web Server Required)")
    print("=" * 50)
    
    # Test cart performance
    cart = Cart()
    book = Book("Test Book", "Fiction", 10.99, "/test.jpg")
    
    # Test with different quantities
    quantities = [1, 10, 100, 1000]
    
    for qty in quantities:
        cart.clear()
        cart.add_book(book, qty)
        
        start_time = time.time()
        total = cart.get_total_price()
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"Cart total ({qty:4d} items): {execution_time:.6f}s - Total: ${total:.2f}")
    
    # Test user operations
    user = User("test@example.com", "password", "Test User")
    
    # Add orders and test retrieval
    for i in range(100):
        order = Order(f"ORDER{i:03d}", "test@example.com", [], {}, {}, 10.99)
        user.add_order(order)
    
    start_time = time.time()
    history = user.get_order_history()
    end_time = time.time()
    
    print(f"Order history retrieval (100 orders): {end_time - start_time:.6f}s")
    print(f"Orders retrieved: {len(history)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        run_quick_performance_test()
    else:
        # Full performance test suite
        suite = PerformanceTestSuite()
        
        # Check if server is running
        if REQUESTS_AVAILABLE:
            try:
                response = requests.get("http://localhost:5000/", timeout=5)
                print("✅ Server is running, starting full performance test suite...")
                suite.run_all_tests()
            except:
                print("❌ Server not running at localhost:5000")
                print("Starting app with: python app.py")
                print("Or run quick test with: python performance_tests.py quick")
                print()
                print("Running quick performance test instead...")
                run_quick_performance_test()
        else:
            print("Running quick performance test (no web server testing)...")
            run_quick_performance_test()