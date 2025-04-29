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
        self.start_time = None

        # PNG simgeyi pencereye ekle
        try:
            icon_image = Image.open("button.png")  # Burada değiştirdik
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(False, icon_photo)
        except Exception as e:
            print("Simge yüklenemedi:", e)

        # Başlık
        self.title_label = tk.Label(root, text="Oyun Alanı Takip Programı", font=("Helvetica", 16, "bold"), fg="darkblue", bg="#F0F0F0")
        self.title_label.grid(row=0, columnspan=2, pady=20)

        # Çocuk adı girişi
        self.name_label = tk.Label(root, text="Çocuk Adı:", font=("Helvetica", 12), bg="#F0F0F0")
        self.name_label.grid(row=1, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(root, font=("Helvetica", 12))
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Başlat ve bitir butonları
        self.start_button = tk.Button(root, text="Başlat", command=self.baslat, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.start_button.grid(row=2, column=0, padx=10, pady=10)
        self.stop_button = tk.Button(root, text="Bitir", command=self.bitir, bg="#FF6347", fg="white", font=("Helvetica", 12))
        self.stop_button.grid(row=2, column=1, padx=10, pady=10)

        # Durum etiketi
        self.status_label = tk.Label(root, text="", font=("Helvetica", 14), fg="blue", bg="#F0F0F0")
        self.status_label.grid(row=3, columnspan=2, pady=10)

        # Kayıtları Göster butonu
        self.show_button = tk.Button(root, text="Kayıtları Göster", command=self.kayitlari_goster, bg="#FFD700", font=("Helvetica", 12))
        self.show_button.grid(row=4, columnspan=2, pady=10)

        # Toplam Geliri Göster butonu
        self.total_button = tk.Button(root, text="Toplam Geliri Göster", command=self.geliri_goster, bg="#FF8C00", font=("Helvetica", 12))
        self.total_button.grid(row=5, columnspan=2, pady=10)

    def baslat(self):
        self.start_time = datetime.now()
        self.status_label.config(text="Başladı...")

    def bitir(self):
        if self.start_time is None:
            self.status_label.config(text="Başlatılmadı!")
        else:
            end_time = datetime.now()
            duration = end_time - self.start_time
            self.status_label.config(text=f"Süre: {duration}")

            with open('game_log.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.name_entry.get(), self.start_time, end_time, duration])

    def kayitlari_goster(self):
        with open('game_log.csv', mode='r') as file:
            reader = csv.reader(file)
            records = list(reader)

        show_window = tk.Toplevel(self.root)
        show_window.title("Kayıtlar")

        for record in records:
            record_label = tk.Label(show_window, text=str(record), font=("Helvetica", 10))
            record_label.pack()

    def geliri_goster(self):
        total_duration = 0
        with open('game_log.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    duration = row[3]
                    total_duration += self.convert_duration_to_minutes(duration)

        self.status_label.config(text=f"Toplam Süre: {round(total_duration, 2)} dakika")

    def convert_duration_to_minutes(self, duration):
        try:
            time_parts = duration.split(":")
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds = int(time_parts[2])
            return hours * 60 + minutes + seconds / 60
        except Exception as e:
            print(f"Hata: {e}")
            return 0

# Uygulamayı başlat
root = tk.Tk()
app = OyunTakipApp(root)
root.mainloop()
