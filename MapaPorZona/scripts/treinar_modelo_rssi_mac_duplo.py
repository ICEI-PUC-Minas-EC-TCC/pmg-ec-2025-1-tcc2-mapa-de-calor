
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import json

# === Arquivos ===
ARQUIVO_DADOS = "dados/dados.csv"
ARQUIVO_ZONAS = "resultados/rssi_por_zona.json"
ARQUIVO_MODELO = "resultados/modelo_rssi_tensorflow.keras"

# === MACs mapeados ===
mac_para_roteador = {
    "52:9f:14:d9:81:25": "Archer",
    "30:cc:21:14:be:83": "Archer",
    "56:4b:54:3b:84:8f": "Archer",
    "50:8a:06:fc:81:4d": "Tenda",
    "22:55:7e:84:10:17": "Tenda",
    "4a:e9:21:8b:e1:ce": "Tenda"
}

# === Carregar zonas e RSSI ===
with open(ARQUIVO_ZONAS, "r") as f:
    rssi_por_zona = json.load(f)

# === Carregar dados reais ===
df = pd.read_csv(ARQUIVO_DADOS)
df = df[['mac', 'rssi']]
df['rssi'] = pd.to_numeric(df['rssi'], errors='coerce')
df['mac'] = df['mac'].str.lower()
df.dropna(inplace=True)
df = df[(df['rssi'] >= -100) & (df['rssi'] <= -10)]

# === Estimar zona para cada registro ===
def estimar_zona(row):
    mac = row['mac']
    rssi = row['rssi']
    roteador = mac_para_roteador.get(mac)
    if not roteador:
        return None
    melhor_zona = None
    menor_dif = float('inf')
    for zona, valores in rssi_por_zona.items():
        if roteador in valores:
            rssi_med = sum(valores[roteador]) / 2
            dif = abs(rssi - rssi_med)
            if dif < menor_dif:
                menor_dif = dif
                melhor_zona = zona
    return melhor_zona

df['zona'] = df.apply(estimar_zona, axis=1)
df.dropna(inplace=True)
print(f"Total de amostras com zona estimada: {len(df)}")

# === Montar X e y ===
X_data = []
y_labels = []
for _, row in df.iterrows():
    mac = row['mac']
    rssi = row['rssi']
    roteador = mac_para_roteador.get(mac)
    if roteador == "Tenda":
        X_data.append([rssi, -100])
    elif roteador == "Archer":
        X_data.append([-100, rssi])
    else:
        continue
    y_labels.append(row['zona'])

# === Pré-processamento ===
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y_labels)

scaler = MinMaxScaler()
X = scaler.fit_transform(X_data)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# === Modelo TensorFlow ===
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(2,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(set(y_encoded)), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=50, batch_size=8, validation_split=0.1)

loss, acc = model.evaluate(X_test, y_test)
print(f"Acurácia no teste: {acc*100:.2f}%")

# === Salvar modelo ===
model.save(ARQUIVO_MODELO)
print(f"Modelo salvo em '{ARQUIVO_MODELO}'")
