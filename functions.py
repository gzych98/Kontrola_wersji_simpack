import os
import tkinter as tk
from tkinter import filedialog, simpledialog
import datetime
from minimalizacja import setup_tray_icon

def custom_text_dialog(root, title, prompt):
    dialog_result = {"text": None}

    def on_submit():
        dialog_result["text"] = text.get("1.0", "end-1c")
        dialog.destroy()

    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("400x200")  # Możesz dostosować rozmiar okna tutaj

    tk.Label(dialog, text=prompt).pack()
    text = tk.Text(dialog, height=8, width=40)  # Ustaw wysokość i szerokość pola tekstowego
    text.pack()
    text.focus_set()

    submit_button = tk.Button(dialog, text="OK", command=on_submit)
    submit_button.pack(pady=5)

    dialog.transient(root)  # Ustawia okno dialogowe jako podrzędne w stosunku do głównego okna
    dialog.wait_window()  # Czeka na zamknięcie okna dialogowego

    return dialog_result["text"]


def app_integration(listbox, info_label, root):
    selected = listbox.curselection()
    if not selected:
        info_label.config(text="Wybierz plik")
        return    
    for index in selected:
        full_path = listbox.get(index)
        filename = os.path.basename(full_path)

        log_text = custom_text_dialog(root, "Log", "Log text:")
        if log_text is None:  # użytkownik anulował dialog
            return
        # Tworzenie nazwy pliku z datą i czasem
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nowa_nazwa_pliku = f"{timestamp}_{filename}.txt"

        # Tworzenie katalogu /log, jeśli nie istnieje
        log_directory = os.path.join(os.path.dirname(full_path), "log")
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # Ścieżka do nowego pliku w katalogu /log
        log_file_path = os.path.join(log_directory, nowa_nazwa_pliku)

        # Zapisywanie tekstu do pliku
        with open(log_file_path, "w", encoding='utf-8') as plik:
            plik.write(log_text)

        info_label.config(text=f'Integration: {filename}')
    return(filename)

def app_measurement(listbox, info_label):
    selected = listbox.curselection()
    if not selected:
        info_label.config(text="Wybierz plik")
        return    
    for index in selected:
        full_path = listbox.get(index)
        filename = os.path.basename(full_path)
    info_label.config(text=f'Measurement: {filename}')
    return(filename)

def dodaj_pliki(listbox):
    pliki = filedialog.askopenfilenames()
    for plik in pliki:
        listbox.insert('end', plik)

def zapisz_tekst_jako_plik(listbox, info_label):
    selected = listbox.curselection()
    if not selected:
        info_label.config(text="Wybierz plik")
        return
    
    for index in selected:
        sciezka_pliku = listbox.get(index)
        nazwa_pliku = os.path.basename(sciezka_pliku)

        # Pobieranie tekstu od użytkownika
        tekst_uzytkownika = simpledialog.askstring("Wprowadź tekst", "Wpisz tekst do zapisania:")
        if tekst_uzytkownika is None:  # użytkownik anulował dialog
            return

        # Tworzenie nazwy pliku z datą i czasem
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nowa_nazwa_pliku = f"{timestamp}_{nazwa_pliku}.txt"

        # Zapisywanie tekstu do pliku w tej samej lokalizacji
        with open(os.path.join(os.path.dirname(sciezka_pliku), nowa_nazwa_pliku), "w") as plik:
            plik.write(tekst_uzytkownika)

        info_label.config(text=f"Zapisano jako: {nowa_nazwa_pliku}")

