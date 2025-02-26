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
        self.diagnosis_button = QPushButton('诊断')
        self.segment_button = QPushButton('分割')
        self.report_button = QPushButton('报告生成')
        self.similar_case_button = QPushButton('相似病例')

        # 添加按钮到界面
        self.main_layout.addWidget(self.diagnosis_button)
        self.main_layout.addWidget(self.segment_button)
        self.main_layout.addWidget(self.report_button)
        self.main_layout.addWidget(self.similar_case_button)


class ResultPage(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        intelligent_diagnostics_group = QGroupBox('智能诊断')
        self.diagnosis_layout = QFormLayout()
        self.diagnosis_result = QLineEdit()
        self.report_result = QTextEdit()

        self.diagnosis_layout.addRow('诊断结果', self.diagnosis_result)
        self.diagnosis_layout.addRow('诊断报告', self.report_result)

        intelligent_diagnostics_group.setLayout(self.diagnosis_layout)
        self.main_layout.addWidget(intelligent_diagnostics_group)


class ZhinengZhenduanPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = WorkstationLayout()
        self.setLayout(self.layout)
        self.similar_window = QWidget()

        # 创建layout
        self.filetree = FileTreeView(config.work_dir)
        self.image_view = MarkableImage()
        self.similar_image_view = MarkableImage()
        self.medical_record_tab = MedicalRecordTab()
        self.similar_record_tab = MedicalRecordTab()
        self.DiagnosisPage = DiagnosisPage()
        self.ResultPage = ResultPage()
        self.mark_label = QHBoxLayout()

        self.clear_button = QPushButton('清除标记')
        self.clear_button.clicked.connect(self.image_view.clear_circles)
        self.save_button = QPushButton('保存标记')
        self.mark_label.addWidget(self.clear_button)
        self.mark_label.addWidget(self.save_button)

        self.medical_record_tab.delete_button.hide()  # 隐藏删除按钮
        self.medical_record_tab.add_image.hide()  # 隐藏添加按钮
        self.medical_record_tab.create_button.hide()  # 隐藏创建按钮

        self.similar_record_tab.delete_button.hide()  # 隐藏删除按钮
        self.similar_record_tab.add_image.hide()  # 隐藏添加按钮
        self.similar_record_tab.create_button.hide()  # 隐藏创建按钮
        self.similar_record_tab.save_button.hide()  # 隐藏保存按钮

        # 信号连接
        self.filetree.item_double_clicked.connect(self.select_image)
        self.filetree.item_double_clicked.connect(self.medical_record_tab.load_record)
        self.DiagnosisPage.diagnosis_button.clicked.connect(self.handle_diagnosis_request)  # 连接诊断按钮
        self.DiagnosisPage.segment_button.clicked.connect(self.handle_segment_request)  # 连接分割按钮
        self.DiagnosisPage.report_button.clicked.connect(self.handle_report_request)  # 连接报告生成按钮
        self.DiagnosisPage.similar_case_button.clicked.connect(self.handle_case_request)  # 连接相似病例按钮

        # 添加layout到主界面
        self.layout.get_mid_left_layout().addWidget(self.filetree)

        self.layout.get_mid_right_layout().addWidget(self.medical_record_tab)
        self.layout.get_mid_right_layout().addWidget(self.ResultPage)

        self.layout.get_center_layout().addWidget(self.image_view)
        self.layout.get_center_layout().addLayout(self.mark_label)

        self.layout.get_bottom_layout().addWidget(self.DiagnosisPage)

        self.current_path = None

        self.medical_record_tab.setMaximumWidth(300)
        self.ResultPage.setMaximumWidth(300)


    def select_image(self, path):
        self.current_path = path
        self.image_view.load_image(path)

    def handle_diagnosis_request(self):
        # image = cv2.imdecode(np.fromfile(self.current_path, dtype=np.uint8), -1)
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # input_image = cv2.resize(image, (224, 224))
        # input_image = input_image.transpose((2, 0, 1))
        # input_image = np.expand_dims(input_image, axis=0)
        #
        # # 使用 ONNX 运行时加载模型
        # session = onnxruntime.InferenceSession("../resources/detect.onnx")
        # # 在 ONNX 运行时中运行模型
        # outputs = session.run(["output"], {"input": input_image.astype(np.float32)})
        # predicted_classes = np.argmax(outputs[0], axis=1)  # 对每一行找到最大值的索引
        # print(predicted_classes[0])
        # if predicted_classes[0] == 1:
        #     result = "恶性"
        # else:
        #     result = "良性"
        #
        # self.ResultPage.diagnosis_result.setText(result)  # 设置诊断结果
        pass

    def handle_segment_request(self):
        # 使用 ONNX 运行时加载模型
        # session = onnxruntime.InferenceSession("../resources/segment.onnx")
        #
        # # 定义一个 ONNX 张量来模拟输入数据
        # image = cv2.imdecode(np.fromfile(self.current_path, dtype=np.uint8), -1)
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # input_image = cv2.resize(image, (256, 256))
        # input_image = input_image.transpose((2, 0, 1))
        # input_image = np.expand_dims(input_image, axis=0)
        #
        # # 在 ONNX 运行时中运行模型
        # outputs = session.run(["output"], {"input": input_image.astype(np.float32)})
        #
        # # 应用sigmoid激活函数将logits转换为概率
        # probabilities = torch.sigmoid(torch.from_numpy(outputs[0]))
        # # 阈值化以获得二进制掩码，阈值通常设为0.5
        # threshold = 0.5
        # mask = (probabilities > threshold).float()
        # # mask现在是一个二分类掩码，shape为(batch_size, 2, height, width)
        # # 其中mask[:, 0, :, :]代表背景，mask[:, 1, :, :]代表前景
        # foreground_mask = mask[:, 1, :, :]
        #
        # # 如果需要，可以将掩码转换为numpy数组并保存或显示
        # foreground_mask_np = foreground_mask.numpy()
        #
        # # 将前景掩码转换为uint8类型
        # foreground_mask_uint8 = (foreground_mask_np[0] * 255).astype(np.uint8)
        #
        # # 使用OpenCV找到轮廓
        # contours, _ = cv2.findContours(foreground_mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #
        # edge_coords_list = []
        # # 检查是否找到了轮廓
        # if not contours:
        #     print("没有检测到病灶。")
        #     edge_coords = np.empty((0, 2))
        # else:
        #     # 遍历每个轮廓
        #     for contour in contours:
        #         # 计算每个轮廓的边界框
        #         x, y, w, h = cv2.boundingRect(contour)
        #
        #         # 计算边界框的周长
        #         perimeter = cv2.arcLength(contour, True)
        #
        #         # 设置周长阈值
        #         min_perimeter, max_perimeter = 30, 100  # 这些值可以根据你的应用场景调整
        #
        #         # 如果边界框的周长在阈值范围内，则添加到列表中
        #         if min_perimeter <= perimeter <= max_perimeter:
        #             edge_coords_list.append((x, y, x + w, y + h))
        #
        #     self.image_view.import_circles(edge_coords_list)
        pass

    def handle_report_request(self):

        tmp = """
所见:
        超声可见:左侧乳腺9点钟位，距乳头旁探及大小约1.8*1.0*1.3cm低回声结节，边缘光整，形态不规则。
        造影可见:呈不均匀低增强，较二维未见增大，周围未见蟹足样粗大滋养血管，结节于58s慢于周围腺体消退，呈不均匀等增强。
        
结论:
        左侧乳腺9点钟乳头旁低回声结节，考虑导管内乳头状肿瘤可能，BI-ADS3类结节性乳腺癌。
            """
        self.ResultPage.report_result.setText(tmp)  # 设置报告结果

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

    def handle_save_label(self):
        pass


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ZhinengZhenduanPage()
    window.show()
    sys.exit(app.exec())
