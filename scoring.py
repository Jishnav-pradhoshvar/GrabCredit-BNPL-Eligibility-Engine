"""
GrabCredit Scoring Engine v2.0
==============================
Explainable, formula-driven credit scoring for BNPL decisioning.

Score range : 0 – 100
Factors     : Income (20), Frequency (20), Repayment (30),
              Maturity (15), Risk Adjustments (±15)

Decision thresholds:
  >= 75  → APPROVED        (full limit, 0% interest)
  45-74  → PARTIALLY_APPROVED (reduced limit, variable interest)
  < 45   → REJECTED
"""

import math
from services.payu import generate_payu_emi_plans


# ---------------------------------------------------------------------------
# Core scoring
# ---------------------------------------------------------------------------

def calculate_credit_score(persona: dict) -> tuple:
    """Return (score: int, breakdown: dict) for the given persona."""

    breakdown = {}

    # ── Factor 1: Income Adequacy (0-20 pts) ──────────────────────────────
    income = persona.get("monthly_income", 0)
    baseline = 50_000
    income_score = round(min((income / baseline) * 12, 20), 1)

    breakdown["income"] = {
        "score": income_score,
        "max": 20,
        "value": f"₹{income:,}",
        "label": "Income Adequacy",
        "detail": f"Monthly income ₹{income:,} against ₹{baseline:,} baseline",
    }

    # ── Factor 2: Transaction Frequency (0-20 pts) ────────────────────────
    txn_count = persona.get("transaction_count", 0)

    if txn_count == 0:
        freq_score = 0.0
    elif txn_count < 10:
        freq_score = round(txn_count * 1.2, 1)
    elif txn_count < 50:
        freq_score = round(10 + (txn_count - 10) * 0.25, 1)
    elif txn_count < 150:
        freq_score = round(16 + (txn_count - 50) * 0.04, 1)
    else:
        freq_score = 20.0

    freq_score = min(freq_score, 20)
    breakdown["frequency"] = {
        "score": freq_score,
        "max": 20,
        "value": str(txn_count),
        "label": "Transaction Activity",
        "detail": f"{txn_count} transactions on record",
    }

    # ── Factor 3: Repayment History (0-30 pts) — MOST IMPORTANT ───────────
    repayment = persona.get("repayment_ratio", 0)

    if txn_count == 0:
        repay_score = 0.0          # Cannot assess without data
    elif repayment >= 0.98:
        repay_score = 30.0
    elif repayment >= 0.95:
        repay_score = 26.0
    elif repayment >= 0.90:
        repay_score = 21.0
    elif repayment >= 0.80:
        repay_score = 14.0
    elif repayment >= 0.70:
        repay_score = 8.0
    else:
        repay_score = round(max(0, repayment * 8), 1)

    breakdown["repayment"] = {
        "score": repay_score,
        "max": 30,
        "value": f"{round(repayment * 100)}%",
        "label": "Repayment Consistency",
        "detail": f"{round(repayment * 100)}% on-time repayment rate",
    }

    # ── Factor 4: Account Maturity (0-15 pts) ─────────────────────────────
    age_days = persona.get("account_age_days", 0)

    if age_days < 7:
        maturity_score = -5.0      # Velocity flag
    elif age_days < 30:
        maturity_score = 2.0
    elif age_days < 90:
        maturity_score = 5.0
    elif age_days < 180:
        maturity_score = 8.0
    elif age_days < 365:
        maturity_score = 12.0
    else:
        maturity_score = 15.0

    if age_days < 365:
        months = age_days // 30
        age_text = f"{months} months" if months > 0 else f"{age_days} days"
    else:
        years = round(age_days / 365, 1)
        age_text = f"{years} years"

    breakdown["maturity"] = {
        "score": maturity_score,
        "max": 15,
        "value": age_text,
        "label": "Account Maturity",
        "detail": f"Account age: {age_text} ({age_days} days)",
    }

    # ── Factor 5: Risk Adjustments (-15 to +15 pts) ───────────────────────
    risk_score = 0.0
    risk_details = []

    # Category diversity bonus
    categories = len(persona.get("categories_used", []))
    cat_bonus = round(min(categories * 1.5, 8), 1)
    risk_score += cat_bonus
    if categories > 0:
        risk_details.append(
            f"+{cat_bonus} diversity ({categories} spending categories)"
        )

    # Return rate penalty
    return_rate = persona.get("return_rate", 0)
    if return_rate > 0.3:
        ret_pen = -10.0
    elif return_rate > 0.15:
        ret_pen = -5.0
    elif return_rate > 0.08:
        ret_pen = -2.0
    else:
        ret_pen = 0.0
    risk_score += ret_pen
    if ret_pen < 0:
        risk_details.append(
            f"{ret_pen} return rate ({round(return_rate * 100)}%)"
        )

    # Liability ratio penalty
    liability = persona.get("existing_liabilities", 0)
    if income > 0:
        liability_ratio = liability / income
        if liability_ratio > 0.5:
            liab_pen = -8.0
        elif liability_ratio > 0.3:
            liab_pen = -4.0
        elif liability_ratio > 0.15:
            liab_pen = -2.0
        else:
            liab_pen = 0.0
        risk_score += liab_pen
        if liab_pen < 0:
            risk_details.append(
                f"{liab_pen} liability ratio ({round(liability_ratio * 100)}%)"
            )

    # Coupon engagement bonus (deal redemption quality signal)
    coupon_rate = persona.get("coupon_redemption_rate", 0)
    if coupon_rate > 0.5 and txn_count > 20:
        coup_bonus = 3.0
        risk_score += coup_bonus
        risk_details.append(
            f"+{coup_bonus} deal engagement ({round(coupon_rate * 100)}% coupon use)"
        )

    breakdown["risk"] = {
        "score": round(risk_score, 1),
        "max": 15,
        "label": "Risk Assessment",
        "details": risk_details,
    }

    # ── Total ─────────────────────────────────────────────────────────────
    total = income_score + freq_score + repay_score + maturity_score + risk_score
    total = max(0, min(100, round(total)))

    return total, breakdown


# ---------------------------------------------------------------------------
# Decision engine
# ---------------------------------------------------------------------------

def make_decision(score: int, persona: dict, product_price: int = 80_000) -> dict:
    """
    Determine BNPL approval status and generate EMI plans.
    Uses proper actuarial EMI calculation:  E = P·r(1+r)^n / ((1+r)^n - 1)
    """

    if score >= 75:
        status = "APPROVED"
        credit_limit = product_price
        interest_rate = 0.0
    elif score >= 45:
        status = "PARTIALLY_APPROVED"
        factor = (score - 45) / 30            # 0.0 at 45, 1.0 at 75
        credit_limit = round(product_price * (0.3 + factor * 0.5) / 1000) * 1000
        interest_rate = round(18 - factor * 10, 1)   # 18% at 45 → 8% at ~75
    else:
        status = "REJECTED"
        credit_limit = 0
        interest_rate = 0.0

    # 3. Call PayU LazyPay Sandbox for EMI disbursal plans
    emi_plans = []
    if credit_limit > 0:
        emi_plans = generate_payu_emi_plans(credit_limit, interest_rate)

    return {
        "status": status,
        "credit_limit": credit_limit,
        "interest_rate": interest_rate,
        "emi_plans": emi_plans,
    }