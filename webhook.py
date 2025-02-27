# webhook.py
from flask import Flask, request, jsonify
from database import adicionar_assinatura
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('action') == 'payment.updated':
        payment_id = data['data']['id']
        status = data['data']['status']
        external_reference = data['data']['external_reference']

        if status == 'approved':
            # Extrai user_id e canal_id da external_reference
            user_id = int(external_reference.split('_')[1])
            canal_id = external_reference.split('_')[3]

            # Adiciona a assinatura ao banco de dados
            adicionar_assinatura(user_id, canal_id, "mensal", "mercado_pago")

            # Envia o link do canal ao usuário (implemente essa função)
            enviar_link_canal(user_id, canal_id)

    return jsonify({"status": "success"}), 200

def enviar_link_canal(user_id, canal_id):
    # Implemente a lógica para enviar o link do canal ao usuário
    pass

if __name__ == '__main__':
    app.run(port=5000)