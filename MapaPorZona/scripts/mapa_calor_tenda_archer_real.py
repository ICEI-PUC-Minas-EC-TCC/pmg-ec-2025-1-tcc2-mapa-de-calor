import pandas as pd
import numpy as np
import json
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from sklearn.preprocessing import MinMaxScaler
from collections import Counter
import os

# === Arquivos ===
ARQUIVO_CSV = "dados/dados.csv"
ARQUIVO_IMAGEM = "dados/A4-2.png"
ARQUIVO_ZONAS = "resultados/zonas_salvas.json"
ARQUIVO_MODELO = "resultados/modelo_rssi_tensorflow.keras"
SAIDA_IMAGEM = "resultados/mapa_calor_separado_tenda_archer.png"

mac_para_roteador = {
    "52:9f:14:d9:81:25": "Archer",
    "30:cc:21:14:be:83": "Archer",
    "56:4b:54:3b:84:8f": "Archer",
    "50:8a:06:fc:81:4d": "Tenda",
    "22:55:7e:84:10:17": "Tenda",
    "4a:e9:21:8b:e1:ce": "Tenda"
}

df = pd.read_csv(ARQUIVO_CSV)
df['mac'] = df['mac'].str.lower()
df['rssi'] = pd.to_numeric(df['rssi'], errors='coerce')
df['roteador'] = df['mac'].map(mac_para_roteador)
df.dropna(subset=['roteador', 'rssi'], inplace=True)

with open(ARQUIVO_ZONAS, "r") as f:
    zonas = json.load(f)
zona_labels = list(zonas.keys())

modelo = tf.keras.models.load_model(ARQUIVO_MODELO)
scaler = MinMaxScaler()

def prever_e_contar(df_filtrado, tipo):
    if df_filtrado.empty:
        return Counter()

    X_data = []
    for _, row in df_filtrado.iterrows():
        if tipo == "Tenda":
            X_data.append([row['rssi'], -100])
        else:
            X_data.append([-100, row['rssi']])

    X_scaled = scaler.fit_transform(X_data)
    preds = modelo.predict(X_scaled)
    zonas_preditas = [zona_labels[np.argmax(p)] for p in preds]
    return Counter(zonas_preditas)

contagem_tenda = prever_e_contar(df[df['roteador'] == 'Tenda'], "Tenda")
contagem_archer = prever_e_contar(df[df['roteador'] == 'Archer'], "Archer")

img = mpimg.imread(ARQUIVO_IMAGEM)
fig, ax = plt.subplots(figsize=(10, 15))
ax.imshow(img, extent=[0, 600, 0, 840])

max_tenda = max(contagem_tenda.values()) if contagem_tenda else 1
max_archer = max(contagem_archer.values()) if contagem_archer else 1
norm_tenda = plt.Normalize(vmin=0, vmax=max_tenda)
norm_archer = plt.Normalize(vmin=0, vmax=max_archer)

for zona, pontos in zonas.items():
    count_t = contagem_tenda.get(zona, 0)
    count_a = contagem_archer.get(zona, 0)
    if count_t > 0:
        cor = plt.cm.Reds(norm_tenda(count_t))
        pol = patches.Polygon(pontos, closed=True, edgecolor='black', facecolor=cor, alpha=0.5)
        ax.add_patch(pol)
    if count_a > 0:
        cor = plt.cm.Blues(norm_archer(count_a))
        pol = patches.Polygon(pontos, closed=True, edgecolor='black', facecolor=cor, alpha=0.5)
        ax.add_patch(pol)

tenda_patch = patches.Patch(color='red', label='Tenda (Reds)', alpha=0.5)
archer_patch = patches.Patch(color='blue', label='Archer (Blues)', alpha=0.5)
plt.legend(handles=[tenda_patch, archer_patch], loc='lower center', ncol=2)

plt.title("Mapa de Calor Separado - Tenda (Vermelho) / Archer (Azul)")
ax.axis('off')

cbar1 = plt.colorbar(plt.cm.ScalarMappable(norm=norm_tenda, cmap=plt.cm.Reds), ax=ax, fraction=0.035, pad=0.02)
cbar1.set_label("Tenda")
cbar2 = plt.colorbar(plt.cm.ScalarMappable(norm=norm_archer, cmap=plt.cm.Blues), ax=ax, fraction=0.035, pad=0.08)
cbar2.set_label("Archer")

os.makedirs("resultados", exist_ok=True)
plt.savefig(SAIDA_IMAGEM, dpi=300, bbox_inches='tight')
plt.show()
