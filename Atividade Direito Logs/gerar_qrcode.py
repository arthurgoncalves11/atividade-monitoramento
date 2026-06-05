import qrcode

url = "http://localhost:5000/evidencia/1"

img = qrcode.make(url)

img.save("evidencia1.png")

print("QR Code gerado!")