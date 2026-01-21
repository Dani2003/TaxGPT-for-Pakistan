from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict
from app.db.session import get_db
from app.db.models import User, WealthStatement
from app.api.auth import get_current_active_user

router = APIRouter()

class WealthInput(BaseModel):
    tax_year: int
    properties: List[Dict] = []
    vehicles: List[Dict] = []
    bank_accounts: List[Dict] = []
    investments: List[Dict] = []
    gold_silver: float = 0
    cash_in_hand: float = 0
    other_assets: List[Dict] = []
    loans: List[Dict] = []
    credit_cards: float = 0
    other_liabilities: List[Dict] = []

@router.post("/")
def create_wealth_statement(
    wealth_data: WealthInput,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Calculate totals
    total_assets = (
        sum([p.get('value', 0) for p in wealth_data.properties]) +
        sum([v.get('value', 0) for v in wealth_data.vehicles]) +
        sum([a.get('balance', 0) for a in wealth_data.bank_accounts]) +
        sum([i.get('value', 0) for i in wealth_data.investments]) +
        wealth_data.gold_silver +
        wealth_data.cash_in_hand +
        sum([a.get('value', 0) for a in wealth_data.other_assets])
    )
    
    total_liabilities = (
        sum([l.get('amount', 0) for l in wealth_data.loans]) +
        wealth_data.credit_cards +
        sum([l.get('amount', 0) for l in wealth_data.other_liabilities])
    )
    
    net_wealth = total_assets - total_liabilities
    
    wealth_statement = WealthStatement(
        user_id=current_user.id,
        tax_year=wealth_data.tax_year,
        properties=wealth_data.properties,
        vehicles=wealth_data.vehicles,
        bank_accounts=wealth_data.bank_accounts,
        investments=wealth_data.investments,
        gold_silver=wealth_data.gold_silver,
        cash_in_hand=wealth_data.cash_in_hand,
        other_assets=wealth_data.other_assets,
        loans=wealth_data.loans,
        credit_cards=wealth_data.credit_cards,
        other_liabilities=wealth_data.other_liabilities,
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        net_wealth=net_wealth
    )
    
    db.add(wealth_statement)
    db.commit()
    db.refresh(wealth_statement)
    
    return {
        "message": "Wealth statement created successfully",
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "net_wealth": net_wealth
    }

@router.get("/{tax_year}")
def get_wealth_statement(
    tax_year: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    statement = db.query(WealthStatement).filter(
        WealthStatement.user_id == current_user.id,
        WealthStatement.tax_year == tax_year
    ).first()
    
    if not statement:
        raise HTTPException(status_code=404, detail="Wealth statement not found")
    
    return statement
