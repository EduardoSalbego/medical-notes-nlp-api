FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# 1. Atualizar o pip para evitar erros de compatibilidade
RUN pip install --upgrade pip

# 2. Instalar bibliotecas
RUN pip install --no-cache-dir -r requirements.txt

# 3. Instalar o modelo via Link Direto (Mais robusto que o comando download)
RUN pip install https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-3.7.0/pt_core_news_sm-3.7.0-py3-none-any.whl

COPY . .

EXPOSE 8001