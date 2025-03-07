import qrcode
qr='www.youtube.com'
qr_img=qrcode.make(qr)
save_pa='4. QR코드 생성기\\' + qr + '.png'
qr_img.save(save_pa)
