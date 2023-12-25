import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image
from tkinter import filedialog

class GirisPenceresi:
    def __init__(self, master):
        # Pencere başlığı ve boyutları ayarlanıyor
        self.master = master
        master.title("EduGraph")
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = 750
        window_height = 520
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Giriş formunu oluşturan metodu çağırma
        self.giris_icerik()

    def giris_icerik(self):
        # Giriş formu frame'i oluşturuluyor
        frame = tk.Frame(self.master)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.edugraph_label = tk.Label(self.master, text="EduGraph", font=("Arial", 28, "bold"))
        self.edugraph_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Kullanıcı Adı Label ve Entry
        self.kullanici_adi_label = tk.Label(frame, text="Kullanıcı Adı:", font=("Arial", 14))
        self.kullanici_adi_label.grid(row=0, column=0, pady=10, padx=(0, 10), sticky="e")
        self.kullanici_adi_entry = tk.Entry(frame, font=("Arial", 14))
        self.kullanici_adi_entry.grid(row=0, column=1, pady=10, padx=(0, 10), sticky="w")

        # Şifre Label ve Entry
        self.sifre_label = tk.Label(frame, text="Şifre:", font=("Arial", 14))
        self.sifre_label.grid(row=1, column=0, pady=10, padx=(0, 10), sticky="e")
        self.sifre_entry = tk.Entry(frame, show="*", font=("Arial", 14))
        self.sifre_entry.grid(row=1, column=1, pady=10, padx=(0, 10), sticky="w")

        # Giriş Butonu
        self.giris_buton = tk.Button(frame, text="Giriş", command=self.giris_kontrol, font=("Arial", 14), cursor="hand2", width=12, height=1)
        self.giris_buton.grid(row=2, column=0, columnspan=2, pady=20)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        #Info Butonu
        self.info_buton = tk.Button(self.master, text="ℹ", command=self.goster_hakkinda, font=("Arial", 10), cursor="hand2", width=2, height=1)
        self.info_buton.place(relx=0.98, rely=0.98, anchor=tk.SE)
    
    def goster_hakkinda(self):
        # Hakkında bilgisi göster
        hakkimizda_mesaji = "EduGraph\nVersion 1.0\n\nBu program eğitim verilerini yönetmek ve grafikler oluşturmak için tasarlanmıştır."
        messagebox.showinfo("Hakkında", hakkimizda_mesaji)    

    def giris_kontrol(self):
        # Kullanıcı giriş bilgilerini kontrol et
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()
        hata_mesaji = ""

        if kullanici_adi == "admin" and sifre == "12345":
            # Giriş başarılı ise giriş elemanlarını kaldır
            self.edugraph_label.destroy()
            self.kullanici_adi_label.destroy()
            self.kullanici_adi_entry.destroy()
            self.sifre_label.destroy()
            self.sifre_entry.destroy()
            self.giris_buton.destroy()
            
            # Yeni butonları ekleyerek farklı pencerelere geçiş sağla
            self.hg_label = tk.Label(self.master, text="Hoş Geldiniz!", font=("Arial", 16, "bold"))
            self.hg_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
            
            self.buton1 = tk.Button(self.master, text="Öğrenci Kayıt Sistemi", command=self.ogrenci_penceresi_ac, font=("Arial", 14), cursor="hand2", fg="red", width=20, height=3)
            self.buton1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

            self.buton2 = tk.Button(self.master, text="Grafik Oluşturma Aracı", command=self.grafik_penceresi_ac, font=("Arial", 14), cursor="hand2", fg="red", width=20, height=3)
            self.buton2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        else:
            hata_mesaji = "Kullanıcı adı veya şifre hatalı!"
            if not kullanici_adi:
                hata_mesaji += "\nKullanıcı adı boş bırakılamaz."
            elif kullanici_adi != "admin":
                hata_mesaji += "\nKullanıcı adı hatalı."

            if not sifre:
                hata_mesaji += "\nŞifre boş bırakılamaz."
            elif sifre != "12345":
                hata_mesaji += "\nŞifre hatalı."

        if hata_mesaji:
            messagebox.showerror("Hata", hata_mesaji)
            self.master.focus_force()

    def ogrenci_penceresi_ac(self):
        # Öğrenci penceresini aç
        ogrenci_penceresi = tk.Toplevel(self.master)
        ogrenci_penceresi.title("Öğrenci Kayıt Sistemi")
        OgrenciKayitSistemi(ogrenci_penceresi)

    def grafik_penceresi_ac(self):
        # Grafik penceresini aç
        grafik_penceresi = tk.Toplevel(self.master)
        grafik_penceresi.title("Grafik Penceresi")
        GrafikOluşturucu(grafik_penceresi)

