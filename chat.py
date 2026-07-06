import os
import json
import requests
from flask import Flask, request, jsonify, render_template, send_file
import threading
import webbrowser

app = Flask(__name__, template_folder='.')

# Lendo a chave da API do arquivo .env manualmente para não depender do pacote python-dotenv
def load_env():
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('GROQ_API'):
                    # Pega o valor e remove possíveis aspas e espaços
                    valor = line.split('=', 1)[1].strip().strip('"').strip("'")
                    return valor
    except FileNotFoundError:
        return None

GROQ_API_KEY = load_env()

def carregar_banco():
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bancodados.json')
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_banco(dados):
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bancodados.json')
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

@app.route('/historico', methods=['GET'])
def historico():
    banco = carregar_banco()
    return jsonify({"historico": banco.get('historico', [])})

@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    banco = carregar_banco()
    if dados.get('user') == banco['user'] and dados.get('senha') == banco['senha']:
        return jsonify({"sucesso": True})
    return jsonify({"sucesso": False, "erro": "Usuário ou senha inválidos"}), 401

@app.route('/bg-video')
def bg_video():
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mylivewallpapers-com-Nine-Tails-Fox-Kurama-4K.mp4')
    return send_file(caminho, mimetype='video/mp4')

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    dados = request.json
    mensagem_usuario = dados.get('mensagem', '')

    if not GROQ_API_KEY:
        return jsonify({"erro": "Chave da API Groq não encontrada no arquivo .env"}), 500

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-8b-instant", # Modelos atualizados: llama-3.1-8b-instant, mixtral-8x7b-32768
        "messages": [{
            "role": "system",
            "content": "Voce é o Naruto Uzumaki, tenha a personalidade de um ninja determinado e leal. Responda apenas em português do Brasil."
        },
            {"role": "user", "content": mensagem_usuario}
        ]
    }
    
    try:
        resposta = requests.post(url, headers=headers, json=payload)
        resposta_json = resposta.json()
        
        if resposta.status_code == 200:
            texto_ia = resposta_json['choices'][0]['message']['content']
            banco = carregar_banco()
            banco.setdefault('historico', []).append({"role": "user", "text": mensagem_usuario})
            banco.setdefault('historico', []).append({"role": "bot", "text": texto_ia})
            salvar_banco(banco)
            return jsonify({"resposta": texto_ia})
        else:
            erro_msg = resposta_json.get('error', {}).get('message', 'Erro desconhecido da API.')
            return jsonify({"erro": f"Erro na API Groq: {erro_msg}"}), 500
            
    except Exception as e:
        return jsonify({"erro": f"Erro no servidor: {str(e)}"}), 500

def abrir():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1, abrir).start()
    app.run(debug=True)