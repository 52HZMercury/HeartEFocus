import os, sys
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel

from components.layouts import AutoGridWidget
from components.tabview import TabView
from pages.bingliguanli_page import BingliGuanliPage
from pages.huifang_page import HuiFangPage
from pages.labelVentriclePage import labelVentriclePage
from pages.shishizhinengjiance_page import ShishiZhiNengJiancePage
from pages.xiaoxizhongxin_page import ChatWindow
from pages.zhinengzhenduan_page import ZhinengZhenduanPage
from pages.dashujufenxi_page import DashujuFenxiPage

home_path = os.path.dirname(sys.argv[0])

class HomePage(QWidget):
    def __init__(self, tabview: TabView, parent=None):
        super(HomePage, self).__init__(parent=parent)
        self.tabview = tabview
        bingli_path = home_path + "/resources/white/dianzibingli.svg"
        binglizhenduan_path = home_path + "/resources/white/chaoshengzhenduanyi.svg"
        shishijiankong_path = home_path + "/resources/white/huabankaobei.svg"
        tongjifenxi_path = home_path + "/resources/white/_shujufenxi.svg"
        tongyongzhenduan_path = home_path + "/resources/white/gerenzhenduan.svg"
        peixunxitong_path = home_path + "/resources/white/peixunxitong.svg"
        gonggao_path = home_path + "/resources/white/gonggao.svg"

        # 心室勾画 室壁勾画 计算射血分数
        self.button0 = QPushButton(' 开始使用')
        # 选择文件夹  todo

        self.button0.setFixedHeight(100)
        self.button0.setFixedWidth(300)
        self.button0.setIcon(QIcon(binglizhenduan_path))
        self.button0.setIconSize(QSize(40, 40))
        self.button0.clicked.connect(
            lambda: self.tabview.add_tab('心脏数据标注', labelVentriclePage(), True, icon=QIcon(binglizhenduan_path)))

        # self.button1 = QPushButton(text='  室壁勾画')
        # self.button1.setMinimumHeight(100)
        # self.button1.setIcon(QIcon(bingli_path))
        # self.button1.setIconSize(QSize(40, 40))
        # self.button1.clicked.connect(
        #     lambda: self.tabview.add_tab('病历管理', BingliGuanliPage(), True, icon=QIcon(bingli_path)))
        #
        #
        # self.button2 = QPushButton('  射血分数计算')
        # self.button2.setMinimumHeight(100)
        # self.button2.setIcon(QIcon(binglizhenduan_path))
        # self.button2.setIconSize(QSize(40, 40))
        # self.button2.clicked.connect(
        #     lambda: self.tabview.add_tab('射血分数', DashujuFenxiPage(), True, icon=QIcon(binglizhenduan_path)))

        # self.button1 = QPushButton(text='  病历管理')
        # self.button1.setMinimumHeight(100)
        # self.button1.setIcon(QIcon(bingli_path))
        # self.button1.setIconSize(QSize(40, 40))
        # self.button1.clicked.connect(
        #     lambda: self.tabview.add_tab('病历管理', BingliGuanliPage(), True, icon=QIcon(bingli_path)))

        # self.button2 = QPushButton('  智能诊断')
        # self.button2.setMinimumHeight(100)
        # self.button2.setIcon(QIcon(binglizhenduan_path))
        # self.button2.setIconSize(QSize(40, 40))
        # self.button2.clicked.connect(
        #     lambda: self.tabview.add_tab('智能诊断', ZhinengZhenduanPage(), True, icon=QIcon(binglizhenduan_path)))

        # self.button3 = QPushButton('  实时智能监控')
        # self.button3.setMinimumHeight(100)
        # self.button3.setIcon(QIcon(shishijiankong_path))
        # self.button3.setIconSize(QSize(40, 40))
        # self.button3.clicked.connect(
        #     lambda: self.tabview.add_tab('实时智能监控', ShishiZhiNengJiancePage(), True))
        #
        # self.button4 = QPushButton('  大数据分析')
        # self.button4.setMinimumHeight(100)
        # self.button4.setIcon(QIcon(tongjifenxi_path))
        # self.button4.setIconSize(QSize(40, 40))
        # self.button4.clicked.connect(
        #     lambda: self.tabview.add_tab('大数据分析', DashujuFenxiPage(), True, icon=QIcon(tongjifenxi_path)))

        # self.button5 = QPushButton('  通用诊断')
        # # self.button5.setMinimumHeight(100)
        # self.button5.setIcon(QIcon(tongyongzhenduan_path))
        # self.button5.setIconSize(QSize(40, 40))
        # self.button5.clicked.connect(lambda: self.tabview.add_tab('通用诊断', QLabel('通用诊断'), True))

        # self.button5 = QPushButton('  病例回访')
        # self.button5.setMinimumHeight(100)
        # self.button5.setIcon(QIcon(tongyongzhenduan_path))
        # self.button5.setIconSize(QSize(40, 40))
        # self.button5.clicked.connect(lambda: self.tabview.add_tab('病例回访', HuiFangPage(), True, icon=QIcon(tongyongzhenduan_path)))
        #
        # self.button6 = QPushButton('  培训系统（开发中）')
        # self.button6.setMinimumHeight(100)
        # self.button6.setIcon(QIcon(peixunxitong_path))
        # self.button6.setIconSize(QSize(40, 40))
        # self.button6.clicked.connect(lambda: self.tabview.add_tab('培训系统（开发中）', QLabel('培训系统'), True, icon=QIcon(peixunxitong_path)))
        #
        # self.button7 = QPushButton('消息中心')
        # self.button7.setMinimumHeight(100)
        # self.button7.setIcon(QIcon(gonggao_path))
        # self.button7.setIconSize(QSize(40, 40))
        # self.button7.clicked.connect(
        #     lambda: self.tabview.add_tab('消息中心', ChatWindow(), True, icon=QIcon(gonggao_path)))

        title_label = QLabel('HeartEFcous')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 40px; font-weight: bold;')

        description_label = QLabel('v0.1')
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet('font-size: 20px; font-weight: bold;')

        grid = AutoGridWidget()
        grid.add_widget(self.button0)
        # grid.add_widget(self.button1)
        # grid.add_widget(self.button2)
        # grid.add_widget(self.button3)
        # grid.add_widget(self.button4)
        # grid.add_widget(self.button5)
        # grid.add_widget(self.button6)
        # grid.add_widget(self.button7)



        self.layout = QVBoxLayout()
        # self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(title_label)
        self.layout.addWidget(description_label)
        self.layout.addWidget(grid, stretch=1)

        self.setLayout(self.layout)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    home_page = HomePage(TabView())
    home_page.show()
    sys.exit(app.exec())
