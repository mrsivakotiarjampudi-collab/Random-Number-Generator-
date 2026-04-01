#!/usr/bin/env python3
"""
PURE LCG Algorithm Testing Suite
Testing the specific requirements from the comprehensive review request:
- Pure LCG Formula: X(n+1) = (a * X(n) + c) mod m
- Manual calculations vs API responses
- Specific seed testing as requested
"""

import requests
import json
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = "https://lcg-random-gen.preview.emergentagent.com/api"

# LCG Parameters (same as in backend)
LCG_A = 1664525  # Multiplier
LCG_C = 1013904223  # Increment
LCG_M = 2**32  # Modulus (4294967296)

def manual_lcg_calculation(seed: int) -> int:
    """
    Manual calculation of Pure LCG Formula: X(n+1) = (a * X(n) + c) mod m
    """
    return (LCG_A * seed + LCG_C) % LCG_M

def map_to_range_manual(value: int, min_val: int, max_val: int) -> int:
    """
    Manual mapping of LCG output to range [0, 9]
    """
    normalized = value / LCG_M
    scaled = int(normalized * (max_val - min_val + 1)) + min_val
    return scaled

def categorize_manual(number: int) -> str:
    """
    Manual categorization: 0-4 = Small, 5-9 = Big
    """
    return "Small" if 0 <= number <= 4 else "Big"

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

