# payments/paypal.py
import paypalrestsdk
from config import PAYPAL_CLIENT_ID, PAYPAL_SECRET_KEY

def configurar_paypal():
    paypalrestsdk.configure({
        "mode": "sandbox",  # Mudar para "live" em produção
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_SECRET_KEY
    })

def gerar_pagamento_paypal(valor, descricao):
    configurar_paypal()
    pagamento = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": f"{valor:.2f}",
                "currency": "BRL"
            },
            "description": descricao
        }],
        "redirect_urls": {
            "return_url": "https://www.seusite.com/sucesso",
            "cancel_url": "https://www.seusite.com/erro"
        }
    })
    if pagamento.create():
        return pagamento.links[1].href  # Retorna o link de pagamento
    else:
        return None

def verificar_pagamento_paypal(payment_id):
    configurar_paypal()
    pagamento = paypalrestsdk.Payment.find(payment_id)
    if pagamento.state == 'approved':
        return True
    else:
        return False