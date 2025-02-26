from PySide6.QtWidgets import QWidget

from components.layouts import WorkstationLayout


class TongyongZhenduanPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = WorkstationLayout()
        self.setLayout(self.layout)