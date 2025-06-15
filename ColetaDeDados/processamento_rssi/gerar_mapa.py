import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import re

# ====== CONFIGURAÇÕES DO PROJETO ======

# Caminho para a imagem da planta baixa
caminho_imagem = 'dados/A4-2.png'

# Caminho para a planilha CSV com dados de RSSI
caminho_csv = 'dados/modelo_matriz_rssi.csv'

# ====== CARREGAMENTO DOS DADOS ======

# Carrega a imagem da planta
img = mpimg.imread(caminho_imagem)

# Carrega a matriz de RSSI
matriz_rssi = pd.read_csv(caminho_csv)

# ====== DEFINIÇÃO MANUAL DAS POSIÇÕES (x, y) DE CADA SUBZONA ======

# Mapa de posições aproximadas para cada subzona
posicoes = {
    'Escada 1': (50, 800),
    'Escada 2': (70, 780),
    'Escada 3': (90, 760),
    'Area Externa 1': (500, 800),
    'Area Externa 2': (520, 780),
    'Cozinha 1': (300, 600),
    'Cozinha 2': (320, 580),
    'Cozinha 3': (340, 560),
    'Banheiro 1': (450, 500),
    'Banheiro 2': (470, 480),
    'Banheiro 3': (490, 460),
    'Banheiro 4': (510, 440),
    'Corredor 1': (200, 500),
    'Corredor 2': (220, 480),
    'Corredor 3': (240, 460),
    'Corredor 4': (260, 440),
    'Quarto Azul 1': (400, 300),
    'Quarto Azul 2': (420, 280),
    'Quarto Azul 3': (440, 260),
    'Quarto Vermelho 1': (500, 300),
    'Quarto Vermelho 2': (520, 280),
    'Quarto Vermelho 3': (540, 260),
    'Quarto Vermelho 4': (560, 240),
    'Sala 1': (300, 400),
    'Sala 2': (320, 380),
    'Sala 3': (340, 360),
    'Sala 4': (360, 340),
    'Varanda 1': (400, 200),
    'Varanda 2': (420, 180),
    'Varanda 3': (440, 160),
    'Varanda 4': (460, 140),
    'Varanda 5': (480, 120),
    'Varanda 6': (500, 100)
}

# ====== PLOTAGEM ======

# Cria a figura
fig, ax = plt.subplots(figsize=(10, 15))

# Mostra a imagem da planta
ax.imshow(img, extent=[0, 600, 0, 840])  # Extensão baseada na resolução da imagem

# Plotar os pontos
for idx, row in matriz_rssi.iterrows():
    subzona = row['Subzona']
    if subzona in posicoes:
        x, y = posicoes[subzona]

        # Interpretar a cor baseada no RSSI (Tenda)
        rssi = row['RSSI_Tenda (dBm)']
        rssi_texto = str(rssi)
        numeros_encontrados = re.findall(r'\d+', rssi_texto)
        if numeros_encontrados:
            rssi_val = int(numeros_encontrados[0])

            # Escolher a cor
            if rssi_val >= 70:
                cor = 'green'
            elif rssi_val >= 60:
                cor = 'yellow'
            else:
                cor = 'red'

            # Plotar o ponto
            ax.scatter(x, y, color=cor, s=300, edgecolors='black')
            ax.text(x, y+10, subzona, color='black', ha='center', fontsize=8)

# Ajustes finais
ax.axis('off')
plt.title('Mapa Visual de RSSI sobre Planta Baixa', fontsize=16)

# Mostrar o mapa
plt.show()

# (Opcional) Salvar o resultado
fig.savefig('resultados/mapa_gerado.png', dpi=300)