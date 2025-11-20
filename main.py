import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegistrationIn(BaseModel):
    team: str = Field(..., min_length=2, max_length=64)
    institution: str = Field(..., min_length=2, max_length=128)
    email: EmailStr
    members: List[str] = []


class TeamScore(BaseModel):
    id: str
    team: str
    score: int


# Mock in-memory stores (simple demo). In production connect MongoDB.
TEAMS: List[TeamScore] = [
    TeamScore(id="t1", team="Vector Vipers", score=92),
    TeamScore(id="t2", team="Quantum Crew", score=88),
    TeamScore(id="t3", team="Servo Saints", score=80),
    TeamScore(id="t4", team="Neon Navigators", score=75),
    TeamScore(id="t5", team="Circuit Cartel", score=70),
]


@app.get("/")
def read_root():
    return {"message": "ROBO-HEIST backend running"}


@app.get("/api/leaderboard")
def leaderboard():
    sorted_teams = sorted(TEAMS, key=lambda t: t.score, reverse=True)
    return {"teams": [t.dict() for t in sorted_teams]}


@app.post("/api/register")
def register_team(payload: RegistrationIn):
    # Very light mock validation/creation
    if any(t.team.lower() == payload.team.lower() for t in TEAMS):
        raise HTTPException(status_code=400, detail="Team name already registered")
    new = TeamScore(id=f"t{len(TEAMS)+1}", team=payload.team, score=random.randint(50, 95))
    TEAMS.append(new)
    return {"ok": True, "team": new.dict()}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "🧪 Mock (in-memory)",
    }
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
