from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route("/evidencia/<id>")
def evidencia(id):

    ip = request.headers.get(
        "X-Forwarded-For",
        request.remote_addr
    )

    user_agent = request.headers.get("User-Agent")

    log = f"""
Evidência: {id}
Data/Hora: {datetime.now()}
IP: {ip}
User-Agent: {user_agent}
------------------------
"""

    with open("logs.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(log)

    return f"""
    <h1>Evidência acessada!</h1>

    <pre>
{log}
    </pre>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)