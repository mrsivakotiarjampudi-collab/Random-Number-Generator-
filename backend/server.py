from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from typing import Optional

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LCG Parameters (Numerical Recipes)
LCG_A = 1664525  # Multiplier
LCG_C = 1013904223  # Increment
LCG_M = 2**32  # Modulus

class RandomNumberResponse(BaseModel):
    number: int
    category: str
    seed_used: int

def generate_lcg_number(seed: int) -> int:
    """
    Generate a random number using Linear Congruential Generator
    Pure LCG Formula: X(n+1) = (a * X(n) + c) mod m
    
    Using standard LCG parameters from Numerical Recipes
    """
    # Pure LCG formula - no seed preprocessing
    result = (LCG_A * seed + LCG_C) % LCG_M
    
    return result

def map_to_range(value: int, min_val: int, max_val: int) -> int:
    """
    Map LCG output to desired range [min_val, max_val]
    """
    # Normalize to [0, 1)
    normalized = value / LCG_M
    # Scale to [min_val, max_val + 1)
    scaled = int(normalized * (max_val - min_val + 1)) + min_val
    return scaled

def categorize_number(number: int) -> str:
    """
    Categorize number as 'Small' (0-4) or 'Big' (5-9)
    """
    if 0 <= number <= 4:
        return "Small"
    elif 5 <= number <= 9:
        return "Big"
    else:
        return "Unknown"

@app.get("/")
async def root():
    return {
        "message": "Random Number Generator API with LCG",
        "endpoints": [
            "/api/generate-random - Generate random number (0-9)"
        ]
    }

class GenerateRequest(BaseModel):
    seed: Optional[int] = None

@app.post("/api/generate-random", response_model=RandomNumberResponse)
async def generate_random(request: GenerateRequest = GenerateRequest()):
    """
    Generate a random number between 0-9 using Linear Congruential Generator
    Can accept optional seed value, otherwise auto-generates from timestamp
    """
    try:
        # Use provided seed or auto-generate from timestamp
        if request.seed is not None:
            seed = request.seed % LCG_M
        else:
            # Auto-generate seed from current timestamp (nanosecond precision)
            seed = int(time.time() * 1000000) % LCG_M
        
        # Generate random number using LCG
        lcg_output = generate_lcg_number(seed)
        
        # Map to range 0-9
        random_number = map_to_range(lcg_output, 0, 9)
        
        # Categorize the number
        category = categorize_number(random_number)
        
        return RandomNumberResponse(
            number=random_number,
            category=category,
            seed_used=seed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating random number: {str(e)}")

@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "Random Number Generator"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)