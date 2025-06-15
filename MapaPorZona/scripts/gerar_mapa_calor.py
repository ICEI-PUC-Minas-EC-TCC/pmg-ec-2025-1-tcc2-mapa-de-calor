import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import json
import os

# === Caminhos ===
caminho_csv = "dados/dados.csv"
caminho_imagem = "dados/A4-2.png"
caminho_zonas = "resultados/zonas_salvas.json"
caminho_rssi = "resultados/rssi_por_zona.json"
caminho_modelo = "resultados/modelo_rssi_tensorflow.keras"

# === MACs por roteador ===
macs_routers = {
    "Tenda": ["50:8a:06:fc:81:4d", "22:55:7E:84:10:17", "4A:E9:21:8B:E1:CE"],
    "Archer": ["52:9F:14:D9:81:25", "30:cc:21:14:be:83", "56:4b:54:3b:84:8f"]
}

# === Carregar dados ===
df = pd.read_csv(caminho_csv)

# Corrigir nome das colunas se necessário
df.columns = [col.strip().lower() for col in df.columns]
df = df[['mac', 'rssi']]
df['rssi'] = df['rssi'].astype(float)

# === Separar por roteador ===
df_tenda = df[df['mac'].str.lower().isin([mac.lower() for mac in macs_routers['Tenda']])]
df_archer = df[df['mac'].str.lower().isin([mac.lower() for mac in macs_routers['Archer']])]

# === Agrupar RSSI médio por MAC ===
rssi_tenda = df_tenda.groupby('mac')['rssi'].mean()
rssi_archer = df_archer.groupby('mac')['rssi'].mean()

# === Juntar RSSI Tenda e Archer ===
all_macs = set(rssi_tenda.index) | set(rssi_archer.index)
data = []
for mac in all_macs:
    rssi_t = rssi_tenda.get(mac, -100)
    rssi_a = rssi_archer.get(mac, -100)
    data.append([rssi_t, rssi_a])

X_raw = np.array(data)

# === Normalizar como no treino ===
scaler = MinMaxScaler()
with open(caminho_rssi, 'r') as f:
    zonas_rssi = json.load(f)

# Recalcular scaler com os mesmos dados usados no treino
dados_sinteticos = []
for valores in zonas_rssi.values():
    if 'Tenda' in valores and 'Archer' in valores:
        med_tenda = np.mean(valores['Tenda'])
        med_archer = np.mean(valores['Archer'])
        for _ in range(30):
            dados_sinteticos.append([
                med_tenda + np.random.normal(0, 2),
                med_archer + np.random.normal(0, 2)
            ])
scaler.fit(dados_sinteticos)
X = scaler.transform(X_raw)

# === Carregar modelo e zonas ===
model = tf.keras.models.load_model(caminho_modelo)
with open(caminho_zonas, 'r') as f:
    zonas = json.load(f)
encoder = LabelEncoder()
y_labels = list(zonas.keys())
encoder.fit(y_labels)

# === Previsão ===
preds = model.predict(X)
labels_pred = encoder.inverse_transform(np.argmax(preds, axis=1))

# === Contar ocorrências por zona ===
zona_contagem = {}
for zona in labels_pred:
    zona_contagem[zona] = zona_contagem.get(zona, 0) + 1

# === Mapa base ===
img = mpimg.imread(caminho_imagem)
fig, ax = plt.subplots(figsize=(10, 15))
ax.imshow(img, extent=[0, 600, 0, 840])

# === Colorir zonas com intensidade proporcional ===
max_count = max(zona_contagem.values()) if zona_contagem else 1

for nome, pontos in zonas.items():
    count = zona_contagem.get(nome, 0)
    intensidade = count / max_count
    cor = plt.cm.hot(intensidade)  # Usar colormap 'hot'

    poligono = patches.Polygon(pontos, closed=True, edgecolor='black', facecolor=cor, alpha=0.6)
    ax.add_patch(poligono)

    # Nome no centro
    xs, ys = zip(*pontos)
    cx, cy = sum(xs)/len(xs), sum(ys)/len(ys)
    ax.text(cx, cy, nome, ha='center', va='center', fontsize=6, color='black')

# Finalizar
ax.axis('off')
plt.title("Mapa de Calor por Zona - Previsão com TensorFlow", fontsize=14)
plt.tight_layout()

# Salvar
os.makedirs("resultados", exist_ok=True)
fig.savefig("resultados/mapa_calor_predito.png", dpi=300)
plt.show()
