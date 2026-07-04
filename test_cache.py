import time
from weather_api import get_weather

def main():
    print("=== Testing Redis Caching ===\n")
    
    # First call - should be slow (2 seconds)
    print("First call to get_weather('Jakarta')...")
    start = time.time()
    result1 = get_weather("Jakarta")
    time1 = time.time() - start
    print(f"Result: {result1}")
    print(f"First call time: {time1:.2f}s\n")
    
    # Second call - should be fast (< 0.1 second)
    print("Second call to get_weather('Jakarta') (cached)...")
    start = time.time()
    result2 = get_weather("Jakarta")
    time2 = time.time() - start
    print(f"Result: {result2}")
    print(f"Second call time: {time2:.2f}s\n")
    
    # Third call for another city (should be slow again)
    print("First call to get_weather('Bandung')...")
    start = time.time()
    result3 = get_weather("Bandung")
    time3 = time.time() - start
    print(f"Result: {result3}")
    print(f"First call time for Bandung: {time3:.2f}s\n")
    
    # Summary
    print("=== Summary ===")
    print(f"First call (Jakarta): {time1:.2f}s")
    print(f"Second call (Jakarta): {time2:.2f}s")
    print(f"First call (Bandung): {time3:.2f}s")
    print(f"\nPerbandingan: Second call {time1 / time2:.1f}x lebih cepat!")

if __name__ == "__main__":
    main()

