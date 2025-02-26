from typing import Union

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, Qt, QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QBoxLayout, QLabel, QFileIconProvider, \
    QScrollArea

from components.buttons import NestedButton


class TabView(QWidget):
    tab_added = Signal(int)
    tab_changed = Signal(int)
    tab_closed = Signal(int, QWidget)
    # tabs_closed = Signal(list)
    tab_moved = Signal(int, int)

    def __init__(self, widgets_layout: Union[bool, QBoxLayout] = True, parent=None):
        """
        Create a tab view with a horizontal layout for the buttons and a vertical layout for the widgets.
        :param widgets_layout: If True, create a new QHBoxLayout for the buttons. If a QBoxLayout is provided, use it. If False, don't create a buttons layout.
        :param parent: The parent widget.
        """
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)

        self.buttons = []
        self.widgets = []
        self.closeable_tabs = []

        self.current_index = 0

        self.buttons_layout = QHBoxLayout()

        # 设置向左对齐
        self.buttons_layout.setAlignment(Qt.AlignLeft)
        self.widgets_layout = QHBoxLayout()

        if isinstance(widgets_layout, QBoxLayout):
            # widget = QWidget()
            # widget.setAcceptDrops(True)
            # widget.dropEvent = lambda event: print("dropEvent")
            # widget.setLayout(self.buttons_layout)
            # buttons_layout.addWidget(widget)
            self.widgets_layout = widgets_layout
        elif widgets_layout is False:
            self.widgets_layout = QHBoxLayout()
        else:
            self.widgets_layout = QHBoxLayout()
            self.main_layout.addLayout(self.widgets_layout)

        # self.main_layout.addLayout(self.buttons_layout)

        # 创建一个 QWidget 来包含布局
        self.buttons_widget = QWidget()
        self.buttons_widget.setLayout(self.buttons_layout)

        # 创建 QScrollArea 并设置按钮部件
        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(True)  # 允许根据内容自动调整
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.buttons_widget)

        self.main_layout.addWidget(self.scroll_area)
        # self.main_layout.setContentsMargins(0, 0, 0, 0)
        # self.setLayout(self.main_layout)

        self.setAcceptDrops(True)
        self.clear_margins()

    def get_widget(self, index):
        return self.widgets[index]

    def get_current_widget(self):
        return self.widgets[self.current_index]

    def dropEvent(self, event):
        print("dropEvent")
        mime_data = event.mimeData()
        # Check if the dragged data contains text
        if mime_data.property("object"):
            dragging_button = mime_data.property("object")
            print(f"Currently dragging: {dragging_button}")
        else:
            event.ignore()
            return

        dragging_button_index = self.buttons.index(dragging_button)
        move_to_index = dragging_button_index

        pos = event.pos()
        # pos在哪两个按钮之间
        first_button = self.buttons[0]
        first_button_pos = first_button.pos()
        if pos.x() < first_button_pos.x() + first_button.width() / 2:
            print("move to", 0)
            move_to_index = 0

        last_button = self.buttons[-1]
        last_button_pos = last_button.pos()
        if pos.x() > last_button_pos.x() + last_button.width() / 2:
            print("move to", len(self.buttons) - 1)
            move_to_index = len(self.buttons) - 1

        for i in range(1, len(self.buttons)):
            button1 = self.buttons[i - 1]
            button2 = self.buttons[i]

            if pos.x() > button1.pos().x() + button1.width() / 2 and pos.x() < button2.pos().x() + button2.width() / 2:
                if dragging_button_index == i:
                    # print("move to", i - 1)
                    pass
                elif dragging_button_index < i:
                    print("move to", i - 1)
                    move_to_index = i - 1
                else:
                    print("move to", i)
                    move_to_index = i
                    break

        if move_to_index != dragging_button_index:
            # self.buttons[dragging_button_index].setDefault(True)
            self.move_tab(dragging_button_index, move_to_index)
            # self.change_tab(move_to_index)
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        # print("dragEnterEvent")
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        event.accept()

    def get_button_index(self, button):
        return self.buttons.index(button)

    def create_button(self, text, closeable, icon=None):
        button_width = 40
        for t in text:
            if ord(t) > 127:
                button_width += 20
            else:
                button_width += 10

        if icon is None:
            icon = QFileIconProvider().icon(QFileIconProvider.File)
        button = NestedButton(icon=icon, text=text, parent=self)
        button.setFixedWidth(button_width)
        button.clicked.connect(lambda: self.change_tab(self.get_button_index(button)))
        if closeable:
            close_button = QPushButton(icon=QIcon("resources/close.svg"), text="", parent=self)
            close_button.setFixedSize(25, 25)
            close_button.setStyleSheet("border: none;")
            button.add_inner_button(close_button)
            close_button.clicked.connect(lambda: self.remove_tab(self.get_button_index(button)))

            close_action = QAction("Close", self)
            close_action.triggered.connect(lambda: self.close_tab(self.get_button_index(button)))
            button.addAction(close_action)

        close_left_action = QAction("Close Tabs to the Left", self)
        close_left_action.triggered.connect(lambda: self.close_tabs_at_left(self.get_button_index(button)))
        button.addAction(close_left_action)

        close_right_action = QAction("Close Tabs to the Right", self)
        close_right_action.triggered.connect(lambda: self.close_tabs_at_right(self.get_button_index(button)))
        button.addAction(close_right_action)

        return button

    def add_tab(self, text, widget, closeable=True, icon=None):
        return self.insert_tab(text, widget, -1, closeable, icon=icon)

    def insert_tab(self, text, widget, index=-1, closeable=True, icon=None):
        if index < 0 or index > len(self.buttons):
            index = len(self.buttons)

        button = self.create_button(text, closeable, icon)

        self.buttons_layout.addWidget(button)
        self.buttons.insert(index, button)

        self.widgets_layout.addWidget(widget)
        self.widgets.insert(index, widget)

        self.closeable_tabs.insert(index, closeable)

        self.tab_added.emit(index)
        self.change_tab(index)
        return index

    def remove_tab(self, index, change_tab_immediately=True):
        self.buttons[index].deleteLater()
        self.widgets[index].deleteLater()
        self.buttons.pop(index)
        self.widgets.pop(index)
        self.closeable_tabs.pop(index)
        self.buttons_layout.removeItem(self.buttons_layout.itemAt(index))
        self.widgets_layout.removeItem(self.widgets_layout.itemAt(index))
        self.update()

        if index <= self.current_index:
            if change_tab_immediately:
                self.change_tab(self.current_index - 1)
            else:
                self.current_index -= 1

    def close_tab(self, index, change_tab_immediately=True):
        print(f"close_tab {index}", self.closeable_tabs)
        if self.closeable_tabs[index]:
            old_widget = self.widgets[index]
            self.remove_tab(index, change_tab_immediately)
            self.tab_closed.emit(index, old_widget)

    def close_tabs(self, indices):
        indices = sorted(indices, reverse=True)
        for index in indices:
            self.close_tab(index, change_tab_immediately=False)
        self.change_tab(self.current_index)

    def close_all_tabs(self):
        self.close_tabs(range(len(self.buttons)))

    def close_tabs_at_left(self, index):
        # 关闭左侧所有标签页，并切换到当前标签页
        self.close_tabs(range(index))

    def close_tabs_at_right(self, index):
        # 关闭右侧所有标签页，并切换到当前标签页
        self.close_tabs(range(index + 1, len(self.buttons)))

    def change_tab(self, index):
        if index >= len(self.buttons):
            index = len(self.buttons) - 1
        if index < 0:
            index = 0

        if index >= len(self.buttons):
            return

        for i in range(len(self.buttons)):
            self.buttons[i].setDefault(False)
            self.widgets[i].setVisible(False)

        self.buttons[index].setDefault(True)
        self.widgets[index].setVisible(True)
        self.buttons[index].setFocus()

        self.current_index = index

        self.tab_changed.emit(self.current_index)

    def move_tab(self, index, new_index):
        if new_index < 0 or new_index >= len(self.buttons):
            return

        button = self.buttons.pop(index)
        widget = self.widgets.pop(index)
        closeable = self.closeable_tabs.pop(index)

        self.buttons.insert(new_index, button)
        self.widgets.insert(new_index, widget)
        self.closeable_tabs.insert(new_index, closeable)

        self.buttons_layout.insertWidget(new_index, button)
        self.widgets_layout.insertWidget(new_index, widget)

        self.update()
        if index > self.current_index >= new_index:
            self.current_index += 1
        elif index < self.current_index <= new_index:
            self.current_index -= 1

        print(f"move_tab {index} to {new_index} done, current_index:", self.current_index)
        self.tab_moved.emit(index, new_index)

    def clear_margins(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(5)
        self.widgets_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication, QTextEdit

    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)

    tab_view = TabView(layout)

    text_edit1 = QTextEdit()
    text_edit2 = QTextEdit()
    text_edit3 = QTextEdit()

    tab_view.add_tab("Text 1", text_edit1)
    tab_view.add_tab("Text 2", text_edit2)
    tab_view.add_tab("Text 3", text_edit3)

    window.setLayout(layout)

    layout2 = QHBoxLayout()
    layout2.addWidget(QLabel("Text 4"))
    layout2.addWidget(QLabel("Text 5"))
    layout2.addWidget(QLabel("Text 6"))
    layout.addLayout(layout2)

    tab_view.change_tab(0)
    layout.addWidget(tab_view)
    window.show()

    sys.exit(app.exec())
