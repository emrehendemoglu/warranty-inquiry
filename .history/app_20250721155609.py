from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="fsmvu",
    database="thor_db"
)

@app.route("/", methods=["GET", "POST"])
def index():
    urun_bilgisi = None
    kalan_sure = None

    if request.method == "POST":
        urun_numarasi = request.form.get("urun_numarasi")

        if urun_numarasi:
            imlec = db.cursor(dictionary=True)
            sql = "SELECT urun_Adi, urun_numarasi, eklenme_tarihi FROM urunler WHERE urun_numarasi = %s"
            imlec.execute(sql, (urun_numarasi,))
            urun_bilgisi = imlec.fetchone()

            if urun_bilgisi:
                eklenme_tarihi = urun_bilgisi['eklenme_tarihi']
                garanti_bitis_tarihi = eklenme_tarihi + timedelta(days=365*2)  # 2 yıl sonrası
                suanki_tarih = datetime.now()

                if suanki_tarih > garanti_bitis_tarihi:
                    kalan_sure = "Garanti süresi dolmuş."
                else:
                    fark = garanti_bitis_tarihi - suanki_tarih
                    # kalan süreyi gün olarak gösterelim
                    kalan_sure = f"{fark.days} gün"

            imlec.close()

    return render_template("index.html", urun_bilgisi=urun_bilgisi, kalan_sure=kalan_sure)

if __name__ == "__main__":
    app.run(debug=True)
