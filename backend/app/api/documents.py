from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import shutil
import os
from datetime import datetime
from app.db.session import get_db
from app.db.models import User, Document, ExtractedData
from app.api.auth import get_current_active_user
from app.services.ocr_service import extract_text_from_pdf
from app.core.config import settings

router = APIRouter()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

class DocumentResponse(BaseModel):
    id: int
    document_type: str
    original_filename: str
    upload_date: datetime
    processing_status: str
    ocr_confidence: float | None
    
    class Config:
        from_attributes = True

class ExtractedDataResponse(BaseModel):
    field_name: str
    field_value: str
    confidence_score: float | None
    
    class Config:
        from_attributes = True

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "bank_statement",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(('.pdf', '.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Only PDF and image files allowed")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{current_user.id}_{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_size = os.path.getsize(file_path) // 1024
    
    document = Document(
        user_id=current_user.id,
        document_type=document_type,
        file_path=file_path,
        original_filename=file.filename,
        file_size_kb=file_size,
        processing_status="uploaded"
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    try:
        document.processing_status = "processing"
        db.commit()
        
        extracted_text = extract_text_from_pdf(file_path)
        
        extracted_field = ExtractedData(
            document_id=document.id,
            field_name="raw_text",
            field_value=extracted_text[:5000],
            confidence_score=0.85,
            is_validated=False
        )
        
        db.add(extracted_field)
        document.processing_status = "completed"
        document.ocr_confidence = 0.85
        db.commit()
        db.refresh(document)
        
    except Exception as e:
        document.processing_status = "error"
        document.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")
    
    return document

@router.get("/", response_model=List[DocumentResponse])
def list_documents(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return documents

@router.get("/{document_id}/data", response_model=List[ExtractedDataResponse])
def get_extracted_data(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    extracted_data = db.query(ExtractedData).filter(ExtractedData.document_id == document_id).all()
    return extracted_data

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    db.delete(document)
    db.commit()
    
    return None
