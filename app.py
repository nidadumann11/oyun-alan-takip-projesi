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
        self.center_window(600, 500)  # Genişlik: 600, Yükseklik: 500

        # PNG simgeyi pencereye ekle
        try:
            icon_image = Image.open("button.png")  # Burada değiştirdik
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(False, icon_photo)
        except Exception as e:
            print("Simge yüklenemedi:", e)

        # Başlık
        self.title_label = tk.Label(root, text="Oyun Alanı Takip Programı", font=("Helvetica", 16, "bold"), fg="darkblue", bg="#F0F0F0")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Çocuk adı girişi
        self.name_label = tk.Label(root, text="Çocuk Adı:", font=("Helvetica", 12), bg="#F0F0F0")
        self.name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = tk.Entry(root, font=("Helvetica", 12))
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Başlat ve bitir butonları
        self.start_button = tk.Button(root, text="Başlat", command=self.baslat, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.start_button.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.stop_button = tk.Button(root, text="Bitir", command=self.bitir, bg="#FF6347", fg="white", font=("Helvetica", 12))
        self.stop_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Çocuk listesi
        self.child_listbox = tk.Listbox(root, font=("Helvetica", 12), height=10, width=40)
        self.child_listbox.grid(row=3, column=0, columnspan=2, pady=10)

        # Kayıtları ve geliri göster butonları
        self.show_records_button = tk.Button(root, text="Kayıtları Göster", command=self.kayitlari_goster, bg="#2196F3", fg="white", font=("Helvetica", 12))
        self.show_records_button.grid(row=5, column=0, padx=10, pady=5)  # Listenin altına taşındı
        self.show_income_button = tk.Button(root, text="Geliri Göster", command=self.geliri_goster, bg="#FF9800", fg="white", font=("Helvetica", 12))
        self.show_income_button.grid(row=6, column=0, padx=10, pady=5)  # Alt alta olacak şekilde düzenlendi

        # Durum etiketi
        self.status_label = tk.Label(root, text="", font=("Helvetica", 14), fg="blue", bg="#F0F0F0")
        self.status_label.grid(row=7, column=0, columnspan=2, pady=10)

    def center_window(self, width, height):
        """Pencereyi ekrana ortalamak için bir yardımcı fonksiyon."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def baslat(self):
        child_name = self.name_entry.get().strip()
        if not child_name:
            self.status_label.config(text="Çocuk adı boş olamaz!")
            return

        if child_name in self.start_times:
            self.status_label.config(text="Bu çocuk zaten başladı!")
            return

        start_time = datetime.now()
        self.start_times[child_name] = start_time
        self.child_listbox.insert(tk.END, f"{child_name} - Başladı: {start_time.strftime('%H:%M:%S')}")
        self.status_label.config(text=f"{child_name} için takip başladı.")

    def bitir(self):
        selected_index = self.child_listbox.curselection()
        if not selected_index:
            self.status_label.config(text="Lütfen bir çocuk seçin!")
            return

        selected_text = self.child_listbox.get(selected_index)
        child_name = selected_text.split(" - ")[0]

        if child_name not in self.start_times:
            self.status_label.config(text="Bu çocuk için başlangıç zamanı bulunamadı!")
            return

        start_time = self.start_times.pop(child_name)
        end_time = datetime.now()
        duration = end_time - start_time
        minutes = duration.total_seconds() / 60
        cost = round(minutes * 2, 2)  # Dakika başına 2 birim ücret
        self.total_income += cost
        self.status_label.config(text=f"{child_name} için süre: {duration}, Ücret: {cost} TL")

        # Kayıtları CSV'ye yaz
        with open('game_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([child_name, start_time, end_time, duration, cost])

        # Listeden kaldır
        self.child_listbox.delete(selected_index)

    def kayitlari_goster(self):
        try:
            with open('game_log.csv', mode='r') as file:
                records = file.readlines()
                self.status_label.config(text=f"Kayıtlar:\n{''.join(records[-5:])}")  # Son 5 kaydı göster
        except FileNotFoundError:
            self.status_label.config(text="Henüz kayıt bulunmuyor!")

    def geliri_goster(self):
        self.status_label.config(text=f"Toplam Gelir: {self.total_income} TL")

# Uygulamayı başlat
root = tk.Tk()
app = OyunTakipApp(root)
root.mainloop()
