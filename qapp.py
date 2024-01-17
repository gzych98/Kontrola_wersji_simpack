from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon
from qfunctions import app_process, process_active
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidget, QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QMimeData, QTimer
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

class DragDropListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDrop)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = [url.toLocalFile() for url in event.mimeData().urls()]
            for link in links:
                self.addItem(link)
        else:
            event.ignore()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setup_tray_icon()
        self.setup_monitoring()


    def initUI(self):
        self.setWindowTitle("Kontrola wersji - v0.1")
        self.setGeometry(0, 0, 500, 300)  # tymczasowa geometria
        self.setWindowPosition()  

        self.setWindowIcon(QIcon(r"wrench-solid.ico"))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Tworzenie widgetów
       #self.listWidget = DragDropListWidget(self)
        self.listbox = DragDropListWidget(self)

        # self.add_button = QPushButton("Dodaj pliki", self)
        # self.add_button.clicked.connect(lambda: dodaj_pliki(self.listbox))

        self.integration_button = QPushButton("Integration", self)
        self.integration_button.clicked.connect(lambda: app_process(self.listbox, self.info_label, self, ["--integration", "--file"]))

        self.measurement_button = QPushButton("Measurement", self)
        self.measurement_button.clicked.connect(lambda: app_process(self.listbox, self.info_label, self, ["--measurement", "--file"]))

        self.minimize_button = QPushButton("Minimalizuj", self)
        self.minimize_button.clicked.connect(self.hide_window)

        self.delete_button = QPushButton("Wyczyść", self)
        self.delete_button.clicked.connect(self.clear_list)

        self.status_label = QLabel("Stan procesu: Nieaktywny", self)
        

        self.info_label = QLabel("", self)

        # Układanie widgetów
        buttons_layout = QHBoxLayout()
        # buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.integration_button)
        buttons_layout.addWidget(self.measurement_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.listbox)
        main_layout.addWidget(self.info_label)        
        main_layout.addWidget(self.delete_button)
        main_layout.addWidget(self.status_label)  # Dodanie etykiety statusu do layoutu
        main_layout.addWidget(self.minimize_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_monitoring(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)  # Sprawdzanie co sekundę

    def update_status(self):
        if process_active.is_set():
            self.status_label.setText("Stan procesu: Aktywny")
        else:
            self.status_label.setText("Stan procesu: Nieaktywny")

    def check_queue(self):
        while not self.output_queue.empty():
            message = self.output_queue.get()
            # Aktualizuj UI na podstawie wiadomości
            self.statusBar().showMessage(message)

    def focusInEvent(self, event):
        self.setWindowOpacity(1.0)  # Normalna przezroczystość
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setWindowOpacity(0.2)  # Zmniejszona przezroczystość
        super().focusOutEvent(event)

    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(r"favicon.ico"))

        show_action = QAction("Pokaż", self)
        show_action.triggered.connect(self.show_window)
        exit_action = QAction("Wyjdź", self)
        exit_action.triggered.connect(self.close)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_window()

    def show_window(self):
        if self.isMinimized() or not self.isVisible():
            self.showNormal()
        self.activateWindow()

    
    def setWindowPosition(self):
        desktop = QDesktopWidget()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        position_right = screen_width - 520  # szerokość okna = 200
        position_down = screen_height - 400  # wysokość okna = 100
        self.setGeometry(position_right, position_down, 500, 300)

    def hide_window(self):
        self.hide()
        self.tray_icon.showMessage("Informacja", "Aplikacja została zminimalizowana do zasobnika systemowego.")
    
    def clear_list(self):
        # Funkcja czyszcząca listę
        self.listbox.clear()

if __name__ == "__main__":
    app = QApplication([])
    main_app = MainApp()
    main_app.show()
    app.exec_()
