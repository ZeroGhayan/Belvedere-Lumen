# payments/mercado_pago.py
import mercadopago
from config import MERCADO_PAGO_ACCESS_TOKEN

def gerar_pagamento_mp(valor, descricao, user_id, canal_id):
    sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)
    preference_data = {
        "items": [
            {
                "title": descricao,
                "quantity": 1,
                "unit_price": valor,
                "currency_id": "BRL"
            }
        ],
        "payer": {
            "email": "comprador@example.com"
        },
        "back_urls": {
            "success": "https://seusite.com/sucesso",  # URL de redirecionamento
            "failure": "https://seusite.com/erro",
            "pending": "https://seusite.com/pendente"
        },
        "auto_return": "approved",
        "notification_url": "https://seusite.com/webhook",  # Webhook para notificações
        "external_reference": f"user_{user_id}_canal_{canal_id}"  # Referência única
    }
    preference_response = sdk.preference().create(preference_data)
    return preference_response["response"]["init_point"]

def verificar_pagamento_mp(payment_id):
    """ Verifica o status do pagamento pelo ID """
    sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)  # Instancia SDK
    pagamento_response = sdk.payment().get(payment_id)
    
    # Verificar se a resposta contém o campo 'status'
    if "status" in pagamento_response["response"]:
        status = pagamento_response["response"]["status"]
        return status  # Pode ser "approved", "pending", "rejected", etc.
    else:
        # Tratar caso o status não seja encontrado
        raise Exception("Erro ao verificar o pagamento: Status não encontrado")