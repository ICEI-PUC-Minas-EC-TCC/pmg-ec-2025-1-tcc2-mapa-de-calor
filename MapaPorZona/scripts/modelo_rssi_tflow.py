import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import json
import pandas as pd

# === Carregar zonas de RSSI ===
with open("resultados/rssi_por_zona.json", "r") as f:
    rssi_zonas = json.load(f)

# === MACs por roteador ===
mac_para_roteador = {
    "52:9F:14:D9:81:25": "Archer",
    "30:cc:21:14:be:83": "Archer",
    "56:4b:54:3b:84:8f": "Archer",
    "50:8a:06:fc:81:4d": "Tenda",
    "22:55:7E:84:10:17": "Tenda",
    "4A:E9:21:8B:E1:CE": "Tenda"
}

# === Carregar dados reais ===
df = pd.read_csv("dados/dados.csv")
df['rssi'] = df['rssi'].astype(float)
df['roteador'] = df['mac'].map(mac_para_roteador)
df.dropna(subset=['roteador'], inplace=True)

# === Estimar zona mais próxima com base no RSSI e roteador ===
def estimar_zona(row):
    rssi = row['rssi']
    roteador = row['roteador']
    menor_diferenca = float('inf')
    melhor_zona = None

    for zona, valores in rssi_zonas.items():
        if roteador in valores:
            minimo, maximo = valores[roteador]
            media = (minimo + maximo) / 2
            diferenca = abs(rssi - media)
            if diferenca < menor_diferenca:
                menor_diferenca = diferenca
                melhor_zona = zona

    return melhor_zona

df['zona'] = df.apply(estimar_zona, axis=1)
df.dropna(subset=['zona'], inplace=True)

# === Preparar dados para treino ===
X_data = []
y_labels = []

for mac in df['mac'].unique():
    mac_df = df[df['mac'] == mac]
    r = mac_para_roteador.get(mac)
    if not r:
        continue
    for i, row in mac_df.iterrows():
        rssi_tenda = row['rssi'] if r == 'Tenda' else -90
        rssi_archer = row['rssi'] if r == 'Archer' else -90
        X_data.append([rssi_tenda, rssi_archer])
        y_labels.append(row['zona'])

print(f"Total de amostras reais: {len(X_data)}")

# === Modelagem com TensorFlow ===
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y_labels)

scaler = MinMaxScaler()
X = scaler.fit_transform(X_data)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

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

model.save("resultados/modelo_rssi_tensorflow.keras")
print("Modelo salvo em 'resultados/modelo_rssi_tensorflow.keras'")
