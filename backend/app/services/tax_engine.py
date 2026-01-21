from typing import List, Dict, Tuple
from app.core.config import TAX_SLABS

def calculate_income_tax(taxable_income: float) -> Tuple[float, List[Dict]]:
    slabs = TAX_SLABS["slabs"]
    total_tax = 0
    breakdown = []
    remaining_income = taxable_income
    
    for slab in slabs:
        if remaining_income <= 0:
            break
        
        slab_min = slab["min"]
        slab_max = slab["max"]
        slab_rate = slab["rate"]
        fixed_tax = slab["fixed"]
        
        # Handle last slab (no upper limit)
        if slab_max == 999999999:
            taxable_in_slab = remaining_income
        elif remaining_income + slab_min <= slab_max:
            taxable_in_slab = remaining_income
        else:
            taxable_in_slab = slab_max - slab_min + 1
        
        slab_tax = fixed_tax + (taxable_in_slab * slab_rate)
        total_tax = slab_tax
        
        max_display = "Above" if slab_max == 999999999 else format_currency(slab_max)
        
        breakdown.append({
            "slab": f"{format_currency(slab_min)} - {max_display}",
            "rate": f"{slab_rate * 100}%",
            "taxable_amount": round(taxable_in_slab, 2),
            "tax_in_slab": round(slab_tax, 2)
        })
        
        remaining_income -= taxable_in_slab
    
    return round(total_tax, 2), breakdown

def apply_deductions(deductions_amount: float) -> float:
    return round(deductions_amount, 2)

def calculate_tax_for_salaried_individual(
    annual_salary: float,
    other_income: float = 0,
    deductions: float = 0
) -> Dict:
    total_income = annual_salary + other_income
    taxable_income = max(0, total_income - deductions)
    tax_liability, breakdown = calculate_income_tax(taxable_income)
    
    return {
        "gross_income": round(total_income, 2),
        "deductions": round(deductions, 2),
        "taxable_income": round(taxable_income, 2),
        "tax_liability": round(tax_liability, 2),
        "monthly_tax": round(tax_liability / 12, 2),
        "breakdown": breakdown
    }

def format_currency(amount: float) -> str:
    if amount >= 999999999:
        return "Above"
    return f"Rs. {amount:,.0f}"

def get_tax_saving_suggestions(income: float, current_deductions: float) -> List[str]:
    suggestions = []
    
    if income > 1200000:
        suggestions.append("Consider life insurance premiums (deductible up to Rs. 300,000)")
        suggestions.append("Donate to approved charities (deductible up to 30% of taxable income)")
    
    if income > 2400000:
        suggestions.append("Invest in approved pension funds")
        suggestions.append("Explore investment in approved savings schemes")
    
    if current_deductions < income * 0.1:
        suggestions.append("You may be eligible for additional deductions. Consult a tax expert.")
    
    return suggestions

def calculate_advance_tax(tax_liability: float, months_remaining: int = 12) -> float:
    return round(tax_liability / months_remaining, 2)
