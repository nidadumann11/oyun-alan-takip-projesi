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

        # Başlat ve bitir butonları
        self.start_button = tk.Button(root, text="Başlat", command=self.baslat, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.start_button.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.stop_button = tk.Button(root, text="Bitir", command=self.bitir, bg="#FF6347", fg="white", font=("Helvetica", 12))
        self.stop_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Çocuk listesi (Treeview)
        self.child_tree = ttk.Treeview(root, columns=("name", "parent", "start_time"), show="headings", height=10)
        self.child_tree.grid(row=4, column=0, columnspan=3, pady=10)
        self.child_tree.heading("name", text="Çocuk Adı")
        self.child_tree.heading("parent", text="Ebeveyn Numarası")
        self.child_tree.heading("start_time", text="Giriş Saati")
        self.child_tree.column("name", width=200)
        self.child_tree.column("parent", width=200)
        self.child_tree.column("start_time", width=150)

        # Kayıtları ve geliri göster butonları
        self.show_records_button = tk.Button(root, text="Kayıtları Göster", command=self.kayitlari_goster, bg="#2196F3", fg="white", font=("Helvetica", 12))
        self.show_records_button.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.show_income_button = tk.Button(root, text="Geliri Göster", command=self.geliri_goster, bg="#FF9800", fg="white", font=("Helvetica", 12))
        self.show_income_button.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Durum etiketi
        self.status_label = tk.Label(root, text="", font=("Helvetica", 14), fg="blue", bg="#F0F0F0")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=10)

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
        if not child_name or not parent_number:
            self.status_label.config(text="Çocuk adı veya ebeveyn numarası boş olamaz!")
            return

        if child_name in self.start_times:
            self.status_label.config(text="Bu çocuk zaten başladı!")
            return

        start_time = datetime.now()
        self.start_times[child_name] = (parent_number, start_time)
        self.child_tree.insert("", "end", values=(child_name, parent_number, start_time.strftime('%H:%M')))
        self.status_label.config(text=f"{child_name} için takip başladı.")

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

        parent_number, start_time = self.start_times.pop(child_name)
        end_time = datetime.now()
        duration = end_time - start_time
        minutes = duration.total_seconds() / 60
        cost = round(minutes * 2, 2)  # Dakika başına 2 birim ücret
        self.total_income += cost
        self.status_label.config(text=f"{child_name} için süre: {duration}, Ücret: {cost} TL")

        # Kayıtları CSV'ye yaz
        with open('game_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([child_name, parent_number, start_time, end_time, duration, cost])
            
        # Listeden kaldır
        self.child_tree.delete(selected_item)

    def geliri_goster(self):
        try:
            with open('game_log.csv', mode='r') as file:
                reader = csv.reader(file)
                child_income = {}
                total_income = 0

                # Her çocuğun gelirini hesapla
                for row in reader:
                    if len(row) < 6:  # Satırda en az 6 sütun olduğundan emin olun
                        continue
                    child_name = row[0]
                    cost = float(row[5])
                    total_income += cost
                    if child_name in child_income:
                        child_income[child_name] += cost
                    else:
                        child_income[child_name] = cost

                # Gelirleri ve toplam geliri göster
                income_text = "\n".join([f"{child}: {income} TL" for child, income in child_income.items()])
                self.status_label.config(text=f"Gelirler:\n{income_text}\nToplam Gelir: {total_income} TL")
        except FileNotFoundError:
            self.status_label.config(text="Henüz kayıt bulunmuyor!")

    def kayitlari_goster(self):
        try:
            with open('game_log.csv', mode='r') as file:
                reader = csv.reader(file)
                records = list(reader)

                if not records:
                    self.status_label.config(text="Henüz kayıt bulunmuyor!")
                    return

                # Kayıtları bir metin olarak birleştir
                records_text = "\n".join([", ".join(row) for row in records])
                self.status_label.config(text=f"Kayıtlar:\n{records_text}")
        except FileNotFoundError:
            self.status_label.config(text="Henüz kayıt bulunmuyor!")

# Uygulamayı başlat
root = tk.Tk()
app = OyunTakipApp(root)
root.mainloop()