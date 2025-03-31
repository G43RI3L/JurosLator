import json
import os
import requests  # Biblioteca para fazer requisições HTTP

# Nome do arquivo onde vamos salvar as aplicações registradas
ARQUIVO_HISTORICO = "historico_aplicacoes.json"

def obter_taxa_selic():
    """ Obtém automaticamente a taxa SELIC atual do Banco Central. """
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json"
    try:
        resposta = requests.get(url).json()
        return float(resposta[0]["valor"]) / 100  # Convertendo para formato decimal
    except:
        return None  # Retorna None caso haja erro na requisição

def salvar_aplicacao(tipo, principal, taxa, tempo, juros, montante_final, mensal, selic_comparacao):
    """ Salva os dados da aplicação no arquivo JSON para manter histórico. """
    nova_entrada = {
        "tipo": tipo,
        "principal": principal,
        "taxa": taxa,
        "tempo": tempo,
        "juros": juros,
        "montante_final": montante_final,
        "mensal": mensal,
        "comparacao_selic": selic_comparacao
    }

    # Se o arquivo já existir, carrega os dados, senão cria um novo histórico
    historico = []
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r") as file:
            try:
                historico = json.load(file)
            except json.JSONDecodeError:
                pass  # Caso o arquivo esteja vazio ou com erro, ignora

    # Adiciona a nova aplicação ao histórico e salva no arquivo
    historico.append(nova_entrada)
    with open(ARQUIVO_HISTORICO, "w") as file:
        json.dump(historico, file, indent=4)

def calcular_juros_simples(principal, taxa, tempo):
    """ Calcula os juros simples com a fórmula J = P * i * t. """
    juros = principal * taxa * tempo
    montante_final = principal + juros
    mensal = juros / tempo
    return juros, montante_final, mensal

def calcular_juros_compostos(principal, taxa, tempo):
    """ Calcula os juros compostos com a fórmula M = P(1 + i)^t. """
    montante_final = principal * (1 + taxa) ** tempo
    juros = montante_final - principal
    mensal = juros / tempo
    return juros, montante_final, mensal

def comparar_com_selic(montante_final, principal, tempo):
    """ Compara os rendimentos com a taxa SELIC para dizer se foi um investimento melhor ou pior. """
    taxa_selic = obter_taxa_selic()
    if taxa_selic is None:
        return "Não foi possível obter a taxa SELIC."

    # Simulação de investimento com SELIC
    montante_selic = principal * (1 + taxa_selic) ** tempo
    diferenca = ((montante_final / montante_selic) - 1) * 100  # Diferença percentual

    if diferenca > 0:
        return f"Seu investimento foi {diferenca:.2f}% melhor que a SELIC."
    else:
        return f"Seu investimento foi {abs(diferenca):.2f}% pior que a SELIC."

def main():
    """ Menu principal para calcular juros e visualizar o histórico. """
    while True:
        print("\nCalculadora de Juros")
        print("1. Juros Simples")
        print("2. Juros Compostos")
        print("3. Ver Histórico de Aplicações")
        print("4. Sair")
        escolha = input("Digite uma opção (1-4): ")

        if escolha == "4":
            print("Saindo... Obrigado!")
            break

        if escolha == "3":
            with open(ARQUIVO_HISTORICO, "r") as file:
                print(json.dumps(json.load(file), indent=4))
            continue

        if escolha not in ["1", "2"]:
            print("Opção inválida.")
            continue

        # Entrada de dados
        principal = float(input("Valor inicial: "))
        taxa = float(input("Taxa de juros (%): ")) / 100
        tempo = float(input("Tempo (meses): "))

        # Escolha entre juros simples e compostos
        if escolha == "1":
            juros, montante_final, mensal = calcular_juros_simples(principal, taxa, tempo)
            tipo = "Juros Simples"
        else:
            juros, montante_final, mensal = calcular_juros_compostos(principal, taxa, tempo)
            tipo = "Juros Compostos"

        # Comparação com SELIC
        comparacao = comparar_com_selic(montante_final, principal, tempo)

        print(f"\n🔹 {tipo}:")
        print(f"Juros: R$ {juros:.2f}")
        print(f"Montante final: R$ {montante_final:.2f}")
        print(f"Comparação com SELIC: {comparacao}")

        # Salvar no histórico
        salvar_aplicacao(tipo, principal, taxa, tempo, juros, montante_final, mensal, comparacao)

if __name__ == "__main__":
    main()
