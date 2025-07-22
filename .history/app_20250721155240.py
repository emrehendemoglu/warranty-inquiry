from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL bağlantısı
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="fsmvu",  # Şifrenizi buraya yazın
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
            sql = "SELECT urun_Adi, eklenme_tarihi FROM thor_db WHERE urun_numarasi = %s"
            imlec.execute(sql, (urun_numarasi,))
            urun_bilgisi = imlec.fetchone()

            if urun_bilgisi:
                # örnek: kalan_sure hesaplama, eklenme_tarihi üzerinden fark hesaplanabilir
                # burada sadece örnek olarak None bırakıyorum, istediğin mantığı ekleyebilirsin
                kalan_sure = "Örnek süre"

            imlec.close()

    return render_template("index.html", urun_bilgisi=urun_bilgisi, kalan_sure=kalan_sure)

if __name__ == "__main__":
    app.run(debug=True)