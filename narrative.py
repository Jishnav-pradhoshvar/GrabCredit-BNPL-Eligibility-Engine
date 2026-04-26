"""
GrabCredit Narrative Engine v2.0
================================
Generates personalized, data-driven credit decision narratives.
Fully deterministic — no external API dependency.

Every narrative:
  • Starts with "You qualify because…" or "We're unable to approve…"
  • Cites 2-3 specific behavioural signals
  • Is unique to each persona's actual data
"""


# ---------------------------------------------------------------------------
# Narrative generator
# ---------------------------------------------------------------------------

def generate_narrative(
    persona: dict,
    score: int,
    breakdown: dict,
    decision: dict,
) -> str:
    """Build a human-readable eligibility narrative from raw scoring data."""

    name = persona.get("name", "User")
    first_name = name.split()[0]
    status = decision["status"]
    txn_count = persona.get("transaction_count", 0)
    repayment = persona.get("repayment_ratio", 0)
    income = persona.get("monthly_income", 0)
    age_days = persona.get("account_age_days", 0)
    return_rate = persona.get("return_rate", 0)
    categories = persona.get("categories_used", [])
    credit_limit = decision.get("credit_limit", 0)
    interest_rate = decision.get("interest_rate", 0)

    # ── APPROVED ──────────────────────────────────────────────────────────
    if status == "APPROVED":
        positives = []
        if breakdown.get("repayment", {}).get("score", 0) >= 25:
            positives.append(
                f"your excellent repayment consistency of {round(repayment * 100)}%"
            )
        if breakdown.get("frequency", {}).get("score", 0) >= 15:
            positives.append(
                f"a strong transaction footprint of {txn_count} purchases"
            )
        if breakdown.get("income", {}).get("score", 0) >= 15:
            positives.append(f"a stable income profile of ₹{income:,}/month")
        if breakdown.get("maturity", {}).get("score", 0) >= 12:
            positives.append(
                f"a well-established account history of {round(age_days / 30)} months"
            )

        if len(positives) >= 3:
            factors = f"{positives[0]}, {positives[1]}, and {positives[2]}"
        elif len(positives) == 2:
            factors = f"{positives[0]} and {positives[1]}"
        elif positives:
            factors = positives[0]
        else:
            factors = "your overall creditworthiness"

        narrative = (
            f"Great news, {first_name}! You qualify because of {factors}. "
            f"With a GrabCredit score of {score}/100, you have access to a "
            f"₹{credit_limit:,} credit line"
        )
        narrative += " at 0% interest." if interest_rate == 0 else f" at {interest_rate}% p.a."

        if len(categories) >= 4:
            narrative += (
                f" Your consistent spending across {len(categories)} categories"
                f" further validates your financial reliability."
            )
        narrative += " Keep up the excellent financial behavior!"

    # ── PARTIALLY APPROVED ────────────────────────────────────────────────
    elif status == "PARTIALLY_APPROVED":
        strengths = []
        improvements = []

        if breakdown.get("repayment", {}).get("score", 0) >= 20:
            strengths.append(f"your {round(repayment * 100)}% repayment rate")
        elif txn_count > 0:
            improvements.append("improving your repayment consistency")

        if breakdown.get("frequency", {}).get("score", 0) >= 12:
            strengths.append("regular transaction activity")
        else:
            improvements.append("increasing your purchase frequency")

        if breakdown.get("income", {}).get("score", 0) >= 10:
            strengths.append("income stability")

        if breakdown.get("maturity", {}).get("score", 0) < 12:
            improvements.append("maintaining your account for a longer period")

        if return_rate > 0.08:
            improvements.append("reducing your product return rate")

        if len(categories) < 5 and txn_count > 0:
            improvements.append(
                f"diversifying your spending beyond {len(categories)} categories"
            )

        if persona.get("existing_liabilities", 0) > 10_000:
            improvements.append("reducing existing liabilities")

        strength_text = (
            " and ".join(strengths[:2]) if strengths else "your account standing"
        )
        improve_text = (
            " and ".join(improvements[:2])
            if improvements
            else "continued platform engagement"
        )

        narrative = (
            f"{first_name}, you've been partially approved for Buy Now, Pay Later. "
            f"We recognize {strength_text} as positive signals in your profile. "
            f"Your current GrabCredit score of {score}/100 qualifies you for a reduced "
            f"credit line of ₹{credit_limit:,}"
        )
        if interest_rate > 0:
            narrative += f" at {interest_rate}% p.a."
        narrative += f". To unlock the full amount, focus on {improve_text}. "
        narrative += "We'll automatically reassess your profile in 30 days."

    # ── REJECTED ──────────────────────────────────────────────────────────
    else:
        reasons = []
        suggestions = []

        if txn_count == 0:
            reasons.append(
                "you have no prior transaction history on our platform"
            )
            suggestions.append(
                "completing a few purchases to establish your profile"
            )

        if age_days < 7:
            reasons.append(
                f"your account was created only {age_days} days ago "
                f"(minimum 7 days required)"
            )
            suggestions.append("waiting at least 7 days after registration")

        if 0 < repayment < 0.8:
            reasons.append(
                f"your repayment ratio of {round(repayment * 100)}% "
                f"is below our 80% minimum threshold"
            )
            suggestions.append(
                "clearing outstanding dues and maintaining on-time payments"
            )

        if return_rate > 0.15:
            reasons.append(
                f"your product return rate of {round(return_rate * 100)}% "
                f"signals elevated risk"
            )
            suggestions.append(
                "reducing return frequency to demonstrate purchase intent"
            )

        if not reasons:
            reasons.append(
                "insufficient credit signals across key assessment factors"
            )
            suggestions.append("building your transaction history")

        if len(reasons) > 1:
            reason_text = reasons[0] + "; additionally, " + reasons[1]
        else:
            reason_text = reasons[0]

        suggestion_text = " and ".join(suggestions[:2])

        narrative = (
            f"{first_name}, we're unable to approve Buy Now, Pay Later at this "
            f"time because {reason_text}. "
            f"Your current GrabCredit score is {score}/100. "
            f"To improve your eligibility, we recommend {suggestion_text}. "
            f"Your profile is continuously monitored and will be reassessed "
            f"as new data becomes available."
        )

    return narrative


