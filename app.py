# Importando bibliotecas necessárias
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "API Flask funcionando no Render!"

@app.route('/calcular', methods=['POST'])
def calcular():
    """Calcula juros compostos"""
    dados = request.json
    principal = float(dados['principal'])
    taxa = float(dados['taxa']) / 100
    tempo = int(dados['tempo'])

    montante = principal * (1 + taxa) ** tempo
    juros = montante - principal

    return jsonify({"juros": juros, "montante_final": montante})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Define a porta correta para Render
    app.run(host="0.0.0.0", port=port)  # Permite conexões externas
