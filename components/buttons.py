from PySide6.QtCore import Signal, QMimeData
from PySide6.QtGui import QCursor, Qt, QIcon, QDrag, QPixmap
from PySide6.QtWidgets import QPushButton, QMenu, QHBoxLayout, QWidget, QApplication


class NestedButton(QPushButton):
    clicked = Signal()

    def __init__(self, icon: QIcon, text: str, parent: QWidget = None):
        super(NestedButton, self).__init__(icon=icon, text=text, parent=parent)

        # super(NestedButtonWidget, self).__init__(*args, **kwargs)
        # self.main_layout = QHBoxLayout(self)  # 设置布局为水平
        # self.main_layout.setSpacing(0)  # 设置间距为0
        # self.main_layout.setContentsMargins(0, 0, 0, 0)  # 设置边距为0

        self.setStyleSheet("text-align: left;")  # 设置文字左对齐
        # self.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键菜单
        # self.customContextMenuRequested.connect(self.showMenu)  # 绑定右键菜单显示函数
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.inner_buttons_layout = QHBoxLayout()  # 设置布局为水平
        self.inner_buttons_layout.addStretch(1)
        self.inner_buttons_layout.setSpacing(0)
        self.inner_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.inner_buttons_layout)

        self.inner_buttons = []  # 内部按钮列表
        # 设置文字靠左
        # self.menu = QMenu(self)

        self.always_show_inner_buttons = True  # 是否显示内部按钮悬停效果

        # 重写 contextMenuEvent 方法来捕获右键点击
        self.drag_start_position = QCursor.pos()  # 鼠标按下时的位置

    def contextMenuEvent(self, event):
        """右键点击事件"""
        if self.actions():
            # print("右键点击事件")
            menu = QMenu(self)

            for action in self.actions():
                menu.addAction(action)

            menu.exec(QCursor.pos())
            event.accept()

    def add_inner_button(self, button):
        """添加内部按钮"""
        button.setParent(self)  # 设置内部按钮的父对象为外部按钮
        self.inner_buttons.append(button)
        self.inner_buttons_layout.addWidget(button)  # 添加内部按钮到布局中
        if not self.always_show_inner_buttons:
            button.hide()  # 隐藏内部按钮

    def enterEvent(self, event):
        """鼠标移动事件"""
        if not self.always_show_inner_buttons:
            for button in self.inner_buttons:
                button.show()
        super(NestedButton, self).enterEvent(event)

    def leaveEvent(self, event):
        """鼠标移出事件"""
        if not self.always_show_inner_buttons:
            for button in self.inner_buttons:
                button.hide()
        super(NestedButton, self).leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        super(NestedButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            drag_distance = (event.pos() - self.drag_start_position).manhattanLength()
            if drag_distance < QApplication.startDragDistance():
                return

            drag = QDrag(self)
            mime_data = QMimeData()

            # 设置拖拽的显示内容
            mime_data.setText(None)
            mime_data.setProperty("object", self)
            drag.setMimeData(mime_data)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.setHotSpot(event.pos())

            # 开始拖拽
            drag.exec(Qt.MoveAction)

        super(NestedButton, self).mouseMoveEvent(event)
