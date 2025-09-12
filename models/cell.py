from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem
from PyQt6.QtGui import QBrush, QPen, QColor

CELL_DEFAULT_COLOR = QColor(255, 255, 255)
EXPANSION_INDICATOR_COLOR = QColor(180, 180, 180, 180)
CELL_BORDER_COLOR = QColor(80, 80, 80)


class CellItem(QGraphicsRectItem):
    def __init__(self, x, y, size, color=CELL_DEFAULT_COLOR):
        super().__init__(0, 0, size, size)
        self.grid_pos = (x, y)
        self.setBrush(QBrush(color))
        self.setPen(QPen(CELL_BORDER_COLOR))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

    def set_color(self, color: QColor):
        self.setBrush(QBrush(color))


class ExpansionIndicator(QGraphicsRectItem):
    def __init__(self, x, y, size):
        super().__init__(0, 0, size, size)
        self.grid_pos = (x, y)
        self.setBrush(QBrush(EXPANSION_INDICATOR_COLOR))
        self.setPen(QPen(EXPANSION_INDICATOR_COLOR))
        self.setOpacity(0.9)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
