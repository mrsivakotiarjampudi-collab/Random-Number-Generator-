#!/usr/bin/env python3
"""
Backend Test Suite for Random Number Generator API with Custom Seed Support
Testing the specific requirements from the review request
"""

import requests
import json
import time
from typing import Dict, Any

# Backend URL from environment
BACKEND_URL = "https://lcg-random-gen.preview.emergentagent.com/api"

def test_api_health():
    """Test if the API is running and healthy"""
    print("🔍 Testing API Health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            return True
        else:
            print(f"❌ API Health Check: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health Check: FAILED - {str(e)}")
        return False

def test_custom_seed_12345():
    """Test Case 1: Test with custom seed 12345 - should return number 0, category 'Small'"""
    print("\n🔍 Testing Custom Seed 12345...")
    try:
        payload = {"seed": 12345}
        response = requests.post(f"{BACKEND_URL}/generate-random", 
                               json=payload, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            
            # Verify expected results
            expected_number = 0
            expected_category = "Small"
            expected_seed = 12345
            
            success = True
            if data.get("number") != expected_number:
                print(f"❌ Number mismatch: expected {expected_number}, got {data.get('number')}")
                success = False
            
            if data.get("category") != expected_category:
                print(f"❌ Category mismatch: expected {expected_category}, got {data.get('category')}")
                success = False
                
            if data.get("seed_used") != expected_seed:
                print(f"❌ Seed mismatch: expected {expected_seed}, got {data.get('seed_used')}")
                success = False
            
            if success:
                print("✅ Custom Seed 12345 Test: PASSED")
                return True
            else:
                print("❌ Custom Seed 12345 Test: FAILED - Results don't match expected values")
                return False
        else:
            print(f"❌ Custom Seed 12345 Test: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Custom Seed 12345 Test: FAILED - {str(e)}")
        return False

def test_custom_seed_99999():
    """Test Case 2: Test with custom seed 99999 - should return number 9, category 'Big'"""
    print("\n🔍 Testing Custom Seed 99999...")
    try:
        payload = {"seed": 99999}
        response = requests.post(f"{BACKEND_URL}/generate-random", 
                               json=payload, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            
            # Verify expected results
            expected_number = 9
            expected_category = "Big"
            expected_seed = 99999
            
            success = True
            if data.get("number") != expected_number:
                print(f"❌ Number mismatch: expected {expected_number}, got {data.get('number')}")
                success = False
            
            if data.get("category") != expected_category:
                print(f"❌ Category mismatch: expected {expected_category}, got {data.get('category')}")
                success = False
                
            if data.get("seed_used") != expected_seed:
                print(f"❌ Seed mismatch: expected {expected_seed}, got {data.get('seed_used')}")
                success = False
            
            if success:
                print("✅ Custom Seed 99999 Test: PASSED")
                return True
            else:
                print("❌ Custom Seed 99999 Test: FAILED - Results don't match expected values")
                return False
        else:
            print(f"❌ Custom Seed 99999 Test: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Custom Seed 99999 Test: FAILED - {str(e)}")
        return False

def test_empty_body_auto_seed():
    """Test Case 3: Test without seed (empty body) - should use timestamp-based seed"""
    print("\n🔍 Testing Empty Body (Auto Seed)...")
    try:
        payload = {}
        response = requests.post(f"{BACKEND_URL}/generate-random", 
                               json=payload, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            
            # Verify response structure and ranges
            success = True
            
            # Check number is in range 0-9
            number = data.get("number")
            if not (isinstance(number, int) and 0 <= number <= 9):
                print(f"❌ Number out of range: expected 0-9, got {number}")
                success = False
            
            # Check category is correct based on number
            category = data.get("category")
            expected_category = "Small" if number <= 4 else "Big"
            if category != expected_category:
                print(f"❌ Category incorrect: expected {expected_category}, got {category}")
                success = False
            
            # Check seed_used is present and reasonable (timestamp-based)
            seed_used = data.get("seed_used")
            if not isinstance(seed_used, int) or seed_used <= 0:
                print(f"❌ Invalid seed_used: {seed_used}")
                success = False
            
            if success:
                print("✅ Empty Body (Auto Seed) Test: PASSED")
                return True
            else:
                print("❌ Empty Body (Auto Seed) Test: FAILED")
                return False
        else:
            print(f"❌ Empty Body (Auto Seed) Test: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Empty Body (Auto Seed) Test: FAILED - {str(e)}")
        return False

def test_deterministic_behavior():
    """Test Case 4: Test same seed produces same result - deterministic behavior"""
    print("\n🔍 Testing Deterministic Behavior (Same Seed = Same Result)...")
    try:
        payload = {"seed": 12345}
        
        # First call
        response1 = requests.post(f"{BACKEND_URL}/generate-random", 
                                json=payload, 
                                headers={"Content-Type": "application/json"},
                                timeout=10)
        
        # Second call with same seed
        response2 = requests.post(f"{BACKEND_URL}/generate-random", 
                                json=payload, 
                                headers={"Content-Type": "application/json"},
                                timeout=10)
        
        if response1.status_code == 200 and response2.status_code == 200:
            data1 = response1.json()
            data2 = response2.json()
            
            print(f"First call: {data1}")
            print(f"Second call: {data2}")
            
            # Verify both calls return identical results
            if (data1.get("number") == data2.get("number") and 
                data1.get("category") == data2.get("category") and
                data1.get("seed_used") == data2.get("seed_used")):
                print("✅ Deterministic Behavior Test: PASSED - Same seed produces identical results")
                return True
            else:
                print("❌ Deterministic Behavior Test: FAILED - Same seed produced different results")
                return False
        else:
            print(f"❌ Deterministic Behavior Test: FAILED - HTTP errors: {response1.status_code}, {response2.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Deterministic Behavior Test: FAILED - {str(e)}")
        return False

def test_invalid_seed_handling():
    """Test Case 5: Test invalid seed handling - edge cases"""
    print("\n🔍 Testing Invalid Seed Handling...")
    
    test_cases = [
        {"name": "Very Large Seed", "seed": 999999999999999999999},
        {"name": "Negative Seed", "seed": -12345},
        {"name": "Zero Seed", "seed": 0},
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n  Testing {test_case['name']}: {test_case['seed']}")
        try:
            payload = {"seed": test_case["seed"]}
            response = requests.post(f"{BACKEND_URL}/generate-random", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"  Response: {data}")
                
                # Verify response is valid regardless of seed value
                number = data.get("number")
                category = data.get("category")
                seed_used = data.get("seed_used")
                
                if (isinstance(number, int) and 0 <= number <= 9 and
                    category in ["Small", "Big"] and
                    isinstance(seed_used, int)):
                    print(f"  ✅ {test_case['name']}: PASSED")
                else:
                    print(f"  ❌ {test_case['name']}: FAILED - Invalid response format")
                    all_passed = False
            else:
                print(f"  ❌ {test_case['name']}: FAILED - Status {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"  ❌ {test_case['name']}: FAILED - {str(e)}")
            all_passed = False
    
    if all_passed:
        print("\n✅ Invalid Seed Handling Test: PASSED")
    else:
        print("\n❌ Invalid Seed Handling Test: FAILED")
    
    return all_passed

def run_all_tests():
    """Run all test cases and provide summary"""
    print("=" * 80)
    print("🚀 RANDOM NUMBER GENERATOR API - CUSTOM SEED TESTING")
    print("=" * 80)
    
    test_results = []
    
    # Run all tests
    test_results.append(("API Health", test_api_health()))
    test_results.append(("Custom Seed 12345", test_custom_seed_12345()))
    test_results.append(("Custom Seed 99999", test_custom_seed_99999()))
    test_results.append(("Empty Body Auto Seed", test_empty_body_auto_seed()))
    test_results.append(("Deterministic Behavior", test_deterministic_behavior()))
    test_results.append(("Invalid Seed Handling", test_invalid_seed_handling()))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal Tests: {len(test_results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Custom seed functionality is working correctly.")
        return True
    else:
        print(f"\n⚠️  {failed} TEST(S) FAILED! Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)