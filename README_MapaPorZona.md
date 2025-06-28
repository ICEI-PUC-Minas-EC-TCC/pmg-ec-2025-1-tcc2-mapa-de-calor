
#  MapaPorZona

Este projeto implementa um sistema modular de monitoramento de ocupação em ambientes físicos, utilizando captura passiva de pacotes Wi-Fi, técnicas de aprendizado de máquina e visualização em mapas de calor vetorizados. A solução foi desenvolvida como parte de um Trabalho de Conclusão de Curso no Instituto de Ciências Exatas e Informática da PUC Minas.

---

## 📁 Estrutura do Projeto

O repositório está organizado em duas formas principais de execução:

- `docker/`: ambiente conteinerizado com `docker-compose` para isolamento e reprodutibilidade
- `local/`: execução direta com ambiente Python local (recomendada para testes rápidos e notebooks)

---

## ⚙️ Instalação do Ambiente Local (via venv)

1. Clone este repositório:

```bash
git clone https://github.com/ICEI-PUC-Minas-EC-TCC/pmg-ec-2025-1-tcc2-mapa-de-calor
cd pmg-ec-2025-1-tcc2-mapa-de-calor
````

2. Crie o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

> As bibliotecas principais incluem: `pyshark`, `pandas`, `numpy`, `tensorflow`, `opencv-python`, `matplotlib`, entre outras.

---

## 📌 Principais Scripts

| Arquivo                | Descrição                                                             |
| ---------------------- | --------------------------------------------------------------------- |
| `gerar_mp_rssi.py`     | Agrupa os valores de RSSI por zona a partir dos dados extraídos       |
| `modelo_rssi_tflow.py` | Treina um modelo de rede neural com TensorFlow para classificar zonas |
| `mp_calor_kerasC.py`   | Aplica o modelo aos dados e gera os mapas de calor                    |
| `desenhar_mp_zonas.py` | Gera a imagem final com as zonas sobre planta baixa vetorizada        |

---

## ✏️ Definição das Zonas sobre a Planta Baixa

Antes de gerar qualquer predição, é necessário mapear as zonas físicas do ambiente. Para isso:

1. Acesse o notebook `notebook.ipynb`
2. Execute as células sequencialmente:

   * A planta baixa será exibida.
   * Você poderá clicar nos pontos que delimitam cada zona manualmente e visuzalizar sua coordenada.

> ⚠️ Este passo é essencial para que os dados de RSSI sejam corretamente associados ao espaço físico.

---

## 🐳 Execução com Docker (Alternativa)

1. Entre na pasta `docker`:

```bash
cd docker/
```

2. Inicie os serviços:

```bash
docker-compose up
```

> O container `app` roda o processamento com Python + Tshark, e o container `mysql` (opcional) pode ser usado para persistência dos dados.

---

## 🔐 Considerações sobre Privacidade e LGPD

* Apenas os campos **MAC (anonimizados com hash)** e **RSSI** são coletados.
* Nenhum dado sensível ou pessoal é armazenado.
* O sistema foi projetado para ser compatível com os princípios da LGPD.

---

## 📊 Exemplo de Execução

1. Capture os pacotes `.pcap` usando `tcpdump` no roteador com OpenWRT.
2. Extraia os dados com script PyShark (endereços MAC e RSSI).
3. Defina as zonas com `coordenadas_zonas.ipynb`.
4. Treine o modelo com `modelo_rssi_tflow.py`.
5. Gere o mapa de calor com `mp_calor_kerasC.py`.
6. Visualize os resultados em `desenhar_mp_zonas.py`.

---


```