# ---------------------------------------------------------------------------
# Reason codes
# ---------------------------------------------------------------------------

def generate_reason_codes(breakdown: dict, persona: dict) -> list:
    """Generate structured reason codes that map score factors → explanations."""

    codes = []
    income = persona.get("monthly_income", 0)
    txn_count = persona.get("transaction_count", 0)
    repayment = persona.get("repayment_ratio", 0)
    age_days = persona.get("account_age_days", 0)
    return_rate = persona.get("return_rate", 0)
    categories = persona.get("categories_used", [])

    # Income
    inc_score = breakdown.get("income", {}).get("score", 0)
    if inc_score >= 15:
        codes.append({
            "type": "positive",
            "factor": "Income",
            "text": f"Strong income adequacy (₹{income:,}/month)",
        })
    elif inc_score >= 8:
        codes.append({
            "type": "neutral",
            "factor": "Income",
            "text": f"Moderate income (₹{income:,}/month)",
        })
    else:
        codes.append({
            "type": "negative",
            "factor": "Income",
            "text": f"Below-baseline income (₹{income:,}/month)",
        })

    # Transaction frequency
    if txn_count >= 100:
        codes.append({
            "type": "positive",
            "factor": "Activity",
            "text": f"High platform engagement ({txn_count} transactions)",
        })
    elif txn_count >= 30:
        codes.append({
            "type": "neutral",
            "factor": "Activity",
            "text": f"Moderate activity ({txn_count} transactions)",
        })
    elif txn_count > 0:
        codes.append({
            "type": "negative",
            "factor": "Activity",
            "text": f"Low activity ({txn_count} transactions)",
        })
    else:
        codes.append({
            "type": "negative",
            "factor": "Activity",
            "text": "No transaction history available",
        })

    # Repayment
    if txn_count == 0:
        codes.append({
            "type": "negative",
            "factor": "Repayment",
            "text": "No repayment data — cannot assess reliability",
        })
    elif repayment >= 0.95:
        codes.append({
            "type": "positive",
            "factor": "Repayment",
            "text": f"Excellent repayment consistency ({round(repayment * 100)}%)",
        })
    elif repayment >= 0.85:
        codes.append({
            "type": "neutral",
            "factor": "Repayment",
            "text": f"Fair repayment rate ({round(repayment * 100)}%)",
        })
    else:
        codes.append({
            "type": "negative",
            "factor": "Repayment",
            "text": f"Below-threshold repayment ({round(repayment * 100)}%)",
        })

    # Account maturity
    if age_days >= 365:
        codes.append({
            "type": "positive",
            "factor": "Maturity",
            "text": f"Established account ({round(age_days / 30)} months)",
        })
    elif age_days >= 90:
        codes.append({
            "type": "neutral",
            "factor": "Maturity",
            "text": f"Growing account ({round(age_days / 30)} months)",
        })
    elif age_days >= 7:
        codes.append({
            "type": "negative",
            "factor": "Maturity",
            "text": f"New account ({age_days} days)",
        })
    else:
        codes.append({
            "type": "negative",
            "factor": "Maturity",
            "text": f"⚠ Velocity risk — account is only {age_days} days old",
        })

    # Category diversity
    if len(categories) >= 4:
        codes.append({
            "type": "positive",
            "factor": "Diversity",
            "text": f"Diversified spending ({len(categories)} categories)",
        })
    elif len(categories) >= 2:
        codes.append({
            "type": "neutral",
            "factor": "Diversity",
            "text": f"Limited category spread ({len(categories)} categories)",
        })
    elif txn_count > 0:
        codes.append({
            "type": "negative",
            "factor": "Diversity",
            "text": "Narrow spending pattern",
        })

    # Return rate
    if return_rate > 0.15:
        codes.append({
            "type": "negative",
            "factor": "Returns",
            "text": f"High return rate ({round(return_rate * 100)}%)",
        })
    elif return_rate > 0.05 and txn_count > 0:
        codes.append({
            "type": "neutral",
            "factor": "Returns",
            "text": f"Moderate returns ({round(return_rate * 100)}%)",
        })
    elif txn_count > 10:
        codes.append({
            "type": "positive",
            "factor": "Returns",
            "text": f"Low return rate ({round(return_rate * 100)}%)",
        })

    return codes