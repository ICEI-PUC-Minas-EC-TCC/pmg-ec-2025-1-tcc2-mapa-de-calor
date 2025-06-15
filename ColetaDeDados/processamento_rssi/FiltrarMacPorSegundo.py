

from datetime import datetime
import re

input_file = 'dados.txt'  
output_file = 'dados_filtrados.txt'  


ultimos_registros = {}

linhas_filtradas = []

padrao_linha = re.compile(r'^(.*?) \| (.*?) \| (.*?) \| (.*?) \|')

with open(input_file, 'r') as f:
    linhas = f.readlines()

for linha in linhas:
    match = padrao_linha.match(linha)
    if match:
        timestamp_str, mac, ssid, rssi = match.groups()
        timestamp = datetime.strptime(timestamp_str.strip(), '%Y-%m-%d %H:%M:%S.%f')
        segundo_chave = timestamp.replace(microsecond=0)  # tira os microssegundos

        chave = (mac, segundo_chave)

        if chave not in ultimos_registros:
            ultimos_registros[chave] = linha
            linhas_filtradas.append(linha)

with open(output_file, 'w') as f:
    f.writelines(linhas_filtradas)

print(f'Arquivo {output_file} gerado com sucesso com {len(linhas_filtradas)} registros.')
