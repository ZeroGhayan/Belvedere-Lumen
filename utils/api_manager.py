# utils/api_manager.py
class APIManager:
    def __init__(self, filename="Bell.txt"):
        self.credentials = self.load_credentials(filename)
        self.validar_credenciais()

    def load_credentials(self, filename):
        credentials = {}
        with open(filename, 'r') as file:
            for line in file:
                if '=' in line and '*' in line:
                    key, value = line.strip().split('=')
                    credentials[key.strip()] = value.strip().strip('*')
        return credentials

    def validar_credenciais(self):
        credenciais_necessarias = [
            "Telegram HTTP API",
            "Mercado Pago access token",
            "Paypal Client ID",
            "PayPal Secret key 1",
            "ZBD API Key"
        ]
        for credencial in credenciais_necessarias:
            if credencial not in self.credentials:
                raise ValueError(f"Credencial faltando: {credencial}")

    def get_credential(self, key):
        return self.credentials.get(key, None)