def test_pure_lcg_formula_verification():
    """
    Test 1: Pure LCG Formula Verification
    Test specific seeds with manual calculations: 0, 1, 2, 5, 10, 100, 123, 456, 999
    """
    print("\n🔍 Testing Pure LCG Formula Verification...")
    print("Formula: X(n+1) = (a * X(n) + c) mod m")
    print(f"Parameters: a={LCG_A}, c={LCG_C}, m={LCG_M}")
    
    test_seeds = [0, 1, 2, 5, 10, 100, 123, 456, 999]
    all_passed = True
    
    print("\nManual Calculations vs API Results:")
    print("-" * 80)
    
    for seed in test_seeds:
        try:
            # Manual calculation
            manual_lcg = manual_lcg_calculation(seed)
            manual_mapped = map_to_range_manual(manual_lcg, 0, 9)
            manual_category = categorize_manual(manual_mapped)
            
            # API call
            payload = {"seed": seed}
            response = requests.post(f"{BACKEND_URL}/generate-random", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                api_number = data.get("number")
                api_category = data.get("category")
                api_seed_used = data.get("seed_used")
                
                # Verify results match
                lcg_match = True
                number_match = manual_mapped == api_number
                category_match = manual_category == api_category
                seed_match = seed == api_seed_used
                
                status = "✅" if (number_match and category_match and seed_match) else "❌"
                
                print(f"Seed {seed:3d}: Manual LCG={manual_lcg:10d} → {manual_mapped} ({manual_category:5s}) | API: {api_number} ({api_category:5s}) {status}")
                
                if not (number_match and category_match and seed_match):
                    print(f"         MISMATCH - Manual: {manual_mapped}/{manual_category}, API: {api_number}/{api_category}")
                    all_passed = False
                    
            else:
                print(f"Seed {seed:3d}: API ERROR - Status {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"Seed {seed:3d}: ERROR - {str(e)}")
            all_passed = False
    
    print("-" * 80)
    if all_passed:
        print("✅ Pure LCG Formula Verification: PASSED - All manual calculations match API results")
    else:
        print("❌ Pure LCG Formula Verification: FAILED - Mismatches found")
    
    return all_passed

def test_consistency():
    """
    Test 2: Consistency Test
    Same seed must produce same number ALWAYS
    Test seed=123 and seed=456 multiple times (5 times each)
    """
    print("\n🔍 Testing Consistency (Same Seed = Same Result)...")
    
    test_seeds = [123, 456]
    all_passed = True
    
    for seed in test_seeds:
        print(f"\nTesting seed {seed} - 5 consecutive calls:")
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
                    print(f"  Call {i+1}: number={data.get('number')}, category={data.get('category')}")
                else:
                    print(f"  Call {i+1}: ERROR - Status {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                print(f"  Call {i+1}: ERROR - {str(e)}")
                all_passed = False
        
        # Check if all results are identical
        if len(results) == 5:
            first_result = results[0]
            all_identical = all(
                r["number"] == first_result["number"] and 
                r["category"] == first_result["category"] and 
                r["seed_used"] == first_result["seed_used"]
                for r in results
            )
            
            if all_identical:
                print(f"  ✅ Seed {seed}: All 5 calls produced identical results")
            else:
                print(f"  ❌ Seed {seed}: Results were not consistent")
                all_passed = False
        else:
            print(f"  ❌ Seed {seed}: Could not complete all 5 calls")
            all_passed = False
    
    if all_passed:
        print("\n✅ Consistency Test: PASSED - Same seeds produce identical results")
    else:
        print("\n❌ Consistency Test: FAILED - Inconsistent results found")
    
    return all_passed

def test_mapping_to_range():
    """
    Test 3: Mapping to 0-9 Range
    Verify LCG output is correctly mapped to range [0, 9]
    Test 20 different seeds
    """
    print("\n🔍 Testing Mapping to 0-9 Range...")
    
    test_seeds = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
    all_passed = True
    
    print("Testing 20 different seeds for range [0, 9]:")
    
    for seed in test_seeds:
        try:
            payload = {"seed": seed}
            response = requests.post(f"{BACKEND_URL}/generate-random", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                number = data.get("number")
                
                if isinstance(number, int) and 0 <= number <= 9:
                    print(f"  Seed {seed:2d}: {number} ✅")
                else:
                    print(f"  Seed {seed:2d}: {number} ❌ (out of range)")
                    all_passed = False
            else:
                print(f"  Seed {seed:2d}: API ERROR - Status {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"  Seed {seed:2d}: ERROR - {str(e)}")
            all_passed = False
    
    if all_passed:
        print("✅ Mapping to 0-9 Range: PASSED - All results in valid range")
    else:
        print("❌ Mapping to 0-9 Range: FAILED - Some results out of range")
    
    return all_passed

def test_categorization():
    """
    Test 4: Categorization
    Numbers 0,1,2,3,4 → "Small"
    Numbers 5,6,7,8,9 → "Big"
    """
    print("\n🔍 Testing Categorization Logic...")
    
    # Test seeds that should produce each number 0-9
    # We'll test a range of seeds and verify categorization
    test_seeds = list(range(0, 100, 10))  # 0, 10, 20, 30, ..., 90
    all_passed = True
    
    small_count = 0
    big_count = 0
    
    print("Testing categorization for various seeds:")
    
    for seed in test_seeds:
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
                
                # Verify categorization logic
                expected_category = "Small" if 0 <= number <= 4 else "Big"
                
                if category == expected_category:
                    print(f"  Seed {seed:2d}: number={number}, category={category} ✅")
                    if category == "Small":
                        small_count += 1
                    else:
                        big_count += 1
                else:
                    print(f"  Seed {seed:2d}: number={number}, category={category} ❌ (expected {expected_category})")
                    all_passed = False
            else:
                print(f"  Seed {seed:2d}: API ERROR - Status {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"  Seed {seed:2d}: ERROR - {str(e)}")
            all_passed = False
    
    print(f"\nCategorization Summary: Small={small_count}, Big={big_count}")
    
    if all_passed:
        print("✅ Categorization Test: PASSED - All numbers correctly categorized")
    else:
        print("❌ Categorization Test: FAILED - Incorrect categorization found")
    
    return all_passed

def test_distribution_analysis():
    """
    Test 5: Distribution Analysis
    Test seeds 1-100, count how many produce 0, 1, 2, ..., 9
    Show distribution statistics
    """
    print("\n🔍 Testing Distribution Analysis (Seeds 1-100)...")
    
    distribution = {i: 0 for i in range(10)}  # Count for each number 0-9
    small_count = 0
    big_count = 0
    all_passed = True
    
    print("Analyzing distribution for seeds 1-100...")
    
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
                
                if isinstance(number, int) and 0 <= number <= 9:
                    distribution[number] += 1
                    if category == "Small":
                        small_count += 1
                    elif category == "Big":
                        big_count += 1
                else:
                    print(f"  Seed {seed}: Invalid number {number}")
                    all_passed = False
            else:
                print(f"  Seed {seed}: API ERROR - Status {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"  Seed {seed}: ERROR - {str(e)}")
            all_passed = False
    
    # Display distribution statistics
    print("\nDistribution Statistics:")
    print("-" * 40)
    for number, count in distribution.items():
        percentage = (count / 100) * 100
        category = "Small" if number <= 4 else "Big"
        print(f"Number {number} ({category:5s}): {count:2d} times ({percentage:4.1f}%)")
    
    print("-" * 40)
    print(f"Small (0-4): {small_count} times ({(small_count/100)*100:.1f}%)")
    print(f"Big (5-9):   {big_count} times ({(big_count/100)*100:.1f}%)")
    
    if all_passed:
        print("✅ Distribution Analysis: PASSED - All seeds processed successfully")
    else:
        print("❌ Distribution Analysis: FAILED - Some seeds had errors")
    
    return all_passed

def test_three_digit_period_numbers():
    """
    Test 6: 3-Digit Period Numbers
    Test: 100, 200, 300, 400, 500, 600, 700, 800, 900, 999
    """
    print("\n🔍 Testing 3-Digit Period Numbers...")
    
    test_seeds = [100, 200, 300, 400, 500, 600, 700, 800, 900, 999]
    all_passed = True
    
    print("Testing 3-digit period numbers:")
    
    for seed in test_seeds:
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
                
                # Verify all fields are valid
                if (isinstance(number, int) and 0 <= number <= 9 and
                    category in ["Small", "Big"] and
                    seed_used == seed):
                    print(f"  Seed {seed}: number={number}, category={category} ✅")
                else:
                    print(f"  Seed {seed}: Invalid response - number={number}, category={category}")
                    all_passed = False
            else:
                print(f"  Seed {seed}: API ERROR - Status {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"  Seed {seed}: ERROR - {str(e)}")
            all_passed = False
    
    if all_passed:
        print("✅ 3-Digit Period Numbers: PASSED - All seeds work correctly")
    else:
        print("❌ 3-Digit Period Numbers: FAILED - Some seeds had issues")
    
    return all_passed

def run_comprehensive_lcg_tests():
    """Run all comprehensive LCG tests as requested in the review"""
    print("=" * 80)
    print("🚀 COMPREHENSIVE PURE LCG ALGORITHM TESTING")
    print("Formula: X(n+1) = (a * X(n) + c) mod m")
    print(f"Parameters: a={LCG_A}, c={LCG_C}, m={LCG_M}")
    print("=" * 80)
    
    test_results = []
    
    # Run all tests as specified in the review request
    test_results.append(("API Health", test_api_health()))
    test_results.append(("Pure LCG Formula Verification", test_pure_lcg_formula_verification()))
    test_results.append(("Consistency Test", test_consistency()))
    test_results.append(("Mapping to 0-9 Range", test_mapping_to_range()))
    test_results.append(("Categorization", test_categorization()))
    test_results.append(("Distribution Analysis", test_distribution_analysis()))
    test_results.append(("3-Digit Period Numbers", test_three_digit_period_numbers()))
    
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
        print("\n🎉 ALL COMPREHENSIVE LCG TESTS PASSED!")
        print("✅ Pure LCG Formula implementation is mathematically correct")
        print("✅ Manual calculations match API results perfectly")
        print("✅ Consistency, distribution, and categorization all verified")
        return True
    else:
        print(f"\n⚠️  {failed} TEST(S) FAILED! Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_lcg_tests()
    exit(0 if success else 1)