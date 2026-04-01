#!/usr/bin/env python3
"""
Detailed LCG Analysis - Investigating the distribution issue
"""

import requests
import json

# Backend URL from environment
BACKEND_URL = "https://lcg-random-gen.preview.emergentagent.com/api"

# LCG Parameters (same as in backend)
LCG_A = 1664525  # Multiplier
LCG_C = 1013904223  # Increment
LCG_M = 2**32  # Modulus (4294967296)

def manual_lcg_calculation(seed: int) -> int:
    """Manual calculation of Pure LCG Formula"""
    return (LCG_A * seed + LCG_C) % LCG_M

def map_to_range_manual(value: int, min_val: int, max_val: int) -> int:
    """Manual mapping of LCG output to range [0, 9]"""
    normalized = value / LCG_M
    scaled = int(normalized * (max_val - min_val + 1)) + min_val
    return scaled

def analyze_lcg_distribution():
    """Analyze LCG output and mapping for first 20 seeds"""
    print("🔍 Detailed LCG Analysis - First 20 Seeds")
    print("=" * 80)
    print(f"LCG Parameters: a={LCG_A}, c={LCG_C}, m={LCG_M}")
    print("Formula: X(n+1) = (a * X(n) + c) mod m")
    print("=" * 80)
    
    print(f"{'Seed':<6} {'LCG Output':<12} {'Normalized':<12} {'Mapped':<6} {'API':<6} {'Match':<6}")
    print("-" * 80)
    
    for seed in range(0, 20):
        try:
            # Manual calculation
            lcg_output = manual_lcg_calculation(seed)
            normalized = lcg_output / LCG_M
            mapped = map_to_range_manual(lcg_output, 0, 9)
            
            # API call
            payload = {"seed": seed}
            response = requests.post(f"{BACKEND_URL}/generate-random", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                api_number = data.get("number")
                match = "✅" if mapped == api_number else "❌"
                
                print(f"{seed:<6} {lcg_output:<12} {normalized:<12.6f} {mapped:<6} {api_number:<6} {match:<6}")
            else:
                print(f"{seed:<6} {'ERROR':<12} {'ERROR':<12} {'ERROR':<6} {'ERROR':<6} {'❌':<6}")
                
        except Exception as e:
            print(f"{seed:<6} {'ERROR':<12} {'ERROR':<12} {'ERROR':<6} {'ERROR':<6} {'❌':<6}")
    
    print("-" * 80)

def test_larger_seeds():
    """Test larger seeds to see if distribution improves"""
    print("\n🔍 Testing Larger Seeds for Better Distribution")
    print("=" * 60)
    
    large_seeds = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    
    for seed in large_seeds:
        try:
            # Manual calculation
            lcg_output = manual_lcg_calculation(seed)
            mapped = map_to_range_manual(lcg_output, 0, 9)
            
            # API call
            payload = {"seed": seed}
            response = requests.post(f"{BACKEND_URL}/generate-random", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                api_number = data.get("number")
                category = data.get("category")
                
                print(f"Seed {seed:7d}: LCG={lcg_output:10d} → Manual={mapped}, API={api_number} ({category})")
            else:
                print(f"Seed {seed:7d}: API ERROR")
                
        except Exception as e:
            print(f"Seed {seed:7d}: ERROR - {str(e)}")

def test_mathematical_properties():
    """Test mathematical properties of the LCG"""
    print("\n🔍 Mathematical Properties Analysis")
    print("=" * 50)
    
    # Test the LCG period and distribution
    print("Testing LCG mathematical properties:")
    
    # Check if the issue is with small seeds clustering
    seeds_to_test = [0, 1, 2, 3, 4, 5, 10, 100, 1000, 10000]
    
    for seed in seeds_to_test:
        lcg_output = manual_lcg_calculation(seed)
        normalized = lcg_output / LCG_M
        mapped = map_to_range_manual(lcg_output, 0, 9)
        
        print(f"Seed {seed:5d}: LCG={lcg_output:10d}, Norm={normalized:.6f}, Mapped={mapped}")
    
    # Check the increment effect
    print(f"\nLCG Increment (c): {LCG_C}")
    print(f"LCG Increment normalized: {LCG_C / LCG_M:.6f}")
    print(f"LCG Increment mapped to 0-9: {map_to_range_manual(LCG_C, 0, 9)}")

if __name__ == "__main__":
    analyze_lcg_distribution()
    test_larger_seeds()
    test_mathematical_properties()