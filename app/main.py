from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import time
from datetime import datetime
from sqlalchemy.exc import OperationalError

app = FastAPI(title="Projeto Zero - Mgrpoison Edition")

# No seu main.py, mude para:
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@db:5432/saas_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELOS ---
class FinancialRecord(Base):
    __tablename__ = "financial_records"
    id = Column(Integer, primary_key=True, index=True)
    area = Column(String)
    pl_line = Column(String)
    category = Column(String)
    cost_center = Column(String)
    provider = Column(String)
    value = Column(Float)
    month_ref = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class BudgetRecord(Base):
    __tablename__ = "budget_records"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    value = Column(Float)
    month_ref = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# --- INICIALIZAÇÃO FORÇADA (SQL PURO) ---
def init_db():
    print("Mgrpoison, executando DDL de emergência...")
    sql_create_budget = """
    CREATE TABLE IF NOT EXISTS budget_records (
        id SERIAL PRIMARY KEY,
        category VARCHAR,
        value FLOAT,
        month_ref VARCHAR,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    for i in range(10):
        try:
            # Tenta o método do SQLAlchemy
            Base.metadata.create_all(bind=engine)
            # Tenta o método SQL Puro para garantir
            with engine.connect() as conn:
                conn.execute(text(sql_create_budget))
                conn.commit()
            print("✅ Tabelas verificadas e forçadas com sucesso!")
            break
        except Exception as e:
            print(f"⚠️ Erro ao criar: {e}. Tentativa {i+1}/10")
            time.sleep(5)

init_db()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- ROTAS ---
@app.post("/ingest")
def ingest_real(data: list[dict], db: Session = Depends(get_db)):
    for item in data:
        db.add(FinancialRecord(**item))
    db.commit()
    return {"status": "sucesso", "destino": "realizado"}

@app.post("/budget")
def ingest_budget(data: list[dict], db: Session = Depends(get_db)):
    for item in data:
        db.add(BudgetRecord(**item))
    db.commit()
    return {"status": "sucesso", "destino": "orçado"}

@app.get("/metrics/comparison")
def get_comparison(db: Session = Depends(get_db)):
    realizado = db.query(FinancialRecord.category, func.sum(FinancialRecord.value).label("total")).group_by(FinancialRecord.category).all()
    orcado = db.query(BudgetRecord.category, func.sum(BudgetRecord.value).label("total")).group_by(BudgetRecord.category).all()
    return {
        "realizado": {row.category: row.total for row in realizado},
        "orcado": {row.category: row.total for row in orcado}
    }