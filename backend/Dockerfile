# Usa uma imagem oficial do Python otimizada, versão 'slim' (menor tamanho, mais segurança)
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de requisitos primeiro
# (Isso otimiza o cache do Docker. Se o código mudar, mas as bibliotecas não, o Docker pula essa etapa, economizando tempo)
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Agora copia o resto do código da pasta local 'app' para dentro da pasta '/app/app' no container
COPY ./app ./app

# Expõe a porta que o FastAPI vai utilizar
EXPOSE 8000

# Comando final que inicia o servidor de alta performance (Uvicorn)
# O host "0.0.0.0" permite que conexões externas (fora do container) cheguem à API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]