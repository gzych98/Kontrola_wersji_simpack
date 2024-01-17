from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QInputDialog
import os, subprocess, threading, queue
import time, datetime

def uruchom_analize_w_watku(arguments, solver_path, delay_time, output_queue):
    analiza_thread = threading.Thread(target=uruchom_analize, args=(arguments, solver_path, delay_time, output_queue))
    analiza_thread.start()

def uruchom_proces2(argument, solver_path, output_queue):
    subprocess.Popen([solver_path] + argument, creationflags=subprocess.CREATE_NEW_CONSOLE)
    #proces.wait()
    output_queue.put(f"Model: {argument[2]}")

def uruchom_proces(argument, solver_path, output_queue):
    print("WYSTARTOWAŁ")
    process_thread = threading.Thread(target=subprocess.Popen, args=([solver_path] + argument, ), kwargs={'creationflags': subprocess.CREATE_NEW_CONSOLE})
    process_thread.start()

def uruchom_analize(arguments, solver_path, delay_time, output_queue):
    start_time = datetime.datetime.now()
    print(f"APLIKACJA:\tRozpoczęcie analizy! {start_time} ")

    if delay_time >= 0:
        while delay_time > 0:
            print(f"APLIKACJA:\tPozostały czas: {delay_time} [min]")
            time.sleep(60)
            delay_time -= 1

    for argument in arguments:
        if isinstance(argument, list):
            threading.Thread(target=uruchom_proces, args=(argument, solver_path, output_queue)).run()
        else:
            print("APLIKACJA:\tERRPR:\targument nie jest listą")

    # end_time = datetime.datetime.now()
    # result = f"Analiza zakończona ({start_time} : {end_time})"
    # print(result)

def uruchom_analize2(arguments, solver_path, delay_time, output_queue):
    """
    Uruchamia serię analiz symulacyjnych przy użyciu podanego solvera.

    Args:
    - arguments (list of list of str): Lista argumentów dla każdej analizy. Każda podlista zawiera zestaw 
      argumentów dla jednej analizy.
    - solver_path (str): Ścieżka do pliku wykonywalnego solvera.
    - delay_time (int): Czas opóźnienia przed rozpoczęciem analiz w minutach.

    Funkcja wypisuje na ekranie czas rozpoczęcia i zakończenia analiz, a także informacje o pozostałym czasie 
    opóźnienia, jeśli jest ustawione. Wykonuje polecenia solvera z podanymi argumentami.
    """
    start_time = datetime.datetime.now()
    print(f"APLIKACJA:\tINFO\tRozpoczęcie analizy! {start_time} ")
    
    if delay_time >= 0:
        while delay_time > 0:
            print(f"APLIKACJA:\tINFO\tPozostały czas: {delay_time} [min]")
            time.sleep(60)
            delay_time -= 1
    
    procesy = []    
    
    for argument in arguments:
        # Upewnij się, że argument jest listą
        if isinstance(argument, list):
            proces = subprocess.Popen([solver_path] + argument)
            procesy.append(proces)  # Dodanie procesu do listy            
        else:
            print("APLIKACJA:\tERROR:\targument nie jest listą")
    
    for proces in procesy:
        proces.wait()

    result = f"APLIKACJA:\tINFO\tAnaliza zakończona ({start_time} : {datetime.datetime.now()})"
    print(result)
    output_queue.put(result)

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



def app_integration(listbox, info_label, mainWindow):
    selected_items = listbox.selectedItems()
    if not selected_items:
        info_label.setText("Wybierz plik")
        return

    for item in selected_items:
        full_path = item.text()
        arguments = [["--integration", "--file", full_path]]
        solver = r"C:\Program Files\Simpack-2023x.3\run\bin\win64\simpack-slv"
        filename = os.path.basename(full_path)

        dialog = CustomTextDialog(mainWindow, "Log", "Log text:")
        if dialog.exec_() == QDialog.Accepted:
            log_text = dialog.getText()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nowa_nazwa_pliku = f"{timestamp}_{filename}.txt"

            log_directory = os.path.join(os.path.dirname(full_path), "log")
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)

            log_file_path = os.path.join(log_directory, nowa_nazwa_pliku)

            # Zapis log_text do pliku
            with open(log_file_path, "w", encoding='utf-8') as plik:
                plik.write("Log tekst:\n" + log_text + "\n\n")

            output_queue = queue.Queue()
            uruchom_analize_w_watku(arguments, solver, 0, output_queue)

            while True:
                if not output_queue.empty():
                    result = output_queue.get()
                    with open(log_file_path, "a", encoding='utf-8') as plik:
                        plik.write(result + "\n")
                    break

            




def dodaj_pliki(listWidget):
    pliki, _ = QFileDialog.getOpenFileNames()
    for plik in pliki:
        listWidget.addItem(plik)




def zapisz_tekst_jako_plik(listWidget, info_label):
    selected = listWidget.curselection()
    if not selected:
        info_label.setText(text="Wybierz plik")
        return
    
    for index in selected:
        sciezka_pliku = listWidget.get(index)
        nazwa_pliku = os.path.basename(sciezka_pliku)

        # Pobieranie tekstu od użytkownika

    tekst_uzytkownika, ok = QInputDialog.getText(None, "Wprowadź tekst", "Wpisz tekst do zapisania:")
    if ok:
        # Tworzenie nazwy pliku z datą i czasem
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nowa_nazwa_pliku = f"{timestamp}_{nazwa_pliku}.txt"

        # Zapisywanie tekstu do pliku w tej samej lokalizacji
        with open(os.path.join(os.path.dirname(sciezka_pliku), nowa_nazwa_pliku), "w") as plik:
            plik.write(tekst_uzytkownika)

        info_label.config(text=f"Zapisano jako: {nowa_nazwa_pliku}")

