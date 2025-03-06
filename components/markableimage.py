import sys

from PySide6.QtCore import Qt, QPoint, QLineF
from PySide6.QtGui import QPen, QColor, QPainter, QPixmap, QMouseEvent
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMainWindow, QGraphicsPixmapItem, \
    QGraphicsEllipseItem


class MarkableImage(QGraphicsView):
    def __init__(self, image_path='/Users/xiangyang/PycharmProjects/medai/resources/01737_0.jpg', parent=None):
        super(MarkableImage, self).__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setSceneRect(0, 0, 800, 1200)  # 设置场景大小
        self.setRenderHint(QPainter.Antialiasing)
        self.lastPos = QPoint()  # 记录上一个点的位置
        self.pen = QPen(QColor(240, 190, 80), 2, Qt.SolidLine)  # 调整画笔宽度
        self.circles = []  # 存储圆圈的列表
        self.lines = []  # 存储线的列表
        self.selected_circle = None  # 选中的圆圈

        self.load_image(image_path)
        self.drawing = True
        self.dragging = False

    def clear_image(self):
        # 清空场景中的所有内容
        self.scene().clear()
        # 重置图片项为 None
        self.pixmap_item = None
        # 清空标记点和线条列表
        self.circles.clear()
        self.lines.clear()
        self.selected_circle = None

    def load_image(self, image_path):
        # 加载并显示一张图片
        pixmap = QPixmap(image_path)  # 创建一个QPixmap对象
        self.pixmap_item = QGraphicsPixmapItem(pixmap)  # 用图片创建QGraphicsPixmapItem
        self.pixmap_item.setPos(0, 0)  # 设置图片的位置
        self.scene().addItem(self.pixmap_item)  # 将图片项添加到场景中
        self.update_image()

    def update_image(self):
        self.setSceneRect(self.pixmap_item.boundingRect())  # 适应场景大小
        self.fitInView(self.pixmap_item, Qt.KeepAspectRatio)  # 确保图片适应视图

    def resizeEvent(self, event):
        # 重写resizeEvent方法，使场景的大小随着视图的大小变化而变化
        self.update_image()
        super(MarkableImage, self).resizeEvent(event)

    def select_one_circle(self, circle):
        # 选中一个圆圈
        for c in self.circles:
            c.setBrush(QColor(240, 190, 80, 120))
            c.setPen(QPen(QColor(240, 190, 80), 1, Qt.SolidLine))  # 调整画笔宽度
        circle.setBrush(QColor(190, 80, 80, 200))
        circle.setPen(QPen(QColor(190, 80, 80), 1, Qt.SolidLine))  # 调整画笔宽度
        self.selected_circle = circle

    def clear_selected_circle(self):
        # 清除选中的圆圈
        if self.selected_circle:
            self.selected_circle.setBrush(QColor(240, 190, 80, 120))
            self.selected_circle.setPen(QPen(QColor(240, 190, 80), 1, Qt.SolidLine))  # 调整画笔宽度
            self.selected_circle = None

    def mousePressEvent(self, event: QMouseEvent):
        mouse_in_scene = self.mapToScene(event.pos())

        if not self.drawing:
            for circle in self.circles:
                # 判断圆圈是否在鼠标点击位置的10px范围内
                circle_pos = circle.pos() + QPoint(2.5, 2.5)  # 调整偏移量
                if (mouse_in_scene - circle_pos).manhattanLength() < 5:  # 调整范围
                    self.select_one_circle(circle)
                    self.dragging = True
                    break
            return

        # 如果在圆圈范围，则选中该圆圈
        for circle in self.circles:
            # 判断圆圈是否在鼠标点击位置的10px范围内
            circle_pos = circle.pos() + QPoint(2.5, 2.5)  # 调整偏移量
            if (mouse_in_scene - circle_pos).manhattanLength() < 5:  # 调整范围
                self.select_one_circle(circle)
                break
        else:
            self.clear_selected_circle()
            # if event.button() == Qt.LeftButton:
            # 创建一个新的圆圈标记
            circle = QGraphicsEllipseItem(0, 0, 5, 5)  # 调整大小
            # 设置圆圈的颜色和透明度
            circle.setBrush(QColor(240, 190, 80, 120))
            circle.setPen(QPen(QColor(240, 190, 80), 1, Qt.SolidLine))  # 调整画笔宽度

            mouse_in_scene = self.mapToScene(event.pos())
            circle.setPos(mouse_in_scene - QPoint(2.5, 2.5))  # 调整偏移量
            self.scene().addItem(circle)
            self.select_one_circle(circle)
            self.circles.append(circle)
            if len(self.circles) > 1:
                # 画线连接上一个圆圈和当前圆圈
                line = self.draw_line(self.circles[-2].pos() + QPoint(2.5, 2.5), mouse_in_scene)
                self.lines.append(line)

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.drawing:
            if self.dragging:
                if self.selected_circle:
                    mouse_in_scene = self.mapToScene(event.pos())
                    self.selected_circle.setPos(mouse_in_scene - QPoint(2.5, 2.5))  # 调整偏移量
                    self.clear_lines()
                    for i, circle in enumerate(self.circles):
                        if i == 0:
                            continue
                        line = self.draw_line(self.circles[i - 1].pos() + QPoint(2.5, 2.5), circle.pos() + QPoint(2.5, 2.5))
                        self.lines.append(line)
                    line = self.draw_line(self.circles[-1].pos() + QPoint(2.5, 2.5), self.circles[0].pos() + QPoint(2.5, 2.5))
                    self.lines.append(line)
            return

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.dragging:
            self.dragging = False
            self.clear_selected_circle()
            print('dragging release')
            for circle in self.circles:
                print(circle.pos())

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if not self.drawing:
            return

        mouse_in_scene = self.mapToScene(event.pos())

        if event.button() == Qt.LeftButton:
            if len(self.circles) > 2:
                # 画线连接最后一个圆圈和双击的位置
                line = self.draw_line(self.circles[-1].pos() + QPoint(2.5, 2.5), mouse_in_scene)
                self.lines.append(line)
                # 画线连接双击的位置和第一个圆圈
                line = self.draw_line(mouse_in_scene, self.circles[0].pos() + QPoint(2.5, 2.5), )
                self.lines.append(line)

                self.drawing = False

    def draw_line(self, start, end):
        # 画线的方法
        line = QLineF(start, end)
        line_item = self.scene().addLine(line, self.pen)
        return line_item

    def clear_lines(self):
        for line in self.lines:
            self.scene().removeItem(line)
        self.lines.clear()

    def clear_circles(self):
        for circle in self.circles:
            self.scene().removeItem(circle)
        self.circles.clear()
        self.clear_lines()
        self.selected_circle = None
        self.drawing = True

    def import_circles(self, positions: list):
        # 导入圆圈的位置
        self.clear_circles()
        for pos in positions:
            circle = QGraphicsEllipseItem(0, 0, 5, 5)  # 调整大小
            circle.setBrush(QColor(240, 190, 80, 120))
            circle.setPen(QPen(QColor(240, 190, 80), 1, Qt.SolidLine))  # 调整画笔宽度
            circle.setPos(pos[0] - 2.5, pos[1] - 2.5)  # 调整偏移量
            self.scene().addItem(circle)
            self.circles.append(circle)
        for i, circle in enumerate(self.circles):
            if i == 0:
                continue
            line = self.draw_line(self.circles[i - 1].pos() + QPoint(2.5, 2.5), circle.pos() + QPoint(2.5, 2.5))
            self.lines.append(line)
        line = self.draw_line(self.circles[-1].pos() + QPoint(2.5, 2.5), self.circles[0].pos() + QPoint(2.5, 2.5))
        self.lines.append(line)

        self.drawing = False

    def export_circles(self):
        # 导出圆圈的位置
        positions = []
        for circle in self.circles:
            positions.append((circle.pos().x() + 2.5, circle.pos().y() + 2.5))  # 调整偏移量
        return positions


if __name__ == '__main__':
    # 主窗口
    class MainWindow(QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.mark_label = MarkableImage(image_path='/Users/xiangyang/PycharmProjects/medai/resources/01737_0.jpg',
                                            parent=self)
            self.mark_label.import_circles([(100, 100), (100, 200), (200, 200), (200, 100)])
            self.setGeometry(100, 100, 1000, 600)
            self.setCentralWidget(self.mark_label)


    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
