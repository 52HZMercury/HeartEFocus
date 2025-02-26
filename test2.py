from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QFont

# 创建应用程序
app = QApplication([])

# 设置全局字体
font = QFont("Arial", 40)  # 设置字体为 Arial，字号为 12
app.setFont(font)

# 创建一个窗口和标签
window = QWidget()
layout = QVBoxLayout()

label1 = QLabel("This is a label with the global font.")
label2 = QLabel("Another label with the same global font.")

layout.addWidget(label1)
layout.addWidget(label2)
window.setLayout(layout)

# 显示窗口
window.show()

# 启动应用程序事件循环
app.exec()