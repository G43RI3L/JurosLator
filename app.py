import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Arquivo JSON para armazenar usuários e histórico
DB_FILE = "usuarios.json"

# Função para carregar os dados do JSON
def carregar_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

# Função para salvar os dados no JSON
def salvar_dados(dados):
    with open(DB_FILE, "w") as file:
        json.dump(dados, file, indent=4)

# Criar conta ou fazer login
@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint para criar ou logar um usuário.
    Espera um JSON com {"usuario": "nome", "senha": "senha"}.
    Se o usuário não existir, cria um novo.
    """
    dados = request.json
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if not usuario or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios!"}), 400

    db = carregar_dados()

    # Se o usuário já existe
    if usuario in db:
        if db[usuario]["senha"] != senha:
            return jsonify({"erro": "Senha incorreta!"}), 401
    else:
        # Criando novo usuário
        db[usuario] = {"senha": senha, "historico": []}
        salvar_dados(db)

    return jsonify({"mensagem": "Login bem-sucedido!", "usuario": usuario})

# Salvar aplicação no histórico do usuário
@app.route('/salvar', methods=['POST'])
def salvar():
    """
    Salva uma aplicação no histórico do usuário.
    Espera um JSON com {"usuario": "nome", "dados": {...detalhes da aplicação...}}.
    """
    dados = request.json
    usuario = dados.get("usuario")
    dados_aplicacao = dados.get("dados")

    db = carregar_dados()
    if usuario not in db:
        return jsonify({"erro": "Usuário não encontrado!"}), 404

    db[usuario]["historico"].append(dados_aplicacao)
    salvar_dados(db)
    
    return jsonify({"mensagem": "Aplicação salva com sucesso!"})

# Obter histórico de um usuário
@app.route('/historico/<usuario>', methods=['GET'])
def historico(usuario):
    """
    Retorna o histórico de aplicações do usuário.
    """
    db = carregar_dados()
    if usuario not in db:
        return jsonify({"erro": "Usuário não encontrado!"}), 404

    return jsonify({"historico": db[usuario]["historico"]})

# Apagar uma aplicação do histórico
@app.route('/apagar', methods=['POST'])
def apagar():
    """
    Remove uma aplicação específica do histórico.
    Espera um JSON com {"usuario": "nome", "indice": índice da aplicação}.
    """
    dados = request.json
    usuario = dados.get("usuario")
    indice = dados.get("indice")

    db = carregar_dados()
    if usuario not in db:
        return jsonify({"erro": "Usuário não encontrado!"}), 404

    try:
        db[usuario]["historico"].pop(indice)
        salvar_dados(db)
        return jsonify({"mensagem": "Aplicação apagada com sucesso!"})
    except IndexError:
        return jsonify({"erro": "Índice inválido!"}), 400

# Apagar todo o histórico
@app.route('/resetar', methods=['POST'])
def resetar():
    """
    Remove todas as aplicações do usuário.
    Espera um JSON com {"usuario": "nome"}.
    """
    dados = request.json
    usuario = dados.get("usuario")

    db = carregar_dados()
    if usuario not in db:
        return jsonify({"erro": "Usuário não encontrado!"}), 404

    db[usuario]["historico"] = []
    salvar_dados(db)

    return jsonify({"mensagem": "Histórico resetado!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
