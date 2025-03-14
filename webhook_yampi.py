from flask import Flask, request
import json

app = Flask(__name__)

# Simulação de banco de dados de usuários pagos
usuarios_pagos = {}

@app.route('/webhook', methods=['POST'])
def yampi_webhook():
    data = request.get_json()  # Obtém os dados do webhook
    print("Recebido webhook:", data)

    user_id = data.get('customer', {}).get('email')  # Substitua por um identificador único do cliente
    status_pagamento = data.get('status')  # Status do pagamento

    if status_pagamento == 'paid':  # Se o pagamento foi concluído
        usuarios_pagos[user_id] = True
        print(f"✅ Pagamento confirmado para {user_id}")

    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
