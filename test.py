import re

import qtvscodestyle
from PySide6.QtWidgets import QWidget, QTextEdit

from components.filetreeview import FileTreeView
from components.layouts import WorkstationLayout
from components.tabview import TabView

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    stylesheet = qtvscodestyle.load_stylesheet(qtvscodestyle.Theme.DARK_VS)
    # stylesheet = qtvscodestyle.load_stylesheet(qtvscodestyle.Theme.LIGHT_VS)
    # 查找QPushButton:pressed的样式并在其后添加QPushButton:default
    stylesheet = re.sub("QPushButton:pressed", r"QPushButton:not(NestedButton):pressed, NestedButton:default",
                        stylesheet)

    app.setStyleSheet(stylesheet)

    window = QWidget()
    ws_layout = WorkstationLayout()
    # ws_layout.get_top_layout().setContentsMargins(0, 0, 0, 0)
    # ws_layout.get_top_layout().setSpacing(5)

    window.setLayout(ws_layout)
    window.resize(1280, 800)

    tab_view = TabView(ws_layout.get_center_layout())
    tab_view.add_tab("主页", QTextEdit("欢迎来到，西南交通大学多病种智慧诊断平台项目"), closeable=False)
    tab_view.add_tab("功能1", QTextEdit("功能1"))
    tab_view.add_tab("功能2", QTextEdit("功能2"))
    tab_view.add_tab("功能3", QTextEdit("功能3"))
    tab_view.add_tab("功能4", QTextEdit("功能4"))

    ws_layout.get_top_layout().addWidget(tab_view)
    ws_layout.get_mid_left_layout().addWidget(FileTreeView())
    window.show()

    sys.exit(app.exec())
