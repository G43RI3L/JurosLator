import os
import requests  # Biblioteca para fazer requisições HTTP
from flask import Flask, request, jsonify
from flask_cors import CORS

# Criando a aplicação Flask
app = Flask(__name__)
CORS(app)  # Permite que o front-end acesse a API

# Rota principal para testar a API
@app.route('/')
def home():
    return "API Flask funcionando no Render!"

# Função para obter a taxa SELIC atualizada do Banco Central
def obter_taxa_selic():
    """
    Consulta a API do Banco Central para obter a taxa SELIC mais recente.
    Retorna a taxa SELIC em formato decimal (exemplo: 0.1125 para 11,25%).
    """
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json"
    try:
        resposta = requests.get(url).json()
        return float(resposta[0]["valor"]) / 100  # Convertendo para decimal
    except:
        return None  # Retorna None caso a consulta falhe

# Rota para calcular os juros e comparar com a SELIC
@app.route('/calcular', methods=['POST'])
def calcular():
    """
    Recebe um JSON com:
    {
        "principal": valor inicial investido,
        "taxa": taxa de juros (%),
        "tempo": número de meses
    }

    Retorna um JSON com:
    {
        "juros": valor total dos juros,
        "montante_final": valor final acumulado,
        "comparacao_selic": mensagem comparando com a SELIC
    }
    """
    # Obtendo os dados da requisição
    dados = request.json
    principal = float(dados['principal'])
    taxa = float(dados['taxa']) / 100  # Convertendo % para decimal
    tempo = int(dados['tempo'])

    # Calculando juros compostos: M = P(1 + i)^t
    montante = principal * (1 + taxa) ** tempo
    juros = montante - principal

    # Obtendo a taxa SELIC atual
    taxa_selic = obter_taxa_selic()

    # Comparação com SELIC
    if taxa_selic is not None:
        montante_selic = principal * (1 + taxa_selic) ** tempo
        diferenca = ((montante / montante_selic) - 1) * 100

        if diferenca > 0:
            comparacao = f"Seu investimento foi {diferenca:.2f}% melhor que a SELIC."
        else:
            comparacao = f"Seu investimento foi {abs(diferenca):.2f}% pior que a SELIC."
    else:
        comparacao = "Não foi possível obter a taxa SELIC no momento."

    # Retornando os valores calculados no formato JSON
    return jsonify({
        "juros": round(juros, 2),
        "montante_final": round(montante, 2),
        "comparacao_selic": comparacao
    })

# Definição da porta e execução da aplicação
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
