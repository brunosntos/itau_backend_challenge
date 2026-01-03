from decimal import Decimal
from datetime import datetime

from flask import Flask, request, jsonify, Response

app = Flask(__name__)

db = []

@app.route("/transacao", methods=["POST"])
def criar_transacao():
    try:
        dados = request.get_json()

        valor = dados.get("valor", "")
        dataHora = dados.get("dataHora", "")

        if str(valor).strip() == "" or str(dataHora).strip() == "":
            return Response(status=422)
        
        valor_decimal = Decimal(valor)
        if valor_decimal < 0:
            return Response(status=422)
        
        dataHora_str = str(dataHora)
        dataHora_datetime = datetime.fromisoformat(dataHora_str)
        agora = datetime.now().isoformat()
        agora_datetime = datetime.fromisoformat(agora)

        if (dataHora_datetime > agora_datetime):
            return Response(status=422)
        
        dados["dataHora"] = dataHora_datetime
        dados["valor"] = valor_decimal

        db.append(dados)
        return Response(status=201)
    
    except Exception:
        return Response(status=400)

@app.route("/transacao", methods=["DELETE"])
def limpar_transacoes():
    global db
    db = []
    
    return Response(status=200)


if __name__ == "__main__":
    app.run(debug=True)