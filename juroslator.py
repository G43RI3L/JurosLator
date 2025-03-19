import json
import os

# Caminho do arquivo onde os dados serão salvos
ARQUIVO_HISTORICO = "historico_aplicacoes.json"

def salvar_aplicacao(tipo, principal, taxa, tempo, juros, montante_final, mensal):
    """Salva os dados da simulação em um arquivo JSON."""
    nova_entrada = {
        "tipo": tipo,
        "principal": principal,
        "taxa": taxa,
        "tempo": tempo,
        "juros": juros,
        "montante_final": montante_final,
        "mensal": mensal
    }

    # Carregar histórico existente (se houver)
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r") as file:
            try:
                historico = json.load(file)
            except json.JSONDecodeError:
                historico = []
    else:
        historico = []

    # Adicionar nova entrada e salvar de volta
    historico.append(nova_entrada)

    with open(ARQUIVO_HISTORICO, "w") as file:
        json.dump(historico, file, indent=4)

def exibir_historico():
    """Exibe as aplicações salvas."""
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r") as file:
            try:
                historico = json.load(file)
                if not historico:
                    print("Nenhuma aplicação registrada ainda.")
                    return
                
                print("\n📊 Histórico de Aplicações:")
                for idx, entrada in enumerate(historico, 1):
                    print(f"{idx}. {entrada['tipo']} - R$ {entrada['principal']:.2f} por {entrada['tempo']} períodos, Juros: R$ {entrada['juros']:.2f}, Final: R$ {entrada['montante_final']:.2f}")
            except json.JSONDecodeError:
                print("Erro ao carregar histórico.")
    else:
        print("Nenhuma aplicação registrada ainda.")

def calcular_juros_simples(principal, taxa, tempo):
    juros = principal * taxa * tempo
    montante_final = principal + juros
    mensal = juros / tempo
    return juros, montante_final, mensal

def calcular_juros_compostos(principal, taxa, tempo):
    montante_final = principal * (1 + taxa) ** tempo
    juros = montante_final - principal
    mensal = juros / tempo
    return juros, montante_final, mensal

def main():
    while True:
        print("\nCalculadora de Juros")
        print("1. Juros Simples")
        print("2. Juros Compostos")
        print("3. Ver Histórico de Aplicações")
        print("4. Sair")
        escolha = input("Digite uma opção (1-4): ")

        if escolha == "4":
            print("Saindo... Obrigado por usar a calculadora!")
            break

        if escolha == "3":
            exibir_historico()
            continue

        if escolha not in ["1", "2"]:
            print("Opção inválida. Por favor, escolha 1, 2, 3 ou 4.")
            continue

        principal = float(input("Digite o valor principal (capital inicial): "))
        taxa = float(input("Digite a taxa de juros (em %): ")) / 100
        tempo = float(input("Digite o tempo (período): "))

        if escolha == "1":
            juros, montante_final, mensal = calcular_juros_simples(principal, taxa, tempo)
            tipo = "Juros Simples"
        elif escolha == "2":
            juros, montante_final, mensal = calcular_juros_compostos(principal, taxa, tempo)
            tipo = "Juros Compostos"

        print(f"\n🔹 {tipo}:")
        print(f"Juros: R$ {juros:.2f}")
        print(f"Montante final: R$ {montante_final:.2f}")
        print(f"Valor médio por período: R$ {mensal:.2f}")

        salvar_aplicacao(tipo, principal, taxa, tempo, juros, montante_final, mensal)

if __name__ == "__main__":
    main()
