from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os, time, sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv() 
app = FastAPI(title="Projeto Zero - Mgrpoison Edition")

DATABASE_URL = os.getenv("DATABASE_URL") 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ÁREA DE MODELOS (Fácil de Expandir) ---
# Para criar mais tabelas, basta adicionar novas classes herdando de Base aqui.

class FinancialRecord(Base):
    __tablename__ = "financial_records"
    id = Column(Integer, primary_key=True, index=True)
    area = Column(String); pl_line = Column(String); category = Column(String)
    cost_center = Column(String); provider = Column(String); value = Column(Float)
    month_ref = Column(String); created_at = Column(DateTime, default=datetime.utcnow)

class BudgetRecord(Base):
    __tablename__ = "budget_records"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String); value = Column(Float); month_ref = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# --- INICIALIZAÇÃO AUTOMÁTICA NO STARTUP ---
@app.on_event("startup")
def startup_event():
    print("MGRPOISON: Verificando integridade do banco...", flush=True)
    for i in range(10):
        try:
            # metadata.create_all mapeia TUDO que herdou de Base automaticamente
            Base.metadata.create_all(bind=engine)
            print("✅ MGRPOISON: Tabelas sincronizadas e prontas!", flush=True)
            return
        except Exception as e:
            print(f"⚠️ MGRPOISON: Banco em aquecimento (Tentativa {i+1}/10). Erro: {e}", flush=True)
            time.sleep(5)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- ROTAS ---
@app.post("/ingest")
def ingest_real(data: list[dict], db: Session = Depends(get_db)):
    try:
        for item in data:
            db.add(FinancialRecord(**item))
        db.commit()
        return {"status": "sucesso", "destino": "realizado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/budget")
def ingest_budget(data: list[dict], db: Session = Depends(get_db)):
    try:
        for item in data:
            db.add(BudgetRecord(**item))
        db.commit()
        return {"status": "sucesso", "destino": "orçado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/metrics/comparison")
def get_comparison(db: Session = Depends(get_db)):
    realizado = db.query(FinancialRecord.category, func.sum(FinancialRecord.value).label("total")).group_by(FinancialRecord.category).all()
    orcado = db.query(BudgetRecord.category, func.sum(BudgetRecord.value).label("total")).group_by(BudgetRecord.category).all()
    return {
        "realizado": {row.category: row.total for row in realizado},
        "orcado": {row.category: row.total for row in orcado}
    }


