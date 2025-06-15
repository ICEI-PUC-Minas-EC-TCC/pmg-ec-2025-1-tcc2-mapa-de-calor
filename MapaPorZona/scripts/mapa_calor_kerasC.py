import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import json
import os
from matplotlib.path import Path
from scipy.ndimage import gaussian_filter

# === Caminhos ===
ARQUIVO_CSV = "dados/dados.csv"
ARQUIVO_IMG = "dados/A4-2.png"
ARQUIVO_MODELO = "resultados/modelo_rssi_tensorflow.keras"
ARQUIVO_ZONAS = "resultados/zonas_salvas.json"
ARQUIVO_RSSI = "resultados/rssi_por_zona.json"

# === MACs por roteador ===
mac_para_roteador = {
    "52:9f:14:d9:81:25": "Archer",
    "30:cc:21:14:be:83": "Archer",
    "56:4b:54:3b:84:8f": "Archer",
    "50:8a:06:fc:81:4d": "Tenda",
    "22:55:7e:84:10:17": "Tenda",
    "4a:e9:21:8b:e1:ce": "Tenda"
}

# === Carregar modelo e zonas ===
model = tf.keras.models.load_model(ARQUIVO_MODELO)
with open(ARQUIVO_ZONAS, "r") as f:
    zonas = json.load(f)

with open(ARQUIVO_RSSI, 'r') as f:
    rssi_ref = json.load(f)

# === Carregar dados ===
df = pd.read_csv(ARQUIVO_CSV)
df['mac'] = df['mac'].str.lower()
df['rssi'] = pd.to_numeric(df['rssi'], errors='coerce')
df.dropna(inplace=True)
df['roteador'] = df['mac'].map(mac_para_roteador)
df.dropna(subset=['roteador'], inplace=True)

# === Preparar entrada X para predição ===
X_data = []
for _, row in df.iterrows():
    rssi = row['rssi']
    roteador = row['roteador']
    if roteador == "Tenda":
        X_data.append([rssi, -100])
    elif roteador == "Archer":
        X_data.append([-100, rssi])

X_array = np.array(X_data)

# === Reutilizar escala do treinamento ===
sintetico = []
for zona, valores in rssi_ref.items():
    if "Tenda" in valores and "Archer" in valores:
        med_t = sum(valores['Tenda']) / 2
        med_a = sum(valores['Archer']) / 2
        for _ in range(30):
            sintetico.append([med_t + np.random.normal(0, 2), med_a + np.random.normal(0, 2)])

scaler = MinMaxScaler().fit(sintetico)
X_scaled = scaler.transform(X_array)

# === Previsão com modelo ===
preds = model.predict(X_scaled)
zona_labels = list(zonas.keys())
zona_preditas = [zona_labels[np.argmax(p)] for p in preds]

# === Inicializar matriz da planta ===
altura, largura = 840, 600
heatmap = np.zeros((altura, largura))

# === Contagem e preenchimento por zona ===
from collections import Counter
contagem = Counter(zona_preditas)

def ponto_dentro(ponto, poligono):
    return Path(poligono).contains_point(ponto)

# === Aplicar valor de intensidade para cada zona ===
max_contagem = max(contagem.values())

for zona, pontos in zonas.items():
    intensidade = contagem.get(zona, 0) / max_contagem  # normalizado entre 0-1
    xs, ys = zip(*pontos)
    min_x, max_x = int(min(xs)), int(max(xs))
    min_y, max_y = int(min(ys)), int(max(ys))
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if ponto_dentro((x, y), pontos):
                heatmap[y, x] = intensidade

# === Suavização ===
heatmap_blur = gaussian_filter(heatmap, sigma=10)

# === Plotar imagem ===
img = mpimg.imread(ARQUIVO_IMG)
fig, ax = plt.subplots(figsize=(10, 15))
ax.imshow(img, extent=[0, largura, 0, altura])
im = ax.imshow(heatmap_blur, extent=[0, largura, 0, altura],
               origin='lower', cmap='RdYlBu_r', alpha=0.6)

plt.colorbar(im, ax=ax, label="Presença Estimada por Zona")
plt.title("Mapa de Calor - Previsão com TensorFlow (Tenda + Archer)", fontsize=14)
ax.axis("off")
plt.tight_layout()
plt.savefig("resultados/mapa_calor_final_blur.png", dpi=300)
plt.show()
