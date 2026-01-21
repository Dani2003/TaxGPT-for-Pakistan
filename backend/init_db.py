"""
Database Initialization Script
Run this to create all tables
"""
import sys
sys.path.append('.')

from app.db.session import init_db

if __name__ == "__main__":
    print(" Initializing database...")
    init_db()
    print(" Database setup complete!")
    print("\nYou can now run: uvicorn app.main:app --reload")
