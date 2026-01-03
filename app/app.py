from decimal import Decimal
from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask import Flask, request, jsonify, Response

app = Flask(__name__)
app.json.sort_keys = False

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

@app.route("/estatisticas", methods=["GET"])
def obter_estatisticas():
    global db
    db_filtro = []

    agora_str = datetime.now().isoformat()
    agora_datetime = datetime.fromisoformat(agora_str)
    limite_de_tempo = agora_datetime - relativedelta(minutes=1)

    dados = {
        "count": "0",
        "sum": "0",
        "avg": "0",
        "min": "0",
        "max": "0"
    }

    for transacao in db:
        if transacao["dataHora"] < limite_de_tempo: continue

        db_filtro.append(transacao["valor"])
    
    if len(db_filtro) == 0: return jsonify(dados), 200
        
    dados["count"] = len(db_filtro)
    dados["sum"] = sum(db_filtro)
    dados["avg"] = round(sum(db_filtro) / len(db_filtro), 2)
    dados["min"] = min(db_filtro)
    dados["max"] = max(db_filtro)

    return jsonify(dados), 200



if __name__ == "__main__":
    app.run(debug=True)