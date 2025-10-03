from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/today")
def today():
    return {
        "seed_fund": {"amount": 100, "next_goal": 500},
        "treasury": {"ops": 12, "cloud_ai": 4, "upgrade": 60, "emergency": 25},
        "security": {"grade": "B+", "score": 86},
        "proposal": "Try FlipSim beta with a TikTok short to attract users."
    }
