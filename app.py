import tkinter as tk
from tkinter import ttk
from functions import app_integration, app_measurement, dodaj_pliki, zapisz_tekst_jako_plik
from minimalizacja import setup_tray_icon

# Instancja głównego okna
root = tk.Tk()
root.title("Aplikacja GZ")
root.geometry("500x300") # Ustawienie rozmiaru okna
myFont = ('Verdana', 10)

style = ttk.Style()
style.configure("TButton", font=('Helvetica', 10))
style.configure("TLabel", font=('Helvetica', 10))

##################### FRAME
frame_buttons = tk.Frame(root)
frame_listbox = tk.Frame(root)

##################### LISTBOX
listbox = tk.Listbox(frame_listbox)

##################### MINIMALIZUJ
hide_window = setup_tray_icon(root, "nazwa_ikony", "Tooltip ikony")

##################### BUTTON
add_button = ttk.Button(frame_buttons, text="Dodaj pliki", command=lambda: dodaj_pliki(listbox), style="TButton")
integration_button = ttk.Button(frame_buttons, text="Integration", command=lambda: app_integration(listbox, info_label, root), style="TButton")
measurement_button = ttk.Button(frame_buttons, text="Measurement", command=lambda: app_measurement(listbox, info_label, root), style="TButton")
minimize_button = tk.Button(root, text="Minimalizuj", command=hide_window)


##################### LABEL
info_label = ttk.Label(root, text="", style="TLabel")

##################### PACK #####################
frame_buttons.pack(pady=10)
frame_listbox.pack(fill="both", expand=True)
listbox.pack(side="left", fill="both", expand=True)
add_button.grid(row=0, column=0, padx=5)
integration_button.grid(row=0, column=1, padx=5)
measurement_button.grid(row=0, column=2, padx=5)
info_label.pack()
minimize_button.pack()
################################################

# Uruchomienie pętli zdarzeń
root.mainloop()
