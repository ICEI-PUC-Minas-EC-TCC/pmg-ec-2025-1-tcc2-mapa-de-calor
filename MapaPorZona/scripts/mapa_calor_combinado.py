import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
from scipy.interpolate import griddata

# === Arquivos ===
CSV = "dados/dados.csv"
IMG = "dados/A4-2.png"
ZONAS = "resultados/zonas_salvas.json"
RSSI_ZONAS = "resultados/rssi_por_zona.json"
OUT = "resultados/mapa_calor_combinado_rssi.png"

# MACs por roteador
macs_roteador = {
    "52:9f:14:d9:81:25": "Archer",
    "30:cc:21:14:be:83": "Archer",
    "56:4b:54:3b:84:8f": "Archer",
    "50:8a:06:fc:81:4d": "Tenda",
    "22:55:7e:84:10:17": "Tenda",
    "4a:e9:21:8b:e1:ce": "Tenda",
}

# === Carregar dados ===
df = pd.read_csv(CSV)
df['mac'] = df['mac'].str.lower()
df['rssi'] = pd.to_numeric(df['rssi'], errors='coerce')
df.dropna(inplace=True)
df['roteador'] = df['mac'].map(macs_roteador)
df.dropna(subset=['roteador'], inplace=True)

# === Carregar zonas ===
with open(ZONAS) as f:
    zonas = json.load(f)
with open(RSSI_ZONAS) as f:
    rssi_por_zona = json.load(f)

# === Estimar a zona mais provável com base no RSSI médio ===
pontos = []
valores = []

for _, row in df.iterrows():
    rssi = row['rssi']
    roteador = row['roteador']

    # Encontrar a zona mais próxima com base em RSSI
    melhor_zona = None
    menor_dif = float('inf')
    for zona, valores_z in rssi_por_zona.items():
        if roteador in valores_z:
            rssi_ref = sum(valores_z[roteador]) / 2
            diff = abs(rssi - rssi_ref)
            if diff < menor_dif:
                menor_dif = diff
                melhor_zona = zona

    if melhor_zona and melhor_zona in zonas:
        # Calcular centro da zona
        coords = zonas[melhor_zona]
        xs, ys = zip(*coords)
        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)
        pontos.append((cx, cy))
        valores.append(rssi)

# === Verificação
if not pontos:
    raise ValueError("Nenhum ponto válido encontrado para plotar o mapa.")

# === Interpolação e Plot
xi = np.linspace(0, 600, 300)
yi = np.linspace(0, 840, 300)
grid_x, grid_y = np.meshgrid(xi, yi)
grid_z = griddata(pontos, valores, (grid_x, grid_y), method='cubic')

# === Plotagem
plt.figure(figsize=(10, 15))
img = mpimg.imread(IMG)
plt.imshow(img, extent=[0, 600, 0, 840])
heatmap = plt.imshow(grid_z.T, extent=(0, 600, 0, 840), origin='lower', cmap='Spectral_r', alpha=0.75)
cbar = plt.colorbar(heatmap)
cbar.set_label("Intensidade RSSI (dBm)")
plt.title("Mapa de Calor Combinado - Tenda + Archer")
plt.axis('off')
plt.savefig(OUT, dpi=300, bbox_inches='tight')
plt.show()
