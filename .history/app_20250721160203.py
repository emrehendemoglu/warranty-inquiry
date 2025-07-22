from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    urun_bilgisi = None
    kalan_sure = None

    if request.method == "POST":
        urun_numarasi = request.form["urun_numarasi"]

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="fsmvu",
                database="thor_db"
            )

            imlec = db.cursor(dictionary=True)
            imlec.execute("SELECT urun_Adi, urun_numarasi, eklenme_tarihi FROM thor_db WHERE urun_numarasi = %s", (urun_numarasi,))
            urun_bilgisi = imlec.fetchone()
            imlec.close()
            db.close()

            if urun_bilgisi:
                eklenme_tarihi = urun_bilgisi["eklenme_tarihi"]
                garanti_bitis_tarihi = eklenme_tarihi + timedelta(days=365 * 2)  # 2 yıl garanti
                bugun = datetime.now()
                kalan_sure = garanti_bitis_tarihi - bugun
                if kalan_sure.days < 0:
                    kalan_sure = "Garanti süresi dolmuş."
                else:
                    kalan_sure = f"{kalan_sure.days} gün kaldı"
            else:
                kalan_sure = "Ürün bulunamadı."

        except mysql.connector.Error as err:
            kalan_sure = f"Hata: {err}"

    return render_template("index.html", urun_bilgisi=urun_bilgisi, kalan_sure=kalan_sure)
