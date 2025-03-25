from flask import Flask, jsonify
import random

app = Flask(__name__)

charadas = [
    {'id': 1, 'charada': 'A Dora é mestre em artes marciais. Sabe qual é o seu golpe preferido?', 'resposta': 'A voa-Dora'},
    {'id': 2, 'charada': 'Como chama o policial que se olhou no espelho?', 'resposta': 'Policial civil'},
    {'id': 3, 'charada': 'Qual é a mãe mais brava do mundo?', 'resposta': 'A eletricidade. Mexe nos fio dela pra você ver…'},
    {'id': 4, 'charada': 'O que o mar falou a um náufrago que estava se afogando?', 'resposta': 'Nada'},
    {'id': 5, 'charada': 'Por que os bombeiros não gostam de andar?', 'resposta': 'Porque eles só-correm'},
    {'id': 6, 'charada': 'Sabe por que nunca se deve desistir dos sonhos?', 'resposta': 'Porque se não tiver na padaria mais próxima pode ser que tenha na outra'},
    {'id': 7, 'charada': 'Onde os minions moram?', 'resposta': 'Em condo-minions'},
    {'id': 8, 'charada': 'Qual é o esporte favorito dos músicos?', 'resposta': 'Lançamento de disco.'},
    {'id': 9, 'charada': 'Sabe qual é a melhor forma de machucar alguém com as palavras?', 'resposta': 'Batendo nela com um dicionário'},
    {'id': 10, 'charada': 'Como uma mulher consegue ficar 8 dias sem dormir?', 'resposta': 'Dormindo durante a noite'},
    {'id': 11, 'charada': 'Por que os ovos não contam piadas?', 'resposta': 'Para não rachar de rir'},
    {'id': 12, 'charada': 'Por que o homem invisível não aceitou um emprego?', 'resposta': 'Porque ele não se via fazendo aquilo'}
]

@app.route('/')
def index():
    return 'API - CHARADAS'

@app.route('/charadas', methods=['GET'])
def charada():
    charada = random.choice(charadas) 
    return charada

@app.route('/charadas/<campo>/<busca>', methods=['GET'])
def busca(campo, busca):
    if campo not in ['id','charada','resposta']:
        return jsonify({'mensagem':'ERRO! Campo não encontrado.'}), 404

    if campo == 'id':
        busca = int(busca)

    for charada in charadas:
        if charada[campo] == busca:
            return jsonify(charada), 200
    else:
        return jsonify({'mensagem':'ERRO! Usuário não encontrado.'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)