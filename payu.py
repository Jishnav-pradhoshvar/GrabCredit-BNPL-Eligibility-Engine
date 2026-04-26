"""
PayU LazyPay Sandbox API — Mock Service
=======================================
Simulates the PayU LazyPay disbursal flow. 
In a real production environment, the generate_emi_plans function 
would perform an HTTPS POST request to PayU's sandbox endpoints.
"""

def generate_payu_emi_plans(credit_limit: float, interest_rate: float) -> list:
    """
    Mock implementation of PayU LazyPay 'get_emi_offers' endpoint.
    Calculates 3/6/9 month plans based on approved credit limit and interest.
    """
    if credit_limit <= 0:
        return []

    plans = []
    for months in [3, 6, 9]:
        monthly_rate = interest_rate / 100 / 12
        
        if monthly_rate > 0:
            # Standard Actuarial EMI Formula: E = P * r * (1+r)^n / ((1+r)^n - 1)
            emi = (
                credit_limit 
                * monthly_rate 
                * (1 + monthly_rate) ** months 
                / ((1 + monthly_rate) ** months - 1)
            )
        else:
            # 0% Interest Case
            emi = credit_limit / months

        plans.append({
            "months": months,
            "emi_amount": round(emi),
            "total_cost": round(emi * months),
            "interest_rate": interest_rate,
            "provider": "PayU LazyPay" # Marking the provider
        })

    return plans
