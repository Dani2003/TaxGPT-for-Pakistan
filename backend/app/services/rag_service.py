import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os

class TaxKnowledgeBase:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []
        self.index_file = 'tax_knowledge.index'
        self.docs_file = 'tax_knowledge.pkl'
        
        # FBR Tax Knowledge
        self.tax_knowledge = [
            "Tax year 2025-26: Income up to Rs. 600,000 is exempt from tax in Pakistan.",
            "For income between Rs. 600,001 to 1,200,000, tax rate is 2.5% in Pakistan.",
            "For income between Rs. 1,200,001 to 2,400,000, tax rate is 12.5% with fixed Rs. 15,000.",
            "For income between Rs. 2,400,001 to 3,600,000, tax rate is 20% with fixed Rs. 165,000.",
            "For income between Rs. 3,600,001 to 6,000,000, tax rate is 25% with fixed Rs. 405,000.",
            "For income between Rs. 6,000,001 to 12,000,000, tax rate is 32.5% with fixed Rs. 1,005,000.",
            "For income above Rs. 12,000,000, tax rate is 35% with fixed Rs. 2,955,000.",
            "Zakat deduction is 2.5% of savings for Muslims in Pakistan.",
            "Charity donations to approved institutions are tax deductible up to 30% of taxable income.",
            "Life insurance premiums are deductible up to Rs. 300,000 annually.",
            "Investment in approved pension funds qualifies for tax deductions.",
            "Salaried individuals must file tax returns by September 30 each year.",
            "Business owners and companies must file by December 31.",
            "FBR requires declaration of all assets including properties, vehicles, and bank accounts.",
            "Foreign income and assets must be declared in wealth statement.",
            "Advance tax is paid in quarterly installments throughout the year.",
            "Late filing penalty ranges from Rs. 1,000 to Rs. 100,000 depending on income.",
            "National Tax Number (NTN) is required for filing tax returns.",
            "Computerized National Identity Card (CNIC) must be linked to NTN.",
            "Tax refunds are processed within 60 days of filing complete returns.",
            "Property sale transactions require tax withholding at source.",
            "Vehicle purchase requires payment of advance income tax.",
            "Rental income is taxable and must be included in annual returns.",
            "Capital gains from sale of securities are subject to capital gains tax.",
            "Agricultural income up to certain limits is exempt from tax.",
        ]
        
        self._build_index()
    
    def _build_index(self):
        if os.path.exists(self.index_file) and os.path.exists(self.docs_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.docs_file, 'rb') as f:
                self.documents = pickle.load(f)
            print(" Loaded existing RAG index")
        else:
            self.documents = self.tax_knowledge
            embeddings = self.model.encode(self.documents)
            embeddings = np.array(embeddings).astype('float32')
            
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings)
            
            faiss.write_index(self.index, self.index_file)
            with open(self.docs_file, 'wb') as f:
                pickle.dump(self.documents, f)
            print(" Built new RAG index")
    
    def search(self, query: str, k: int = 3):
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                results.append({
                    'text': self.documents[idx],
                    'score': float(distance)
                })
        
        return results

# Global instance
tax_kb = TaxKnowledgeBase()
