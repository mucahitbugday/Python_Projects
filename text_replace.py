import tkinter as tk
from tkinter import filedialog

def dosya_degistir():
    dosya_yolu = filedialog.askopenfilename(filetypes=[("Metin Dosyaları", "*.txt")])
    if dosya_yolu:
        with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
            icerik = dosya.read()
            icerik = icerik.replace('\n', ' ')
        
        yeni_dosya_yolu = dosya_yolu[:-4] + '__NEW.txt'
        with open(yeni_dosya_yolu, 'w', encoding='utf-8') as yeni_dosya:
            yeni_dosya.write(icerik)
        
        dosya_yolu_etiketi.config(text="Seçilen Dosyanın Yolu: " + dosya_yolu)
        yeni_dosya_yolu_etiketi.config(text="Yeni Dosyanın Yolu: " + yeni_dosya_yolu)

app = tk.Tk()
app.title("Dosya İçeriği Değiştirici")
app.geometry("500x100")

label = tk.Label(app, text="Dosya Seç:")
label.pack()

secim_butonu = tk.Button(app, text="Değiştir", command=dosya_degistir)
secim_butonu.pack()

dosya_yolu_etiketi = tk.Label(app, text="")
dosya_yolu_etiketi.pack()

yeni_dosya_yolu_etiketi = tk.Label(app, text="")
yeni_dosya_yolu_etiketi.pack()

app.mainloop()
