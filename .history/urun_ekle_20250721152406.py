import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="fsmvu",  
    database="thor_db"
)

cursor = db.cursor()

# Yeni ürün ekle
urun_adi = "Emre Hendemoğlu"
urun_numarasi = "ABC123XYZ"

query = "INSERT INTO urunler (urun_numarasi, urun_adi) VALUES (%s, %s)"
values = (urun_numarasi, urun_adi)

try:
    cursor.execute(query, values)
    db.commit()
    print("Ürün başarıyla eklendi.")
except mysql.connector.Error as err:
    print("Hata:", err)

db.close()
