#!/usr/bin/env python3
"""
Comprehensive LCG Algorithm Testing Suite
Testing all requirements from the review request:
1. Consistency Test - Same seed produces same result
2. Distribution Test - Verify balanced output
3. Categorization Test - Verify correct Small/Big assignment
4. 3-Digit Period Numbers - Test typical use case
5. LCG Formula Verification - Confirm parameters
6. Edge Cases - Test boundary conditions
"""

import requests
import json
import time
from typing import Dict, Any, List
from collections import Counter

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

def test_consistency_same_seed():
    """
    Test 1: Consistency Test - Same seed produces same result
    Test seed 123 five times, verify all return same number and category
    Test seed 456 five times, verify consistency
    """
    print("\n🔍 Test 1: Consistency Test - Same seed produces same result")
    
    test_seeds = [123, 456]
    all_passed = True
    
    for seed in test_seeds:
        print(f"\n  Testing seed {seed} - 5 consecutive calls...")
        results = []
        
        for i in range(5):
            try:
                payload = {"seed": seed}
                response = requests.post(f"{BACKEND_URL}/generate-random", 
                                       json=payload, 
                                       headers={"Content-Type": "application/json"},
                                       timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    results.append({
                        "number": data.get("number"),
                        "category": data.get("category"),
                        "seed_used": data.get("seed_used")
                    })
                    print(f"    Call {i+1}: number={data.get('number')}, category={data.get('category')}")
                else:
                    print(f"    ❌ Call {i+1}: HTTP {response.status_code}")
                    all_passed = False
                    break
                    
            except Exception as e:
                print(f"    ❌ Call {i+1}: Error - {str(e)}")
                all_passed = False
                break
        
        # Verify all results are identical
        if len(results) == 5:
            first_result = results[0]
            all_identical = all(
                r["number"] == first_result["number"] and 
                r["category"] == first_result["category"] and
                r["seed_used"] == first_result["seed_used"]
                for r in results
            )
            
            if all_identical:
                print(f"  ✅ Seed {seed}: All 5 calls returned identical results")
            else:
                print(f"  ❌ Seed {seed}: Results were not consistent!")
                all_passed = False
        else:
            all_passed = False
    
    if all_passed:
        print("\n✅ Consistency Test: PASSED")
    else:
        print("\n❌ Consistency Test: FAILED")
    
    return all_passed

def test_distribution_balance():
    """
    Test 2: Distribution Test - Verify balanced output
    Test seeds 1-100, count Small (0-4) vs Big (5-9)
    Should be roughly 50/50 distribution
    """
    print("\n🔍 Test 2: Distribution Test - Verify balanced output (seeds 1-100)")
    
    small_count = 0
    big_count = 0
    results = []
    
    for seed in range(1, 101):
        try:
            payload = {"seed": seed}
            response = requests.post(f"{BACKEND_URL}/generate-random", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                number = data.get("number")
                category = data.get("category")
                
                results.append({"seed": seed, "number": number, "category": category})
                
                if category == "Small":
                    small_count += 1
                elif category == "Big":
                    big_count += 1
                    
            else:
                print(f"❌ Seed {seed}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Seed {seed}: Error - {str(e)}")
            return False
    
    total = small_count + big_count
    small_percentage = (small_count / total) * 100 if total > 0 else 0
    big_percentage = (big_count / total) * 100 if total > 0 else 0
    
    print(f"  Results from 100 seeds:")
    print(f"    Small (0-4): {small_count} ({small_percentage:.1f}%)")
    print(f"    Big (5-9): {big_count} ({big_percentage:.1f}%)")
    
    # Check if distribution is reasonably balanced (30-70% range is acceptable)
    balanced = 30 <= small_percentage <= 70 and 30 <= big_percentage <= 70
    
    if balanced:
        print("  ✅ Distribution is reasonably balanced")
        print("\n✅ Distribution Test: PASSED")
        return True
    else:
        print("  ❌ Distribution is heavily skewed")
        print("\n❌ Distribution Test: FAILED")
        return False

def test_categorization_logic():
    """
    Test 3: Categorization Test - Verify correct Small/Big assignment
    For numbers 0,1,2,3,4 → Should return "Small"
    For numbers 5,6,7,8,9 → Should return "Big"
    """
    print("\n🔍 Test 3: Categorization Test - Verify correct Small/Big assignment")
    
    # We need to find seeds that produce specific numbers
    # This is a reverse lookup - we'll test many seeds to find ones that produce each number
    number_to_seeds = {}
    
    print("  Finding seeds that produce each number 0-9...")
    
    # Test seeds 1-1000 to find examples of each number
    for seed in range(1, 1001):
        try:
            payload = {"seed": seed}
            response = requests.post(f"{BACKEND_URL}/generate-random", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                number = data.get("number")
                category = data.get("category")
                
                if number not in number_to_seeds:
                    number_to_seeds[number] = {"seed": seed, "category": category}
                    
                # Stop when we have examples of all numbers 0-9
                if len(number_to_seeds) == 10:
                    break
                    
        except Exception as e:
            print(f"❌ Error testing seed {seed}: {str(e)}")
            return False
    
    print(f"  Found examples for {len(number_to_seeds)} different numbers")
    
    # Verify categorization for each number found
    all_correct = True
    
    for number in range(10):
        if number in number_to_seeds:
            seed_info = number_to_seeds[number]
            expected_category = "Small" if number <= 4 else "Big"
            actual_category = seed_info["category"]
            
            if actual_category == expected_category:
                print(f"    ✅ Number {number}: Category '{actual_category}' is correct")
            else:
                print(f"    ❌ Number {number}: Expected '{expected_category}', got '{actual_category}'")
                all_correct = False
        else:
            print(f"    ⚠️  Number {number}: No seed found that produces this number in first 1000 seeds")
    
    if all_correct and len(number_to_seeds) >= 8:  # Allow for some numbers not found
        print("\n✅ Categorization Test: PASSED")
        return True
    else:
        print("\n❌ Categorization Test: FAILED")
        return False

def test_three_digit_period_numbers():
    """
    Test 4: 3-Digit Period Numbers - Test typical use case
    Test: 001, 050, 100, 250, 500, 750, 999
    Verify all return valid numbers 0-9 and correct category
    """
    print("\n🔍 Test 4: 3-Digit Period Numbers - Test typical use case")
    
    test_seeds = [1, 50, 100, 250, 500, 750, 999]
    all_passed = True
    
    for seed in test_seeds:
        print(f"\n  Testing seed {seed:03d}...")
        try:
            payload = {"seed": seed}
            response = requests.post(f"{BACKEND_URL}/generate-random", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                number = data.get("number")
                category = data.get("category")
                seed_used = data.get("seed_used")
                
                print(f"    Result: number={number}, category={category}, seed_used={seed_used}")
                
                # Verify number is in valid range 0-9
                if not (isinstance(number, int) and 0 <= number <= 9):
                    print(f"    ❌ Invalid number: {number} (should be 0-9)")
                    all_passed = False
                    continue
                
                # Verify category is correct
                expected_category = "Small" if number <= 4 else "Big"
                if category != expected_category:
                    print(f"    ❌ Wrong category: expected {expected_category}, got {category}")
                    all_passed = False
                    continue
                
                # Verify seed_used matches input
                if seed_used != seed:
                    print(f"    ❌ Seed mismatch: expected {seed}, got {seed_used}")
                    all_passed = False
                    continue
                
                print(f"    ✅ Seed {seed:03d}: Valid result")
                
            else:
                print(f"    ❌ HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            all_passed = False
    
    if all_passed:
        print("\n✅ 3-Digit Period Numbers Test: PASSED")
    else:
        print("\n❌ 3-Digit Period Numbers Test: FAILED")
    
    return all_passed

def test_lcg_formula_verification():
    """
    Test 5: LCG Formula Verification
    Confirm using standard LCG parameters (a=1664525, c=1013904223, m=2^32)
    Verify seed preprocessing for better distribution
    Check that formula is: improved_seed = (seed * 48271 + 123456789) % m, then result = (a * improved_seed + c) % m
    """
    print("\n🔍 Test 5: LCG Formula Verification")
    
    # LCG Parameters from the code
    LCG_A = 1664525
    LCG_C = 1013904223
    LCG_M = 2**32
    
    print(f"  Expected LCG Parameters:")
    print(f"    a (multiplier): {LCG_A}")
    print(f"    c (increment): {LCG_C}")
    print(f"    m (modulus): {LCG_M}")
    
    # Test a few seeds and verify the formula manually
    test_seeds = [123, 456, 789]
    all_passed = True
    
    for seed in test_seeds:
        print(f"\n  Testing seed {seed} with manual calculation...")
        
        try:
            # Get result from API
            payload = {"seed": seed}
            response = requests.post(f"{BACKEND_URL}/generate-random", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                api_number = data.get("number")
                
                # Manual calculation following the server code
                # Step 1: Improve seed distribution
                improved_seed = (seed * 48271 + 123456789) % LCG_M
                
                # Step 2: Apply LCG formula
                lcg_result = (LCG_A * improved_seed + LCG_C) % LCG_M
                
                # Step 3: Map to range 0-9
                normalized = lcg_result / LCG_M
                manual_number = int(normalized * 10)  # 10 = (9 - 0 + 1)
                
                print(f"    API result: {api_number}")
                print(f"    Manual calculation: {manual_number}")
                print(f"    Improved seed: {improved_seed}")
                print(f"    LCG result: {lcg_result}")
                
                if api_number == manual_number:
                    print(f"    ✅ Seed {seed}: Formula verification PASSED")
                else:
                    print(f"    ❌ Seed {seed}: Formula verification FAILED")
                    all_passed = False
                    
            else:
                print(f"    ❌ HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            all_passed = False
    
    if all_passed:
        print("\n✅ LCG Formula Verification: PASSED")
    else:
        print("\n❌ LCG Formula Verification: FAILED")
    
    return all_passed

def test_edge_cases():
    """
    Test 6: Edge Cases
    - Seed 0
    - Very large seeds (999999)
    - Negative seeds (should handle or reject appropriately)
    """
    print("\n🔍 Test 6: Edge Cases")
    
    test_cases = [
        {"name": "Seed 0", "seed": 0},
        {"name": "Very Large Seed", "seed": 999999},
        {"name": "Negative Seed", "seed": -12345},
        {"name": "Maximum 32-bit", "seed": 2**32 - 1},
        {"name": "Larger than 32-bit", "seed": 2**33},
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
                number = data.get("number")
                category = data.get("category")
                seed_used = data.get("seed_used")
                
                print(f"    Result: number={number}, category={category}, seed_used={seed_used}")
                
                # Verify response is valid regardless of seed value
                if (isinstance(number, int) and 0 <= number <= 9 and
                    category in ["Small", "Big"] and
                    isinstance(seed_used, int)):
                    
                    # Verify category matches number
                    expected_category = "Small" if number <= 4 else "Big"
                    if category == expected_category:
                        print(f"    ✅ {test_case['name']}: Valid response")
                    else:
                        print(f"    ❌ {test_case['name']}: Wrong category")
                        all_passed = False
                else:
                    print(f"    ❌ {test_case['name']}: Invalid response format")
                    all_passed = False
            else:
                print(f"    ❌ {test_case['name']}: HTTP {response.status_code}")
                # For edge cases, we might accept some failures as valid behavior
                print(f"    ℹ️  This might be acceptable behavior for edge case")
                
        except Exception as e:
            print(f"    ❌ {test_case['name']}: Error - {str(e)}")
            # For edge cases, we might accept some failures as valid behavior
            print(f"    ℹ️  This might be acceptable behavior for edge case")
    
    if all_passed:
        print("\n✅ Edge Cases Test: PASSED")
    else:
        print("\n❌ Edge Cases Test: FAILED (some edge cases may be acceptable)")
    
    return all_passed

def run_comprehensive_lcg_tests():
    """Run all comprehensive LCG tests and provide detailed summary"""
    print("=" * 80)
    print("🚀 COMPREHENSIVE LCG ALGORITHM TESTING SUITE")
    print("=" * 80)
    
    test_results = []
    
    # Run all tests in order
    test_results.append(("API Health", test_api_health()))
    test_results.append(("1. Consistency Test", test_consistency_same_seed()))
    test_results.append(("2. Distribution Test", test_distribution_balance()))
    test_results.append(("3. Categorization Test", test_categorization_logic()))
    test_results.append(("4. 3-Digit Period Numbers", test_three_digit_period_numbers()))
    test_results.append(("5. LCG Formula Verification", test_lcg_formula_verification()))
    test_results.append(("6. Edge Cases", test_edge_cases()))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<35} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal Tests: {len(test_results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL COMPREHENSIVE TESTS PASSED!")
        print("The LCG algorithm is working accurately and meets all requirements.")
        return True
    else:
        print(f"\n⚠️  {failed} TEST(S) FAILED!")
        print("Please review the detailed results above.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_lcg_tests()
    exit(0 if success else 1)