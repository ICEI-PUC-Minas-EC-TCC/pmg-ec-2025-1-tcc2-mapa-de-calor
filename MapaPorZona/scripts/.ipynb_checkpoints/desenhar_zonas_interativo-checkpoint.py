import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json

# Carregar a imagem
img = mpimg.imread('dados/A4-2.png')

# Configurações iniciais
fig, ax = plt.subplots(figsize=(10, 15))
ax.imshow(img, extent=[0, 600, 0, 840])
ax.set_title('Clique para marcar os pontos da área. Feche a janela quando terminar.')

# Lista para guardar todas as zonas
zonas = {}
# Lista para guardar pontos da zona atual
pontos_atuais = []

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        print(f'Clicado: ({event.xdata:.2f}, {event.ydata:.2f})')
        pontos_atuais.append((event.xdata, event.ydata))
        ax.plot(event.xdata, event.ydata, 'ro')  # Marca ponto em vermelho
        fig.canvas.draw()

def onkey(event):
    if event.key == 'enter':
        nome = input('Digite o nome da área que você acabou de desenhar: ')
        zonas[nome] = pontos_atuais.copy()
        pontos_atuais.clear()
        print(f'Área "{nome}" salva! Continue clicando para a próxima área ou feche a janela.')

# Conectar eventos
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', onkey)

plt.show()

# Depois que fechar a janela, salvar os dados
with open('zonas_salvas.json', 'w') as f:
    json.dump(zonas, f, indent=2)

print('Zonas salvas no arquivo zonas_salvas.json.')
