import tkinter as tk
from tkinter import ttk
from datetime import datetime
import csv
from PIL import Image, ImageTk  # PNG simge için gerekli

class OyunTakipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Oyun Alanı Takip Programı")
        self.root.configure(bg="#F0F0F0")
        self.start_times = {}  # Çocuk adı ve başlangıç zamanlarını tutmak için
        self.total_income = 0  # Toplam gelir

        # Menü çubuğu ekle
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Günsonu raporu menüsü
        self.report_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.report_menu.add_command(label="Günsonu Raporu Al", command=self.gunsonu_raporu)
        self.menu_bar.add_cascade(label="Günsonu Raporu", menu=self.report_menu)

        # Ayarlar menüsü
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.settings_menu.add_command(label="Ayarlar", command=self.ayarlar_islemi)
        self.menu_bar.add_cascade(label="Ayarlar", menu=self.settings_menu)

        # Pencereyi ekrana ortala
        self.center_window(700, 600)  # Genişlik: 700, Yükseklik: 600

        # Başlık
        self.title_label = tk.Label(root, text="Oyun Alanı Takip Programı", font=("Helvetica", 16, "bold"), fg="darkblue", bg="#F0F0F0")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Çocuk adı ve ebeveyn numarası girişi
        self.name_label = tk.Label(root, text="Çocuk Adı:", font=("Helvetica", 12), bg="#F0F0F0")
        self.name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = tk.Entry(root, font=("Helvetica", 12))
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.parent_label = tk.Label(root, text="Ebeveyn Numarası:", font=("Helvetica", 12), bg="#F0F0F0")
        self.parent_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.parent_entry = tk.Entry(root, font=("Helvetica", 12))
        self.parent_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Kalış süresi seçimi
        self.duration_label = tk.Label(root, text="Kalış Süresi:", font=("Helvetica", 12), bg="#F0F0F0")
        self.duration_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.duration_var = tk.StringVar(value="30 dk")  # Varsayılan olarak 30 dk seçilmiş

        # 30 dk seçeneği
        self.radio_30 = tk.Radiobutton(root, text="30 dk", variable=self.duration_var, value="30 dk",
                                       font=("Helvetica", 12), bg="#F0F0F0", activebackground="#F0F0F0",
                                       indicatoron=True)
        self.radio_30.grid(row=3, column=1, padx=5, pady=10, sticky="w")

        # 60 dk seçeneği
        self.radio_60 = tk.Radiobutton(root, text="60 dk", variable=self.duration_var, value="60 dk",
                                       font=("Helvetica", 12), bg="#F0F0F0", activebackground="#F0F0F0",
                                       indicatoron=True)
        self.radio_60.grid(row=3, column=1, padx=5, pady=10, sticky="e")

        # Başlat, bitir ve jeton butonları
        self.start_button = tk.Button(root, text="Başlat", command=self.baslat, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.start_button.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        self.stop_button = tk.Button(root, text="Bitir", command=self.bitir, bg="#FF6347", fg="white", font=("Helvetica", 12))
        self.stop_button.grid(row=4, column=2, padx=10, pady=10, sticky="w")

        self.token_button = tk.Button(root, text="Jeton", command=self.jeton_islemi, bg="blue", fg="white", font=("Helvetica", 12))
        self.token_button.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Çocuk listesi (Treeview)
        self.child_tree = ttk.Treeview(root, columns=("name", "parent", "start_time", "end_time", "cost", "payment"), show="headings", height=10)
        self.child_tree.grid(row=6, column=0, columnspan=3, pady=10)
        self.child_tree.heading("name", text="Çocuk Adı")
        self.child_tree.heading("parent", text="Ebeveyn Numarası")
        self.child_tree.heading("start_time", text="Giriş Saati")
        self.child_tree.heading("end_time", text="Çıkış Saati")
        self.child_tree.heading("cost", text="Ücret")
        self.child_tree.heading("payment", text="Ödeme")
        self.child_tree.column("name", width=200)
        self.child_tree.column("parent", width=200)
        self.child_tree.column("start_time", width=150)
        self.child_tree.column("end_time", width=150)
        self.child_tree.column("cost", width=100)
        self.child_tree.column("payment", width=100)

        # Geliri göster butonu
        self.show_income_button = tk.Button(root, text="Geliri Göster", command=self.geliri_goster, bg="#FF9800", fg="white", font=("Helvetica", 12))
        self.show_income_button.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        # Durum etiketi
        self.status_label = tk.Label(root, text="", font=("Helvetica", 14), fg="blue", bg="#F0F0F0")
        self.status_label.grid(row=8, column=0, columnspan=3, pady=10)

    def center_window(self, width, height):
        """Pencereyi ekrana ortalamak için bir yardımcı fonksiyon."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def baslat(self):
        child_name = self.name_entry.get().strip()
        parent_number = self.parent_entry.get().strip()
        duration = self.duration_var.get()  # Seçilen kalış süresi

        if not child_name or not parent_number:
            self.status_label.config(text="Çocuk adı veya ebeveyn numarası boş olamaz!")
            return

        if child_name in self.start_times:
            self.status_label.config(text="Bu çocuk zaten başladı!")
            return

        # Ücreti hesapla
        if duration == "30 dk":
            cost = 150
        elif duration == "60 dk":
            cost = 200
        else:
            cost = 0

        start_time = datetime.now()
        self.start_times[child_name] = (parent_number, start_time, duration, cost)
        # Yeni eklenen çocuğu listenin en üstüne ekle
        self.child_tree.insert("", 0, values=(child_name, parent_number, start_time.strftime('%H:%M'), "", f"{cost} TL", "Alınmadı"))
        self.status_label.config(text=f"{child_name} için takip başladı. Kalış Süresi: {duration}, Ücret: {cost} TL")

    def bitir(self):
        selected_item = self.child_tree.selection()
        if not selected_item:
            self.status_label.config(text="Lütfen bir çocuk seçin!")
            return

        values = self.child_tree.item(selected_item, "values")
        child_name = values[0]

        if child_name not in self.start_times:
            self.status_label.config(text="Bu çocuk için başlangıç zamanı bulunamadı!")
            return

        parent_number, start_time, duration, cost = self.start_times.pop(child_name)
        end_time = datetime.now()

        # Çıkış saatini ve ödeme durumunu güncelle
        self.child_tree.item(selected_item, values=(child_name, parent_number, start_time.strftime('%H:%M'), end_time.strftime('%H:%M'), f"{cost} TL", "Alındı"))
        self.status_label.config(text=f"{child_name} için takip sona erdi. Çıkış Saati: {end_time.strftime('%H:%M')}, Ücret: {cost} TL")

        # CSV dosyasına yaz
        try:
            with open('game_log.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([child_name, parent_number, start_time.strftime('%H:%M'), end_time.strftime('%H:%M'), duration, cost])
        except Exception as e:
            self.status_label.config(text=f"Dosyaya yazma hatası: {str(e)}")

    def geliri_goster(self):
        try:
            with open('game_log.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Başlık satırını atla (eğer varsa)
                child_income = {}
                total_income = 0

                # Her çocuğun gelirini hesapla
                for row in reader:
                    if len(row) < 6:  # Satırda en az 6 sütun olduğundan emin olun
                        continue
                    child_name = row[0]
                    cost = float(row[5])  # Ücret sütununu al ve float'a çevir
                    total_income += cost
                    if child_name in child_income:
                        child_income[child_name] += cost
                    else:
                        child_income[child_name] = cost

                # Gelirleri ve toplam geliri göster
                if child_income:
                    income_text = "\n".join([f"{child}: {income} TL" for child, income in child_income.items()])
                    self.status_label.config(text=f"Gelirler:\n{income_text}\nToplam Gelir: {total_income} TL")
                else:
                    self.status_label.config(text="Henüz gelir kaydı bulunmuyor!")
        except FileNotFoundError:
            self.status_label.config(text="Gelir dosyası bulunamadı!")
        except ValueError:
            self.status_label.config(text="Dosyadaki veriler hatalı!")
        except Exception as e:
            self.status_label.config(text=f"Bir hata oluştu: {str(e)}")

    def jeton_islemi(self):
        """Jeton işlemleri için yer tutucu."""
        self.status_label.config(text="Jeton işlemi seçildi!")

    def ayarlar_islemi(self):
        """Ayarlar işlemleri için yer tutucu."""
        self.status_label.config(text="Ayarlar işlemi seçildi!")

    def gunsonu_raporu(self):
        """Günsonu raporu işlemleri için yer tutucu."""
        self.status_label.config(text="Günsonu raporu al seçildi!")

# Uygulamayı başlat
root = tk.Tk()
app = OyunTakipApp(root)
root.mainloop()