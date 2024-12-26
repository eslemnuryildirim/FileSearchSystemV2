
import os
import tkinter as tk
from tkinter import messagebox
import time

# Global bir liste
results = []

# Metin dosyalarını kontrol etmek için geçerli uzantılar
text_extensions = ['.txt', '.md', '.html', '.css', '.js', '.json', '.xml', '.py']

# Dosyada anahtar kelimeyi arayan fonksiyon
def search_in_file(file_name, keyword):
    if not any(file_name.endswith(ext) for ext in text_extensions):
        results.append(f"Skipping non-text file: {file_name}")
        return

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                if keyword in line:
                    results.append(f'Found "{keyword}" in {file_name} on line {line_num}')
    except Exception as e:
        results.append(f'Error reading {file_name}: {e}')

# Dizin içinde anahtar kelimeyi arama
def search_directory(directory, keyword):
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            search_in_file(full_path, keyword)

# Manuel iş parçacığı işlevi (Threading alternatifi)
def thread_task(directory, keyword):
    print(f"Thread started for directory: {directory}")
    search_directory(directory, keyword)
    print(f"Thread finished for directory: {directory}")

# Manuel işlem işlevi (Multiprocessing alternatifi)
def process_task(directory, keyword):
    pid = os.fork()  # Yeni bir süreç başlat
    if pid == 0:  # Çocuk süreç
        print(f"Child process started for directory: {directory}")
        search_directory(directory, keyword)
        os._exit(0)  # Çocuk süreç işini bitirince çıkmalı
    else:  # Ana süreç
        print(f"Parent process waiting for child process (PID: {pid}) to finish.")
        os.wait()  # Çocuk süreçlerin tamamlanmasını bekle

# Arama başlatma fonksiyonu
def start_search():
    keyword = entry_keyword.get()
    directories = entry_directories.get().split(',')

    if not keyword or not directories:
        messagebox.showerror("Input Error", "Both fields must be filled out!")
        return

    global results
    results = []

    # Paralel olarak her dizinde anahtar kelimeyi ara
    for directory in directories:
        directory = directory.strip()
        if os.path.isdir(directory):
            # İşlem başlat (Manual Process)
            process_task(directory, keyword)

            # İş Parçacığı başlat (Manual Thread)
            thread_task(directory, keyword)

        else:
            results.append(f"Invalid directory: {directory}")

    # Sonuçları liste kutusunda göster
    results_listbox.delete(0, tk.END)
    for result in results:
        results_listbox.insert(tk.END, result)

# Tkinter arayüzü
root = tk.Tk()
root.title("File Search Application")

# Arka plan rengini ayarla
root.config(bg='#FFE156')

# Ana başlık etiketi
header_label = tk.Label(root, text="File Search Application", font=("Helvetica", 16, "bold"), bg='#FF8C00', fg="white")
header_label.grid(row=0, column=0, columnspan=2, pady=10)

# Anahtar kelime etiketi ve girişi
tk.Label(root, text="Keyword:", font=("Helvetica", 12), bg='#FFE156', fg="#333").grid(row=1, column=0, padx=10, pady=5, sticky='e')
entry_keyword = tk.Entry(root, font=("Helvetica", 12), width=40, bd=2, relief="solid", fg="#333")
entry_keyword.grid(row=1, column=1, padx=10, pady=5)

# Dizinin etiketi ve girişi
tk.Label(root, text="Directories (comma-separated):", font=("Helvetica", 12), bg='#FFE156', fg="#333").grid(row=2, column=0, padx=10, pady=5, sticky='e')
entry_directories = tk.Entry(root, font=("Helvetica", 12), width=40, bd=2, relief="solid", fg="#333")
entry_directories.grid(row=2, column=1, padx=10, pady=5)

# Başlat butonu
start_button = tk.Button(root, text="Start Search", font=("Helvetica", 12), bg="#00BFFF", fg="white", command=start_search, relief="raised", bd=3)
start_button.grid(row=3, column=0, columnspan=2, pady=10)

# Sonuçları gösteren liste kutusu
results_listbox = tk.Listbox(root, font=("Helvetica", 12), width=80, height=20, bd=2, relief="sunken", fg="#333", bg="#FFEDB6")
results_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Tkinter ana döngüsünü başlat
root.mainloop()
