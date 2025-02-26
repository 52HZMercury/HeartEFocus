# import os
import pathlib
import platform

from PySide6.QtWidgets import QWidget

from components.markableimage import MarkableImage

# 获取操作系统名称
os_name = platform.system()

# 获取详细操作系统版本信息
os_version = platform.version()
#
# # 输出操作系统信息
# print(f"当前操作系统: {os_name}")
# print(f"操作系统版本: {os_version}")
# # 如果是mac系统则不加载
# if os_name != 'Darwin':
#     pass
# import vlc
#
# from PySide6.QtCore import QTimer
# from PySide6.QtGui import QPalette, QColor, Qt
# from PySide6.QtWidgets import QWidget, QLabel, QMessageBox, QVBoxLayout, QScrollArea, QFrame, \
#     QSlider, QHBoxLayout, QPushButton, QTabWidget, QCheckBox
#
# import config
# from components.filetreeview import FileTreeView
# from components.layouts import WorkstationLayout, AutoGridWidget
#
#
# class VideoRecordTab(QWidget):
#     def __init__(self):
#
#         super().__init__()
#
#         # self.instance = vlc.Instance()
#         self.instance = vlc.Instance()
#         self.media = None
#         # Create an empty vlc media player
#         self.mediaplayer = self.instance.media_player_new()
#         self.frame_path = None
#         self.is_paused = False
#         self.filetree = FileTreeView(config.videos_dir)
#
#         self.tab_widget = QTabWidget()
#         self.create_video_ui()
#
#     def auto_load(self, file_path):
#         file_path = pathlib.Path(file_path)
#         if file_path.is_dir():
#             print("load dir", file_path)
#             first_file = next((item for item in file_path.iterdir() if item.suffix == ".mp4"), None)
#             self.load_video(first_file)
#             return
#         if file_path.suffix in [".mp4", ".avi", ".mov", ".mkv", ".wmv"]:
#             self.load_video(file_path)
#         else:
#             QMessageBox.warning(self, "警告!!", "不支持的文件类型")
#
#     def load_video(self, video_path):
#         if pathlib.Path(video_path).suffix not in [".mp4", ".avi", ".mov", ".mkv", ".wmv"]:
#             QMessageBox.warning(self, "警告!!", "不支持的文件类型")
#             return
#
#         self.media = self.instance.media_new(video_path)
#         self.mediaplayer.set_media(self.media)
#         self.media.parse()
#
#         self.setWindowTitle(self.media.get_meta(vlc.Meta.Title))
#
#         print(int(self.videoframe.winId()))
#         if os_name == 'Darwin':
#             self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
#         elif os_name == 'Windows':
#             self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
#         elif os_name == 'Linux':
#             self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
#         else:
#             QMessageBox.warning(self, "警告!!", "不支持的操作系统")
#             return
#
#         # self.time_text.setText(str(self.mediaplayer.get_time() / 1000) + "/" + str(self.mediaplayer.get_length() / 1000))
#
#         # keyboard.add_hotkey('space', lambda: self.play_pause(), trigger_on_release=True)
#         self.play_pause()
#         self.setFocus()
#
#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_Space:
#             self.play_pause()
#
#         if event.key() == Qt.Key_S:
#             self.get_frame()
#
#     def create_video_ui(self):
#         main_layout = QVBoxLayout()
#
#         self.videoframe = QFrame()
#         self.palette = self.videoframe.palette()
#         self.palette.setColor(QPalette.Window, QColor(0, 0, 0))
#         self.videoframe.setPalette(self.palette)
#         self.videoframe.setAutoFillBackground(True)
#
#         self.positionslider = QSlider(Qt.Orientation.Horizontal, self)
#         self.positionslider.setToolTip("Position")
#         self.positionslider.setMaximum(1000)
#         self.positionslider.sliderMoved.connect(self.set_position)
#
#         # self.time_text = QLabel()
#
#         self.volumeslider = QSlider(Qt.Orientation.Horizontal, self)
#         self.volumeslider.setMaximum(1000)
#         self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
#         self.volumeslider.setToolTip("Volume")
#         self.volumeslider.valueChanged.connect(self.set_volume)
#
#         self.hbuttonbox = QHBoxLayout()
#         self.stream_checkbox = QCheckBox("是否来源于HDMI信号")
#         self.hbuttonbox.addWidget(self.stream_checkbox)
#
#         # self.previousbutton = QPushButton("上一个")
#         # self.hbuttonbox.addWidget(self.previousbutton)
#         # self.previousbutton.clicked.connect(self.previous_video)
#
#         self.playbutton = QPushButton("播放")
#         self.hbuttonbox.addWidget(self.playbutton)
#         self.playbutton.clicked.connect(self.play_pause)
#
#         # self.nextbutton = QPushButton("下一个")
#         # self.hbuttonbox.addWidget(self.nextbutton)
#         # self.nextbutton.clicked.connect(self.next_video)
#
#         # self.stopbutton = QPushButton("停止")
#         # self.hbuttonbox.addWidget(self.stopbutton)
#         # self.stopbutton.clicked.connect(self.stop)
#         self.hbuttonbox.addStretch(1)
#         self.volumes_text = QLabel("音量")
#         # self.volumes_text.setStyleSheet("QLabel { font-family: 'Arial'; font-size: 8px; font-weight: bold; }")
#         self.hbuttonbox.addWidget(self.volumes_text)
#         self.hbuttonbox.addWidget(self.volumeslider)
#
#         scroll = QScrollArea()
#         layout = AutoGridWidget(item_width=800)
#         layout.add_widget(self.videoframe)
#         layout.add_widget(self.positionslider)
#         # layout.add_widget(self.time_text)
#
#         scroll.setWidget(layout)
#         scroll.setWidgetResizable(True)
#         self.video_layout = QVBoxLayout()
#         self.video_layout.addWidget(scroll)
#
#         main_layout.addLayout(self.video_layout, 1)
#         main_layout.addLayout(self.hbuttonbox, 1)
#         main_layout.addWidget(self.tab_widget, 1)
#         # main_layout.addLayout(self.mark_label)
#
#         # main_layout.setStretchFactor(self.video_layout, 1)
#         # main_layout.setStretchFactor(self.hbuttonbox, 1)
#         # main_layout.setStretchFactor(self.image_view_layout, 1)
#         # main_layout.setStretchFactor(self.mark_label, 1)
#
#         # 设置主布局
#         self.setLayout(main_layout)
#
#         self.timer = QTimer(self)
#         self.timer.setInterval(100)
#         self.timer.timeout.connect(self.update_ui)
#
#         self.volumeslider.setValue(50)
#         self.mediaplayer.audio_set_volume(50)
#
#     def play_pause(self):
#         if self.mediaplayer.is_playing():
#             self.mediaplayer.pause()
#             self.playbutton.setText("播放")
#             self.is_paused = True
#             self.timer.stop()
#         else:
#             self.mediaplayer.play()
#             self.playbutton.setText("暂停")
#             self.timer.start()
#             self.is_paused = False
#
#     def stop(self):
#         self.mediaplayer.stop()
#         self.playbutton.setText("播放")
#
#     def set_volume(self, volume):
#         self.mediaplayer.audio_set_volume(volume)
#
#     def set_position(self, position):
#         pos = position / 1000.0
#         self.mediaplayer.set_position(pos)
#
#     def update_ui(self):
#         media_pos = int(self.mediaplayer.get_position() * 1000)
#         self.positionslider.setValue(media_pos)
#
#         if not self.mediaplayer.is_playing():
#             self.timer.stop()
#             if not self.is_paused:
#                 self.stop()
#
#     def get_frame(self):
#         self.current_time = self.mediaplayer.get_time() / 1000.0  # 转换为秒
#         print(f"获取图片帧，时间 {self.current_time} 秒")
#         # self.frame_path = self.get_frame(self.mediaplayer, self.current_time)
#
#         os.makedirs("resources/frames", exist_ok=True)
#         snapshot_path = f"resources/frames/frame_{self.current_time}.png"
#         self.mediaplayer.video_take_snapshot(0, snapshot_path, 0, 0)
#
#         time_format = f"{int(self.current_time // 60):02d}: {int(self.current_time % 60):02d}"
#         image_view = MarkableImage()
#         image_view.load_image(snapshot_path)
#         self.tab_widget.addTab(image_view, time_format)
#         self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
#         # return snapshot_path
#
#
class ShishiZhiNengJiancePage(QWidget):
    def __init__(self):
        super().__init__()
        # if os_name == 'Darwin':
        #     QMessageBox.warning(self, "警告!!", "暂不支持Mac系统")
        #     return

        # self.layout = WorkstationLayout()
        # self.setLayout(self.layout)
        #
        # self.video_view = VideoRecordTab()
        # self.filetree = FileTreeView(config.videos_dir)

        self.filetree.item_double_clicked.connect(self.video_view.load_video)

        self.layout.get_mid_left_layout().addWidget(self.filetree)
        self.layout.get_center_layout().addWidget(self.video_view)

#
# def main():
#     import sys
#     from PySide6.QtWidgets import QApplication
#
#     app = QApplication(sys.argv)
#     window = ShishiZhiNengJiancePage()
#     window.show()
#     sys.exit(app.exec())
#
#
# if __name__ == "__main__":
#     main()
#     # pass
