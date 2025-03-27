import os
import random

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QScrollArea, \
    QLabel, QSizePolicy

import config

work_dir = config.work_dir
yisheng_path = "resources/xiaoxizhongxin_page_images/yisheng.png"
huanzhe_path = "resources/xiaoxizhongxin_page_images/huanzhe1.png"
# 设置默认头像路径
default_avatar_path = "resources/xiaoxizhongxin_page_images/touxiang.png"


def is_image_file(file_path):
    # 定义支持的图像扩展名
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}

    # 检查文件是否存在
    if not os.path.exists(file_path):
        return False

    # 获取文件扩展名并判断
    file_extension = os.path.splitext(file_path)[1].lower()
    return file_extension in image_extensions


def list_folders(directory):
    try:
        # 获取指定目录中的所有文件和文件夹
        items = os.listdir(directory)

        # 过滤出文件夹
        folders = [item for item in items if os.path.isdir(os.path.join(directory, item)) and item != '_']

        return folders
    except Exception as e:
        print(f"错误：{e}")
        return []


# 用法示例
folders = list_folders(work_dir)  # 文件夹名称存储在这个变量中
# 创建一个字典来存储文件夹名称
patient_dict = {f"patient{1}": "name"}
# 将文件夹名称存储到字典中
for j, folder in enumerate(folders, start=1):
    patient_dict[f"patient{j}"] = folder

# 创建一个字典来存储头像路径
patient_avatars = {f"patient{1}": ""}
# 根据文件名生成图像路径
file_name = '患者照片'
for j, folder in enumerate(folders, start=1):
    for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
        img_path = os.path.join(work_dir, folder, f"{file_name}{ext}")
        if is_image_file(img_path):
            patient_avatars[f"patient{j}"] = img_path
            break
        else:
            patient_avatars[f"patient{j}"] = default_avatar_path


