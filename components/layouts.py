from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QSplitter, QWidget, QGridLayout


class WorkstationLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.top_layout = QHBoxLayout()
        self.mid_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.addLayout(self.top_layout)
        self.addLayout(self.mid_layout, 1)

        self.addLayout(self.bottom_layout)

        self.splitter = QSplitter()
        self.mid_left_widget = QWidget()
        self.mid_left_layout = QVBoxLayout()
        self.mid_left_widget.setLayout(self.mid_left_layout)

        self.center_widget = QWidget()
        self.center_layout = QVBoxLayout()
        self.center_widget.setLayout(self.center_layout)

        self.mid_right_widget = QWidget()
        self.mid_right_layout = QVBoxLayout()
        self.mid_right_widget.setLayout(self.mid_right_layout)

        self.splitter.addWidget(self.mid_left_widget)
        self.splitter.addWidget(self.center_widget)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 1)
        self.splitter.addWidget(self.mid_right_widget)
        self.mid_layout.addWidget(self.splitter)

        self.clear_margins()

    def get_top_layout(self):
        return self.top_layout

    def get_mid_left_layout(self):
        return self.mid_left_layout

    def get_center_layout(self):
        return self.center_layout

    def get_mid_right_layout(self):
        return self.mid_right_layout

    def get_bottom_layout(self):
        return self.bottom_layout

    def clear_margins(self):
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.mid_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.mid_left_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.mid_right_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)


class AutoGridWidget(QWidget):
    def __init__(self, parent=None, item_width=400):
        super(AutoGridWidget, self).__init__(parent=parent)
        self.item_width = item_width

        self.widgets = []
        # 排列按钮，随着窗口大小变化而改变行列元素的数量
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.clear_margins()

    def resizeEvent(self, event):
        super(AutoGridWidget, self).resizeEvent(event)
        # 重新排列按钮，使其在窗口大小变化时，按钮的位置也随之变化
        columns = (self.width() // self.item_width) + 1
        rows = len(self.widgets) // columns + 1

        for i in range(len(self.widgets)):
            row = i // columns
            column = i % columns
            self.layout.addWidget(self.widgets[i], row, column)

    def add_widget(self, widget):
        self.widgets.append(widget)
        self.layout.addWidget(widget)

    def clear_margins(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)


class SandwichLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super(SandwichLayout, self).__init__(parent=parent)
        self.top_layout = QHBoxLayout()
        self.mid_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.addLayout(self.top_layout)
        self.addLayout(self.mid_layout, 1)
        self.addLayout(self.bottom_layout)
        self.clear_margins()

    def get_top_layout(self):
        return self.top_layout

    def get_mid_layout(self):
        return self.mid_layout

    def get_bottom_layout(self):
        return self.bottom_layout

    def clear_margins(self):
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.mid_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
