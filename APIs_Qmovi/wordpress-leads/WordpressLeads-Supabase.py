# API python para receber dados JSON e inserir esses dados em um BD Supabase.
# vou utilizar biblioteca requests para fazer requisições HTTP para a API REST do Supa + biblioteca json para manipular dados JSON.

from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# configs do supa
SUPABASE_URL = "https://czamkekjevphjzjzggve.supabase.co/rest/v1/leads_wordpress"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

@app.route('/receber-lead', methods=['POST'])
def receber_lead():
    try:

        # pega os dado json enviado pelo formulário

        content_type = request.headers.get('Content-Type')


        if content_type == 'application/json':
            data = request.get_json()

        elif content_type.startswith('application/x-www-form-urlencoded') or content_type.startswith('multipart/form-data'):
            data = request.form.to_dict()
        else:
            return jsonify({"erro": "Formato de conteúdo não suportado"}), 400

        if not data:
            return jsonify({"erro": "Nenhum dado recebido"}), 400
        
        print('Dados recebidos:', data)


        # manda as informacoes recebidas pro supa
        response = requests.post(
            SUPABASE_URL,
            json=data,
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
        )

        if response.status_code in (200, 201):
            return jsonify({"mensagem": "Dados inseridos com sucesso!"}), 201
        else:
            return jsonify({
                "erro": "Falha ao inserir no Supabase",
                "status": response.status_code,
                "detalhes": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


