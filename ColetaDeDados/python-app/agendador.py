import subprocess

ip_router = "192.168.1.1"
usuario = "root"
arquivo_remoto = "/captura.pcap"
arquivo_local = "/home/joaom/projetos/coleta-de-dados-de-redes/pcap/captura.pcap"
duracao = 60  # 5 minutos de captura

# Comando de captura sem limite de tamanho
comando_captura = (
    f'ssh {usuario}@{ip_router} "tcpdump -i mon0 -G {duracao} -W 1 -w {arquivo_remoto}"'
)

# Comando para baixar o arquivo via scp (com -O)
comando_scp = f"scp -O {usuario}@{ip_router}:{arquivo_remoto} {arquivo_local}"

print("[*] Iniciando captura no roteador...")
subprocess.run(comando_captura, shell=True)

print("[*] Baixando arquivo capturado para o host...")
subprocess.run(comando_scp, shell=True)

print("[*] Processando com PyShark...")
subprocess.run("docker-compose run --rm app", shell=True)

print("[✓] Concluído.")
