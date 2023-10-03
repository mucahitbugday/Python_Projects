# tkinter ve diğer gerekli modülleri içe aktarın
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from pydub import AudioSegment
import shutil

# Varsayılan bölme uzunluğu (5 dakika)
default_split_length = 5

# MP3 dosyasını belirtilen uzunlukta parçalara ayırmak için kullanılacak fonksiyon
def split_mp3(file_path, split_length, output_format, progress_bar):
    # MP3 dosyasını yükleyin ve dosya adını alın
    audio = AudioSegment.from_mp3(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Toplam bölünmüş parçaların sayısını ve ilerleme adımını hesaplayın
    total_splits = len(audio) // (split_length * 1000) + 1
    progress_step = 100 / total_splits

    # Yeni bir klasör oluşturun ve bölünmüş parçaları kaydedin
    output_folder = os.path.join(os.path.dirname(file_path), f"{file_name}")
    os.makedirs(output_folder, exist_ok=True)

    for i in range(0, len(audio), split_length * 1000):
        split = audio[i:i + split_length * 1000]
        split_index = i // (split_length * 1000) + 1
        output_file = os.path.join(output_folder, f"{file_name}_{split_index}.{output_format}")
        split.export(output_file, format=output_format)
        progress_bar["value"] += progress_step
        root.update_idletasks()

    # İşlem tamamlandığında ilerleme çubuğunu sıfırlayın
    progress_bar["value"] = 0

# Dosya seçme işlevini tanımlayın
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Dosyaları", "*.mp3")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

# Bölme düğmesine tıklanınca çağrılacak işlevi tanımlayın
def split_button_click():
    file_path = file_entry.get()
    split_length = int(length_entry.get()) * 60
    output_format = format_var.get()

    if os.path.isfile(file_path):
        # İşlem başladığında ilerleme çubuğunu maksimuma ayarlayın
        progress_bar["maximum"] = 100
        # MP3 dosyasını bölme işlemini başlatın ve sonucu bildirin
        split_mp3(file_path, split_length, output_format, progress_bar)
        status_label.config(text="MP3 dosyası bölündü ve isimler güncellendi!")
    else:
        # Dosya bulunamadığında hata mesajı verin
        status_label.config(text="Dosya bulunamadı!")

# Tkinter penceresi oluşturun
root = tk.Tk()
root.title("MP3 Bölücü")

# Dosya seçme düğmesi
select_button = tk.Button(root, text="MP3 Dosya Seç", command=select_file)
select_button.pack()

# Dosya seçme aracı
file_label = tk.Label(root, text="Seçilen MP3 Dosya:")
file_label.pack()
file_entry = tk.Entry(root, width=50)
file_entry.pack()

# Uzunluk girişi
length_label = tk.Label(root, text="Bölme Uzunluğu (dakika):")
length_label.pack()
length_entry = tk.Entry(root, width=10)
length_entry.pack()
length_entry.insert(0, default_split_length)  # Varsayılan değeri ayarla

# Ses formatı seçimi
format_label = tk.Label(root, text="Çıkış Formatı:")
format_label.pack()
formats = ["mp3", "wav", "ogg"]  # Ekleyebilirsiniz
format_var = tk.StringVar(value=formats[0])
format_menu = ttk.Combobox(root, textvariable=format_var, values=formats)
format_menu.pack()

# Bölme düğmesi
split_button = tk.Button(root, text="MP3 Dosyasını Böl", command=split_button_click)
split_button.pack()

# Durum etiketi
status_label = tk.Label(root, text="")
status_label.pack()

# İlerleme çubuğu
progress_bar = ttk.Progressbar(root, length=200, mode="determinate")
progress_bar.pack()

# Sürüm ve yazılımcı etiketi
version_label = tk.Label(root, text=" V.1.0 | @m")
version_label.pack(side="bottom", anchor="e")

# GUI'yi başlatma
root.mainloop()