from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QColor
from models.cell import CellItem, ExpansionIndicator, CELL_DEFAULT_COLOR


class CanvasScene(QGraphicsScene):
    def __init__(self, cell_pixel_size):
        super().__init__()
        self.cell_size = cell_pixel_size
        self.cells = {}       # (x,y) -> CellItem
        self.indicators = {}  # (x,y) -> ExpansionIndicator
        self.current_color = QColor(200, 30, 30)
        self.tool = "draw"
        self._init_center()

    def _init_center(self):
        self.add_cell(0, 0)
        self.update_indicators()

    def add_cell(self, gx, gy, color=CELL_DEFAULT_COLOR):
        if (gx, gy) in self.cells:
            return self.cells[(gx, gy)]
        item = CellItem(gx, gy, self.cell_size, color)
        item.setPos(gx * self.cell_size, gy * self.cell_size)
        self.addItem(item)
        self.cells[(gx, gy)] = item
        if (gx, gy) in self.indicators:
            self.removeItem(self.indicators[(gx, gy)])
            del self.indicators[(gx, gy)]
        self.update_indicators()
        return item

    def remove_cell(self, gx, gy):
        if (gx, gy) not in self.cells:
            return
        self.removeItem(self.cells[(gx, gy)])
        del self.cells[(gx, gy)]
        self.update_indicators()

    def update_indicators(self):
        neighbors = set()
        for (x, y) in self.cells.keys():
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                pos = (x + dx, y + dy)
                if pos not in self.cells:
                    neighbors.add(pos)

        for pos in list(self.indicators.keys()):
            if pos not in neighbors:
                self.removeItem(self.indicators[pos])
                del self.indicators[pos]

        for pos in neighbors:
            if pos in self.indicators:
                continue
            gx, gy = pos
            ind = ExpansionIndicator(gx, gy, int(self.cell_size * 0.4))
            ind.setPos(
                gx * self.cell_size + self.cell_size * 0.3,
                gy * self.cell_size + self.cell_size * 0.3,
            )
            self.addItem(ind)
            self.indicators[pos] = ind

    def set_cell_size(self, size_px):
        old_cells = dict(self.cells)
        self.clear()
        self.cells.clear()
        self.cell_size = size_px
        for (gx, gy), old_item in old_cells.items():
            self.add_cell(gx, gy, old_item.brush().color())
        self.update_indicators()

    def set_bead_size(self, bead_size_cm):
        # qui puoi calcolare nuova dimensione cella se serve
        pass

    # Gestione click
    def mousePressEvent(self, ev):
        pos = ev.scenePos()
        gx = int(pos.x() // self.cell_size)
        gy = int(pos.y() // self.cell_size)
        if ev.button().value == 1:  # Left click
            if (gx, gy) in self.indicators:
                self.add_cell(gx, gy, self.current_color if self.tool == "draw" else CELL_DEFAULT_COLOR)
                return
            if self.tool == "draw":
                if (gx, gy) not in self.cells:
                    self.add_cell(gx, gy, self.current_color)
                else:
                    self.cells[(gx, gy)].set_color(self.current_color)
            elif self.tool == "erase":
                if (gx, gy) in self.cells:
                    self.remove_cell(gx, gy)
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        pos = ev.scenePos()
        gx = int(pos.x() // self.cell_size)
        gy = int(pos.y() // self.cell_size)
        if ev.buttons().value & 1:  # Left click
            if self.tool == "draw":
                if (gx, gy) not in self.cells:
                    self.add_cell(gx, gy, self.current_color)
                else:
                    self.cells[(gx, gy)].set_color(self.current_color)
            elif self.tool == "erase":
                if (gx, gy) in self.cells:
                    self.remove_cell(gx, gy)
        super().mouseMoveEvent(ev)
