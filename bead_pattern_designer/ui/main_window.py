from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QComboBox, QFileDialog,
    QColorDialog, QFrame, QTextEdit
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize,Qt
from bead_pattern_designer.ui.canvas_view import CanvasView
from bead_pattern_designer.models.pattern import CanvasScene
from bead_pattern_designer.utils.pdf_export import export_pattern_pdf
from bead_pattern_designer.layout.Button_layout import MAIN_BUTTON_LAYOUT

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bead Pattern Designer")

        # --- SCENE & VIEW ---
        self.scene = CanvasScene(cell_pixel_size=20)
        self.view = CanvasView(self.scene)
        self.view.zoomChanged.connect(self.on_zoom_changed)

        # --- ROOT CONTAINER ---
        container = QWidget()
        root_layout = QVBoxLayout(container)  # verticale: top / center / bottom

        # ======================
        # TOP BAR (settings)
        # ======================
        top_bar = QFrame()
        top_bar.setStyleSheet("background-color: #76877d; color: white; border: 1px solid white; border-radius: 5px;")
        top_layout = QHBoxLayout(top_bar)

        self.color_preview = QPushButton()
        self.color_preview.setFixedSize(24, 24)
        self.color_preview.setStyleSheet(
            "background-color: black; border: 1px solid white;"
        )
        self.color_preview.clicked.connect(self.choose_color)
        self.color_preview.setCursor(Qt.CursorShape.PointingHandCursor)

        bead_label = QLabel("Dimensione perla (cm)")
        bead_label.setStyleSheet("color: white;")
        bead_combo = QComboBox()
        bead_combo.addItems(["0.2", "0.3", "0.35", "0.4", "0.5", "0.6"])
        bead_combo.setCurrentText("0.4")
        bead_combo.currentTextChanged.connect(self.on_bead_size_changed)

        bead_zoom_label = QLabel("Zoom: ")
        bead_zoom_label.setStyleSheet("color: white;")
        self.zoom_label_value = QLabel("0")
        self.zoom_label_value.setStyleSheet("color: white;")

        top_layout.addWidget(self.color_preview)
        top_layout.addWidget(bead_label)
        top_layout.addWidget(bead_combo)
        top_layout.addWidget(bead_zoom_label)
        top_layout.addWidget(self.zoom_label_value)
        top_layout.addStretch()

        root_layout.addWidget(top_bar)


        # ======================
        # CENTER AREA (toolbar + canvas)
        # ======================
        center_frame = QFrame()
        center_layout = QHBoxLayout(center_frame)

        # Toolbar sinistra
        toolbar = QFrame()
        toolbar.setStyleSheet("background-color: #76877d; border-radius: 5px;")
        tb_layout = QVBoxLayout(toolbar)
        

        draw_btn = QPushButton("Disegna")
        draw_btn.setCheckable(True)

        erase_btn = QPushButton("Cancella")
        pan_btn = QPushButton("Pan")
        export_pdf_btn = QPushButton("Esporta PDF")
        zoom_reset_btn = QPushButton("Reset Zoom")
        reset_btn = QPushButton("Reset")

        # 🔗 collegamenti bottoni
        draw_btn.clicked.connect(lambda: self.set_tool("draw"))
        erase_btn.clicked.connect(lambda: self.set_tool("erase"))
        pan_btn.clicked.connect(lambda: self.set_tool("pan"))
        export_pdf_btn.clicked.connect(self.export_pdf)
        zoom_reset_btn.clicked.connect(lambda: self.view.zoomReset())
        reset_btn.clicked.connect(lambda: self.scene.reset())

        for btn in (draw_btn, erase_btn, pan_btn, export_pdf_btn, zoom_reset_btn, reset_btn):
            tb_layout.addWidget(btn)

        center_layout.addWidget(toolbar)
        center_layout.addWidget(self.view, 1)
        root_layout.addWidget(center_frame, 1)

        # === FINALIZE ===
        self.setCentralWidget(container)
        self.status = self.statusBar()
        self.status.showMessage("Pronto")

        self.bead_size_cm = 0.4

    def set_tool(self, tool):
        self.scene.tool = tool
        self.status.showMessage(f"Tool: {tool}")

    def choose_color(self):
        col = QColorDialog.getColor(self.scene.current_color, self, "Scegli colore")
        if col.isValid():
            self.scene.current_color = col
            self.color_preview.setStyleSheet(
                f"background-color: {col.name()}; border: 1px solid white;"
            )


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

    def on_zoom_changed(self, level):
        self.zoom_label_value.setText(str(level)) 
