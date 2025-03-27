import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout,
    QWidget, QLabel, QRadioButton, QCheckBox, QComboBox
)
from PySide6.QtCharts import (
    QChart, QChartView, QPieSeries, QBarSet, QBarSeries,
    QBarCategoryAxis, QValueAxis, QLineSeries
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QFont


class DashujuFenxiPage(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化生活方式复选框字典
        self.lifestyle_checkboxes = {
            "吸烟": QCheckBox("吸烟"),
            "不吸烟": QCheckBox("不吸烟"),
            "喝酒": QCheckBox("喝酒"),
            "不喝酒": QCheckBox("不喝酒"),
            "长期使用激素": QCheckBox("长期使用激素"),
            "未长期使用激素": QCheckBox("未长期使用激素")
        }

        self.setWindowTitle("乳腺智慧诊断系统 - 数据分析")
        self.setGeometry(100, 100, 1200, 800)

        # 初始化当前状态变量
        self.current_lifestyle = "吸烟"  # 默认选项
        self.current_psychology = "稳定"  # 默认选项

        # 设置默认选择为不吸烟、不喝酒、未长期使用激素
        self.lifestyle_checkboxes["不吸烟"].setChecked(True)
        self.lifestyle_checkboxes["不喝酒"].setChecked(True)
        self.lifestyle_checkboxes["未长期使用激素"].setChecked(True)

        # 创建主布局 (水平布局)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)  # 主水平布局

        # 左侧布局（垂直）并设置间距和边距
        left_layout = QVBoxLayout()
        left_layout.setSpacing(5)  # 设置垂直间距
        left_layout.setContentsMargins(10, 10, 10, 10)  # 设置边距

        # 生活方式选择
        left_layout.addWidget(QLabel("选择生活方式："))

        # 创建两个水平布局以放置复选框
        lifestyle_layout1 = QHBoxLayout()
        lifestyle_layout2 = QHBoxLayout()

        # 添加复选框到第一个水平布局
        lifestyle_layout1.addWidget(self.lifestyle_checkboxes["吸烟"])
        lifestyle_layout1.addWidget(self.lifestyle_checkboxes["喝酒"])
        lifestyle_layout1.addWidget(self.lifestyle_checkboxes["长期使用激素"])

        # 添加复选框到第二个水平布局
        lifestyle_layout2.addWidget(self.lifestyle_checkboxes["不吸烟"])
        lifestyle_layout2.addWidget(self.lifestyle_checkboxes["不喝酒"])
        lifestyle_layout2.addWidget(self.lifestyle_checkboxes["未长期使用激素"])

        # 连接互斥信号槽
        self.lifestyle_checkboxes["吸烟"].stateChanged.connect(lambda: self.mutex_selection("吸烟", "不吸烟"))
        self.lifestyle_checkboxes["不吸烟"].stateChanged.connect(lambda: self.mutex_selection("不吸烟", "吸烟"))
        self.lifestyle_checkboxes["喝酒"].stateChanged.connect(lambda: self.mutex_selection("喝酒", "不喝酒"))
        self.lifestyle_checkboxes["不喝酒"].stateChanged.connect(lambda: self.mutex_selection("不喝酒", "喝酒"))
        self.lifestyle_checkboxes["长期使用激素"].stateChanged.connect(
            lambda: self.mutex_selection("长期使用激素", "未长期使用激素"))
        self.lifestyle_checkboxes["未长期使用激素"].stateChanged.connect(
            lambda: self.mutex_selection("未长期使用激素", "长期使用激素"))

        # 将水平布局添加到左侧布局
        left_layout.addLayout(lifestyle_layout1)
        left_layout.addLayout(lifestyle_layout2)

        # 将复选框的状态变化连接到更新图表的槽函数
        for checkbox in self.lifestyle_checkboxes.values():
            checkbox.stateChanged.connect(self.update_lifestyle_chart)

        # 生活方式饼图
        self.lifestyle_chart_view = self.create_lifestyle_pie_chart()
        left_layout.addWidget(self.lifestyle_chart_view)

        # 年龄段分布折线图（移动到左下角）
        self.age_distribution_chart_view = self.create_age_distribution_line_chart()
        left_layout.addWidget(self.age_distribution_chart_view)

        # 右侧布局（垂直）
        right_layout = QVBoxLayout()

        # 心理状态选择
        right_layout.addWidget(QLabel("选择心理状态："))

        # 使用水平布局来排列心理状态的选项
        psychology_layout = QHBoxLayout()

        self.psychology_buttons = {
            "稳定": QRadioButton("稳定"),
            "轻度抑郁": QRadioButton("轻度抑郁"),
            "重度抑郁": QRadioButton("重度抑郁"),
            "轻度焦虑": QRadioButton("轻度焦虑"),
            "重度焦虑": QRadioButton("重度焦虑")
        }

        # 默认选择
        self.psychology_buttons["稳定"].setChecked(True)

        # 将按钮添加到水平布局中
        for button in self.psychology_buttons.values():
            button.toggled.connect(self.update_psychology_chart)
            psychology_layout.addWidget(button)

        # 将心理状态布局添加到右侧布局
        right_layout.addLayout(psychology_layout)

        # 添加心理状态、身高分布、年龄分布的垂直排列
        self.psychology_chart_view = self.create_psychology_bar_chart()
        right_layout.addWidget(self.psychology_chart_view)

        self.height_chart_view = self.create_height_bar_chart()
        right_layout.addWidget(self.height_chart_view)

        self.weight_chart_view = self.create_weight_bar_chart()
        right_layout.addWidget(self.weight_chart_view)

        # 将左右布局添加到主水平布局
        main_layout.addLayout(left_layout, 15)  # 调宽左侧布局，比例设置为 25
        main_layout.addLayout(right_layout, 20)  # 调窄右侧布局，比例设置为 20
    def create_font(self):
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        return font

    def mutex_selection(self, selected_key, opposite_key):
        if self.lifestyle_checkboxes[selected_key].isChecked():
            self.lifestyle_checkboxes[opposite_key].setChecked(False)
            self.update_lifestyle_chart()  # 选择后更新饼图

    def create_lifestyle_pie_chart(self):
        self.pie_series = QPieSeries()
        self.lifestyle_series = QPieSeries()
        self.update_lifestyle_data()  # 在这里更新生活方式数据

        chart = QChart()
        chart.addSeries(self.lifestyle_series)
        chart.setTitle("生活方式对应肿瘤类别")
        chart.setTitleFont(self.create_font())  # 设置标题字体

        self.lifestyle_series.setPieSize(0.95)  # 增加饼状图比例，使其更大，这里可以调整为更大的值

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
        return chart_view

    # 更新生活方式饼图的数据
    def update_lifestyle_data(self):
        self.lifestyle_series.clear()

        # 获取当前生活方式选择
        smoking = self.lifestyle_checkboxes["吸烟"].isChecked()
        drinking = self.lifestyle_checkboxes["喝酒"].isChecked()
        hormone_use = self.lifestyle_checkboxes["长期使用激素"].isChecked()

        # 根据选择动态更新数据（这里用示例数据）
        benign_tumor = 30
        malignant_tumor = 20

        if smoking:
            benign_tumor -= 10
            malignant_tumor += 10

        if drinking:
            benign_tumor -= 8
            malignant_tumor += 8

        if hormone_use:
            benign_tumor -= 3
            malignant_tumor += 3

        # 更新饼图
        slice_benign = self.lifestyle_series.append("良性肿瘤", benign_tumor)
        slice_malignant = self.lifestyle_series.append("恶性肿瘤", malignant_tumor)

        # 修改饼图的比例，仅调整饼图的显示大小，不影响其逻辑
        slice_benign.setExploded(True)  # 使良性肿瘤部分突显出来
        slice_benign.setExplodeDistanceFactor(0.1)  # 设置突显的距离

        slice_malignant.setExploded(False)  # 恶性肿瘤部分不突显

    def update_lifestyle_chart(self):
        self.update_lifestyle_data()

    def create_height_bar_chart(self):
        self.height_series = QBarSeries()
        self.update_height_data()

        chart = QChart()
        chart.addSeries(self.height_series)
        chart.setTitle("身高分布")
        chart.setTitleFont(self.create_font())  # 设置标题字体
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ["150-160cm", "160-170cm", "170-180cm", "180-190cm"]
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsFont(self.create_font())  # 设置X轴字体
        chart.addAxis(axisX, Qt.AlignBottom)
        self.height_series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, 100)
        axisY.setLabelsFont(self.create_font())  # 设置Y轴字体
        chart.addAxis(axisY, Qt.AlignLeft)
        self.height_series.attachAxis(axisY)

        chart.legend().hide()  # 隐藏图例

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
        return chart_view

    def update_height_data(self):
        self.height_series.clear()
        height_set = QBarSet("身高人数")
        height_set.append([40, 70, 60, 51])  # 模拟数据，总数为221
        self.height_series.append(height_set)

    def create_weight_bar_chart(self):
        self.weight_series = QBarSeries()
        self.update_weight_data()

        chart = QChart()
        chart.addSeries(self.weight_series)
        chart.setTitle("体重分布")
        chart.setTitleFont(self.create_font())  # 设置标题字体
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ["40-50kg", "50-60kg", "60-70kg", "70-80kg"]
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsFont(self.create_font())  # 设置X轴字体
        chart.addAxis(axisX, Qt.AlignBottom)
        self.weight_series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, 100)
        axisY.setLabelsFont(self.create_font())  # 设置Y轴字体
        chart.addAxis(axisY, Qt.AlignLeft)
        self.weight_series.attachAxis(axisY)

        chart.legend().hide()  # 隐藏图例

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
        return chart_view

    def update_weight_data(self):
        self.weight_series.clear()
        weight_set = QBarSet("体重人数")
        weight_set.append([30, 60, 80, 51])  # 模拟数据，总数为221
        self.weight_series.append(weight_set)

    def create_psychology_bar_chart(self):
        # 创建心理状态柱状图
        self.psychology_series = QBarSeries()
        self.update_psychology_data()  # 初始化数据

        chart = QChart()
        chart.addSeries(self.psychology_series)
        chart.setTitle("心理状态分布")
        chart.setTitleFont(self.create_font())  # 设置标题字体
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ["20-30岁", "30-40岁", "40-50岁", "50-60岁"]
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsFont(self.create_font())  # 设置X轴字体
        chart.addAxis(axisX, Qt.AlignBottom)
        self.psychology_series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, 100)
        axisY.setLabelsFont(self.create_font())  # 设置Y轴字体
        chart.addAxis(axisY, Qt.AlignLeft)
        self.psychology_series.attachAxis(axisY)

        chart.legend().hide()  # 隐藏图例

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
        return chart_view

    def update_psychology_data(self):
        # 获取当前心理状态选择
        selected_psychology = next(key for key, button in self.psychology_buttons.items() if button.isChecked())

        # 根据不同的心理状态更新数据（这里只是示例数据，可以根据实际数据来源进行调整）
        self.psychology_series.clear()

        if selected_psychology == "稳定":
            data = [42, 31, 51, 63]  # 模拟数据，表示不同年龄段的分布
        elif selected_psychology == "轻度抑郁":
            data = [30, 51, 46, 30]
        elif selected_psychology == "重度抑郁":
            data = [15, 25, 26, 20]
        elif selected_psychology == "轻度焦虑":
            data = [13, 26, 20, 15]
        elif selected_psychology == "重度焦虑":
            data = [26, 42, 35, 12]

        bar_set = QBarSet(selected_psychology)
        bar_set.append(data)
        self.psychology_series.append(bar_set)

    def update_psychology_chart(self):
        self.update_psychology_data()  # 更新数据

    def create_age_distribution_line_chart(self):
        # 创建年龄段分布折线图（右上角）
        self.age_series = QLineSeries()
        self.update_age_distribution_data()  # 初始化数据

        # 创建图表并添加系列
        chart = QChart()
        chart.addSeries(self.age_series)
        chart.setTitle("年龄段分布")
        chart.setTitleFont(self.create_font())  # 设置标题字体
        chart.setAnimationOptions(QChart.SeriesAnimations)

        chart.legend().hide()  # 隐藏图例

        # 设置X轴标签
        axisX = QValueAxis()
        axisX.setRange(20, 60)  # 年龄范围
        axisX.setLabelFormat("%d")
        axisX.setTitleText("年龄")
        chart.addAxis(axisX, Qt.AlignBottom)
        self.age_series.attachAxis(axisX)

        # 设置Y轴标签
        axisY = QValueAxis()
        axisY.setRange(0, 100)
        axisY.setLabelFormat("%d")
        axisY.setTitleText("人数")
        chart.addAxis(axisY, Qt.AlignLeft)
        self.age_series.attachAxis(axisY)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
        return chart_view

    def update_age_distribution_data(self):
        # 获取当前生活方式选择
        smoking = self.lifestyle_checkboxes["吸烟"].isChecked()
        drinking = self.lifestyle_checkboxes["喝酒"].isChecked()
        hormone_use = self.lifestyle_checkboxes["长期使用激素"].isChecked()

        self.age_series.clear()

        # 根据生活方式动态更新年龄段数据
        if smoking and drinking and hormone_use:
            data = [10, 25, 30, 35, 50]  # 全部不健康习惯
        elif smoking and drinking:
            data = [15, 20, 31, 35, 42]  # 吸烟和喝酒
        elif smoking and hormone_use:
            data = [25, 29, 30, 40, 45]  # 吸烟和长期使用激素
        elif drinking and hormone_use:
            data = [21, 32, 35, 40, 55]  # 喝酒和长期使用激素
        elif smoking:
            data = [23, 30, 36, 40, 50]  # 只有吸烟
        elif drinking:
            data = [25, 35, 40, 45, 60]  # 只有喝酒
        elif hormone_use:
            data = [15, 20, 30, 45, 50]  # 只有长期使用激素
        else:
            data = [15, 17, 20, 30, 35]  # 所有健康习惯

        # 将数据添加到年龄段折线图中，X轴为年龄，Y轴为人数
        ages = [20, 30, 40, 50, 60]
        for i, age in enumerate(ages):
            self.age_series.append(age, data[i])  # 添加年龄和人数数据

    def update_lifestyle_chart(self):
        self.update_lifestyle_data()
        self.update_age_distribution_data()  # 更新年龄段数据

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashujuFenxiPage()
    window.show()
    sys.exit(app.exec())
