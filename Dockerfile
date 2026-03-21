# Usa uma imagem leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o conteúdo da pasta src para dentro de /app
COPY . .

# Comando para rodar o bot
CMD ["python", "main.py"]