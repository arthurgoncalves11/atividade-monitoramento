from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

ARQUIVO_LOG = "logs.txt"


@app.route("/")
def home():
    return """
    <h1>Sistema de Monitoramento de Evidências</h1>

    <p>Projeto sobre rastros digitais (logs, IPs e carimbos de tempo).</p>

    <a href="/evidencia/1">
        Acessar Evidência 1
    </a>

    <br><br>

    <a href="/acessos">
        Ver Histórico de Acessos
    </a>
    """


@app.route("/evidencia/<id>")
def evidencia(id):

    return f"""
    <h1>Evidência {id}</h1>

    <p>Informe seu nome para registrar o acesso.</p>

    <form action="/registrar/{id}" method="post">

        <label>Nome:</label>
        <input
            type="text"
            name="nome"
            required
        >

        <br><br>

        <button type="submit">
            Registrar Acesso
        </button>

    </form>
    """


@app.route("/registrar/<id>", methods=["POST"])
def registrar(id):

    nome = request.form.get("nome")

    ip = request.headers.get(
        "X-Forwarded-For",
        request.remote_addr
    ).split(",")[0].strip()

    user_agent = request.headers.get("User-Agent")

    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    log = (
        f"Nome: {nome}|"
        f"Evidência: {id}|"
        f"Data: {data}|"
        f"IP: {ip}|"
        f"UserAgent: {user_agent}\n"
    )

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(log)

    return f"""
    <h1>Acesso registrado com sucesso!</h1>

    <p><strong>Nome:</strong> {nome}</p>
    <p><strong>Evidência:</strong> {id}</p>
    <p><strong>Data/Hora:</strong> {data}</p>
    <p><strong>IP:</strong> {ip}</p>

    <br>

    <a href="/acessos">
        Ver Histórico de Acessos
    </a>
    """


@app.route("/acessos")
def acessos():

    try:

        with open(ARQUIVO_LOG, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        html = """
        <h1>Histórico de Acessos</h1>

        <table border="1" cellpadding="8">
            <tr>
                <th>Nome</th>
                <th>Evidência</th>
                <th>Data/Hora</th>
                <th>IP</th>
            </tr>
        """

        for linha in reversed(linhas):

            partes = linha.strip().split("|")

            nome = partes[0].replace("Nome: ", "")
            evidencia = partes[1].replace("Evidência: ", "")
            data = partes[2].replace("Data: ", "")
            ip = partes[3].replace("IP: ", "")

            html += f"""
            <tr>
                <td>{nome}</td>
                <td>{evidencia}</td>
                <td>{data}</td>
                <td>{ip}</td>
            </tr>
            """

        html += """
        </table>

        <br>

        <a href="/">
            Voltar para o início
        </a>
        """

        return html

    except FileNotFoundError:
        return """
        <h2>Nenhum acesso registrado ainda.</h2>

        <a href="/">
            Voltar para o início
        </a>
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)