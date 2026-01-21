#  Tax Filing Automation System for Pakistan

AI-powered tax filing system using RAG, OCR, and FBR tax rules automation.

##  Features

-  **User Authentication** - Secure JWT-based auth
-  **Tax Calculator** - Automatic FBR tax slab calculations
-  **Document OCR** - Extract data from bank statements
-  **AI Chatbot with RAG** - Tax advice using retrieval-augmented generation
-  **Wealth Statement** - Comprehensive asset & liability tracking
-  **PostgreSQL Database** - Production-ready persistence

##  Tech Stack

**Backend:**
- FastAPI
- PostgreSQL
- SQLAlchemy
- PyPDF2 & Tesseract OCR
- scikit-learn (TF-IDF RAG)
- Groq AI (Llama 3.3)

**Frontend:** (Coming in Phase 2)
- React.js + TypeScript
- Tailwind CSS

##  Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 16+

### Setup

1. Clone repository:
\\\ash
git clone https://github.com/Dani2003/tax-automation-pk.git
cd tax-automation-pk/backend
\\\

2. Create virtual environment:
\\\ash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
\\\

3. Install dependencies:
\\\ash
pip install -r requirements.txt
\\\

4. Setup PostgreSQL:
\\\ash
createdb tax_automation_db
\\\

5. Configure environment:
\\\ash
cp .env.example .env
# Edit .env with your credentials
\\\

6. Initialize database:
\\\ash
python init_db.py
\\\

7. Run server:
\\\ash
uvicorn app.main:app --reload
\\\

8. Access API docs:
\\\
http://localhost:8000/docs
\\\

##  API Endpoints

### Authentication
- \POST /api/auth/register\ - Register new user
- \POST /api/auth/login\ - Login & get JWT token
- \GET /api/auth/me\ - Get current user

### Tax Calculation
- \POST /api/tax/calculate\ - Calculate tax liability
- \GET /api/tax/history\ - Get calculation history
- \POST /api/tax/chat\ - Ask AI tax questions
- \GET /api/tax/slabs\ - Get current tax slabs

### Documents
- \POST /api/documents/upload\ - Upload & process docs
- \GET /api/documents/\ - List user documents
- \GET /api/documents/{id}/data\ - Get extracted data

### Wealth Statement
- \POST /api/wealth/\ - Create wealth statement
- \GET /api/wealth/{tax_year}\ - Get wealth statement

##  FYP Project Details

**Student:** Abdul Bari (2022-LSC-04)  
**Supervisor:** Mr. Mohsin (NetSol Technologies)  
**Institution:** Superior College / FCIT Punjab University  
**Duration:** 24 weeks  

**Project Objectives:**
- Automate FBR tax filing process
- Reduce filing time from 4+ hours to <30 minutes
- Implement AI-powered tax assistance
- Generate wealth statements automatically

##  Future Enhancements (Phase 2)

- [ ] Complete FBR Form 114 generation
- [ ] Multi-document processing
- [ ] Expense tracking (bills, utilities)
- [ ] Investment portfolio management
- [ ] Mobile app (React Native)
- [ ] Advanced RAG with vector databases (FAISS/Pinecone)

##  License

MIT License - See LICENSE file

##  Author

Abdul Bari - [GitHub](https://github.com/Dani2003) | [LinkedIn](https://www.linkedin.com/in/abdulbaripgmr/)

---

 Star this repo if you find it helpful!
