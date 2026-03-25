# arquivo: backend/app/rabbitmq.py
import pika
import json
import os

# Em containers, o localhost vira o nome do serviço no docker-compose
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin_password")

def get_rabbitmq_connection():
    """Cria e retorna uma conexão com o RabbitMQ."""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    return pika.BlockingConnection(parameters)

def publicar_mensagem(fila: str, mensagem: dict):
    """Publica um dicionário como JSON na fila especificada."""
    try:
        conexao = get_rabbitmq_connection()
        canal = conexao.channel()
        
        # Garante que a fila existe (se não existir, ele cria)
        canal.queue_declare(queue=fila, durable=True)
        
        # Publica a mensagem
        canal.basic_publish(
            exchange='',
            routing_key=fila,
            body=json.dumps(mensagem),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Torna a mensagem persistente (não some se o RabbitMQ reiniciar)
            )
        )
        conexao.close()
        return True
    except Exception as e:
        print(f"Erro ao publicar no RabbitMQ: {e}")
        return False