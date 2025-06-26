import make_qrcode

url = "https://github.com/killodla/killo123"

qr = make_qrcode.QRCode(
    version=1,
    error_correction=make_qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("github_qrcode.png")

print("QR 코드가 'github_qrcode.png' 파일로 저장되었습니다.")
