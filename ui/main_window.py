from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox, QFileDialog, QColorDialog, QFrame
from ui.canvas_view import CanvasView
from models.pattern import CanvasScene
from utils.pdf_export import export_pattern_pdf

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bead Pattern Designer")

        self.scene = CanvasScene(cell_pixel_size=20)
        self.view = CanvasView(self.scene)

        container = QWidget()
        layout = QHBoxLayout()
        left = QVBoxLayout()

        toolbar = QFrame()
        tb_layout = QVBoxLayout()

        # Tool buttons
        draw_btn = QPushButton("Disegna")
        erase_btn = QPushButton("Cancella")
        pan_btn = QPushButton("Pan")
        export_pdf_btn = QPushButton("Esporta PDF")
        color_btn = QPushButton("Colore")

        draw_btn.clicked.connect(lambda: self.set_tool("draw"))
        erase_btn.clicked.connect(lambda: self.set_tool("erase"))
        pan_btn.clicked.connect(lambda: self.set_tool("pan"))
        color_btn.clicked.connect(self.choose_color)
        export_pdf_btn.clicked.connect(self.export_pdf)

        for btn in (draw_btn, erase_btn, pan_btn, color_btn, export_pdf_btn):
            tb_layout.addWidget(btn)

        bead_label = QLabel("Dimensione perla (cm)")
        bead_combo = QComboBox()
        bead_combo.addItems(["0.2", "0.3", "0.35", "0.4", "0.5", "0.6"])
        bead_combo.setCurrentText("0.4")
        bead_combo.currentTextChanged.connect(self.on_bead_size_changed)

        tb_layout.addWidget(bead_label)
        tb_layout.addWidget(bead_combo)

        toolbar.setLayout(tb_layout)
        left.addWidget(toolbar)

        layout.addLayout(left)
        layout.addWidget(self.view, 1)
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = self.statusBar()
        self.status.showMessage("Pronto")
        self.set_tool("draw")

        self.bead_size_cm = 0.4

    def set_tool(self, tool):
        self.scene.tool = tool
        self.status.showMessage(f"Tool: {tool}")

    def choose_color(self):
        col = QColorDialog.getColor(self.scene.current_color, self, "Scegli colore")
        if col.isValid():
            self.scene.current_color = col

    def on_bead_size_changed(self, text):
        try:
            self.bead_size_cm = float(text)
            self.scene.set_bead_size(self.bead_size_cm)
            self.status.showMessage(f"Bead size: {self.bead_size_cm} cm")
        except ValueError:
            pass

    def export_pdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Esporta PDF", filter="PDF Files (*.pdf)")
        if fn:
            export_pattern_pdf(fn, self.scene, self.bead_size_cm, self.status)
