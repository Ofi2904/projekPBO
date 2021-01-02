import sqlite3

import pathlib

#Class untuk meng-handle query sql
class DatabaseHandler:
    def __init__(self):
        #formula mendapatkan directori database yg disimpan ke variable berupa string
        database = str(pathlib.Path().absolute())+"\YukSehat.db"
        #melakukan koneksi pada database
        self.connector = sqlite3.connect(database)
        #inisiasi fungsi cursor database, sehingga dapat menjalankan fungsi query lainnya
        self.cursor = self.connector.cursor()
        
    #fungsi untuk menjalankan query dan menerima return value atau tidak
    def jalankanQuery(self, query, nilaiKembali=False):
        #menjalankan perintah query
        self.cursor.execute(query)
        #menyimpan hasil query ke dalam variable data
        data = self.cursor.fetchall()
        #mengkonfir1masi perintah query
        self.connector.commit()
        #nilaiKembali dipakai kalau def jalankanQuery perlu mengembalikan nilai atau tidak
        if nilaiKembali:
            return data

#Class untuk meng-handle login, meng-inherit dari class DatabaseHandler
class Program(DatabaseHandler):
    def __init__(self):
        #menginisiasi atribut DatabaseHandler, supaya dapat digunakan dalam class Program
        DatabaseHandler.__init__(self)
        #menyiapkan atribut yang masih bernilai kosong, supaya dapat digunakan di dalam class ini
        self.jenis_kelamin = None
        self.umur = None
        self.tinggi = None
        self.berat = 0
        self.berat_ideal = 0

    def memasukkanData(self, jenis_kelamin, umur, tinggi, berat):
        self.jenis_kelamin = jenis_kelamin
        self.umur = umur
        self.tinggi = tinggi
        self.berat = berat
        self.berat_ideal = self.tinggi - 110
        
    def hitungBeratIdeal(self):
        #formula menghitung body mass index. round((...), 2) dipakai agar nilai desimal yg didapat hanya 2 angka di belakang koma 
        bmi = round((self.berat/(round(((self.tinggi/100)**2), 2))), 2)
        print("Data Anda")
        print(f"Berat: {self.berat} kg")
        print(f"Tinggi: {self.tinggi} cm")
        print("="*6)
        print(f"Berat Ideal: {self.berat_ideal} kg")
        print(f"Body Mass Index (BMI): {bmi}")
        #mengecek nilai BMI
        if bmi <= 18.4:
            kategori = 'Kurang'
        elif 18.5 < bmi and bmi < 25:
            kategori = 'Normal'
        elif 25 <= bmi and bmi < 30:
            kategori = 'Berlebih'
        elif bmi >= 30:
            kategori = 'Obesitas'  
        print(f"Kategori Berat Badan: {kategori}")
        #menyiapkan query bahasa pemrograman sql ke dalam variabel query
        query = 'INSERT INTO tb_hitung_berat_ideal (jenis_kelamin, umur, tinggi, berat, berat_ideal, bmi, kategori) \
                VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'
        #memasukkan VALUES yang ditandai dengan %s sesuai urutan kolom data
        query = query % (self.jenis_kelamin, self.umur, self.tinggi, self.berat, self.berat_ideal, bmi, kategori)
        #var query dijalan masukkan ke method
        self.jalankanQuery(query)
        
    def daftar_makanan(self):
        #mengambil semua data dari tabel tb_daftar_kalori
        query = 'SELECT * FROM tb_daftar_kalori'
        #var tabel disini memiliki data karena pada method jalankanQuery, parameter nilaiKembali bernilai True
        tabel = self.jalankanQuery(query, True)
        #menyusuri semua isi var tabel lalu memprintnya
        for i in tabel:
            print(f"{i[0]}, kalori = {i[1]} kkal")
        
    def penghitungKalori(self, list_barang):
        query = 'SELECT * FROM tb_daftar_kalori'
        tabel = self.jalankanQuery(query, True)
        total_kalori = 0
        #mengecek isi tabel makanan, apakah dari list makanan inputan user ada nama makanan yang sama, jika ada maka
        #menambahkan nilai kalori yg sudah dikali jumlah makanan ke dalam jumlah total kalori
        for i in tabel:
            for j in list_barang:
                if j[0] == i[0]:
                    total_kalori += j[1]*i[1]
        #memprint makanan-makanan yang diinputkan user serta memasukkannya ke dalam tabel sql
        numbering = 0
        for i in list_barang:
            numbering += 1
            print(f"{numbering}. {i[0]}, jumlah: {i[1]:,} item")
            query = 'INSERT INTO tb_list_barang (nama_barang, jumlah) \
                VALUES (\'%s\', \'%s\')'
            query = query % (i[0], i[1])
            self.jalankanQuery(query)
        print(f"Total kalori = {total_kalori:,} kkal")
        
    def kaloriSehari(self):
        #formula perhitungan kebutuhan kalori sehari agar ideal sesuai jenis kelamin
        if self.jenis_kelamin == 'l':
            kalori_perhari = (88.4 + 13.4 * self.berat) + (4.8 * self.tinggi) - (5.68 * self.umur)
        elif self.jenis_kelamin == 'p':
            kalori_perhari = (447.6 + 9.25 * self.berat) + (3.10 * self.tinggi) - (4.33 * self.umur)
        print("Data Anda")
        print(f"Umur: {self.umur} tahun")
        print(f"Tinggi: {self.tinggi} cm")
        print(f"Berat: {self.berat} kg")
        print("="*6)
        print(f"Kalori yang Anda butuhkan sebanyak {round(kalori_perhari, 2):,} kkal per hari agar mencapai\nberat badan ideal")
        #
        query = 'INSERT INTO tb_hitung_kecukupan_kalori (jenis_kelamin, umur, tinggi, berat, kalori_perhari) \
                VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'
        query = query % (self.jenis_kelamin, self.umur, self.tinggi, self.berat, kalori_perhari)
        self.jalankanQuery(query)

