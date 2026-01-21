import os
from groq import Groq
from app.core.config import settings
from app.services.rag_service import tax_kb

client = None
if settings.GROQ_API_KEY:
    client = Groq(api_key=settings.GROQ_API_KEY)

async def ask_tax_question(question: str) -> str:
    if not client:
        return "AI service not configured. Please set GROQ_API_KEY in .env file."
    
    # Use RAG to get relevant context
    relevant_docs = tax_kb.search(question, k=3)
    context = "\n".join([doc['text'] for doc in relevant_docs])
    
    system_prompt = f'''You are a Pakistani tax expert assistant. Use this knowledge to answer questions:

{context}

Provide accurate, helpful answers about Pakistani tax rules and FBR regulations.'''
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            model=settings.GROQ_MODEL,
            temperature=0.3,
            max_tokens=500
        )
        
        answer = chat_completion.choices[0].message.content
        
        # Add sources
        sources = [doc['text'][:100] + "..." for doc in relevant_docs]
        return f"{answer}\n\n**Sources:** {', '.join(sources)}"
        
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"

async def extract_financial_info_with_ai(text: str) -> dict:
    if not client:
        return {"error": "AI service not configured"}
    
    prompt = f'''
    Extract the following information from this financial document text:
    - Monthly/Annual Income
    - Employer Name
    - Account Number
    - Bank Name
    
    Text:
    {text[:2000]}
    
    Respond in JSON format:
    {{
        "monthly_income": <number or null>,
        "employer_name": "<name or null>",
        "account_number": "<number or null>",
        "bank_name": "<name or null>"
    }}
    '''
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a financial document analyzer. Extract information accurately and return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            model=settings.GROQ_MODEL,
            temperature=0.1,
            max_tokens=300
        )
        
        response = chat_completion.choices[0].message.content
        
        import json
        extracted_data = json.loads(response)
        return extracted_data
        
    except Exception as e:
        return {"error": str(e)}
