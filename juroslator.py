from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Pode ser alterado para PostgreSQL no Render
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta'

# Inicializando módulos
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Modelos do Banco de Dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    principal = db.Column(db.Float, nullable=False)
    taxa = db.Column(db.Float, nullable=False)
    tempo = db.Column(db.Integer, nullable=False)
    montante = db.Column(db.Float, nullable=False)
    selic_diferenca = db.Column(db.Float, nullable=False)

# Criar Banco de Dados
db.create_all()

# Rota de Registro
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuário registrado com sucesso!'})

# Rota de Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        return jsonify({'token': access_token})
    return jsonify({'message': 'Credenciais inválidas'}), 401

# Rota para Cálculo e Armazenamento
@app.route('/calcular', methods=['POST'])
@jwt_required()
def calcular():
    data = request.json
    user_id = get_jwt_identity()
    principal = data['principal']
    taxa = data['taxa'] / 100
    tempo = data['tempo']
    montante = principal * (1 + taxa) ** tempo
    
    # Comparação com SELIC
    selic_taxa = 0.1325  # Exemplo fixo, substituir por taxa dinâmica depois
    montante_selic = principal * (1 + selic_taxa) ** tempo
    selic_diferenca = ((montante / montante_selic) - 1) * 100
    
    new_calc = Calculation(user_id=user_id, principal=principal, taxa=data['taxa'], tempo=tempo, 
                           montante=montante, selic_diferenca=selic_diferenca)
    db.session.add(new_calc)
    db.session.commit()
    
    return jsonify({'montante_final': montante, 'comparacao_selic': selic_diferenca})

# Rota para Recuperar Histórico
@app.route('/historico', methods=['GET'])
@jwt_required()
def historico():
    user_id = get_jwt_identity()
    historico = Calculation.query.filter_by(user_id=user_id).all()
    historico_lista = [{
        'id': h.id, 'principal': h.principal, 'taxa': h.taxa,
        'tempo': h.tempo, 'montante': h.montante, 'selic_diferenca': h.selic_diferenca
    } for h in historico]
    return jsonify(historico_lista)

# Rota para Excluir Cálculo
@app.route('/delete/<int:calc_id>', methods=['DELETE'])
@jwt_required()
def delete(calc_id):
    user_id = get_jwt_identity()
    calc = Calculation.query.filter_by(id=calc_id, user_id=user_id).first()
    if not calc:
        return jsonify({'message': 'Cálculo não encontrado'}), 404
    db.session.delete(calc)
    db.session.commit()
    return jsonify({'message': 'Cálculo removido com sucesso'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Porta configurável para Render
