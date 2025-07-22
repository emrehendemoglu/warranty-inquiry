from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

# Veritabanı bağlantısı
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senin_sifren",  # BURAYA MySQL ŞİFRENİ YAZ
    database="thor_db"
)

cursor = db.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    kalan_sure = ""
    urun_bilgisi = {}

    if request.method == "POST":
        urun_numarasi = request.form["urun_numarasi"]

        # Ürün verisini sorgula
        cursor.execute("SELECT urun_adi, eklenme_tarihi FROM urunler WHERE urun_numarasi = %s", (urun_numarasi,))
        result = cursor.fetchone()

        if result:
            urun_adi, eklenme_tarihi = result
            garanti_suresi = timedelta(days=730)  # 2 yıl
            bitis_tarihi = eklenme_tarihi + garanti_suresi
            simdi = datetime.now()
            kalan = bitis_tarihi - simdi

            if kalan.total_seconds() > 0:
                days = kalan.days
                seconds = kalan.seconds
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                secs = seconds % 60
                kalan_sure = f"{days} gün, {hours} saat, {minutes} dakika, {secs} saniye kaldı"
            else:
                kalan_sure = "Garanti süresi dolmuş."

            urun_bilgisi = {
                "urun_adi": urun_adi,
                "urun_numarasi": urun_numarasi
            }
        else:
            kalan_sure = "Ürün bulunamadı."

    return render_template("index.html", kalan_sure=kalan_sure, urun_bilgisi=urun_bilgisi)
    
if __name__ == "__main__":
    app.run(debug=True)
