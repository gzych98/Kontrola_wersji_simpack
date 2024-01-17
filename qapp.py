from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon
from qfunctions import app_integration, dodaj_pliki, zapisz_tekst_jako_plik
# from minimalizacja import setup_tray_icon  # To wymaga osobnej implementacji dla PyQt5

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Kontrola wersji - v0.1")
        self.setGeometry(0, 0, 500, 300)  # tymczasowa geometria
        self.setWindowPosition()  

        self.setWindowIcon(QIcon(r"D:\PY_SCRIPT\Aplikacja_kontroli_wersji\wrench-solid.ico"))

        # Tworzenie widgetów
        self.listbox = QListWidget(self)

        self.add_button = QPushButton("Dodaj pliki", self)
        self.add_button.clicked.connect(lambda: dodaj_pliki(self.listbox))

        self.integration_button = QPushButton("Integration", self)
        self.integration_button.clicked.connect(lambda: app_integration(self.listbox, self.info_label, self))

        self.measurement_button = QPushButton("Measurement", self)
        self.measurement_button.clicked.connect(lambda: app_integration(self.listbox, self.info_label, self))

        self.minimize_button = QPushButton("Minimalizuj", self)
        # self.minimize_button.clicked.connect(hide_window)  # To wymaga osobnej implementacji dla PyQt5

        self.info_label = QLabel("", self)

        # Układanie widgetów
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.integration_button)
        buttons_layout.addWidget(self.measurement_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.listbox)
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.minimize_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def setWindowPosition(self):
        desktop = QDesktopWidget()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        position_right = screen_width - 520  # szerokość okna = 200
        position_down = screen_height - 400  # wysokość okna = 100
        self.setGeometry(position_right, position_down, 500, 300)


if __name__ == "__main__":
    app = QApplication([])
    main_app = MainApp()
    main_app.show()
    app.exec_()
