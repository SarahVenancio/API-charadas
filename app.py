from flask import Flask, jsonify, request
import random
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

#Pega a variável de ambiente e converte para JSON
FBKEY = json.loads(os.getenv('CONFIG_FIREBASE'))

cred = credentials.Certificate(FBKEY)
firebase_admin.initialize_app(cred)

#Conexão com o Firestore da Firebase
db = firestore.client()



#ROTA PRINCIPAL DE TESTE
@app.route('/')
def index():
    return 'API - CHARADAS'

#MÉTODO GET - CHARADA ALEATÓRIA
@app.route('/charadas', methods=['GET'])
def charada_aleatoria():
    charadas = []
    lista = db.collection('charadas').stream()

    for item in lista:
        charadas.append(item.to_dict())
    
    if charadas:
        return jsonify(random.choice(charadas)), 200
    else:
        return jsonify({'mensagem':'Erro! Nenhuma charada encontrada.'}), 404

#MÉTODO GET - CHARADA POR ID
@app.route('/charadas/<id>', methods=['GET'])
def busca(id):
    doc_ref = db.collection('charadas').document(id)
    doc = doc_ref.get().to_dict()

    if doc:
        return jsonify(doc), 200
    else:
        return jsonify({'mensagem':'Erro! Nenhuma charada encontrada com esse ID.'}), 404
    
#MÉTODO POST - ADICIONAR CHARADA
@app.route('/charadas', methods=['POST'])
def adicionar_charada():
    dados = request.json

    if "pergunta" not in dados or "resposta" not in dados:
        return jsonify({'mensagem':'Erro! Campos "pergunta" e "resposta" são obrigatórios.'}), 400
    
    #contador
    contador_ref = db.collection('controle_id').document('contador')
    contador_doc = contador_ref.get().to_dict()
    ultimo_id = contador_doc.get('id')
    novo_id = int(ultimo_id) + 1
    contador_ref.update({'id': novo_id})

    db.collection('charadas').document(str(novo_id)).set({
        "id": novo_id,
        "pergunta": dados['pergunta'],
        "resposta": dados['resposta']
    })

    return jsonify({'mensagem':'Charada cadastrada com sucesso!'}), 201

#MÉTODO PUT - ALTERAR CHARADA
@app.route('/charadas/<id>', methods=['PUT'])
def alterar_charada(id):
    dados = request.json

    if "pergunta" not in dados or "resposta" not in dados:
        return jsonify({'mensagem':'Erro! Campos "pergunta" e "resposta" são obrigatórios.'}), 400
    
    doc_ref = db.collection('charadas').document(id)
    doc = doc_ref.get()

    if doc.exists:
        doc_ref.update({
            "pergunta": dados['pergunta'],
            "resposta": dados['resposta']
        })
        return jsonify({'mensagem':'Charada atualizada com sucesso!'}), 201
    else:
        return jsonify({'mensagem':'ERRO! Charada não encontrada!'}), 404
    
#MÉTODO DELETE - EXCLUIR CHARADA
@app.route('/charadas/<id>', methods=['DELETE'])
def excluir_charada(id):
    doc_ref = db.collection('charadas').document(id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({'mensagem':'ERRO! Charada não encontrada!'}), 404
    
    doc_ref.delete()
    return jsonify({'mensagem':'Charada excluída com sucesso!'}), 201



if __name__ == '__main__':
    app.run()