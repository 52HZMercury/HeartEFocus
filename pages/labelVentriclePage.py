import os

from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QGroupBox, QHBoxLayout
)
# import torch
# import onnxruntime
import numpy as np
import config

import cv2
from PySide6.QtGui import QImage
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
    def __init__(self, base_folder):
        super().__init__()
        self.layout = WorkstationLayout()
        self.setLayout(self.layout)
        self.similar_window = QWidget()

        # 初始化 base_folder 属性
        self.base_folder = base_folder

        # 创建 FileTreeView
        self.filetree = FileTreeView(self.base_folder)
        # self.filetree = FileTreeView(config.work_dir)
        self.image_view = MarkableImage()
        self.image_view.setMinimumWidth(700)

        # 视频相关初始化
        self.cap = None
        self.current_frame_index = 0
        self.total_frames = 0

        # 增加上一帧和下一帧按钮
        self.prev_frame_button = QPushButton('上一帧')
        self.next_frame_button = QPushButton('下一帧')
        self.prev_frame_button.setEnabled(False)  # 默认禁用上一帧按钮
        self.next_frame_button.setEnabled(False)  # 默认禁用下一帧按钮

        # 绑定按钮事件
        self.prev_frame_button.clicked.connect(self.show_previous_frame)
        self.next_frame_button.clicked.connect(self.show_next_frame)

        # 将按钮添加到布局
        frame_buttons_layout = QHBoxLayout()
        frame_buttons_layout.addWidget(self.prev_frame_button)
        frame_buttons_layout.addWidget(self.next_frame_button)
        self.layout.get_bottom_layout().addLayout(frame_buttons_layout)


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


        # 信号连接
        self.filetree.item_double_clicked.connect(self.select_video)
        # 信号连接
        # self.filetree.item_double_clicked.connect(self.select_image)


        # 添加layout到主界面
        self.layout.get_mid_left_layout().addWidget(self.filetree)
        self.layout.get_mid_right_layout().addWidget(self.ResultPage)
        self.layout.get_center_layout().addWidget(self.image_view)
        self.layout.get_center_layout().addLayout(self.mark_label)

        # self.layout.get_mid_right_layout().addWidget(self.medical_record_tab)
        # self.layout.get_bottom_layout().addWidget(self.DiagnosisPage)
        self.current_path = None

        # self.medical_record_tab.setMaximumWidth(300)
        self.ResultPage.setMaximumWidth(300)


    def select_image(self, path):
        self.current_path = path
        self.image_view.load_image(path)

    def select_video(self, filename):

        """读取视频并显示第一帧"""
        path =  self.base_folder +'/' +filename
        print(f"Attempting to open video at: {path}")  # 查看控制台输出路径是否正确

        if self.cap:
            self.cap.release()  # 释放之前的视频捕获对象

        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            print(f"无法打开视频文件: {path}")
            return

        # 重置帧索引和按钮状态
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame_index = 0
        self.prev_frame_button.setEnabled(False)
        self.next_frame_button.setEnabled(self.total_frames > 1)
        # 清空 image_view 的内容
        self.image_view.clear_image()  # 假设 MarkableImage 类有 clear_image 方法

        # 显示第一帧
        self.show_frame(self.current_frame_index)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame_index = 0

        # 清空 image_view 的内容
        # self.image_view.clear_image()

        self.show_frame(self.current_frame_index)

        # 启用/禁用按钮
        self.prev_frame_button.setEnabled(False)
        self.next_frame_button.setEnabled(self.total_frames > 1)

    def show_frame(self, frame_index):
        """显示指定帧"""
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.image_view.load_image(q_image)

    def show_previous_frame(self):
        """显示上一帧"""
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            self.show_frame(self.current_frame_index)
            self.next_frame_button.setEnabled(True)
            if self.current_frame_index == 0:
                self.prev_frame_button.setEnabled(False)

    def show_next_frame(self):
        """显示下一帧"""
        if self.current_frame_index < self.total_frames - 1:
            self.current_frame_index += 1
            self.show_frame(self.current_frame_index)
            self.prev_frame_button.setEnabled(True)
            if self.current_frame_index == self.total_frames - 1:
                self.next_frame_button.setEnabled(False)
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