# Menginstantiate objek p dari Class Program
p = Program()
print("Selamat datang di SehatYuk!")
print("Aplikasi pembantu mengontrol pola makan")

#memulai menerima inputan dari user
jenis_kelamin = input("Masukkan jenis kelamin (l/p):").lower()
umur = int(input("Masukkan umurmu (dalam tahun):"))
tinggi = int(input("Masukkan tinggimu (dalam cm):"))
berat = int(input("Masukkan beratmu (dalam kg):"))
#memasukkan inputan ke dalam objek p
p.memasukkanData(jenis_kelamin, umur, tinggi, berat)

print("-"*6, "SehatYuk", "-"*6)
print("(Ketikkan angka menu)")
print("1. Hitung Berat Ideal\n2. Penghitung Kalori\n3. Penghitung Kebutuhan Kalori perhari agar Berat Badan Ideal\n4. Keluar Program")
#Memulai menerima inputan menu
while True:
    menu = input("Menu:")
    #Menu Mengetahui berat badan ideal
    if menu == '1':
        print("-"*6, "Hitung Berat Ideal", "-"*6)
        #Method dibawah tidak memerlukan inputan lagi karena sudah mengambil data dari inputan di atas
        p.hitungBeratIdeal()
    #Menu Mengetahui berapa kalori makanan yang telah akan di konsumsi
    elif menu == '2':
        print("-"*6, "Hitung Kalori", "-"*6)
        p.daftar_makanan()
        list_barang = []
        #memasukkan nama barang secara perulangan hingga user menginputkan 'n'
        while True:
            nama_barang = input("Masukkan nama makanan:").lower()
            jumlah = int(input("Masukkan jumlah makanan:"))
            item = [nama_barang, jumlah]
            list_barang.append(item)
            lagi = input("Tambah makanan? (y/n)")
            if lagi == 'n':
                break
        p.penghitungKalori(list_barang)
    #Menu Mengetahui berapa kalori yang dibutuhkan dalam sehari untuk membuat berat badan menjadi ideal
    elif menu == '3':
        print("-"*6, "Kecukupan Kalori Sehari", "-"*6)
        p.kaloriSehari()
    elif menu == '4':
        print("-"*6, "Selamat Tinggal", "-"*6)
        print("Terima kasih telah mengunjungi SehatYuk")
        break
    else:
        print("Pilih menu dengan menginputkan angka")
        print("1. Hitung Berat Ideal\n2. Penghitung Kalori\n3. Penghitung Kebutuhan Kalori perhari agar Berat Badan Ideal\n4. Keluar Program")
        