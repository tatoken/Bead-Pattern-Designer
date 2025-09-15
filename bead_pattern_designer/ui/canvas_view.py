from PyQt6.QtWidgets import QGraphicsView, QApplication
from PyQt6.QtGui import QPainter,QBrush, QColor
from PyQt6.QtCore import Qt, pyqtSignal,QRectF


class CanvasView(QGraphicsView):
    zoomChanged = pyqtSignal(int)
    zoom_in_factor = 1.05

    def __init__(self, scene):
        super().__init__(scene)

        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        self.zoom_level = 0
        self.setStyleSheet("""
            QGraphicsView {
                background-color: #bdc3c7;
                border-radius: 15px;
                border: 2px solid #ecf0f1;  
            }
        """)

    def zoomReset(self):
        if self.zoom_level != 0:
            factor = self.zoom_in_factor ** self.zoom_level
            self.scale(1 / factor, 1 / factor)  # annullo lo zoom
            self.zoom_level = 0


    def wheelEvent(self, event):

        zoom_out_factor = 1 / self.zoom_in_factor
        zoomed=False

        if (event.angleDelta().y() > 0 and self.zoom_level<30):
            zoom_factor = self.zoom_in_factor
            self.zoom_level += 1
            zoomed=True
        if(event.angleDelta().y() < 0 and self.zoom_level>-30):
            zoom_factor = zoom_out_factor
            self.zoom_level -= 1
            zoomed=True
        if(zoomed):
            self.scale(zoom_factor, zoom_factor)
            self.zoomChanged.emit(self.zoom_level)


    def mousePressEvent(self, event):
        if self._pan_active and event.button() == Qt.MouseButton.LeftButton:
            self._panning = True
            self._last_pan_point = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            return  # non passare l'evento alla scena
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning and self._last_pan_point:
            delta = event.pos() - self._last_pan_point
            self._last_pan_point = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._panning and event.button() == Qt.MouseButton.LeftButton:
            self._panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            return
        super().mouseReleaseEvent(event)

