from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QColor,QBrush
from models.cell import CellItem, ExpansionIndicator, CELL_DEFAULT_COLOR
from PyQt6.QtCore import QRectF

class CanvasScene(QGraphicsScene):
    def __init__(self, width=1000, height=800, cell_pixel_size=20):
        super().__init__()
        self.cell_size = cell_pixel_size
        self.cells = {}
        self.center=(10,0)
        self.indicators = {}
        self.current_color = QColor(230, 239, 233)
        self.tool = "draw"

        self.setSceneRect(0,0, width, height)
        canvas_bg = self.addRect(QRectF(0, 0, width, height),
                                 brush=QBrush(QColor("#ffffff")))  # bianco
        canvas_bg.setZValue(-1)  

        self._init_center()


    def _init_center(self):
        self.add_center()
        self.update_indicators()

    def add_center(self):
        item = CellItem(self.center[0], self.center[1], self.cell_size, color=CELL_DEFAULT_COLOR)
        item.setPos(self.center[0],self.center[1])
        self.addItem(item)
        self.cells[(self.center[0], self.center[1])] = item
        self.update_indicators()

    def add_cell(self, gx, gy, color=CELL_DEFAULT_COLOR):
        if (gx, gy) in self.cells:
            return self.cells[(gx, gy)]
        item = CellItem(gx, gy, self.cell_size, color)
        if (gx, gy) in self.indicators:
            item.setPos(gx * self.cell_size, gy * self.cell_size)
            self.addItem(item)
            self.cells[(gx, gy)] = item
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

    def reset(self):
        for item in list(self.cells.values()):
            self.removeItem(item)
        self.cells.clear()

        for item in list(self.indicators.values()):
            self.removeItem(item)
        self.indicators.clear()

        self.add_center()
        self.update_indicators()



    def update_indicators(self):
        neighbors = set()
        for (x, y) in self.cells.keys():
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),(-1,-1),(-1,1),(1,1),(1,-1)]:
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

    def border(self):
        res=[]
        for i in self.cells:
            if( not ((self.cells[0]+1,self.cells[1]) in self.cells)):
                print()
        