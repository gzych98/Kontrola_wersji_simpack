from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

def setup_tray_icon(self):
    self.tray_icon = QSystemTrayIcon(self)
    self.tray_icon.setIcon(QIcon(r"D:\PY_SCRIPT\Aplikacja_kontroli_wersji\wrench-solid.ico"))

    show_action = QAction("Pokaż", self)
    show_action.triggered.connect(self.show)
    exit_action = QAction("Wyjdź", self)
    exit_action.triggered.connect(self.close)

    tray_menu = QMenu()
    tray_menu.addAction(show_action)
    tray_menu.addAction(exit_action)

    self.tray_icon.setContextMenu(tray_menu)
    self.tray_icon.show()

