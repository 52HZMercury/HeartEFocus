import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

import qtvscodestyle as qtvsc

app = QApplication(sys.argv)
main_win = QMainWindow()
push_button = QPushButton("QtVSCodeStyle!!")
main_win.setCentralWidget(push_button)

stylesheet = qtvsc.load_stylesheet(qtvsc.Theme.DARK_VS)
# stylesheet = load_stylesheet(qtvsc.Theme.LIGHT_VS)
app.setStyleSheet(stylesheet)

main_win.show()

app.exec()
