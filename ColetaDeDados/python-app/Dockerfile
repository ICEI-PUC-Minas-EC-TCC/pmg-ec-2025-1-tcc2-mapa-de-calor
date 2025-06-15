FROM python:3.11-slim

# Instala tshark e dependências do pyshark
RUN apt-get update && apt-get install -y \
    tshark \
    libpcap-dev \
    curl \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Permitir captura sem root (opcional: dependendo do uso)
RUN setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap

# Cria diretório de trabalho
WORKDIR /app

# Copia requirements e instala dependências Python
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia os scripts
COPY coletor.py .

CMD ["python", "coletor.py"]
