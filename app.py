"""
GrabCredit BNPL Engine — FastAPI Server
=======================================
MCP-compliant credit decisioning API for GrabOn BNPL checkout.

Endpoints:
  GET  /            → health check
  GET  /personas    → list all test personas
  POST /evaluate-credit → evaluate a persona and return full BNPL decision
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

import json
import os

from services.scoring import calculate_credit_score, make_decision
from services.narrative import generate_narrative, generate_reason_codes


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="GrabCredit BNPL Engine",
    description="MCP-compliant credit decisioning server for GrabOn BNPL",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PERSONAS_PATH = os.path.join(os.path.dirname(__file__), "data", "personas.json")


# ---------------------------------------------------------------------------
# Request schema
# ---------------------------------------------------------------------------

class PersonaInput(BaseModel):
    id: str
    name: str
    monthly_income: float
    transaction_count: int
    repayment_ratio: float
    total_gmv: float = 0
    categories_used: List[str] = []
    return_rate: float = 0
    account_age_days: int = 0
    existing_liabilities: float = 0
    coupon_redemption_rate: float = 0
    payment_modes: List[str] = []


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def health():
    return {
        "status": "running",
        "service": "GrabCredit BNPL Engine",
        "version": "2.0.0",
    }


@app.get("/personas")
def get_personas():
    """Return all available test personas."""
    with open(PERSONAS_PATH) as f:
        return json.load(f)


@app.post("/evaluate-credit")
def evaluate_credit(persona: PersonaInput):
    """
    MCP-compliant credit evaluation endpoint.

    Accepts user persona data (JSON) and returns a structured decision
    including score breakdown, reason codes, EMI plans, and a
    personalized narrative.
    """
    persona_dict = persona.dict()

    # 1. Calculate credit score with full breakdown
    score, breakdown = calculate_credit_score(persona_dict)

    # 2. Make approval decision with EMI terms
    decision = make_decision(score, persona_dict)

    # 3. Generate structured reason codes
    reason_codes = generate_reason_codes(breakdown, persona_dict)

    # 4. Generate personalized narrative
    narrative = generate_narrative(persona_dict, score, breakdown, decision)

    # 5. Return complete decision payload
    return {
        "user_id": persona.id,
        "user_name": persona.name,
        "score": score,
        "status": decision["status"],
        "credit_limit": decision["credit_limit"],
        "interest_rate": decision["interest_rate"],
        "emi_plans": decision["emi_plans"],
        "breakdown": breakdown,
        "reason_codes": reason_codes,
        "narrative": narrative,
    }