class MessageWidget(QWidget):
    def __init__(self, sender, content, is_self=False, is_image_sender=False):
        super().__init__()
        layout = QHBoxLayout()

        # 发送者图片或名称
        if is_image_sender:
            sender_pixmap = QPixmap(sender)
            scaled_sender = sender_pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            sender_label = QLabel()
            sender_label.setPixmap(scaled_sender)
        else:
            sender_label = QLabel(sender)
            sender_label.setStyleSheet("""
                                font-size: 14px;
                                font-weight: bold;
                            """)

        # 消息内容
        content_label = QLabel(content)
        content_label.setStyleSheet("""
                                        font-size: 14px;
                                        font-weight: bold;
                                    """)
        content_label.setWordWrap(True)
        # content_label.setStyleSheet(
        #     "background-color: #DCF8C6; border-radius: 10px; padding: 10px; margin: 5px;"
        #     if is_self else
        #     "background-color: white; border-radius: 10px; padding: 10px; margin: 5px;"
        # )
        content_label.setStyleSheet(
            "border: 1px solid #cccccc; border-radius: 10px; padding: 10px; margin: 5px;"
            if is_self else
            "border: 1px solid #cccccc;border-radius: 10px; padding: 10px; margin: 5px;"
        )

        content_label.setMaximumWidth(300)
        content_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sender_label.setFixedSize(36, 36)  # 设置固定大小以保持比例
        formatted_content = "<p style='margin: 0;'>" + content.replace("\n", "<br>") + "</p>"
        content_label.setText(formatted_content)

        if is_self:
            layout.addWidget(content_label)
            layout.addWidget(sender_label)
            layout.setAlignment(Qt.AlignRight)
        else:
            layout.addWidget(sender_label)
            layout.addWidget(content_label)
            layout.setAlignment(Qt.AlignLeft)

        self.setLayout(layout)


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("聊天窗口")
        self.setGeometry(100, 100, 800, 600)

        # 使用QHBoxLayout
        main_layout = QHBoxLayout(self)

        # 固定宽度的左侧通知栏
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        self.notification_area = QScrollArea()
        self.notification_area.setWidgetResizable(True)
        notification_widget = QWidget()
        self.notification_layout = QVBoxLayout(notification_widget)
        self.notification_layout.setAlignment(Qt.AlignTop)  # 确保从顶部开始排列
        self.notification_area.setWidget(notification_widget)
        left_layout.addWidget(self.notification_area)
        left_widget.setLayout(left_layout)

        # 设置左侧宽度为固定值
        left_widget.setFixedWidth(310)  # 固定列宽

        main_layout.addWidget(left_widget)

        # 右侧聊天区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.recipient_label = QLabel(patient_dict[f"patient{1}"])
        # self.recipient_label.setStyleSheet("""
        #                         font-size: 14px;
        #                         font-weight: bold;
        #                     """)

        right_layout.addWidget(self.recipient_label)
        self.message_area = QScrollArea()
        self.message_area.setWidgetResizable(True)
        message_widget = QWidget()
        self.message_layout = QVBoxLayout(message_widget)
        self.message_layout.setAlignment(Qt.AlignTop)
        self.message_area.setWidget(message_widget)

        self.input_area = QTextEdit()
        self.input_area.setFixedHeight(60)
        # self.input_area.setStyleSheet("""
        #     border: 1px solid #cccccc;
        #     border-radius: 5px;
        # """)

        self.send_button = QPushButton('发送')
        self.send_button.setMinimumWidth(100)
        # self.send_button.setStyleSheet("""
        #     background-color: #4CAF50;
        #     color: white;
        #     padding: 5px 15px;
        #     border: none;
        #     border-radius: 3px;
        # """)
        self.send_button.clicked.connect(self.send_message)

        right_layout.addWidget(self.message_area)
        right_layout.addWidget(self.input_area)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.send_button)
        right_layout.addLayout(button_layout)

        main_layout.addWidget(right_widget)

        # 添加一些示例消息
        # self.add_message(yisheng_path,
        #                  "您好，您最近的情况如何？",
        #                  True, is_image_sender=True)
        # self.add_message(huanzhe_path, "您好，医生。我这段时间有点焦虑，心里总是想着检查结果。",
        #                  False, is_image_sender=True)
        # self.add_message(yisheng_path,
        #                  "我理解您的担忧。您这段时间有没有感到任何新的症状，比如胸部不适、肿块或者其他变化？",
        #                  True, is_image_sender=True)
        # self.add_message(huanzhe_path,
        #                  "大约有两周了，开始的时候没什么感觉，但现在摸起来有点疼。",
        #                  False, is_image_sender=True)
        # self.add_message(yisheng_path,
        #                  "我明白了。乳腺的肿块有很多可能的原因，有些是良性的，有些可能需要进一步检查。接下来，我们会做一个体检，并安排乳房超声检查，必要时可能还需要做乳腺X光检查。",
        #                  True, is_image_sender=True)
        # self.add_message(huanzhe_path,
        #                  "谢谢医生。检查过程有需要注意的事项吗？",
        #                  False, is_image_sender=True)
        # self.add_message(yisheng_path,
        #                  "在等待检查结果的期间，注意保持心情舒畅，避免过度焦虑。如果有任何不适，请随时联系我。",
        #                  True, is_image_sender=True)

        # 初始化通知
        self.buttons_list = []
        self.initialize_notifications()

    def add_notification_button(self, sender, message_time, content, patient_id):
        button = QPushButton()
        button.setFixedHeight(100)
        # button.setcollapsed(True)
        # button.setFixedWidth(300)
        button.setStyleSheet("""
            background-color: none;
            """)

        layout = QHBoxLayout()  # 使用水平布局
        # layout.setContentsMargins(0, 0, 0, 0)

        # 添加患者头像，使用字典中的头像路径
        avatar_label = QLabel()
        pixmap = QPixmap(patient_avatars[patient_id]).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        avatar_label.setPixmap(pixmap)
        layout.addWidget(avatar_label)

        # 右侧信息布局
        info_layout = QVBoxLayout()

        # 使用水平布局对齐发送者和时间
        top_layout = QHBoxLayout()

        # 发送者名称
        sender_label = QLabel(sender)
        # sender_label.setStyleSheet("font-weight: bold; font-size: 12px; ")
        top_layout.addWidget(sender_label)

        # 添加伸缩项，把时间推到右侧
        top_layout.addStretch()
        # 时间标签
        time_label = QLabel(message_time)
        time_label.setAlignment(Qt.AlignRight)  # 右对齐时间
        # time_label.setStyleSheet("font-size: 10px;")
        top_layout.addWidget(time_label)

        info_layout.addLayout(top_layout)

        # 消息内容
        button.content_label = QLabel(content)
        button.content_label.setWordWrap(True)
        # content_label.setStyleSheet("font-size: 12px;")
        info_layout.addWidget(button.content_label)

        layout.addLayout(info_layout)
        button.setLayout(layout)
        button.clicked.connect(lambda: self.load_chat_history(patient_id, button))
        button.adjustSize()
        self.notification_layout.addWidget(button)
        # self.notification_layout.setSpacing(0)
        self.buttons_list.append(button)

    def load_chat_history(self, patient_id, button):
        self.current_button = button
        self.current_patient_id = patient_id
        # 清空现有消息
        for i in reversed(range(self.message_layout.count())):
            self.message_layout.itemAt(i).widget().setParent(None)
        # 根据 patient_id 加载相应的聊天记录，和头像
        if patient_id in patient_avatars:
            # 使用 patients 头像
            patient_image = patient_avatars[patient_id]
            patient_name = patient_dict[patient_id]
            # if not is_image_file(patient_image):
            #     patient_image = default_avatar_path

            # 根据patient_id加载相应的聊天记录
            if patient_id == "patient1":
                self.add_message(yisheng_path,
                                 "您好，您最近的情况如何？",
                                 True, is_image_sender=True)
                self.add_message(patient_image, "您好，医生。我这段时间有点焦虑，心里总是想着检查结果。",
                                 False, is_image_sender=True)
                self.recipient_label.setText(patient_name)

            if patient_id == "patient2":
                self.add_message(yisheng_path,
                                 "您好，最近感觉如何？",
                                 True, is_image_sender=True)
                self.add_message(patient_image, "医生您好,我最近感觉还不错，但有点担心之前的检查结果。",
                                 False, is_image_sender=True)
                self.add_message(yisheng_path,
                                 "我理解您的担忧。您这段时间有没有感到任何新的症状，比如胸部不适、肿块或者其他变化？",
                                 True, is_image_sender=True)
                self.recipient_label.setText(patient_name)
            if patient_id == "patient3":
                self.add_message(yisheng_path,
                                 "您好，感谢您今天来复诊。您最近的情况怎么样？",
                                 True, is_image_sender=True)
                self.add_message(patient_image, "您好，医生。虽然这段时间病情没有加重，但心里总是很担心检查结果。",
                                 False, is_image_sender=True)
                self.add_message(yisheng_path,
                                 "我理解您的感受，等待结果的过程确实很不容易。我们会通过进一步的检查来确认情况。",
                                 True, is_image_sender=True)
                self.recipient_label.setText(patient_name)
            if patient_id == "patient4":
                self.add_message(yisheng_path, "您好，最近感觉怎么样？", True, is_image_sender=True)
                self.add_message(patient_image, "医生，上次检查结果出来了，如果真的是癌症，我该怎么做？", False,
                                 is_image_sender=True)
                self.add_message(yisheng_path,
                                 "如果确诊为乳腺癌，我们会有多种治疗选择，包括手术、化疗和放疗。治疗方案会根据癌症的分期以及你的整体健康状况来制定。我们会和你一起制定一个适合你的治疗计划。",
                                 True, is_image_sender=True)
                self.recipient_label.setText(patient_name)
            if patient_id == "patient5":
                self.add_message(yisheng_path, "您好，今天来复诊感觉怎么样？", True, is_image_sender=True)
                self.add_message(patient_image, "你好，医生。我想了解一下我的检查结果。", False, is_image_sender=True)
                self.add_message(yisheng_path,
                                 "根据我们最近的检查结果，我们发现你有一个乳腺肿块。我们需要进一步确认它的性质。", True,
                                 is_image_sender=True)
                self.recipient_label.setText(patient_name)
            if patient_id == "patient6":
                self.add_message(yisheng_path, "您好，最近感觉如何？", True, is_image_sender=True)
                self.add_message(patient_image, "我很担心治疗的副作用，听说化疗可能会很痛苦。", False,
                                 is_image_sender=True)
                self.add_message(yisheng_path,
                                 "化疗确实有可能会有一些副作用，如恶心、疲劳和脱发，但并不是每个人都会经历所有这些。有些患者的反应较轻，我们会努力根据你的情况来调整治疗方案，尽量减少副作用。",
                                 True, is_image_sender=True)
                self.recipient_label.setText(patient_name)
            if patient_id == "patient7":
                self.add_message(yisheng_path, "您好，请问有什么问题吗？", True, is_image_sender=True)
                self.add_message(patient_image, "我担心我的家人接受不了这个消息。", False, is_image_sender=True)
                self.add_message(yisheng_path,
                                 "你的家人会感到担心和不安是很正常的。他们可能需要时间来消化这个消息。我们可以提供一些支持资源，比如心理咨询，帮助他们更好地应对。",
                                 True, is_image_sender=True)
                self.recipient_label.setText(patient_name)
        if patient_id == "patient8":
            self.add_message(yisheng_path, "您好,最近有什么不适吗?", True, is_image_sender=True)
            self.add_message(huanzhe_path, "医生,我最近总是感觉头晕", False, is_image_sender=True)
            self.add_message(yisheng_path, "头晕是什么症状？", True, is_image_sender=True)
            self.recipient_label.setText(patient_name)
        if patient_id == "patient9":
            self.add_message(yisheng_path, "近期有没有出现什么不舒服的地方？", True, is_image_sender=True)
            self.add_message(huanzhe_path, "医生,我最近感觉恶心", False, is_image_sender=True)
            self.add_message(yisheng_path, "有没有其它伴随症状？", True, is_image_sender=True)
            self.add_message(huanzhe_path, "感觉还有点发热", False, is_image_sender=True)




    def initialize_notifications(self):
        num = len(patient_dict)
        for i in range(1, num + 1):
            patient_name = patient_dict[f"patient{i}"]
            if i == 1:
                self.add_notification_button(patient_name, "刚刚", "您好，医生。我这段时间有点焦虑，心", "patient1")
            if i == 2:
                self.add_notification_button(patient_name, "16:00", "我理解您的担忧。您这段时间有没有", "patient2")
            if i == 3:
                self.add_notification_button(patient_name, "15:57", "乳腺的肿块有很多可能的原因，有些是良性的，有",
                                             "patient3")
            if i == 4:
                self.add_notification_button(patient_name, "15:08", "如果确诊为乳腺癌，我们会有", "patient4")
            if i == 5:
                self.add_notification_button(patient_name, "14:00", "根据我们最近的检查结果，我们", "patient5")
            if i == 6:
                self.add_notification_button(patient_name, "13:30", "化疗确实有可能会有一些副作用", "patient6")
            if i == 7:
                self.add_notification_button(patient_name, "12:00", "你的家人会感到担心和不安是很正常的。", "patient7")

        # 可以继续添加更多通知

    def notification_clicked(self, content, messages):
        # 清空现有消息
        for i in reversed(range(self.message_layout.count())):
            self.message_layout.itemAt(i).widget().setParent(None)

        # 添加预设消息
        for sender_image, message_content, is_self in messages:
            self.add_message(sender_image, message_content, is_self, is_image_sender=True)

        print(f"Notification clicked: {content}")

    def add_message(self, sender_image, content, is_self, is_image_sender=False):
        message = MessageWidget(sender_image, content, is_self, is_image_sender)
        self.message_layout.addWidget(message)

        # 滚动到最新消息
        self.message_area.verticalScrollBar().setValue(
            self.message_area.verticalScrollBar().maximum()
        )

    def send_message(self):
        content = self.input_area.toPlainText().strip()
        if content:
            # 发送用户消息
            self.add_message(yisheng_path, content, True, is_image_sender=True)
            self.input_area.clear()
            self.current_button.content_label.setText(content)

            # 创建一个定时器
            reply_timer = QTimer(self)
            reply_timer.setSingleShot(True)
            reply_timer.timeout.connect(lambda: self.reply_to_message())
            reply_timer.start(2000)  # 5000 毫秒 = 5 秒

    def reply_to_message(self):
        # 模拟接收方回复
        patient_image = patient_avatars[self.current_patient_id]
        reply_content = random.choice(["好的，谢谢医生", "好的。", "医生，我会尽快来医院就诊。", "麻烦您了！"])
        self.add_message(patient_image, reply_content, False, is_image_sender=True)
        self.current_button.content_label.setText(reply_content)

        # 滚动到最新消息
        self.message_area.verticalScrollBar().setValue(
            self.message_area.verticalScrollBar().maximum()
        )


if __name__ == "__main__":
    app = QApplication([])
    window = ChatWindow()
    window.show()
    app.exec()
