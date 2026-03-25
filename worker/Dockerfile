# arquivo: worker/Dockerfile

# Usamos a mesma imagem leve do Python
FROM python:3.11-slim

# Instala dependências do sistema operacional necessárias para o driver do PostgreSQL (psycopg2) compilar corretamente
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte
COPY ./app ./app

# Comando de inicialização: roda o main.py em modo unbuffered (-u) para vermos os logs ao vivo
CMD ["python", "-u", "app/main.py"]