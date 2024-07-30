def calcular_juros_simples(principal, taxa, tempo):
    juros = principal * taxa * tempo
    montante_final = principal + juros
    mensal = ( montante_final - principal ) / tempo
    return juros, montante_final, mensal

def calcular_juros_compostos(principal, taxa, tempo):
    montante_final = principal * (1 + taxa) ** tempo
    juros = montante_final - principal
    mensal = juros / tempo
    return juros, montante_final, mensal

def main():
    print("Calculadora de Juros")
    print("Escolha o tipo de juros:")
    print("1. Juros Simples")
    print("2. Juros Compostos")
    escolha = int(input("Digite 1 ou 2: "))

    principal = float(input("Digite o valor principal (capital inicial): "))
    taxa = float(input("Digite a taxa de juros (em %): ")) / 100
    tempo = float(input("Digite o tempo (período): "))
    #mensal = juros / tempo

    if escolha == 1:
        juros, montante_final, mensal = calcular_juros_simples(principal, taxa, tempo)
        print(f"Os juros simples são: R$ {juros:.2f}")
        print(f"O montante final após juros simples é: R$ {montante_final:.2f} e a cada período é: R$ {mensal:.2f}")
    elif escolha == 2:
        juros, montante_final, mensal = calcular_juros_compostos(principal, taxa, tempo)
        print(f"Os juros compostos são: R$ {juros:.2f}")
        print(f"O montante final após juros compostos é: R$ {montante_final:.2f} e a cada período é: R$ {mensal:.2f}")
    else:
        print("Opção inválida. Por favor, escolha 1 ou 2.")

if __name__ == "__main__":
    main()
