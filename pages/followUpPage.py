import json
import pathlib
from datetime import datetime
from os import makedirs, rename

from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QVBoxLayout, QLineEdit,
    QSpinBox, QComboBox, QCheckBox, QLabel, QTextEdit, QGroupBox, QScrollArea, QHBoxLayout, QPushButton, QMessageBox,
    QDialog
)

import config
from components.filetreeview import FileTreeView
from components.layouts import WorkstationLayout, AutoGridWidget
from components.markableimage import MarkableImage
from pages.medicalRecordPage import MedicalRecordTab


class HuiFangPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = WorkstationLayout()

        self.setLayout(self.layout)

        self.filetree = FileTreeView(config.work_dir)
        self.image_view = MarkableImage()
        self.medical_record_tab = MedicalRecordTab()
        self.medical_record_tab.medical_history_group.hide()
        self.medical_record_tab.lifestyle_group.hide()
        self.medical_record_tab.basic_info_group.setDisabled(True)

        self.medical_record_tab.delete_button.hide()
        self.medical_record_tab.create_button.hide()
        # 从self.medical_record_tab.layout删除widget
        self.medical_record_tab.layout.widgets.remove(self.medical_record_tab.medical_history_group)
        self.medical_record_tab.layout.widgets.remove(self.medical_record_tab.lifestyle_group)

        self.filetree.item_double_clicked.connect(self.load_medical_record)

        title_label = QLabel('病例回访')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        self.layout.get_top_layout().addWidget(title_label)
        self.layout.get_mid_left_layout().addWidget(self.filetree)
        self.layout.get_center_layout().addWidget(self.medical_record_tab)
        # self.layout.get_mid_right_layout().addWidget(QLabel('右边'))

    def load_medical_record(self, file_path):
        self.medical_record_tab.auto_load(file_path)
        self.medical_record_tab.original_path = pathlib.Path(file_path).parent
        self.medical_record_tab.original_file_name = f"回访记录{datetime.now().strftime('%Y年%m月%d日')}.json"



if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = BingliGuanliPage()
    window.show()
    sys.exit(app.exec())
