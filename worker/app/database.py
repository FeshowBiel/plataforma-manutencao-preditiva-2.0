# arquivo: worker/app/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from datetime import datetime

# Captura as credenciais via variáveis de ambiente (passadas pelo Docker)
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "admin_password")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "frotas_db")

# String de conexão padrão do PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

# Cria a engine (o motor de conexão com o banco)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Mapeamento Objeto-Relacional (ORM)
class Telemetria(Base):
    __tablename__ = "telemetria_frota"
    
    id = Column(Integer, primary_key=True, index=True)
    veiculo_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    velocidade_kmh = Column(Float)
    pressao_pneus_psi = Column(JSON) # PostgreSQL lida nativamente com dados JSON!
    temperatura_motor_celsius = Column(Float)
    alerta_fadiga = Column(Boolean)
    carga_perigosa_status = Column(String, nullable=True)

# Este comando cria as tabelas no banco caso elas não existam
Base.metadata.create_all(bind=engine)