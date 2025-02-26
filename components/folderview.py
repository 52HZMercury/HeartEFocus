import os

from PySide6.QtCore import QFileInfo, Signal
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QFileIconProvider, QPushButton, QHBoxLayout, \
    QLabel, QFileDialog, QVBoxLayout, QLineEdit, QHeaderView


class FileTreeView(QWidget):
    open_file_signal = Signal(str)

    def __init__(self, folder=None, parent=None):
        super().__init__(parent)

        if not folder or not os.path.exists(folder):
            # 获取用户目录
            folder = os.path.expanduser('~')

        self.folder = folder
        self.parent = parent
        self.folder_label = QLineEdit(self.folder, self)
        self.folder_label.setReadOnly(True)
        self.select_folder_button = QPushButton('选择', self)
        self.select_folder_button.clicked.connect(self.select_folder)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['文件名', 'Path'])
        self.table.hideColumn(1)
        # 显示排序图标
        # 显示头部
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.setSortingEnabled(True)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setShowGrid(False)
        # self.table.verticalHeader().setVisible(False)
        # self.table.horizontalHeader().setVisible(False)
        self.table.setColumnWidth(0, 300)
        # 搜索过滤框
        self.search_line = QLineEdit(self)
        self.search_line.setPlaceholderText('搜索')
        self.search_line.textChanged.connect(self.search_file)

        self.table.itemDoubleClicked.connect(self.double_click_file)

        # 显示文件列表
        self.show_file_list()

        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout1.addWidget(self.select_folder_button)
        layout2.addWidget(QLabel('当前文件夹：', self))
        layout2.addWidget(self.folder_label)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addWidget(self.search_line)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.clear_margins()

    def search_file(self):
        search_text = self.search_line.text()
        if not search_text:
            self.show_file_list()
            return

        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if search_text in item.text():
                self.table.setRowHidden(i, False)
            else:
                self.table.setRowHidden(i, True)

    def remove_all_items(self):
        for i in range(self.table.rowCount()):
            self.table.removeRow(0)

    def show_file_list(self):
        self.remove_all_items()
        # 假设 self.folder 和 self.file_list_widget 已经定义
        file_list = os.listdir(self.folder)
        file_list.sort()

        # 创建一个 QFileIconProvider 实例
        icon_provider = QFileIconProvider()

        for file in file_list:
            file_name = os.path.join(self.folder, file)
            if os.path.isfile(file_name):
                file_name_only = os.path.basename(file_name)
                row_count = self.table.rowCount()
                row_item0 = QTableWidgetItem(file_name_only)

                # 获取文件的图标
                file_info = QFileInfo(file_name)
                file_icon = icon_provider.icon(file_info)
                row_item0.setIcon(file_icon)

                self.table.insertRow(row_count)
                self.table.setItem(row_count, 0, row_item0)

        self.table.resizeColumnsToContents()
        self.folder_label.setText(f"{self.folder}")

    def double_click_file(self, item):
        file_name = item.text()
        file_path = os.path.join(self.folder, file_name)
        if os.path.isfile(file_path):
            self.open_file_signal.emit(file_path)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择文件夹', self.folder)
        if folder:
            self.folder = folder
            self.show_file_list()

    def clear_margins(self):
        self.layout().setContentsMargins(0, 0, 0, 0)



if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    file_list_view = FileTreeView()
    file_list_view.show()
    sys.exit(app.exec())
