import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import json

img = mpimg.imread('dados/A4-2.png')

with open('resultados/zonas_salvas.json', 'r') as f:
    zonas = json.load(f)

rssi_por_zona = {
  "Escada - Zona 1": {"Tenda": (-69, -70), "Archer": (-73, -74)},
  "Escada - Zona 2": {"Tenda": (-69, -70), "Archer": (-73, -74)},
  "Área Externa - Zona 1": {"Tenda": (-57, -63), "Archer": (-73, -78)},
  "Área Externa - Zona 2": {"Tenda": (-45, -47), "Archer": (-65, -69)},
  "Área Externa - Zona 3": {"Tenda": (-48, -52), "Archer": (-73, -74)},
  "Cozinha - Zona 1": {"Tenda": (-44, -49), "Archer": (-71, -73)},
  "Cozinha - Zona 2": {"Tenda": (-21, -25), "Archer": (-71, -73)},
  "Cozinha - Zona 3": {"Tenda": (-38, -48), "Archer": (-71, -73)},
  "Varanda - Zona 1": {"Tenda": (-48, -52), "Archer": (-73, -74)},
  "Varanda - Zona 2": {"Tenda": (-52, -67), "Archer": (-54, -56)},
  "Varanda - Zona 3": {"Tenda": (-69, -71), "Archer": (-56, -61)},
  "Varanda - Zona 4": {"Tenda": (-71, -81), "Archer": (-53, -56)},
  "Varanda - Zona 5": {"Tenda": (-71, -81), "Archer": (-53, -56)},
  "Varanda - Zona 6": {"Tenda": (-69, -71), "Archer": (-58, 67)},
  "Varanda - Zona 7": {"Tenda": (-69, -71), "Archer": (-58, -67)},
  "Varanda - Zona 8": {"Tenda": (-67, -120), "Archer": (-58, -61)},
  "Banheiro": {"Tenda": (-31, -40), "Archer": (-67, -80)},
  "Sala - Zona 1": {"Tenda": (-57, -59), "Archer": (-66, -70)},
  "Sala - Zona 2": {"Tenda": (-61, -67), "Archer": (-57, -60)},
  "Sala - Zona 3": {"Tenda": (-66, 69), "Archer": (-51, -64)},
  "Sala - Zona 4": {"Tenda": (-68, -70), "Archer": (-46, -55)},
  "Corredor - Zona 1": {"Tenda": (-43, -48), "Archer": (-70, -72)},
  "Corredor - Zona 2": {"Tenda": (-57, -63), "Archer": (-66, -70)},
  "Corredor - Zona 3": {"Tenda": (-57, -63), "Archer": (-59, -69)},
  "Quarto 1": {"Tenda": (-57, -63), "Archer": (-64, -68)},
  "Quarto 2 - Zona 1": {"Tenda": (-67, -71), "Archer": (-19, -30)},
  "Quarto 2 - Zona 2": {"Tenda": (-71, -73), "Archer": (-30, -40)},
  "Quarto 2 - Zona 3": {"Tenda": (-68, -69), "Archer": (-45, -67)}
}


with open('resultados/rssi_por_zona.json', 'w') as f:
    json.dump(rssi_por_zona, f, indent=2)

print('Arquivo rssi_por_zona.json salvo com sucesso!')

# Escolher qual roteador visualizar ('Tenda' ou 'Archer')
roteador = 'Tenda'  # ou 'Archer'

# Função para escolher a cor conforme o RSSI
def cor_por_rssi(rssi_medio):
    if rssi_medio >= -60:
        return 'green' 
    elif rssi_medio >= -70:
        return 'yellow'  
    else:
        return 'red'  

# Criar figura
fig, ax = plt.subplots(figsize=(10, 15))
ax.imshow(img, extent=[0, 600, 0, 840])

for zona, pontos in zonas.items():
    rssi_range = rssi_por_zona.get(zona, {}).get(roteador, (-90, -90))
    rssi_medio = sum(rssi_range) / 2
    cor = cor_por_rssi(rssi_medio)
    poligono = patches.Polygon(pontos, closed=True, edgecolor='black', facecolor=cor, alpha=0.5, label=f'{zona}: {rssi_medio:.1f} dBm')
    ax.add_patch(poligono)

    xs, ys = zip(*pontos)
    centro_x = sum(xs) / len(xs)
    centro_y = sum(ys) / len(ys)
    ax.text(centro_x, centro_y, zona, ha='center', va='center', fontsize=8, color='black')

ax.axis('off')
plt.title(f'Mapa de RSSI - {roteador}', fontsize=16)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
plt.show()

fig.savefig(f'resultados/mapa_rssi_{roteador}.png', dpi=300, bbox_inches='tight')
