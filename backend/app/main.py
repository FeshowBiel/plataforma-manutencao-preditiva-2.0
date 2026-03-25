# arquivo: backend/app/main.py
from fastapi import FastAPI, HTTPException, status
from app.schemas import TelemetriaFrota
from app.rabbitmq import publicar_mensagem

# Instancia a aplicação FastAPI com metadados para a documentação automática (Swagger)
app = FastAPI(
    title="API de Inteligência de Frotas e SST",
    description="Gateway de alta performance para recepção de dados de telemetria.",
    version="2.0.0"
)

@app.get("/health", tags=["Monitoramento"])
async def health_check():
    """Endpoint de verificação de saúde da API."""
    return {"status": "online", "servico": "API Frotas"}

@app.post("/api/v1/telemetria", status_code=status.HTTP_202_ACCEPTED, tags=["Ingestão de Dados"])
async def receber_telemetria(dados: TelemetriaFrota):
    """
    Recebe os dados do veículo, valida via Pydantic e envia para a fila de processamento.
    """
    # Converte o modelo Pydantic validado para um dicionário (e datas para string ISO)
    payload = dados.model_dump(mode='json')
    
    # Tenta publicar na fila do RabbitMQ
    sucesso = publicar_mensagem(fila="telemetria_frota", mensagem=payload)
    
    if not sucesso:
        # Se o RabbitMQ estiver fora do ar, retornamos erro 503 (Serviço Indisponível)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Fila de mensagens indisponível. Tente novamente."
        )
        
    return {
        "mensagem": "Dados recebidos e enfileirados com sucesso",
        "veiculo_id": dados.veiculo_id
    }