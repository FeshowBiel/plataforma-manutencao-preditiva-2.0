# arquivo: backend/app/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TelemetriaFrota(BaseModel):
    veiculo_id: str = Field(..., description="Placa ou ID do veículo (ex: ABC-1234)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data e hora da leitura")
    velocidade_kmh: float = Field(..., ge=0, le=150, description="Velocidade atual")
    pressao_pneus_psi: dict[str, float] = Field(..., description="Dicionário com a pressão de cada pneu")
    temperatura_motor_celsius: float = Field(..., description="Temperatura do motor")
    
    # Dados de SST (Segurança e Saúde do Trabalho)
    alerta_fadiga: bool = Field(default=False, description="Sensor de fadiga do motorista acionado")
    carga_perigosa_status: Optional[str] = Field(None, description="Status de válvulas/pressão da carga")

    class Config:
        json_schema_extra = {
            "example": {
                "veiculo_id": "CTX-9988",
                "velocidade_kmh": 85.5,
                "pressao_pneus_psi": {"dianteiro_esq": 110.0, "traseiro_dir": 108.5},
                "temperatura_motor_celsius": 90.2,
                "alerta_fadiga": False,
                "carga_perigosa_status": "NORMAL"
            }
        }