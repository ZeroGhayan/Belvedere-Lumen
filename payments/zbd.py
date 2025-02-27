# payments/zbd.py
import requests
from config import ZBD_API_KEY

class ZBD:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.zebedee.io/v0"

    def criar_invoice(self, valor, descricao):
        url = f"{self.base_url}/invoices"
        headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key
        }
        data = {
            "amount": f"{valor:.0f}",
            "description": descricao,
            "expiresIn": 600  # 10 minutos para expirar
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def verificar_pagamento(self, invoice_id):
        url = f"{self.base_url}/invoices/{invoice_id}"
        headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

# Exemplo de uso
zbd = ZBD(ZBD_API_KEY)

def gerar_pagamento_zbd(valor, descricao):
    invoice = zbd.criar_invoice(valor, descricao)
    if invoice:
        return invoice["data"]["invoice"]["request"]
    else:
        return None

def verificar_pagamento_zbd(invoice_id):
    pagamento = zbd.verificar_pagamento(invoice_id)
    if pagamento and pagamento["data"]["invoice"]["status"] == "paid":
        return True
    else:
        return False