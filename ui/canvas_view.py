from PyQt6.QtWidgets import QGraphicsView, QApplication
from PyQt6.QtGui import QPainter,QBrush, QColor
from PyQt6.QtCore import Qt


class CanvasView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self._pan = False
        self._last_pan_point = None
        self.zoom_level = 0
        self.setStyleSheet("""
            QGraphicsView {
                border-radius: 15px;
                border: 2px solid #ecf0f1;  /* opzionale, per vedere il bordo */
            }
        """)

    def wheelEvent(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
            self.zoom_level += 1
        else:
            zoom_factor = zoom_out_factor
            self.zoom_level -= 1
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton or (
            event.button() == Qt.MouseButton.LeftButton
            and QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            self._pan = True
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self._last_pan_point = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton or (
            event.button() == Qt.MouseButton.LeftButton
            and QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            self._pan = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self._last_pan_point = None
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self._pan and self._last_pan_point is not None:
            delta = event.pos() - self._last_pan_point
            self._last_pan_point = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(event)
