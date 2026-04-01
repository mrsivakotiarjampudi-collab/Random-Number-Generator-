#!/usr/bin/env python3
"""
Final Pure LCG Verification Test
Confirming the implementation matches the exact mathematical requirements
"""

import requests

# Backend URL
BACKEND_URL = "https://lcg-random-gen.preview.emergentagent.com/api"

# LCG Parameters
LCG_A = 1664525
LCG_C = 1013904223  
LCG_M = 2**32

def manual_lcg_calculation(seed: int) -> int:
    """Pure LCG Formula: X(n+1) = (a * X(n) + c) mod m"""
    return (LCG_A * seed + LCG_C) % LCG_M

def final_verification():
    """Final verification of Pure LCG implementation"""
    print("🔍 FINAL PURE LCG VERIFICATION")
    print("=" * 60)
    print("Testing the exact formula from review request:")
    print("X(n+1) = (a * X(n) + c) mod m")
    print(f"a = {LCG_A} (multiplier)")
    print(f"c = {LCG_C} (increment)")  
    print(f"m = {LCG_M} (modulus = 2^32)")
    print("=" * 60)
    
    # Test the specific manual calculation from review request
    print("\nManual calculation for seed=1:")
    manual_result = (LCG_A * 1 + LCG_C) % LCG_M
    print(f"(1664525 * 1 + 1013904223) % 2^32 = {manual_result}")
    
    # Test API
    payload = {"seed": 1}
    response = requests.post(f"{BACKEND_URL}/generate-random", 
                           json=payload, 
                           headers={"Content-Type": "application/json"},
                           timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        api_number = data.get("number")
        
        # Manual mapping
        normalized = manual_result / LCG_M
        mapped = int(normalized * 10)  # 0-9 range
        
        print(f"Manual LCG result: {manual_result}")
        print(f"Normalized: {normalized:.6f}")
        print(f"Mapped to 0-9: {mapped}")
        print(f"API result: {api_number}")
        
        if mapped == api_number:
            print("✅ PURE LCG FORMULA VERIFIED - Implementation is mathematically correct")
        else:
            print("❌ Mismatch found")
    
    # Test the specific seeds from review request
    print(f"\n{'Seed':<6} {'Manual LCG':<12} {'API Number':<10} {'Status'}")
    print("-" * 40)
    
    test_seeds = [0, 1, 2, 5, 10, 100, 123, 456, 999]
    all_correct = True
    
    for seed in test_seeds:
        manual_lcg = manual_lcg_calculation(seed)
        normalized = manual_lcg / LCG_M
        expected = int(normalized * 10)
        
        payload = {"seed": seed}
        response = requests.post(f"{BACKEND_URL}/generate-random", 
                               json=payload, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            api_number = data.get("number")
            status = "✅" if expected == api_number else "❌"
            print(f"{seed:<6} {manual_lcg:<12} {api_number:<10} {status}")
            
            if expected != api_number:
                all_correct = False
        else:
            print(f"{seed:<6} {'ERROR':<12} {'ERROR':<10} ❌")
            all_correct = False
    
    print("-" * 40)
    if all_correct:
        print("🎉 PURE LCG IMPLEMENTATION VERIFIED")
        print("✅ Formula: X(n+1) = (a * X(n) + c) mod m is correctly implemented")
        print("✅ Parameters a=1664525, c=1013904223, m=2^32 are correct")
        print("✅ Manual calculations match API results perfectly")
        print("✅ The clustering of small seeds around number 2 is mathematically expected")
        return True
    else:
        print("❌ Implementation issues found")
        return False

if __name__ == "__main__":
    success = final_verification()
    exit(0 if success else 1)