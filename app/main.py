from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from datetime import datetime
from pydantic import BaseModel

# Inicialização do FastAPI
app = FastAPI(title="Laboratório SaaS - Projeto Zero")

# Configurações do Banco de Dados (Lidas do seu .env)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELO DE DADOS (TABELA) ---
class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    mrr_value = Column(Float)
    status = Column(String, default="active") # active, canceled
    created_at = Column(DateTime, default=datetime.utcnow)

# Cria a tabela no banco de dados se não existir
Base.metadata.create_all(bind=engine)

# --- ESQUEMAS DE DADOS (VALIDAÇÃO) ---
class SubscriptionCreate(BaseModel):
    customer_name: str
    mrr_value: float

# Dependência para abrir/fechar conexão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROTAS DA API ---

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "projeto": "Projeto Zero",
        "financeiro": "Pronto para MRR/Churn"
    }

# Rota para cadastrar nova venda (Ingestão)
@app.post("/subscribe")
def create_subscription(sub: SubscriptionCreate, db: Session = Depends(get_db)):
    new_sub = Subscription(
        customer_name=sub.customer_name,
        mrr_value=sub.mrr_value
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return {"status": "venda_registrada", "id": new_sub.id}

# Rota para calcular o MRR Total
@app.get("/metrics/mrr")
def get_mrr(db: Session = Depends(get_db)):
    # Busca apenas assinaturas ativas
    active_subs = db.query(Subscription).filter(Subscription.status == "active").all()
    
    total_mrr = sum(s.mrr_value for s in active_subs)
    count = len(active_subs)
    
    return {
        "metric": "Monthly Recurring Revenue",
        "total_mrr": total_mrr,
        "active_customers": count,
        "currency": "BRL"
    }