import re

import qtvscodestyle
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget
# from pyqt_dark_gray_theme.darkGrayTheme import getThemeStyle

from components.layouts import SandwichLayout
from components.tabview import TabView
from pages.home import HomePage, home_path

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    stylesheet = qtvscodestyle.load_stylesheet(qtvscodestyle.Theme.LIGHT_VS)

    # stylesheet = re.sub("QPushButton:pressed", r"QPushButton:pressed { background-color: #4CAF50; color: white; }",
    #                     stylesheet)

    stylesheet += """
    
    QPushButton {
        background-color: #DCDDDF;  /* 灰色背景 */
        color: #444444;  /* 白色文本 */
        border: 1px solid #D9D9D9;  /* 边框颜色 */
        padding: 5px;
        border-radius: 5px;  /* 圆角边框 */
        font-size: 20px;  /* 字体大小 */
    }

    QPushButton:hover {
        background-color: #B5B5B6;  /* 悬停时背景色变为稍亮的灰色 */
        border-color: #777777;  /* 边框颜色变亮 */
    }

    QPushButton:pressed {
        background-color: #8B8B8C;  /* 按下时背景色变为深灰色 */
        color: #FFFFFF;  /* 保持文本白色 */
        border-color: #004085;  /* 边框颜色变为蓝色 */
    }
    """

    app.setStyleSheet(stylesheet)

    window = QWidget()

    layout = SandwichLayout()
    window.setLayout(layout)
    window.setWindowTitle('HeartEFocus')
    window.setWindowIcon(QIcon(home_path + "/resources/lightblue/huabankaobei.svg"))

    tab_view = TabView(layout.get_mid_layout())
    # tab_view = TabView(layout.get_mid_layout(), font_size=10)
    tab_view.add_tab("主页", HomePage(tab_view), closeable=False, icon=QIcon(home_path + "/resources/white/home.svg"))

    layout.get_top_layout().addWidget(tab_view)
    # layout().addWidget(FileTreeView())

    window.resize(1300, 800)
    window.show()

    sys.exit(app.exec())
