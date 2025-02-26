import json
import pathlib
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


class ImageTypeSelectDialog(QDialog):
    def __init__(self, image_path):
        super().__init__()
        image_path = pathlib.Path(image_path)
        self.image_path = image_path

        layout = QVBoxLayout()

        label = QLabel()
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        layout.addWidget(label)

        self.type = QComboBox()
        self.type.addItems(["B型超声", "超声造影", "X线", "磁共振", "CT", "患者照片"])
        default_type = image_path.stem.split("_")[-1]
        self.type.setCurrentText(default_type)
        layout.addWidget(self.type)

        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        self.delete_button = QPushButton("删除")
        self.delete_button.clicked.connect(self.delete_image)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_type(self):
        return self.type.currentText()

    def delete_image(self):
        self.image_path.unlink()
        self.accept()


class MedicalRecordTab(QWidget):
    def __init__(self):
        super().__init__()

        # 主布局
        main_layout = QVBoxLayout()

        # 基础信息分组
        self.basic_info_group = QGroupBox("基础信息")
        basic_info_layout = QFormLayout()
        basic_info_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.record_number = QLineEdit()
        basic_info_layout.addRow("病历卡号:", self.record_number)

        self.name_input = QLineEdit()
        basic_info_layout.addRow("姓名:", self.name_input)

        self.age_input = QSpinBox()
        self.age_input.setRange(0, 120)
        basic_info_layout.addRow("年龄:", self.age_input)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["女", "男", "未知"])
        basic_info_layout.addRow("性别:", self.gender_input)

        self.ethnicity_input = QComboBox()
        self.ethnicity_input.addItems(["汉族", "壮族", "满族", "回族", "其他"])
        basic_info_layout.addRow("民族:", self.ethnicity_input)

        self.basic_info_group.setLayout(basic_info_layout)
        # main_layout.addWidget(self.basic_info_group)

        # 病史信息分组
        self.medical_history_group = QGroupBox("病史信息")
        medical_history_layout = QFormLayout()
        medical_history_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.menarche_age_input = QSpinBox()
        self.menarche_age_input.setRange(8, 20)
        medical_history_layout.addRow("初潮年龄:", self.menarche_age_input)

        self.last_menstruation_age_input = QSpinBox()
        self.last_menstruation_age_input.setRange(30, 60)
        medical_history_layout.addRow("末次月经年龄:", self.last_menstruation_age_input)

        self.family_history_input = QCheckBox("是")
        medical_history_layout.addRow("乳腺癌家族史:", self.family_history_input)

        self.breast_surgery_input = QCheckBox("是")
        medical_history_layout.addRow("乳腺手术史:", self.breast_surgery_input)

        self.childbirth_history_input = QCheckBox("是")
        medical_history_layout.addRow("生育史:", self.childbirth_history_input)

        self.breastfeeding_history_input = QCheckBox("是")
        medical_history_layout.addRow("哺乳史:", self.breastfeeding_history_input)

        self.medical_history_group.setLayout(medical_history_layout)
        # main_layout.addWidget(self.medical_history_group)

        # 检查结果分组
        exam_results_group = QGroupBox("检查结果")
        exam_results_layout = QFormLayout()
        exam_results_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.imaging_results_input = QTextEdit()
        exam_results_layout.addRow("乳腺影像学检查结果:", self.imaging_results_input)

        self.breast_lump_input = QCheckBox("是")
        exam_results_layout.addRow("是否有乳腺肿块:", self.breast_lump_input)

        self.axillary_lymph_input = QCheckBox("是")
        exam_results_layout.addRow("腋窝淋巴结肿大:", self.axillary_lymph_input)

        self.skin_changes_input = QTextEdit()
        exam_results_layout.addRow("乳腺皮肤变化:", self.skin_changes_input)

        exam_results_group.setLayout(exam_results_layout)
        # main_layout.addWidget(exam_results_group)

        # 生活方式分组
        self.lifestyle_group = QGroupBox("生活方式")
        lifestyle_layout = QFormLayout()
        lifestyle_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.hormone_use_input = QCheckBox("是")
        lifestyle_layout.addRow("是否长期使用激素:", self.hormone_use_input)

        self.smoking_history_input = QCheckBox("是")
        lifestyle_layout.addRow("是否吸烟:", self.smoking_history_input)

        self.drinking_history_input = QCheckBox("是")
        lifestyle_layout.addRow("是否饮酒:", self.drinking_history_input)

        self.lifestyle_group.setLayout(lifestyle_layout)
        # main_layout.addWidget(self.lifestyle_group)

        # 心理状况分组
        psychology_group = QGroupBox("心理状况")
        psychology_layout = QFormLayout()
        psychology_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.psychological_assessment_input = QTextEdit()
        psychology_layout.addRow("心理压力评估:", self.psychological_assessment_input)

        psychology_group.setLayout(psychology_layout)
        # main_layout.addWidget(psychology_group)

        # 身高体重和BMI（水平布局）
        bmi_group = QGroupBox("身高/体重与BMI")
        bmi_layout = QFormLayout()

        self.height_input = QSpinBox()
        self.height_input.setRange(50, 250)
        bmi_layout.addRow("身高(cm):", self.height_input)

        self.weight_input = QSpinBox()
        self.weight_input.setRange(2, 200)
        bmi_layout.addRow("体重(kg):", self.weight_input)

        self.bmi_label = QLabel("0.00")
        bmi_layout.addRow("BMI:", self.bmi_label)

        self.height_input.valueChanged.connect(self.calculate_bmi)
        self.weight_input.valueChanged.connect(self.calculate_bmi)

        bmi_group.setLayout(bmi_layout)
        # main_layout.addWidget(bmi_group)

        scroll = QScrollArea()
        self.layout = AutoGridWidget(item_width=500)
        self.layout.add_widget(self.basic_info_group)
        self.layout.add_widget(self.medical_history_group)
        self.layout.add_widget(self.lifestyle_group)
        self.layout.add_widget(bmi_group)
        self.layout.add_widget(exam_results_group)
        self.layout.add_widget(psychology_group)
        scroll.setWidget(self.layout)
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)

        button_layout = QHBoxLayout()
        self.create_button = QPushButton("新建")
        self.create_button.clicked.connect(self.create_record)
        button_layout.addWidget(self.create_button)

        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_record)
        button_layout.addWidget(self.save_button)

        self.delete_button = QPushButton("删除")
        self.delete_button.clicked.connect(self.delete_record)
        button_layout.addWidget(self.delete_button)
        self.add_image = QPushButton("添加影像")
        button_layout.addWidget(self.add_image)
        self.add_image.clicked.connect(self.add_image_to_record)

        main_layout.addLayout(button_layout)
        # 设置主布局
        self.setLayout(main_layout)

        self.original_path = None
        self.original_file_name = None

    def calculate_bmi(self):
        height = self.height_input.value() / 100  # 转换成米
        weight = self.weight_input.value()
        if height > 0:
            bmi = weight / (height * height)
            self.bmi_label.setText(f"{bmi:.2f}")
        else:
            self.bmi_label.setText("0.00")

    def to_dict(self):
        record = dict()
        record["病历卡号"] = self.record_number.text()
        record["姓名"] = self.name_input.text()
        record["年龄"] = self.age_input.value()
        record["性别"] = self.gender_input.currentText()
        record["民族"] = self.ethnicity_input.currentText()
        record["初潮年龄"] = self.menarche_age_input.value()
        record["末次月经年龄"] = self.last_menstruation_age_input.value()
        record["乳腺癌家族史"] = self.family_history_input.isChecked()
        record["乳腺手术史"] = self.breast_surgery_input.isChecked()
        record["生育史"] = self.childbirth_history_input.isChecked()
        record["哺乳史"] = self.breastfeeding_history_input.isChecked()
        record["乳腺影像学检查结果"] = self.imaging_results_input.toPlainText()
        record["是否有乳腺肿块"] = self.breast_lump_input.isChecked()
        record["腋窝淋巴结肿大"] = self.axillary_lymph_input.isChecked()
        record["乳腺皮肤变化"] = self.skin_changes_input.toPlainText()
        record["是否长期使用激素"] = self.hormone_use_input.isChecked()
        record["是否吸烟"] = self.smoking_history_input.isChecked()
        record["是否饮酒"] = self.drinking_history_input.isChecked()
        record["心理压力评估"] = self.psychological_assessment_input.toPlainText()
        record["身高(cm)"] = self.height_input.value()
        record["体重(kg)"] = self.weight_input.value()
        record["BMI"] = self.bmi_label.text()

        return record

    def dict_to_ui(self, record):
        self.record_number.setText(record["病历卡号"])
        self.name_input.setText(record["姓名"])
        self.age_input.setValue(record["年龄"])
        self.gender_input.setCurrentText(record["性别"])
        self.ethnicity_input.setCurrentText(record["民族"])
        self.menarche_age_input.setValue(record["初潮年龄"])
        self.last_menstruation_age_input.setValue(record["末次月经年龄"])
        self.family_history_input.setChecked(record["乳腺癌家族史"])
        self.breast_surgery_input.setChecked(record["乳腺手术史"])
        self.childbirth_history_input.setChecked(record["生育史"])
        self.breastfeeding_history_input.setChecked(record["哺乳史"])
        self.imaging_results_input.setText(record["乳腺影像学检查结果"])
        self.breast_lump_input.setChecked(record["是否有乳腺肿块"])
        self.axillary_lymph_input.setChecked(record["腋窝淋巴结肿大"])
        self.skin_changes_input.setText(record["乳腺皮肤变化"])
        self.hormone_use_input.setChecked(record["是否长期使用激素"])
        self.smoking_history_input.setChecked(record["是否吸烟"])
        self.drinking_history_input.setChecked(record["是否饮酒"])
        self.psychological_assessment_input.setText(record["心理压力评估"])
        self.height_input.setValue(record["身高(cm)"])
        self.weight_input.setValue(record["体重(kg)"])
        self.bmi_label.setText(record["BMI"])

    def save_record(self):
        record = self.to_dict()
        print(record)
        if self.original_path is None:
            self.original_path = pathlib.Path(config.work_dir) / (record["姓名"] + "_" + record["病历卡号"])
            self.original_file_name = "病历.json"
        else:
            # 如果病历卡号或者姓名发生变化，需要将原来的文件夹改名
            if self.original_path.name != (record["姓名"] + record["病历卡号"]):
                new_path = pathlib.Path(config.work_dir) / (record["姓名"] + "_" + record["病历卡号"])
                self.original_path.rename(new_path)
                self.original_path = new_path
        makedirs(self.original_path, exist_ok=True)

        json_path = self.original_path / self.original_file_name
        print(json_path)
        with open(json_path, "w") as f:
            json.dump(record, f, ensure_ascii=False, indent=4)

    def create_record(self):
        record = self.to_dict()
        self.original_path = pathlib.Path(config.work_dir) / (record["姓名"] + "_" + record["病历卡号"])
        self.original_file_name = "病历.json"
        if self.original_path.exists():
            QMessageBox.warning(self, "警告", "该病历已经存在，请重新输入")
            return

        makedirs(self.original_path, exist_ok=True)
        json_path = self.original_path / self.original_file_name
        with open(json_path, "w") as f:
            json.dump(record, f, ensure_ascii=False, indent=4)
        self.original_record_path = json_path
        self.clear_record()

    def load_record(self, json_path):
        path = pathlib.Path(json_path)
        self.original_path = path.parent
        self.original_file_name = path.name
        with open(json_path, "r") as f:
            record = json.load(f)
        self.dict_to_ui(record)

    def clear_record(self):
        self.record_number.clear()
        self.name_input.clear()
        self.age_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.ethnicity_input.setCurrentIndex(0)
        self.menarche_age_input.clear()
        self.last_menstruation_age_input.clear()
        self.family_history_input.setChecked(False)
        self.breast_surgery_input.setChecked(False)
        self.childbirth_history_input.setChecked(False)
        self.breastfeeding_history_input.setChecked(False)
        self.imaging_results_input.clear()
        self.breast_lump_input.setChecked(False)
        self.axillary_lymph_input.setChecked(False)
        self.skin_changes_input.clear()
        self.hormone_use_input.setChecked(False)
        self.smoking_history_input.setChecked(False)
        self.drinking_history_input.setChecked(False)
        self.psychological_assessment_input.clear()
        self.height_input.clear()
        self.weight_input.clear()
        self.bmi_label.clear()

    def delete_record(self):
        if self.original_path is not None:
            import shutil
            shutil.rmtree(self.original_path)
            self.original_path = None
            self.original_record_path = None
            self.clear_record()

    def add_image_to_record(self):
        if self.original_path is None:
            QMessageBox.warning(self, "警告", "请先创建或者加载病历")
            return
        import shutil
        from PySide6.QtWidgets import QFileDialog
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        if file_dialog.exec():
            for file in file_dialog.selectedFiles():
                image_type = self.show_image_in_dialog(file)
                # 文件名修改为image_type+后缀
                image_path = self.original_path / (image_type + pathlib.Path(file).suffix)
                shutil.copy(file, image_path)

    def show_image_in_dialog(self, image_path):
        dialog = ImageTypeSelectDialog(image_path)
        if dialog.exec():
            image_type = dialog.get_type()
            return image_type

    def auto_load(self, file_path):
        file_path = pathlib.Path(file_path)
        if file_path.is_dir():
            print("load dir", file_path)
            self.load_record(file_path / "病历.json")
            return

        if file_path.suffix == ".json":
            self.load_record(file_path)
        elif file_path.suffix in [".jpg", ".png", ".bmp"]:
            image_type = self.show_image_in_dialog(file_path)
            print(image_type)
            if image_type is not None:
                import shutil
                image_path = file_path.parent / (image_type + file_path.suffix)
                rename(file_path, image_path)
        else:
            QMessageBox.warning(self, "警告", "不支持的文件类型")


class BingliGuanliPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = WorkstationLayout()

        self.setLayout(self.layout)

        self.filetree = FileTreeView(config.work_dir)
        self.image_view = MarkableImage()
        self.medical_record_tab = MedicalRecordTab()

        self.filetree.item_double_clicked.connect(self.medical_record_tab.auto_load)

        title_label = QLabel('病历管理')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        self.layout.get_top_layout().addWidget(title_label)
        self.layout.get_mid_left_layout().addWidget(self.filetree)
        self.layout.get_center_layout().addWidget(self.medical_record_tab)
        # self.layout.get_mid_right_layout().addWidget(QLabel('右边'))


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = BingliGuanliPage()
    window.show()
    sys.exit(app.exec())
