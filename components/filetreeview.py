import pathlib

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QTreeWidget, QHBoxLayout, QTreeWidgetItem, QVBoxLayout, QPushButton, \
    QLineEdit
from natsort import natsorted

import config


class FileTreeView(QWidget):
    item_double_clicked = Signal(str)

    def __init__(self, base_folder):
        super().__init__()
        self.base_folder = base_folder
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search")
        self.search.textChanged.connect(self.filter_tree)

        self.treeview = QTreeWidget()
        self.treeview.setHeaderHidden(True)
        self.treeview.setColumnCount(1)
        self.treeview.setIndentation(20)
        self.treeview.setRootIsDecorated(False)
        self.treeview.setSortingEnabled(True)
        self.treeview.sortByColumn(0, Qt.AscendingOrder)
        self.treeview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeview.setExpandsOnDoubleClick(False)
        self.treeview.doubleClicked.connect(self.tree_view_double_click)
        # self.treeview.customContextMenuRequested.connect(self.show_menu)

        self.expand_all_button = QPushButton("展开")
        self.collapse_all_button = QPushButton("收起")
        self.reload_button = QPushButton("刷新")

        self.expand_all_button.clicked.connect(self.treeview.expandAll)
        self.collapse_all_button.clicked.connect(self.treeview.collapseAll)
        self.reload_button.clicked.connect(self.reload)

        layout = QVBoxLayout()
        layout.addWidget(self.search)
        layout.addWidget(self.treeview, 1)
        layout2 = QHBoxLayout()

        # layout2.addWidget(self.expand_all_button)
        # layout2.addWidget(self.collapse_all_button)
        layout2.addWidget(self.reload_button)
        layout.addLayout(layout2)
        self.setLayout(layout)

        self.read_dir_add_to_tree(self.base_folder)
        self.treeview.expandAll()

    def add_item(self, item):
        item_path = pathlib.Path(item)
        item_path = item_path.relative_to(self.base_folder)
        parent = self.treeview.invisibleRootItem()
        print(item_path)
        print(parent)
        parts_len = len(item_path.parts)
        for i, part in enumerate(item_path.parts):
            print(i, part)
            child = self.find_child(parent, part)
            if child is None:
                print("not found")
                child = QTreeWidgetItem(parent)
                if i == 0:
                    # 设置可以勾选
                    child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    child.setCheckState(0, Qt.Unchecked)
                    child.setText(0, part)
                    child.setText(1, str(pathlib.Path(item).parent))
                else:
                    child.setText(0, part)
                    child.setText(1, item)
            parent = child

    def find_child(self, parent, text):
        for index in range(parent.childCount()):
            child = parent.child(index)
            print(child.text(0), text)
            if child.text(0) == text:
                return child
        return None

    def all_files(self, folder):
        import os
        all_files = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                all_files.append(os.path.join(root, file))

        # 使用 sorted 进行字典排序
        return sorted(all_files)

    def read_dir_add_to_tree(self, folder):
        for file in self.all_files(folder):
            self.add_item(file)

    def filter_tree(self):
        search_text = self.search.toPlainText().lower()
        for i in range(self.treeview.topLevelItemCount()):
            item = self.treeview.topLevelItem(i)
            self.filter_item(item, search_text)

    def filter_item(self, item, search_text):
        item.setHidden(False)
        for i in range(item.childCount()):
            child = item.child(i)
            self.filter_item(child, search_text)

        if search_text in item.text(0).lower():
            item.setHidden(False)
            return True
        elif search_text in item.text(1).lower():
            item.setHidden(False)
            return True
        else:
            item.setHidden(True)
            for i in range(item.childCount()):
                child = item.child(i)
                self.filter_item(child, search_text)

    # def tree_view_double_click(self, index):
    #     item = self.treeview.itemFromIndex(index)
    #     if item and item.text(1):
    #         file_path = pathlib.Path(item.text(1))
    #         if file_path.is_file():
    #             self.item_double_clicked.emit(str(file_path))  # 确保这里传递的是绝对路径

    def tree_view_double_click(self, index):
        print("Double click detected!")
        item = self.treeview.currentItem()
        if item:
            print(f"Item text: {item.text(0)}")
            self.item_double_clicked.emit(item.text(0))
        else:
            print("No item selected!")

    def reload(self):
        self.treeview.clear()
        self.read_dir_add_to_tree(self.base_folder)
        self.treeview.expandAll()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    filetreeview = FileTreeView(config.work_dir)
    filetreeview.show()
    sys.exit(app.exec_())
