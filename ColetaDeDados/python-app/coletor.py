import pyshark
from datetime import datetime
import time
import os

print("Aguardando captura iniciar...")
time.sleep(3)

# Caminho de saída do arquivo txt
saida_txt = "output/dados.txt"

# MACs conhecidos dos APs (adicione os reais abaixo)
macs_aps = {
    "B4:0F:3B:FA:66:30": "Tenda (Principal)",
    "50:C7:BF:EF:76:14": "TP-Link Archer C20"
}

try:
    # Garante que o diretório exista (dentro do projeto)
    os.makedirs("output", exist_ok=True)

    # Lê o arquivo pcap
    capture = pyshark.FileCapture('pcap/captura.pcap')

    with open(saida_txt, "a") as f:
        count = 0
        for pkt in capture:
            try:
                mac = pkt.wlan.ta.lower()
                ssid = pkt.wlan.ssid if hasattr(pkt.wlan, 'ssid') else "N/A"
                rssi = int(pkt.radiotap.dbm_antsignal)
                timestamp = pkt.sniff_time

                origem = macs_aps.get(mac, "Cliente desconhecido")

                linha = f"{timestamp} | {mac} | {ssid} | {rssi} dBm | Origem: {origem}\n"
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
