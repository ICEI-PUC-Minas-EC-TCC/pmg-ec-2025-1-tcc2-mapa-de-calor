import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches

# Carregar a imagem da planta
img = mpimg.imread('dados/A4-2.png')

# Criar a figura
fig, ax = plt.subplots(figsize=(10, 15))
ax.imshow(img, extent=[0, 600, 0, 840])

# Função para desenhar uma zona
def desenhar_zona(nome, pontos, cor):
    poligono = patches.Polygon(pontos, closed=True, edgecolor='black', facecolor=cor, alpha=0.5, label=nome)
    ax.add_patch(poligono)
    centro_x = sum(x for x, y in pontos) / len(pontos)
    centro_y = sum(y for x, y in pontos) / len(pontos)
    ax.text(centro_x, centro_y, nome, ha='center', va='center', fontsize=8, color='black')

# >>> Colei aqui seu novo zonas <<<
zonas = {
    'Escada - Zona 1': [(14, 828), (280, 828), (280, 759), (14, 759)],
    'Escada - Zona 2' : [(280, 828), (280, 759), (587, 759), (587, 828)],
    'Área Externa - Zona 1': [(14, 759), (145, 760), (145, 634), (14, 634)],
    'Área Externa - Zona 2': [(145, 760), (310, 760 ), (310, 634 ), (145, 634)],
    'Área Externa - Zona 3': [(310, 760), (504, 760), (504, 634), (310, 634)],
    'Cozinha - Zona 1': [(14, 634), (162, 634), (162, 504), (14, 504)],
    'Cozinha - Zona 2': [(162, 634), (325, 634), (325, 504), (162, 504)],
    'Cozinha - Zona 3': [(325, 634), (504, 634), (504, 504), (325, 504)],
    'Varanda - Zona 1': [(506, 759), (587, 759), (587, 621.2), (506, 621.2)],
    'Varanda - Zona 2': [(506, 621.2), (587, 621.2), (587, 483.4), (506, 483.4)],
    'Varanda - Zona 3': [(506, 483.4), (587, 483.4), (587, 345.6), (506, 345.6)],
    'Varanda - Zona 4': [(506, 345.6), (587, 345.6), (587, 207.8), (506, 207.8)],
    'Varanda - Zona 5': [(506, 207.8), (587, 207.8), (587, 70), (506, 70)],
    'Varanda - Zona 8': [(14, 69), (205.67, 69), (205.67, 9), (14, 9)],
    'Varanda - Zona 7': [(205.67, 69), (397.33, 69), (397.33, 9), (205.67, 9)],
    'Varanda - Zona 6': [(397.33, 69), (589, 69), (589, 9), (397.33, 9)],
    'Banheiro': [(162, 502), (504, 504),(504, 434), (162, 434)],
    'Sala - Zona 1': [(162, 433), (333, 433), (333, 339), (162, 339)],
    'Sala - Zona 2': [(333, 433), (504, 433), (504, 339), (333, 339)],
    'Sala - Zona 3': [(162, 339), (333, 339), (333, 245), (162, 245)],
    'Sala - Zona 4': [(333, 339), (504, 339), (504, 245), (333, 245)],
    'Corredor - Zona 1': [(14, 504), (162, 504), (162, 434), (14, 434)],
    'Corredor - Zona 2': [(14, 434), (162, 434), (162, 339), (14, 339)],
    'Corredor - Zona 3': [(14, 339), (162, 339), (162, 244), (14, 244)],
    'Quarto 1': [(14, 243), (261, 243), (259, 69), (14, 69)],
    'Quarto 2 - Zona 1': [(259, 245), (357, 245), (357, 157), (259, 157)],
    'Quarto 2 - Zona 2': [(357, 245), (504, 245), (504, 157), (357, 157)],
    'Quarto 2 - Zona 3': [(259, 157), (504, 157), (504, 69), (259, 69)],
}

# Cores para cada zona
cores = ['red', 'green', 'blue', 'yellow', 
         'purple', 'cyan', 'orange', 'pink', 
         'gray', 'lime', 'teal', 'brown', 
         'navy', 'violet', 'gold', 'coral', 
         'crimson','goldenrod','magenta',
        'deepskyblue','limegreen','firebrick',
        'orangered','hotpink','gold','dimgray',
        'aqua','royalblue','mediumseagreen']

# Desenhar cada zona
for (nome, pontos), cor in zip(zonas.items(), cores):
    desenhar_zona(nome, pontos, cor)

# Ajustes finais
ax.axis('off')
plt.title('Mapa Base das Zonas da Casa', fontsize=16)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
plt.show()

# (Opcional) Salvar o resultado
fig.savefig('resultados/zonas_base.png', dpi=300, bbox_inches='tight')

import json
with open('resultados/zonas_salvas.json', 'w') as f:
    json.dump(zonas, f, indent=2)

print('Arquivo zonas_salvas.json salvo com sucesso!')
