# Importando bibliotecas necessárias
from flask import Flask, request, jsonify  # Flask para criar a API
from flask_cors import CORS  # Permite requisições de outras origens (ex: frontend)
import os  

# Criando a aplicação Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para evitar bloqueios de segurança ao conectar com o front-end

# Definindo a rota para calcular os juros
@app.route('/calcular', methods=['POST'])
def calcular():
    """
    Endpoint que recebe os dados do usuário via POST e calcula os juros compostos.
    Espera receber um JSON com:
    - "principal": valor inicial investido
    - "taxa": taxa de juros ao mês (%)
    - "tempo": número de meses

    Retorna um JSON com:
    - "juros": valor total dos juros
    - "montante_final": valor final acumulado
    """
    dados = request.json  # Obtém os dados enviados pelo usuário (JSON)
    
    # Pegando valores do JSON e convertendo para número
    principal = float(dados['principal'])
    taxa = float(dados['taxa']) / 100  # Convertendo % para decimal
    tempo = int(dados['tempo'])

    # Calculando o montante final usando a fórmula de juros compostos: M = P(1 + i)^t
    montante = principal * (1 + taxa) ** tempo
    juros = montante - principal  # Juros é o valor acumulado menos o inicial

    # Retorna os valores em formato JSON para o front-end
    return jsonify({"juros": juros, "montante_final": montante})

# Executa o servidor Flask em modo debug
if __name__ == '__main__':
    app.run(debug=True)



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Define a porta do Render
    app.run(host="0.0.0.0", port=port, debug=True)
