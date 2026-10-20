# -*- coding: utf-8 -*-
"""Executive Compensation RSU & Equity Tax Bracket Copilot for GenPark Personal Agent."""
import json
from typing import Dict, Any

class ExecutiveCompensationRSUTaxOptimizer:
    """RSU vesting tax deficit, supplemental withholding cliff, and safe-harbor estimation engine."""

    @staticmethod
    def audit_rsu_vesting_tax_deficit(annual_base_salary_usd: float, rsu_vest_value_usd: float, statutory_withholding_rate_pct: float = 22.0, effective_marginal_tax_bracket_pct: float = 37.0, state_tax_rate_pct: float = 9.3) -> Dict[str, Any]:
        """Detect the classic tech RSU tax trap where companies only withhold 22% despite 37% marginal bracket."""
        total_income = annual_base_salary_usd + rsu_vest_value_usd
        
        # Employer statutory withholding
        employer_withheld = rsu_vest_value_usd * (statutory_withholding_rate_pct / 100.0)
        # Actual marginal obligation
        actual_federal_tax = rsu_vest_value_usd * (effective_marginal_tax_bracket_pct / 100.0)
        # State obligation
        state_tax = rsu_vest_value_usd * (state_tax_rate_pct / 100.0)
        
        # Federal shortfall
        federal_deficit = max(0.0, actual_federal_tax - employer_withheld)
        total_shortfall = federal_deficit + (state_tax * 0.40)  # state often under-withholds as well

        return {
            "total_compensation_usd": round(total_income, 2),
            "rsu_gross_vest_value_usd": round(rsu_vest_value_usd, 2),
            "employer_statutory_withheld_usd": round(employer_withheld, 2),
            "actual_federal_obligation_usd": round(actual_federal_tax, 2),
            "unanticipated_tax_deficit_usd": round(federal_deficit, 2),
            "total_estimated_tax_bill_due_april_usd": round(total_shortfall, 2),
            "risk_assessment": "HIGH_TAX_SURPRISE_RISK" if federal_deficit > 5000.0 else "MANAGED",
            "immediate_recommendation": f"Set aside ${federal_deficit:,.2f} in high-yield cash immediately or submit IRS Form W-4 to increase extra withholding."
        }

    @staticmethod
    def synthesize_quarterly_estimated_tax_plan(total_tax_underwithheld_usd: float, prior_year_total_tax_liability_usd: float, current_projected_liability_usd: float) -> Dict[str, Any]:
        """Compute safe harbor payment threshold (110% of prior year for AGI > $150k) to prevent penalty."""
        safe_harbor_target = prior_year_total_tax_liability_usd * 1.10
        quarterly_payment = round(total_tax_underwithheld_usd / 4.0, 2)

        return {
            "irc_safe_harbor_target_usd": round(safe_harbor_target, 2),
            "total_underwithheld_usd": round(total_tax_underwithheld_usd, 2),
            "quarterly_1040es_payment_usd": quarterly_payment,
            "payment_calendar": [
                {"quarter": "Q1 (April 15)", "amount_usd": quarterly_payment},
                {"quarter": "Q2 (June 15)", "amount_usd": quarterly_payment},
                {"quarter": "Q3 (September 15)", "amount_usd": quarterly_payment},
                {"quarter": "Q4 (January 15)", "amount_usd": quarterly_payment}
            ],
            "penalty_avoidance_note": "Paying via EFTPS avoids IRC Section 6654 underpayment interest penalties."
        }
