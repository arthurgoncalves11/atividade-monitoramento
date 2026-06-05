from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route("/evidencia/<id>")
def evidencia(id):

    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    data = datetime.now()

    log = f"""
Evidência: {id}
Data/Hora: {data}
IP: {ip}
User-Agent: {user_agent}
------------------------
"""

    print(log)

    with open("logs.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(log)

    return "<h1>Evidência acessada!</h1>"

app.run(host="0.0.0.0", port=5000)