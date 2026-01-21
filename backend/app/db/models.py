from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    cnic = Column(String, unique=True)
    phone_number = Column(String)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    tax_calculations = relationship("TaxCalculation", back_populates="user", cascade="all, delete-orphan")
    wealth_statements = relationship("WealthStatement", back_populates="user", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    original_filename = Column(String)
    file_size_kb = Column(Integer)
    upload_date = Column(DateTime, default=datetime.utcnow)
    processing_status = Column(String, default="uploaded")
    ocr_confidence = Column(Float)
    error_message = Column(Text)
    
    user = relationship("User", back_populates="documents")
    extracted_data = relationship("ExtractedData", back_populates="document", cascade="all, delete-orphan")

class ExtractedData(Base):
    __tablename__ = "extracted_data"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    field_name = Column(String, nullable=False)
    field_value = Column(Text)
    confidence_score = Column(Float)
    is_validated = Column(Boolean, default=False)
    user_edited = Column(Boolean, default=False)
    extracted_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="extracted_data")

class TaxCalculation(Base):
    __tablename__ = "tax_calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tax_year = Column(Integer, nullable=False)
    total_income = Column(Float, default=0)
    salary_income = Column(Float, default=0)
    business_income = Column(Float, default=0)
    other_income = Column(Float, default=0)
    total_deductions = Column(Float, default=0)
    taxable_income = Column(Float, default=0)
    tax_liability = Column(Float, default=0)
    calculation_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="draft")
    
    user = relationship("User", back_populates="tax_calculations")
    tax_form = relationship("TaxReturnForm", back_populates="calculation", uselist=False, cascade="all, delete-orphan")

class TaxReturnForm(Base):
    __tablename__ = "tax_return_forms"
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_id = Column(Integer, ForeignKey("tax_calculations.id"), nullable=False, unique=True)
    pdf_file_path = Column(String)
    generation_date = Column(DateTime, default=datetime.utcnow)
    download_count = Column(Integer, default=0)
    
    calculation = relationship("TaxCalculation", back_populates="tax_form")

class WealthStatement(Base):
    __tablename__ = "wealth_statements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tax_year = Column(Integer, nullable=False)
    
    # Assets
    properties = Column(JSON, default=list)
    vehicles = Column(JSON, default=list)
    bank_accounts = Column(JSON, default=list)
    investments = Column(JSON, default=list)
    gold_silver = Column(Float, default=0)
    cash_in_hand = Column(Float, default=0)
    other_assets = Column(JSON, default=list)
    
    # Liabilities
    loans = Column(JSON, default=list)
    credit_cards = Column(Float, default=0)
    other_liabilities = Column(JSON, default=list)
    
    # Totals
    total_assets = Column(Float, default=0)
    total_liabilities = Column(Float, default=0)
    net_wealth = Column(Float, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="wealth_statements")
