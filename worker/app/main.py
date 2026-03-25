# arquivo: worker/app/main.py
import pika
import json
import os
import time
from database import SessionLocal, Telemetria

# Configurações do RabbitMQ
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin_password")

def salvar_no_banco(dados):
    """Abre uma sessão no banco, insere o dado e fecha a sessão."""
    db = SessionLocal()
    try:
        nova_leitura = Telemetria(
            veiculo_id=dados.get("veiculo_id"),
            timestamp=dados.get("timestamp"),
            velocidade_kmh=dados.get("velocidade_kmh"),
            pressao_pneus_psi=dados.get("pressao_pneus_psi"),
            temperatura_motor_celsius=dados.get("temperatura_motor_celsius"),
            alerta_fadiga=dados.get("alerta_fadiga"),
            carga_perigosa_status=dados.get("carga_perigosa_status")
        )
        db.add(nova_leitura)
        db.commit() # Efetiva a gravação
        print(f"✅ Sucesso: Telemetria do veículo {nova_leitura.veiculo_id} salva no PostgreSQL!")
    except Exception as e:
        db.rollback() # Se der erro, desfaz a transação para não corromper o banco
        print(f"❌ Erro ao salvar no banco: {e}")
    finally:
        db.close()

def callback(ch, method, properties, body):
    """Função disparada automaticamente sempre que uma mensagem chega na fila."""
    print("\n📥 Nova mensagem detectada na fila!")
    dados_telemetria = json.loads(body)
    
    salvar_no_banco(dados_telemetria)
    
    # Confirmação manual (ACK): Diz ao RabbitMQ que pode apagar a mensagem da fila
    ch.basic_ack(delivery_tag=method.delivery_tag)

def iniciar_worker():
    """Conecta ao RabbitMQ e começa a escutar a fila."""
    print("⏳ Iniciando o Worker de Processamento de Dados...")
    
    # Pequeno atraso para garantir que o RabbitMQ e Postgres terminaram de ligar no Docker
    time.sleep(5) 
    
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    conexao = pika.BlockingConnection(parameters)
    canal = conexao.channel()
    
    # Garante que a fila existe
    canal.queue_declare(queue='telemetria_frota', durable=True)
    
    # Configura para pegar 1 mensagem por vez (QoS) para não sobrecarregar a memória
    canal.basic_qos(prefetch_count=1)
    canal.basic_consume(queue='telemetria_frota', on_message_callback=callback)
    
    print("🚀 Worker online! Escutando a fila 'telemetria_frota'. Pressione CTRL+C para sair.")
    canal.start_consuming()

if __name__ == "__main__":
    iniciar_worker()