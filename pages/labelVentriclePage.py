import os

from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QGroupBox, QHBoxLayout
)
# import torch
# import onnxruntime
import numpy as np
import cv2
import config
from components.filetreeview import FileTreeView
from components.layouts import WorkstationLayout
from components.markableimage import MarkableImage
from pages.bingliguanli_page import MedicalRecordTab


class DiagnosisPage(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # 创建按钮
        # self.diagnosis_button = QPushButton('诊断')
        # self.segment_button = QPushButton('分割')
        # self.report_button = QPushButton('报告生成')
        # self.similar_case_button = QPushButton('相似病例')

        # 添加按钮到界面
        # self.main_layout.addWidget(self.diagnosis_button)
        # self.main_layout.addWidget(self.segment_button)
        # self.main_layout.addWidget(self.report_button)
        # self.main_layout.addWidget(self.similar_case_button)


class ResultPage(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        intelligent_diagnostics_group = QGroupBox('射血分数计算')
        self.diagnosis_layout = QFormLayout()
        self.diagnosis_result = QLineEdit()
        self.report_result = QTextEdit()

        self.diagnosis_layout.addRow('todo诊断结果', self.diagnosis_result)
        self.diagnosis_layout.addRow('todo诊断报告', self.report_result)

        intelligent_diagnostics_group.setLayout(self.diagnosis_layout)
        self.main_layout.addWidget(intelligent_diagnostics_group)


class labelVentriclePage(QWidget):
    def __init__(self,base_folder):
        super().__init__()
        self.layout = WorkstationLayout()
        self.setLayout(self.layout)
        self.similar_window = QWidget()

        # 初始化 base_folder 属性
        self.base_folder = base_folder

        # 创建 FileTreeView
        self.filetree = FileTreeView(self.base_folder)
        self.image_view = MarkableImage()
        self.image_view.setMinimumWidth(700)

        # 添加布局
        self.layout.get_mid_left_layout().addWidget(self.filetree)
        self.layout.get_center_layout().addWidget(self.image_view)


        self.image_view = MarkableImage()
        self.image_view.setMinimumWidth(700)

        self.similar_image_view = MarkableImage()
        # self.medical_record_tab = MedicalRecordTab()
        # self.similar_record_tab = MedicalRecordTab()
        self.DiagnosisPage = DiagnosisPage()
        self.ResultPage = ResultPage()
        self.mark_label = QHBoxLayout()

        #绑定清除标记函数和保存标记函数
        self.clear_button = QPushButton('清除标记')
        self.clear_button.clicked.connect(self.image_view.clear_circles)
        self.save_button = QPushButton('保存标记')
        self.clear_button.clicked.connect(self.handle_save_label)

        self.mark_label.addWidget(self.clear_button)
        self.mark_label.addWidget(self.save_button)

        # self.medical_record_tab.delete_button.hide()  # 隐藏删除按钮
        # self.medical_record_tab.add_image.hide()  # 隐藏添加按钮
        # self.medical_record_tab.create_button.hide()  # 隐藏创建按钮
        # self.similar_record_tab.delete_button.hide()  # 隐藏删除按钮
        # self.similar_record_tab.add_image.hide()  # 隐藏添加按钮
        # self.similar_record_tab.create_button.hide()  # 隐藏创建按钮
        # self.similar_record_tab.save_button.hide()  # 隐藏保存按钮

        # 信号连接
        self.filetree.item_double_clicked.connect(self.select_image)

        # self.filetree.item_double_clicked.connect(self.medical_record_tab.load_record)
        # self.DiagnosisPage.diagnosis_button.clicked.connect(self.handle_diagnosis_request)  # 连接诊断按钮
        # self.DiagnosisPage.segment_button.clicked.connect(self.handle_segment_request)  # 连接分割按钮
        # self.DiagnosisPage.report_button.clicked.connect(self.handle_report_request)  # 连接报告生成按钮
        # self.DiagnosisPage.similar_case_button.clicked.connect(self.handle_case_request)  # 连接相似病例按钮

        # 添加layout到主界面
        self.layout.get_mid_left_layout().addWidget(self.filetree)
        # self.layout.get_mid_right_layout().addWidget(self.medical_record_tab)
        self.layout.get_mid_right_layout().addWidget(self.ResultPage)
        self.layout.get_center_layout().addWidget(self.image_view)
        self.layout.get_center_layout().addLayout(self.mark_label)
        self.layout.get_bottom_layout().addWidget(self.DiagnosisPage)
        self.current_path = None

        # self.medical_record_tab.setMaximumWidth(300)
        self.ResultPage.setMaximumWidth(300)


    def select_image(self, path):
        self.current_path = path
        self.image_view.load_image(path)
    def handle_save_label(self):
        pass

    def handle_case_request(self):
        print("************", self.current_path)
        self.similar_record_tab.load_record(self.current_path)  # 加载病例
        image_path = os.path.join(*self.current_path.split(os.path.sep)[0:-1])
        for i in os.listdir(image_path):
            if i.startswith('B型超声'):
                _, ext = os.path.splitext(i)
                image_path = os.path.join(image_path, 'B型超声' + ext)  # 加载病例图片
                break

        self.similar_image_view.load_image(image_path)  # 加载病例图片

        similar_layout = WorkstationLayout()
        similar_layout.get_mid_left_layout().addWidget(self.similar_record_tab)
        similar_layout.get_center_layout().addWidget(self.similar_image_view)

        self.similar_window.setLayout(similar_layout)
        self.similar_window.show()




if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = labelVentriclePage()
    window.show()
    sys.exit(app.exec())
