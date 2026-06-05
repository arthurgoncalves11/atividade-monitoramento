import qrcode

url = "https://atividade-monitoramento.onrender.com/evidencia/1"

img = qrcode.make(url)

img.save("qrcode_evidencia_1.png")

print("QR Code gerado com sucesso!")