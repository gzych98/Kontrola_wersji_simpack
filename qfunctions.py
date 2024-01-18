import random
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton
import os, subprocess, threading, queue
import time, datetime
import pygetwindow as gw
import pyautogui


# Globalna flaga stanu procesu (bezpieczna dla wątków)
process_active = threading.Event()

def app_process(listbox, info_label, mainWindow, process_args, solver):
    selected_items = listbox.selectedItems()
    if not selected_items:
        info_label.setText("Wybierz plik")
        return

    for item in selected_items:
        full_path = item.text()
        # Sprawdzenie rozszerzenia pliku
        if not full_path.lower().endswith('.spck'):
            info_label.setText("To nie jest plik .spck")
            continue
        arguments = [process_args + [full_path]]
        print(f"ARGS: {arguments}")
        #solver = r"C:\Program Files\Simpack-2023x.3\run\bin\win64\simpack-slv"
        filename = os.path.basename(full_path)

        # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # nowa_nazwa_pliku = f"{timestamp}_{filename}.txt"
        log_directory = os.path.join(os.path.dirname(full_path), "log")
        os.makedirs(log_directory, exist_ok=True)
        #log_file_path = os.path.join(log_directory, nowa_nazwa_pliku)
        log_file_path = os.path.join(log_directory,  f"{filename}_log.txt")

        dialog_and_logging(mainWindow, full_path, log_file_path)

        output_queue = queue.Queue()
        threading.Thread(target=uruchom_analize, args=(arguments, solver, 0, output_queue)).start()
        #threading.Thread(target=testowy_proces, args=(arguments,)).start()
        threading.Thread(target=process_output, args=(output_queue, log_file_path)).start()
        if process_active.is_set():
            print("PROCES:\tProces jest aktywny")
        else:
            print("PROCES:\tProces nie jest aktywny")

def testowy_proces(arguments):
    global process_active
    process_active.set()  # Ustawienie flagi na aktywną
    try:
        print(f"Rozpoczynam proces z argumentami: {arguments}")
        time.sleep(5)  # Symulacja trwania procesu
        wynik = f"Wynik procesu dla {arguments}: {random.randint(1, 100)}"
        print(wynik)
        return wynik
    finally:
        process_active.clear()  # Wyłączenie flagi na zakończenie procesu

def dialog_and_logging(mainWindow, full_path, log_file_path):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dialog = CustomTextDialog(mainWindow, "Log", "Log text:")
    if dialog.exec_() == QDialog.Accepted:
        log_text = dialog.getText()
        with open(log_file_path, "a", encoding='utf-8') as plik:
            plik.write(f"{timestamp} - Log tekst:\n{log_text}\n\n")

def process_output(output_queue, log_file_path):
    while True:
        if not output_queue.empty():
            result = output_queue.get()
            with open(log_file_path, "a", encoding='utf-8') as plik:
                plik.write(result + "\n")
            break
        time.sleep(0.1)  # Dodajemy krótkie opóźnienie, aby uniknąć nadmiernego obciążenia procesora

def uruchom_w_watku(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

@uruchom_w_watku
def uruchom_analize(arguments, solver_path, delay_time, output_queue):
    global process_active
    process_active.set()  # Ustawienie flagi na aktywną na początek procesu
    procesy = []  # Lista do przechowywania procesów

    try:
        start_time = datetime.datetime.now()
        print(f"APLIKACJA:\tRozpoczęcie analizy! {start_time} ")

        if delay_time >= 0:
            while delay_time > 0:
                print(f"APLIKACJA:\tPozostały czas: {delay_time} [min]")
                time.sleep(60)
                delay_time -= 1

        for argument in arguments:
            if isinstance(argument, list):
                process = subprocess.Popen([solver_path] + argument, creationflags=subprocess.CREATE_NEW_CONSOLE)
                procesy.append(process)  # Dodanie procesu do listy
            else:
                print("APLIKACJA:\tERROR:\targument nie jest listą")

        for process in procesy:
            process.wait()  # Czekanie na zakończenie każdego procesu

        print('APLIKACJA:\tAnaliza zakończona')
    except Exception as e:
        print(f"APLIKACJA:\tERROR:\t{e}")

    process_active.clear()  # Zakończenie procesu i czyszczenie flagi

def aktywuj_simpack_pre_i_otworz_plik(sciezka_pliku):
    sciezka_pliku = sciezka_pliku.replace("/", "\\")

    # Jeśli pierwszy znak to backslash, PyAutoGUI może go interpretować jako kombinację klawiszy,
    # więc dodajemy r przed stringiem, aby zapewnić, że będzie traktowany jako surowy string
    sciezka_pliku = 'r"' + sciezka_pliku + '"'
    okna = [okno for okno in gw.getAllWindows() if "- Simpack 2023x.3 - Pre" in okno.title]

    if okna:
        okno = okna[0]  # Zakładając, że interesuje nas pierwsze znalezione okno
        okno.activate()  # Aktywacja okna

        # Symulacja naciśnięcia CTRL+O
        pyautogui.hotkey('ctrl', 'o')
        time.sleep(1)  # Krótkie opóźnienie, aby upewnić się, że okno dialogowe jest otwarte

        # Wpisanie ścieżki do pliku i naciśnięcie 'Enter'
        pyautogui.write(sciezka_pliku)
        pyautogui.press('enter')
    else:
        print("Nie znaleziono okna Simpack Pre.")
    
class CustomTextDialog(QDialog):
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(400, 200, 400, 200)  # Możesz dostosować rozmiar okna tutaj

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(prompt))

        self.textEdit = QTextEdit(self)
        layout.addWidget(self.textEdit)

        submitButton = QPushButton("OK", self)
        submitButton.clicked.connect(self.accept)
        layout.addWidget(submitButton)

    def getText(self):
        return self.textEdit.toPlainText()
