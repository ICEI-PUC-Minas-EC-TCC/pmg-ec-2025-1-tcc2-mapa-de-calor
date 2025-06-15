import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import json

# Carregar a imagem da planta
img = mpimg.imread('dados/A4-2.png')

# Carregar zonas
with open('resultados/zonas_salvas.json', 'r') as f:
    zonas = json.load(f)

# Carregar RSSI
with open('resultados/rssi_por_zona.json', 'r') as f:
    rssi_por_zona = json.load(f)

# Criar figura
fig, ax = plt.subplots(figsize=(10, 15))
ax.imshow(img, extent=[0, 600, 0, 840])

# Paleta de cores (repetindo se necessário)
cores = [
    'red', 'green', 'blue', 'yellow', 'purple',
    'cyan', 'orange', 'pink', 'gray', 'lime'
]

# Desenhar zonas e mostrar RSSI Tenda + Archer
for i, (zona, pontos) in enumerate(zonas.items()):
    cor = cores[i % len(cores)]
    poligono = patches.Polygon(pontos, closed=True, edgecolor='black', facecolor=cor, alpha=0.5)
    ax.add_patch(poligono)

    # Calcular centro da zona
    xs, ys = zip(*pontos)
    centro_x = sum(xs) / len(xs)
    centro_y = sum(ys) / len(ys)

    # Buscar RSSI
    rssi_tenda = rssi_por_zona.get(zona, {}).get('Tenda', ["?", "?"])
    rssi_archer = rssi_por_zona.get(zona, {}).get('Archer', ["?", "?"])

    # Criar texto a ser exibido
    texto = f"{zona}\nTenda: {rssi_tenda[0]} a {rssi_tenda[1]} dBm\nArcher: {rssi_archer[0]} a {rssi_archer[1]} dBm"

    # Colocar texto na planta
    ax.text(centro_x, centro_y, texto, ha='center', va='center', fontsize=7, color='black')

# Ajustes finais
ax.axis('off')
plt.title('Mapa de Zonas + RSSI Tenda e Archer', fontsize=16)
plt.show()

# Salvar o mapa
fig.savefig('resultados/mapa_zonas_com_rssi.png', dpi=300, bbox_inches='tight')
