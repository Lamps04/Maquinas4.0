import os
import random
import time
from datetime import datetime
import matplotlib.pyplot as plt 


# Limites operacionais padrão
TEMP_LIMITE = 75.0
UMIDADE_LIMITE = 60.0

# Lista de máquinas monitoradas
maquinas = ["Compressor Central", "Robô Soldador", "Esteira Transportadora"]

# Armazenamento de dados para estatísticas
dados = {maquina: {"temperatura": [], "umidade": [], "alertas": 0, "eficiencia": []} for maquina in maquinas}

def configurar_limites():
    """
    Permite ao usuário definir os limites críticos de temperatura e umidade.
    """
    global TEMP_LIMITE, UMIDADE_LIMITE
    try:
        TEMP_LIMITE = float(input("Digite o limite máximo de temperatura (°C): "))
        UMIDADE_LIMITE = float(input("Digite o limite máximo de umidade (%): "))
        print(f"Limites ajustados: Temp={TEMP_LIMITE}°C, Umid={UMIDADE_LIMITE}%\n")
    except ValueError:
        print("Entrada inválida. Usando limites padrão.\n")

def gerar_dados_sensor():
    """
    Gera valores simulados para sensores de temperatura, umidade e eficiência.
    """
    temperatura = round(random.uniform(20, 100), 2)
    umidade = round(random.uniform(30, 70), 2)
    eficiencia = round(random.uniform(70, 100), 2)
    status = "OK" if temperatura <= TEMP_LIMITE and umidade <= UMIDADE_LIMITE else "ALERTA"
    return temperatura, umidade, eficiencia, status

def registrar_log(maquina, temperatura, umidade, eficiencia, status):
    """
    Registra os dados no arquivo de log e atualiza os dados para estatísticas.
    """
    dados[maquina]["temperatura"].append(temperatura)
    dados[maquina]["umidade"].append(umidade)
    dados[maquina]["eficiencia"].append(eficiencia)
    if status == "ALERTA":
        dados[maquina]["alertas"] += 1

    with open("log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {maquina}: Temp={temperatura}°C, Umid={umidade}%, Efic={eficiencia}%, Status={status}\n")

def exibir_status():
    """
    Exibe os dados no terminal e os registra no log.
    """
    print("=== Monitoramento em Tempo Real ===")
    for maquina in maquinas:
        temperatura, umidade, eficiencia, status = gerar_dados_sensor()
        desempenho = "Desempenho Baixo" if eficiencia < 80 else "Desempenho OK"
        print(f"{maquina}: Temp={temperatura}°C, Umid={umidade}%, Efic={eficiencia}%, Status={status}, {desempenho}")
        registrar_log(maquina, temperatura, umidade, eficiencia, status)
    print("-" * 50)

def exibir_estatisticas():
    """
    Exibe as estatísticas consolidadas ao encerrar o monitoramento.
    """
    print("\n=== Estatísticas Consolidadas ===")
    for maquina, valores in dados.items():
        media_temp = round(sum(valores["temperatura"]) / len(valores["temperatura"]), 2)
        media_umid = round(sum(valores["umidade"]) / len(valores["umidade"]), 2)
        total_alertas = valores["alertas"]
        print(f"{maquina}: Média Temp={media_temp}°C, Média Umid={media_umid}%, Alertas={total_alertas}")
    print("-" * 50)
    
def gerar_grafico():
    """
    Gera gráficos separados para temperatura e umidade e salva-os na pasta 'Gráficos',
    com nomes únicos baseados em timestamp.
    """
    # Verifica e cria a pasta 'Gráficos' se não existir
    pasta_graficos = "Gráficos"
    if not os.path.exists(pasta_graficos):
        os.makedirs(pasta_graficos)

    # Gera timestamp para nomes únicos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Gráfico de Temperatura
    plt.figure(figsize=(10, 5))
    for maquina, valores in dados.items():
        plt.plot(
            valores["temperatura"],
            label=f"{maquina}",
            marker="o",
        )
    plt.title("Evolução da Temperatura nas Máquinas")
    plt.xlabel("Ciclos de Monitoramento")
    plt.ylabel("Temperatura (°C)")
    plt.axhline(y=TEMP_LIMITE, color="red", linestyle="--", label="Limite Crítico")
    plt.legend(title="Máquinas")
    plt.grid(True, linestyle="--", alpha=0.7)
    caminho_temperatura = os.path.join(pasta_graficos, f"grafico_temperatura_{timestamp}.png")
    plt.savefig(caminho_temperatura)
    print(f"\nGráfico de Temperatura gerado: '{caminho_temperatura}'\n")

    # Gráfico de Umidade
    plt.figure(figsize=(10, 5))
    for maquina, valores in dados.items():
        plt.plot(
            valores["umidade"],
            label=f"{maquina}",
            marker="s",
        )
    plt.title("Evolução da Umidade nas Máquinas")
    plt.xlabel("Ciclos de Monitoramento")
    plt.ylabel("Umidade (%)")
    plt.axhline(y=UMIDADE_LIMITE, color="blue", linestyle="--", label="Limite Crítico")
    plt.legend(title="Máquinas")
    plt.grid(True, linestyle="--", alpha=0.7)
    caminho_umidade = os.path.join(pasta_graficos, f"grafico_umidade_{timestamp}.png")
    plt.savefig(caminho_umidade)
    print(f"Gráfico de Umidade gerado: '{caminho_umidade}'\n")



# Execução do programa
print("Bem-vindo ao Simulador de Monitoramento da Indústria 4.0!")
print("Configuração inicial...")
configurar_limites()

print("Iniciando o monitoramento da linha de produção...\n")
try:
    while True:
        exibir_status()
        time.sleep(3)
except KeyboardInterrupt:
    print("\nMonitoramento encerrado pelo usuário.\n")
    exibir_estatisticas()
    gerar_grafico()
