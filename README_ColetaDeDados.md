# Coleta de Dados Wi-Fi via OpenWRT

Este módulo é responsável por capturar pacotes Wi-Fi 802.11 via roteador com OpenWRT em modo monitor, transferir os arquivos capturados para o host local e processar os dados usando PyShark.

---

## 📁 Estrutura da Pasta

```
ColetaDeDados/
├── mysql/                     # (opcional) persistência em banco
├── output/                   # saída do processamento (ex: dados.txt)
├── pcap/                     # arquivos .pcap coletados do roteador
├── processamento_rssi/       # scripts de análise posterior
├── python-app/               # scripts principais
│   ├── output/               # dados processados
│   ├── agendador.py          # script que executa captura, SCP e processamento
│   ├── coletor.py            # script que processa o arquivo pcap com PyShark
│   ├── Dockerfile            # ambiente dockerizado
│   ├── requirements.txt      # dependências Python
├── cron.log                  # log opcional para execuções agendadas
└── docker-compose.yml        # orquestração dos serviços
```

---

## ⚙️ Requisitos

- Roteador compatível com **OpenWRT** e **modo monitor** (ex: TP-Link Archer C20)
- SSH habilitado no roteador
- `tcpdump` instalado no roteador
- Docker (para execução conteinerizada) ou ambiente Python local com PyShark

---

## 🛠️ Passos de Configuração

### 1. Habilite o modo monitor no roteador OpenWRT

Acesse via SSH o roteador e execute:

```bash
iw phy phy0 interface add mon0 type monitor
ip link set mon0 up
```

### 2. Verifique se `tcpdump` está disponível no roteador

Caso não esteja, instale com:

```bash
opkg update
opkg install tcpdump
```

---

## 🚀 Execução do Script `agendador.py`

Este script realiza todo o ciclo:

1. Inicia a captura de pacotes via SSH
2. Baixa o arquivo `.pcap` para o diretório `pcap/`
3. Processa o `.pcap` usando o `coletor.py` (dentro de um container Docker)

### 📌 Parâmetros pré-definidos

- IP do roteador: `192.168.1.1`
- Usuário: `root`
- Interface: `mon0`
- Duração: 60 segundos
- Caminho remoto: `/captura.pcap`
- Caminho local: `pcap/captura.pcap`

### ▶️ Execute assim:

```bash
cd ColetaDeDados/python-app
python agendador.py
```

---

## 🔍 O que o `coletor.py` faz?

Este script utiliza a biblioteca **PyShark** para processar o `.pcap` e extrair:

- Endereço MAC
- SSID (se disponível)
- RSSI (intensidade do sinal)
- Timestamp
- Identificação da origem (roteador ou cliente)

Esses dados são salvos no arquivo:

```
output/dados.txt
```

---

## 🧪 Verificando a Saída

Após a execução do `agendador.py`, verifique:

- Se o arquivo `pcap/captura.pcap` foi criado corretamente
- Se o diretório `output/` contém `dados.txt`
- Se o console exibiu as linhas extraídas com RSSI e MACs

---

## 🐳 Execução com Docker (Opcional)

Você pode usar o ambiente conteinerizado para executar o `coletor.py` com as dependências corretas:

```bash
docker-compose run --rm app
```

---

## 🔐 Privacidade e LGPD

- Apenas os campos **endereço MAC  e RSSI** são processados.
- Os **MACs de dispositivos utilizados no experimento** (3 do Archer e 3 do Tenda) **são exibidos em texto claro**, pois são essenciais para validação e análise dos testes.

> ⚠️ Com uma simples alteração no código (`coletor.py`), é possível anonimizar **todos os MACs**, inclusive os usados nos testes. Essa configuração pode ser ajustada conforme a política de privacidade ou o ambiente de aplicação, isso implica em alterações no codigo do arquviso da pasta de MapaZona
