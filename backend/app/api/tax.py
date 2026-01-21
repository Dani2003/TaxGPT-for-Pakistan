from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict
from app.db.session import get_db
from app.db.models import User, TaxCalculation, TaxReturnForm
from app.api.auth import get_current_active_user
from app.services.tax_engine import calculate_income_tax, apply_deductions
from app.services.ai_service import ask_tax_question

router = APIRouter()

class TaxInput(BaseModel):
    salary_income: float = 0
    business_income: float = 0
    other_income: float = 0
    deductions: float = 0

class TaxResult(BaseModel):
    total_income: float
    total_deductions: float
    taxable_income: float
    tax_liability: float
    breakdown: List[Dict]
    
class ChatMessage(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []

@router.post("/calculate", response_model=TaxResult)
def calculate_tax(
    tax_input: TaxInput,
    tax_year: int = 2026,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    total_income = tax_input.salary_income + tax_input.business_income + tax_input.other_income
    total_deductions = apply_deductions(tax_input.deductions)
    taxable_income = max(0, total_income - total_deductions)
    tax_liability, breakdown = calculate_income_tax(taxable_income)
    
    calculation = TaxCalculation(
        user_id=current_user.id,
        tax_year=tax_year,
        total_income=total_income,
        salary_income=tax_input.salary_income,
        business_income=tax_input.business_income,
        other_income=tax_input.other_income,
        total_deductions=total_deductions,
        taxable_income=taxable_income,
        tax_liability=tax_liability,
        status="completed"
    )
    
    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    
    return {
        "total_income": total_income,
        "total_deductions": total_deductions,
        "taxable_income": taxable_income,
        "tax_liability": tax_liability,
        "breakdown": breakdown
    }

@router.get("/history")
def get_tax_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    calculations = db.query(TaxCalculation).filter(
        TaxCalculation.user_id == current_user.id
    ).order_by(TaxCalculation.calculation_date.desc()).all()
    
    return calculations

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    message: ChatMessage,
    current_user: User = Depends(get_current_active_user)
):
    try:
        answer = await ask_tax_question(message.question)
        return {
            "answer": answer,
            "sources": ["FBR Tax Rules 2025-26", "AI Analysis"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@router.get("/slabs")
def get_tax_slabs():
    from app.core.config import TAX_SLABS
    return {
        "tax_year": "2025-26",
        "slabs": TAX_SLABS["slabs"],
        "note": "Tax rates as per Federal Board of Revenue (FBR)"
    }

@router.post("/generate-form/{calculation_id}")
def generate_tax_form(
    calculation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    calculation = db.query(TaxCalculation).filter(
        TaxCalculation.id == calculation_id,
        TaxCalculation.user_id == current_user.id
    ).first()
    
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    form = TaxReturnForm(
        calculation_id=calculation_id,
        pdf_file_path=f"forms/tax_return_{calculation_id}.pdf"
    )
    
    db.add(form)
    db.commit()
    db.refresh(form)
    
    return {
        "message": "Tax form generated successfully",
        "form_id": form.id,
        "download_url": f"/api/tax/download-form/{form.id}"
    }