class OgrenciKayitSistemi:
    def __init__(self, master):
        self.master = master
        self.master.wm_title("Öğrenci Kayıt Sistemi")

        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        position_right = int(self.master.winfo_screenwidth() / 3 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 3 - window_height / 2)
        self.master.geometry(f"755x520+{position_right}+{position_down}")
        self.master.resizable(width=False, height=False)

        # Ana pencerenin düzeni
        F1 = tk.Frame(self.master)
        F1.pack(pady=15, padx=25)

        # Ana pencere butonları
        B1 = tk.Button(F1, text="Öğrenci Ekle", command=self.ekle, font="bold", cursor="hand2", fg="blue", width=15, height=2)
        B1.grid(row=0, column=0, padx=20)
        B2 = tk.Button(F1, text="Öğrenci Listele", command=self.listele, font="bold", cursor="hand2", fg="blue", width=15, height=2)
        B2.grid(row=0, column=1, padx=20)
        B6 = tk.Button(F1, text="Grafiği Göster", command=self.grafik_goster, font="bold", cursor="hand2", fg="blue", width=15, height=2)
        B6.grid(row=0, column=2, padx=20)

        # Alt panellerin oluşturulması
        self.F_listele = tk.Frame(self.master)
        self.F_ekle = tk.Frame(self.master)

        # Veritabanı bağlantısı ve cursor oluşturma
        self.baglanti = sqlite3.connect("ogrenci_kayit.db", check_same_thread=True)
        self.im = self.baglanti.cursor()

        # Veritabanını oluştur
        self.db_oluştur()

   
    def db_oluştur(self):
        try:
            # Veritabanına bağlan
            connection = sqlite3.connect("ogrenci_kayit.db")
            cursor = connection.cursor()

            # Tablo var mı diye kontrol et
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ogrenciler (
                    id INTEGER PRIMARY KEY,
                    Adi VARCHAR(45),
                    Soyadi VARCHAR(45),
                    Cinsiyet VARCHAR(10),
                    Dogum_Yeri VARCHAR(45),
                    Okudugu_Bolum VARCHAR(45),
                    Dogum_Yili INT,
                    Sinif VARCHAR(5)
                )
            """)

            # Değişiklikleri kaydet
            connection.commit()

        except Exception as e:
            print(f"Hata: {str(e)}")

        finally:
            # Bağlantıyı kapat
            if connection:
                connection.close()

    def ekle(self):
        if self.F_listele:
            self.F_listele.destroy()
        if self.F_ekle:
            self.F_ekle.destroy()
            self.F_ekle = tk.Frame(self.master)
            self.F_ekle.place(x=250, y=150)

        # Öğrenci Adı
        ttk.Label(self.F_ekle, text="Öğrenci Adı: ").grid(row=0, column=0, pady=5, sticky=tk.W)
        self.E1 = ttk.Entry(self.F_ekle, width=35)
        self.E1.grid(row=0, column=1, pady=5)

        # Öğrenci Soyadı
        ttk.Label(self.F_ekle, text="Öğrenci Soyadı: ").grid(row=1, column=0, pady=5, sticky=tk.W)
        self.E2 = ttk.Entry(self.F_ekle, width=35)
        self.E2.grid(row=1, column=1, pady=5)

        # Cinsiyet
        ttk.Label(self.F_ekle, text="Cinsiyet: ").grid(row=2, column=0, pady=5, sticky=tk.W)
        cinsiyet_options = ["Erkek", "Kız"]
        self.cinsiyet_combo = ttk.Combobox(self.F_ekle, values=cinsiyet_options, state="readonly", width=33)
        self.cinsiyet_combo.grid(row=2, column=1, pady=5)

        # Doğum Yeri
        ttk.Label(self.F_ekle, text="Doğum Yeri: ").grid(row=3, column=0, pady=5, sticky=tk.W)
        turkish_cities = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir", "Kilis", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Şanlıurfa", "Şırnak", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"]
        self.dogum_yeri_combo = ttk.Combobox(self.F_ekle, values=turkish_cities, state="readonly", width=33)
        self.dogum_yeri_combo.grid(row=3, column=1, pady=5)

        # Okuduğu Bölüm
        ttk.Label(self.F_ekle, text="Okuduğu Bölüm: ").grid(row=4, column=0, pady=5, sticky=tk.W)
        okudugu_bolum_options = [
            "Bilgisayar Mühendisliği",
            "Elektrik Mühendisliği",
            "Makine Mühendisliği",
            "İnşaat Mühendisliği",
            "Kimya Mühendisliği",
            "Biomedikal Mühendisliği",
            "Enerji Sistemleri Mühendisliği",
            "Endüstri Mühendisliği",
            "Gıda Mühendisliği",
            "Mekatronik Mühendisliği",
            "Uçak Mühendisliği",
            "Yazılım Mühendisliği"
        ]
        self.okudugu_bolum_combo = ttk.Combobox(self.F_ekle, values=okudugu_bolum_options, state="readonly", width=33)
        self.okudugu_bolum_combo.grid(row=4, column=1, pady=5)

        # Doğum Yılı
        ttk.Label(self.F_ekle, text="Doğum Yılı: ").grid(row=5, column=0, pady=5, sticky=tk.W)
        self.dogum_yili_spinbox = ttk.Spinbox(self.F_ekle, from_=1950, to=2005, width=33)
        self.dogum_yili_spinbox.grid(row=5, column=1, pady=5)

        # Sınıf
        ttk.Label(self.F_ekle, text="Sınıf: ").grid(row=6, column=0, pady=5, sticky=tk.W)
        sinif_options = ["1.sınıf", "2.sınıf", "3.sınıf", "4.sınıf"]
        self.sinif_combo = ttk.Combobox(self.F_ekle, values=sinif_options, state="readonly", width=33)
        self.sinif_combo.grid(row=6, column=1, pady=5)

        # Kayıt Et butonu
        B3 = tk.Button(self.F_ekle, text="KAYIT ET", command=self.kayit_et, fg="green", cursor="hand2", width=15)
        B3.grid(row=7, column=1, pady=8, sticky=tk.NE)

    def kayit_et(self):
        # Kullanıcıdan alınan verileri kontrol et
        adi = self.E1.get().strip()
        soyadi = self.E2.get().strip()
        cinsiyet = self.cinsiyet_combo.get()
        dogum_yeri = self.dogum_yeri_combo.get()
        okudugu_bolum = self.okudugu_bolum_combo.get()
        dogum_yili = self.dogum_yili_spinbox.get().strip()
        sinif = self.sinif_combo.get()

        # Giriş doğrulama
        if not adi:
            messagebox.showerror("Hata", "Lütfen Ad alanını doldurun.")
            self.master.focus_force()
            return
        if not soyadi:
            messagebox.showerror("Hata", "Lütfen Soyad alanını doldurun.")
            self.master.focus_force()
            return
        if not cinsiyet:
            messagebox.showerror("Hata", "Lütfen Cinsiyet alanını doldurun.")
            self.master.focus_force()
            return
        if not dogum_yeri:
            messagebox.showerror("Hata", "Lütfen Doğum Yeri alanını doldurun.")
            self.master.focus_force()
            return
        if not okudugu_bolum:
            messagebox.showerror("Hata", "Lütfen Okuduğu Bölüm alanını doldurun.")
            self.master.focus_force()
            return
        if not dogum_yili:
            messagebox.showerror("Hata", "Lütfen Doğum Yılı alanını doldurun.")
            self.master.focus_force()
            return
        if not sinif:
            messagebox.showerror("Hata", "Lütfen Sınıf alanını doldurun.")
            self.master.focus_force()
            return

        try:
            # Doğrulama işleminden geçen verileri veritabanına ekle
            sql = """INSERT INTO ogrenciler (
                        Adi, Soyadi, Cinsiyet, Dogum_Yeri, Okudugu_Bolum, Dogum_Yili, Sinif
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)"""

            # Parametreleri bir demet olarak sağlayın
            params = (
                adi,
                soyadi,
                cinsiyet,
                dogum_yeri,
                okudugu_bolum,
                int(dogum_yili),
                sinif
            )

            # SQL sorgusunu çalıştırın
            self.im.execute(sql, params)

            # Değişiklikleri kaydedin
            self.baglanti.commit()

            # Başarılı bir şekilde kaydedildiğine dair mesajı gösterin
            messagebox.showinfo("Bilgi", "Kayıt Başarılı")

        except Exception as e:
            # Hata mesajını daha spesifik bir şekilde gösterin
            messagebox.showerror("Hata", f"Kayıt Oluşturulamadı. Hata: {str(e)}")

    def listele(self):
        try:
            # Eğer ekleme paneli varsa kaldır
            if self.F_ekle:
                self.F_ekle.destroy()
            # Eğer listeleme paneli varsa kaldır
            if self.F_listele:
                self.F_listele.destroy()

            # Yeni listeleme paneli oluştur ve yerleştir
            self.F_listele = tk.Frame(self.master)
            self.F_listele.place(relx=0.5, rely=0.5, anchor="center")

            # Veritabanından öğrenci verilerini çek
            self.im.execute("SELECT * FROM ogrenciler")
            data = self.im.fetchall()

            # Arama fonksiyonu
            def search():
                deger = self.ara.get()
                query = "SELECT id, Adi, Soyadi, Cinsiyet, Dogum_Yeri, Okudugu_Bolum, Dogum_Yili, Sinif " \
                        "FROM ogrenciler WHERE Adi LIKE ? OR Soyadi LIKE ? OR Okudugu_Bolum LIKE ?"

                # Güvenli parametreli sorgu kullanımı
                self.im.execute(query, ('%' + deger + '%', '%' + deger + '%', '%' + deger + '%'))
                
                rows = self.im.fetchall()
                update(rows)

                bulunanVeri = len(rows)
                toplamverilbl["text"] = ""
                AraLBL["text"] = "Bulunan Veri: " + str(bulunanVeri)
                AraLBL.grid(row=3, column=0, sticky="w")

            # Arama kutusu ve butonu
            self.ara = tk.Entry(self.F_listele, width=35)
            self.ara.grid(row=0, column=0, sticky="w", pady=20, padx=10)
            self.araBTN = tk.Button(self.F_listele, text="Ara", fg="blue", command=search, width=5)
            self.araBTN.grid(row=0, column=0, sticky="w", pady=20, padx=230)

            # Tablo görüntüleme için Treeview
            self.tv = ttk.Treeview(self.F_listele, columns=(1, 2, 3, 4, 5, 6, 7, 8), show='headings', height=10)
            self.tv.grid(sticky="nsew")
            self.tv.bind("<Button-3>", self.popup)
            self.tv.heading(1, text='ID')
            self.tv.heading(2, text='Adı')
            self.tv.heading(3, text='Soyadı')
            self.tv.heading(4, text='Cinsiyet')
            self.tv.heading(5, text='Doğum Yeri')
            self.tv.heading(6, text='Okudugu Bolum')
            self.tv.heading(7, text='Doğum Yılı')
            self.tv.heading(8, text='Sınıf')

            # Tablo sütun genişlikleri
            self.tv.column("1", minwidth=10, width=30)
            self.tv.column("2", minwidth=50, width=100)
            self.tv.column("3", minwidth=50, width=100)
            self.tv.column("4", minwidth=50, width=60)
            self.tv.column("5", minwidth=10, width=150)
            self.tv.column("6", minwidth=10, width=150)
            self.tv.column("7", minwidth=10, width=85)
            self.tv.column("8", minwidth=10, width=60)

            # Dikey ve yatay kaydırma çubukları
            sb = tk.Scrollbar(self.F_listele, orient=tk.VERTICAL, command=self.tv.yview)
            sb.grid(row=1, column=1, sticky="ns")
            sb2 = tk.Scrollbar(self.F_listele, orient=tk.HORIZONTAL, command=self.tv.xview)
            sb2.grid(row=2, column=0, sticky="ew")

            # Veri sayısı bilgisi
            toplamVeri = f"{len(data)} Veri Bulundu."
            toplamverilbl = tk.Label(self.F_listele, text=toplamVeri)
            toplamverilbl.grid(row=3, column=0, sticky="w")
            tk.Button(self.F_listele, text="Tabloyu Yenile", fg="green", command=self.yenile).grid(row=3, column=0, sticky="s")
            AraLBL = tk.Label(self.F_listele)

            # Treeview'e veriyi ekle
            self.tv.config(yscrollcommand=sb2.set)
            self.tv.configure(yscrollcommand=sb.set, xscrollcommand=sb2.set)
            s = 1
            for i in data:
                self.tv.insert(parent='', index=s, iid=s, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
                s += 1

            # Verileri güncelleyen fonksiyon
            def update(rows):
                self.tv.delete(*self.tv.get_children())
                for i in rows:
                    self.tv.insert("", "end", values=i)

        except Exception as e:
            # Hata durumunda uyarı göster
            messagebox.showwarning("Hata", "Veri Tabanı Bulunamadı")

    def yenile(self):
        # Listeleme panelini kaldır ve tekrar listele
        self.F_listele.destroy()
        self.listele()

    def popup(self, event):
        # Sağ tıklama menüsü oluştur ve göster
        iid = self.tv.identify_row(event.y)
        if iid:
            m = tk.Menu(root, tearoff=0)
            m.add_command(label="Düzenle", command=self.duzenle)
            self.tv.selection_set(iid)
            self.at = self.tv.selection_set(iid)
            m.post(event.x_root, event.y_root)
        else:
            pass

    def duzenle(self):
        # Seçilen verinin ID'sini al ve düzenleme penceresini oluştur
        focus = self.tv.focus()
        numara = self.tv.item(focus)["values"][0]
        yeniWin = tk.Toplevel()
        yeniWin.wm_title("Düzenle")
        windowWidth = yeniWin.winfo_reqwidth()
        windowHeight = yeniWin.winfo_reqheight()
        positionRight = int(yeniWin.winfo_screenwidth() / 2 - windowWidth / 1)
        positionDown = int(yeniWin.winfo_screenheight() / 3 - windowHeight / 3)
        yeniWin.geometry(f"420x370+{positionRight}+{positionDown}")
        yeniWin.resizable(width=False, height=False)

        # Veriyi kaydetme fonksiyonu
        def veriKayit():
            self.im.execute(
                "CREATE TABLE IF NOT EXISTS ogrenciler (Adi VARCHAR(45), Soyadi VARCHAR(45), Cinsiyet VARCHAR(10), "
                "Dogum_Yeri VARCHAR(45), Okudugu_Bolum VARCHAR(45), Dogum_Yili INT, Sinif VARCHAR(5))")  # Tablo oluşturma

            # Seçilen ID'ye sahip öğrenciyi güncelle
            self.im.execute("UPDATE ogrenciler SET Adi = ?, Soyadi = ?, Okudugu_Bolum = ?, Sinif = ? WHERE id = ?",
                            (self.E1.get(), self.E2.get(), self.okudugu_bolum_combo.get(), self.sinif_combo.get(), numara))
            self.baglanti.commit()
            # Başarılı kayıt mesajını göster
            say = tk.Label(yeniWin, text="Kayıt Edildi.", font="bold", fg="green")
            say.pack(side=tk.BOTTOM)
            say.after(2000, say.destroy)
            # Düzenle butonunu tekrar etkinleştirme
            B4.config(state="normal")
            # Değişiklikleri kaydet butonunu devre dışı bırakma
            B3.config(state="disable")

        # Veriyi düzenleme fonksiyonu
        def veriDuzenle():
            self.E1.config(state="normal")
            self.E2.config(state="normal")
            self.okudugu_bolum_combo.config(state="normal")
            self.sinif_combo.config(state="normal")
            B3.config(state="normal", cursor="hand2")

        # Veriyi silme fonksiyonu
        def veriSil():
            evet = messagebox.askyesno("Sil", "Veri Tabanından silmek istiyormusunuz?")
            self.master.focus_force()
            if evet:
                # Seçilen ID'ye sahip öğrenciyi sil
                self.im.execute("DELETE FROM ogrenciler WHERE id = ?", [numara])
                self.baglanti.commit()
                yeniWin.destroy()

        F_ekle = tk.Frame(yeniWin)
        F_ekle.pack()

        # Öğrenci Adı
        tk.Label(F_ekle, text="Öğrenci Adı: ").grid(row=0, column=0, pady=5, sticky=tk.W)
        self.E1 = tk.Entry(F_ekle, width=35)
        self.E1.insert(0, self.tv.item(focus)["values"][1])
        self.E1.config(state="disable")
        self.E1.grid(row=0, column=1, pady=5)

        # Öğrenci Soyadı
        tk.Label(F_ekle, text="Öğrenci Soyadı: ").grid(row=1, column=0, pady=5, sticky=tk.W)
        self.E2 = tk.Entry(F_ekle, width=35)
        self.E2.insert(0, self.tv.item(focus)["values"][2])
        self.E2.config(state="disable")
        self.E2.grid(row=1, column=1, pady=5)

        # Okuduğu Bölüm
        tk.Label(F_ekle, text="Okuduğu Bölüm: ").grid(row=4, column=0, pady=5, sticky=tk.W)
        self.okudugu_bolum_combo = ttk.Combobox(F_ekle, values=[
            "Bilgisayar Mühendisliği",
            "Elektrik Mühendisliği",
            "Makine Mühendisliği",
            "İnşaat Mühendisliği",
            "Kimya Mühendisliği",
            "Biomedikal Mühendisliği",
            "Enerji Sistemleri Mühendisliği",
            "Endüstri Mühendisliği",
            "Gıda Mühendisliği",
            "Mekatronik Mühendisliği",
            "Uçak Mühendisliği",
            "Yazılım Mühendisliği"], state="readonly", width=33)
        self.okudugu_bolum_combo.set(self.tv.item(focus)["values"][5])
        self.okudugu_bolum_combo.config(state="disable")
        self.okudugu_bolum_combo.grid(row=4, column=1, pady=5)

        # Sınıf
        tk.Label(F_ekle, text="Sınıf: ").grid(row=6, column=0, pady=5, sticky=tk.W)
        sinif_options = ["1.sınıf", "2.sınıf", "3.sınıf", "4.sınıf"]
        self.sinif_combo = ttk.Combobox(F_ekle, values=sinif_options, state="readonly", width=33)
        self.sinif_combo.insert(0, self.tv.item(focus)["values"][7])
        self.sinif_combo.config(state="disable")
        self.sinif_combo.grid(row=6, column=1, pady=5)

        # Kayıt Et butonu
        B3 = tk.Button(F_ekle, text="Kayıt Et", command=veriKayit, fg="green", width=15)
        B3.config(state="disable")
        B3.grid(row=7, column=1, pady=8, sticky=tk.NE)

        # Düzenle butonu
        B4 = tk.Button(F_ekle, text="Düzenle", command=veriDuzenle, fg="blue", cursor="hand2", width=15)
        B4.grid(row=8, column=1, pady=8, sticky=tk.NE)

        # Veriyi Sil butonu
        B5 = tk.Button(F_ekle, text="Veriyi Sil", command=veriSil, fg="red", cursor="hand2", width=15)
        B5.grid(row=9, column=1, pady=8, sticky=tk.NE)

    def exitProgram(self):
        # Programdan çıkış yap
        exit()

    def grafik_goster(self):
        # Grafik penceresini oluştur
        GrafikPenceresi(self.master)

class GrafikPenceresi:
    def __init__(self, master):
        # Pencere oluşturuluyor
        self.master = master
        self.pencere = tk.Toplevel(self.master)
        self.pencere.resizable(False, False)
        self.pencere.title("Öğrenci Sınıf Grafiği")
    
        # Boş bir sınıf oluşturuluyor
        self.grafik_gosterme_sayfasi = tk.Frame(self.pencere)
        self.grafik_gosterme_sayfasi.pack()

        # Veritabanından sınıflara göre öğrenci sayılarını çekip grafiği oluşturma
        self.grafik_ciz()

    def grafik_ciz(self):
        try:
            # Örnek veritabanı bağlantısı (kendi veritabanı bağlantınıza uygun olarak güncelleyin)
            conn = sqlite3.connect("ogrenci_kayit.db")
            cursor = conn.cursor()

            # Sınıflara göre öğrenci sayılarını çekme
            cursor.execute("SELECT CAST(Sinif AS INT), COUNT(*) FROM ogrenciler GROUP BY Sinif")
            sonuclar = cursor.fetchall()

            # Tüm sınıfları temsil eden bir liste oluşturma
            tum_siniflar = list(range(1, 5))
            sinif_sayilari = {satir[0]: satir[1] for satir in sonuclar}

            # Eksik sınıfları 0 ile doldurma
            ogrenci_sayilari = [sinif_sayilari.get(s, 0) for s in tum_siniflar]

            # Matplotlib sütun grafiği oluşturma
            fig, ax = plt.subplots()
            ax.bar(tum_siniflar, ogrenci_sayilari, color='blue')
            ax.set_xlabel('Sınıflar')
            ax.set_ylabel('Öğrenci Sayısı')
            ax.set_title('Sınıflara Göre Öğrenci Sayıları')

            # X ekseni tick'leri özelleştirme
            ax.set_xticks(tum_siniflar)
            ax.set_xticklabels([str(int(s)) for s in tum_siniflar])

            # Veritabanı bağlantısını kapatma
            conn.close()

            # Matplotlib grafiğini Tkinter penceresine ekleyerek gösterme
            canvas = FigureCanvasTkAgg(fig, master=self.grafik_gosterme_sayfasi)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        except Exception as e:
            # Hata durumunda uyarı göster
            messagebox.showwarning("Hata", "Grafik çizilemedi: {}".format(str(e)))
            self.master.focus_force()

class GrafikOluşturucu:
    def __init__(self, root):
        # Ana pencerenin oluşturulması
        self.root = root
        root.resizable(width=False, height=False)
        self.root.title("Grafik Oluşturma Aracı")
        
        # Giriş etiketleri ve giriş kutularının oluşturulması
        self.label_x = tk.Label(root, text="X Ekseni Değerleri'ni Virgül İle Ayırarak Giriniz:")
        self.label_x.grid(row=0, column=0, padx=50, pady=5, sticky='e')
        self.entry_x = tk.Entry(root, width=30)
        self.entry_x.grid(row=0, column=1, padx=5, pady=5)

        self.label_y = tk.Label(root, text="Y Ekseni Değerleri'ni Virgül İle Ayırarak Giriniz:")
        self.label_y.grid(row=1, column=0, padx=50, pady=5, sticky='e')
        self.entry_y = tk.Entry(root,  width=30)
        self.entry_y.grid(row=1, column=1, padx=5, pady=5)

        self.label_x_axis = tk.Label(root, text="X Ekseni Etiketi'ni Giriniz:")
        self.label_x_axis.grid(row=2, column=0, padx=50, pady=5, sticky='e')
        self.entry_x_axis = tk.Entry(root,  width=30)
        self.entry_x_axis.grid(row=2, column=1, padx=5, pady=5)

        self.label_y_axis = tk.Label(root, text="Y Ekseni Etiketi'ni Giriniz:")
        self.label_y_axis.grid(row=3, column=0, padx=50, pady=5, sticky='e')
        self.entry_y_axis = tk.Entry(root,  width=30)
        self.entry_y_axis.grid(row=3, column=1, padx=5, pady=5)

        self.label_title = tk.Label(root, text="Grafik Başlığını Giriniz:")
        self.label_title.grid(row=4, column=0, padx=50, pady=5, sticky='e')
        self.entry_title = tk.Entry(root,  width=30)
        self.entry_title.grid(row=4, column=1, padx=5, pady=5)

        # Grafiği seçmek için Combobox
        self.graph_type_label = tk.Label(root, text="Grafik Türünü Seçiniz:")
        self.graph_type_label.grid(row=5, column=0, padx=50, pady=5, sticky='e')
        self.graph_type_combobox = ttk.Combobox(root, values=["Çizgi Grafiği", "Sütun Grafiği"])
        self.graph_type_combobox.grid(row=5, column=1, padx=5, pady=0)
        self.graph_type_combobox.set("Türü Seçiniz")  # Varsayılan olarak türü seçiniz yazılı
        
        # Temizle butonu
        self.button_clear = tk.Button(root, text="Temizle", command=self.temizle, width=15, fg="red")
        self.button_clear.grid(row=6, column=0, pady=10, padx=45, sticky='w')
        
        # Kaydet butonu
        self.button_save = tk.Button(root, text="Kaydet", command=self.kaydet, width=15, fg="blue")
        self.button_save.grid(row=6, column=0, pady=10, padx=50, sticky='e')
        
        # Grafik oluşturma butonu
        self.button_draw = tk.Button(root, text="Grafik Oluştur", command=self.grafik_olustur, width=20, fg="green")
        self.button_draw.grid(row=6, column=1, pady=10, padx=70, sticky='e')
        
        # Matplotlib figür ve grafik alanının oluşturulması
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        
        # Tkinter için Matplotlib canvas widget'ının oluşturulması
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=7, column=0, columnspan=2)

    def grafik_olustur(self):
    
        # X ve Y değerlerini al
        x_values_str = self.entry_x.get()
        y_values_str = self.entry_y.get()
        
        # Giriş alanlarını kontrol et
        if not x_values_str or not y_values_str:
            messagebox.showerror("Hata", "X ve Y değerleri boş bırakılamaz.")
            self.root.focus_force()
            return

        # X ve Y değerlerini listeye dönüştür
        x_values = [float(x) for x in x_values_str.split(",")]
        y_values = [float(y) for y in y_values_str.split(",")]

        # X ve Y değerlerinin sayısını kontrol et
        if len(x_values) != len(y_values):
            messagebox.showerror("Hata", "X ve Y değerlerinin sayısı eşit olmalıdır.")
            self.root.focus_force()
            return
        
        # Tür seçimini kontrol et
        if self.graph_type_combobox.get() == "Türü Seçiniz":
            messagebox.showerror("Hata", "Lütfen bir grafik türü seçiniz.")
            self.root.focus_force()
            return

        x_label = self.entry_x_axis.get()
        y_label = self.entry_y_axis.get()
        title = self.entry_title.get()

        # Grafiği seçilen türde çiz
        graph_type = self.graph_type_combobox.get()
        self.ax.clear()

        if graph_type == "Çizgi Grafiği":
            self.ax.plot(x_values, y_values, marker='o', color='red', linestyle='-', linewidth=2)
        elif graph_type == "Sütun Grafiği":
            self.ax.bar(x_values, y_values, color='red', edgecolor='black', width=0.4)

        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(title)
        self.ax.grid(True)
        
        # Canvas'ı güncelle
        self.canvas.draw()
   
    def kaydet(self):
        # Dosya kaydetme penceresini aç
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])

        # Eğer bir dosya seçildiyse, grafiği bir resim olarak kaydet
        if file_path:
            self.fig.savefig("temp_plot.jpg", format="jpg")  # Grafiği geçici bir dosyaya kaydet
            img = Image.open("temp_plot.jpg")  # PIL ile resmi aç
            img.save(file_path, "JPEG")  # Seçilen dosyaya JPEG olarak kaydet
            img.close()
            
            messagebox.showinfo("Başarılı", "Grafik başarıyla kaydedildi.")
            self.root.focus_force()            

    def temizle(self):
        result = messagebox.askquestion("Onay", "Girilen verileri temizlemek istiyor musunuz?", icon='warning')
        self.root.focus_force()
        # Kullanıcı "Evet" derse temizleme işlemini gerçekleştir
        if result == 'yes':
           self.entry_x.delete(0, tk.END)
           self.entry_y.delete(0, tk.END)
           self.entry_x_axis.delete(0, tk.END)
           self.entry_y_axis.delete(0, tk.END)
           self.entry_title.delete(0, tk.END)
           self.graph_type_combobox.set("Türü Seçiniz")
           self.ax.clear()
           self.canvas.draw()

root = tk.Tk()
root.title("Ana Pencere")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

giris_penceresi = GirisPenceresi(root)
root.mainloop()
