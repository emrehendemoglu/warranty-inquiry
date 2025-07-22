import mysql.connector
from datetime import datetime, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

# MySQL bağlantısı
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="fsmvu",
    database="thor_db"
)

@app.route('/', methods=['GET', 'POST'])
def index():
    kalan_sure = None
    urun_bilgisi = None

    if request.method == 'POST':
        urun_numarasi = request.form['urun_numarasi']

        imlec = db.cursor(dictionary=True)
        # Tablo ve sütun isimlerine dikkat et (urun_Adi büyük A)
        imlec.execute("SELECT urun_Adi, eklenme_tarihi FROM urunler WHERE urun_numarasi = %s", (urun_numarasi,))
        sonuc = imlec.fetchone()

        if sonuc:
            urun_bilgisi = sonuc['urun_Adi']
            eklenme_tarihi = sonuc['eklenme_tarihi']

            # Garanti süresi 2 yıl (730 gün) olarak hesaplanıyor
            garanti_bitis = eklenme_tarihi + timedelta(days=730)
            su_an = datetime.now()

            if su_an < garanti_bitis:
                fark = garanti_bitis - su_an
                gun = fark.days
                saat = fark.seconds // 3600
                dakika = (fark.seconds % 3600) // 60
                saniye = fark.seconds % 60
                kalan_sure = f"{gun} gün {saat} saat {dakika} dakika {saniye} saniye kaldı."
            else:
                kalan_sure = "Garanti süresi dolmuş."
        else:
            kalan_sure = "Ürün bulunamadı."

    return render_template("index.html", kalan_sure=kalan_sure, urun_bilgisi=urun_bilgisi)

if __name__ == "__main__":
    app.run(debug=True)
