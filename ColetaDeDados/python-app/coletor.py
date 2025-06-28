import pyshark
from datetime import datetime
import time
import os
import hashlib

print("Aguardando captura iniciar...")
time.sleep(3)

# Caminho de saída do arquivo txt
saida_txt = "output/dados.txt"

# MACs dos 6 dispositivos visíveis no TCC (sem anonimização)
macs_visiveis = {
    "52:9f:14:d9:81:25": "Archer",
    "30:cc:21:14:be:83": "Archer",
    "56:4b:54:3b:84:8f": "Archer",
    "50:8a:06:fc:81:4d": "Tenda",
    "22:55:7e:84:10:17": "Tenda",
    "4a:e9:21:8b:e1:ce": "Tenda"
}

# Função para anonimizar MACs desconhecidos
def anonimizar_mac(mac):
    return hashlib.sha256(mac.encode()).hexdigest()[:12]

try:
    # Garante que o diretório de saída exista
    os.makedirs("output", exist_ok=True)

    # Lê o arquivo .pcap da pasta correspondente
    capture = pyshark.FileCapture('pcap/captura.pcap')

    with open(saida_txt, "a") as f:
        count = 0
        for pkt in capture:
            try:
                mac = pkt.wlan.ta.lower()
                rssi = int(pkt.radiotap.dbm_antsignal)
                timestamp = pkt.sniff_time

                # Mantém MAC original apenas se estiver na lista dos 6 visíveis
                mac_exibido = mac if mac in macs_visiveis else anonimizar_mac(mac)

                # Força SSID como "N/A" sempre
                linha = f"{timestamp} | {mac_exibido} | N/A | {rssi} dBm\n"
                print(linha.strip())
                f.write(linha)
                count += 1

            except AttributeError:
                continue  # Ignora pacotes incompletos

    print(f"[✓] Total de registros salvos em '{saida_txt}': {count}")

except Exception as e:
    print(f"[!] Erro ao processar captura: {e}")

finally:
    if 'capture' in locals():
        capture.close()
