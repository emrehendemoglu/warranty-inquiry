import mysql.connector
from datetime import datetime, timedelta

# MySQL bağlantısı
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="fsmvu",  
    database="thor_db"
)

cursor = db.cursor()

def urun_ekle(urun_numarasi, urun_adi):
    try:
        sql = "INSERT INTO thor_db (urun_numarasi, urun_adi) VALUES (%s, %s)"
        cursor.execute(sql, (urun_numarasi, urun_adi))
        db.commit()
        print(f"Ürün {urun_numarasi} başarıyla eklendi.")
    except mysql.connector.Error as err:
        print("Hata:", err)

def garanti_kalan_sure(urun_numarasi):
    try:
        sql = "SELECT eklenme_tarihi FROM thor_db WHERE urun_numarasi = %s"
        cursor.execute(sql, (urun_numarasi,))
        sonuc = cursor.fetchone()
        if sonuc is None:
            return "Ürün bulunamadı."
        
        eklenme_tarihi = sonuc[0]
        garanti_suresi = eklenme_tarihi + timedelta(days=365*2)  # 2 yıl garanti
        simdi = datetime.now()

        if simdi > garanti_suresi:
            return "Garanti süresi dolmuş."
        else:
            kalan = garanti_suresi - simdi
            # Gün, saat, dakika, saniye şeklinde hesapla
            gun = kalan.days
            saat = kalan.seconds // 3600
            dakika = (kalan.seconds % 3600) // 60
            saniye = kalan.seconds % 60
            return f"Garanti süresi bitmesine {gun} gün {saat} saat {dakika} dakika {saniye} saniye kaldı."
    except mysql.connector.Error as err:
        return f"Hata: {err}"

