# Carregar pacotes
library(igraph)
library(ggraph)
library(ggplot2)
library(readr)
library(magick)

# Definir o diretório onde estão os arquivos
setwd("C:/Users/joaom/Desktop/")  # <- Caminho onde estão a imagem e o CSV

# Carregar a planta baixa como imagem
planta <- image_read("A4 - 2.png")

# Carregar a matriz de RSSI
matriz_rssi <- read_csv("modelo_matriz_rssi.csv")

# Criar o grafo manualmente com base nas áreas
vertices <- unique(matriz_rssi$Área)

# Criar as arestas básicas (ligações entre áreas principais)
arestas <- data.frame(
  from = c("Cozinha", "Sala", "Corredor", "Banheiro", "Quarto 1", "Quarto 2", "Varanda", "Escada", "Area Externa"),
  to   = c("Corredor", "Corredor", "Quarto 1", "Sala", "Varanda", "Varanda", "Area Externa", "Area Externa", "Escada")
)

# Criar objeto de grafo
g <- graph_from_data_frame(arestas, vertices = data.frame(name = vertices))

# Definir atributos de RSSI
V(g)$rssi_tenda <- matriz_rssi$`RSSI_Tenda (dBm)`
V(g)$rssi_archer <- matriz_rssi$`RSSI_Archer (dBm)`

# Plotar o grafo sobre a planta
ggplot() +
  annotation_custom(rasterGrob(planta, width = unit(1, "npc"), height = unit(1, "npc")), 
                    -Inf, Inf, -Inf, Inf) +
  ggraph(g, layout = 'kk') + 
  geom_edge_link(aes(start_cap = label_rect(node1.name), end_cap = label_rect(node2.name)), edge_width = 0.8) +
  geom_node_point(aes(color = as.numeric(gsub("[^0-9]", "", rssi_tenda))), size = 5) +
  geom_node_text(aes(label = name), repel = TRUE, vjust = 1.5) +
  scale_color_gradient(low = "red", high = "green") +
  theme_void() +
  ggtitle("Mapa de Potência de Sinal (RSSI) sobre Planta Baixa")
