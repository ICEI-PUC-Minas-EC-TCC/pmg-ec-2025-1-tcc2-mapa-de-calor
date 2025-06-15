import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import numpy as np
import json
from scipy.ndimage import gaussian_filter

# === Carregar a imagem da planta ===
img = mpimg.imread('dados/A4-2.png')

# === Carregar zonas ===
with open('resultados/zonas_salvas.json', 'r') as f:
    zonas = json.load(f)

# === Carregar RSSI por zona ===
with open('resultados/rssi_por_zona.json', 'r') as f:
    rssi_por_zona = json.load(f)

# === Criar matriz de calor ===
largura, altura = 600, 840
heatmap_tenda = np.zeros((altura, largura))
heatmap_archer = np.zeros((altura, largura))

# === Preencher o heatmap com valores de RSSI médios ===
def preencher_heatmap(zona_nome, pontos, heatmap, rssi_range):
    if not rssi_range:
        return
    rssi_medio = np.mean(rssi_range)
    xs, ys = zip(*pontos)
    min_x, max_x = int(min(xs)), int(max(xs))
    min_y, max_y = int(min(ys)), int(max(ys))

    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if ponto_dentro_poligono((x, y), pontos):
                heatmap[y, x] = rssi_medio

# === Função para verificar se ponto está dentro de polígono (zona) ===
def ponto_dentro_poligono(ponto, poligono):
    from matplotlib.path import Path
    return Path(poligono).contains_point(ponto)

# === Preencher mapas ===
for zona, pontos in zonas.items():
    if zona in rssi_por_zona:
        if 'Tenda' in rssi_por_zona[zona]:
            preencher_heatmap(zona, pontos, heatmap_tenda, rssi_por_zona[zona]['Tenda'])
        if 'Archer' in rssi_por_zona[zona]:
            preencher_heatmap(zona, pontos, heatmap_archer, rssi_por_zona[zona]['Archer'])

# === Aplicar filtro gaussiano para suavizar ===
blur_tenda = gaussian_filter(heatmap_tenda, sigma=10)
blur_archer = gaussian_filter(heatmap_archer, sigma=10)

# === Plotar os dois mapas de calor ===
def plotar_mapa(blur_map, titulo, output_file):
    fig, ax = plt.subplots(figsize=(10, 15))
    ax.imshow(img, extent=[0, largura, 0, altura])
    im = ax.imshow(blur_map, extent=[0, largura, 0, altura], origin='lower',
                   cmap='jet', alpha=0.5)

    plt.colorbar(im, ax=ax, label='Intensidade RSSI (dBm)')
    plt.title(titulo)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f'Mapa salvo em: {output_file}')
    plt.show()

plotar_mapa(blur_tenda, 'Mapa de Calor - Tenda', 'resultados/mapa_calor_tenda.png')
plotar_mapa(blur_archer, 'Mapa de Calor - Archer', 'resultados/mapa_calor_archer.png')
