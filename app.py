import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importando o CORS corretamente

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Permite requisições de qualquer origem (GitHub Pages, etc.)

@app.route('/')
def home():
    return "API Flask funcionando no Render!"

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    principal = float(dados['principal'])
    taxa = float(dados['taxa']) / 100
    tempo = int(dados['tempo'])

    montante = principal * (1 + taxa) ** tempo
    juros = montante - principal

    taxa_selic = obter_taxa_selic()

    if taxa_selic is not None:
        montante_selic = principal * (1 + taxa_selic) ** tempo
        diferenca = ((montante / montante_selic) - 1) * 100
        comparacao = f"Seu investimento foi {diferenca:.2f}% melhor que a SELIC." if diferenca > 0 else f"Seu investimento foi {abs(diferenca):.2f}% pior que a SELIC."
    else:
        comparacao = "Não foi possível obter a taxa SELIC no momento."

    return jsonify({
        "juros": round(juros, 2),
        "montante_final": round(montante, 2),
        "comparacao_selic": comparacao
    })

def obter_taxa_selic():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json"
    try:
        resposta = requests.get(url).json()
        return float(resposta[0]["valor"]) / 100
    except:
        return None

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
