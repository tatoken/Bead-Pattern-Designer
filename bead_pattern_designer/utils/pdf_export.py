from PyQt6.QtGui import QPainter, QColor, QPdfWriter, QPageSize
from PyQt6.QtCore import QRectF, QSizeF

def export_pattern_pdf(filename, scene, bead_size_cm, status_bar=None):
    if not scene.cells:
        if status_bar:
            status_bar.showMessage("Nessuna cella da esportare")
        return

    xs = [p[0] for p in scene.cells.keys()]
    ys = [p[1] for p in scene.cells.keys()]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    w_beads = maxx - minx + 1
    h_beads = maxy - miny + 1

    width_cm = w_beads * bead_size_cm
    height_cm = h_beads * bead_size_cm

    pdf = QPdfWriter(filename)
    pdf.setResolution(300)
    pdf.setPageSize(QPageSize(QSizeF(width_cm * 10, height_cm * 10), QPageSize.Unit.Millimeter))

    painter = QPainter(pdf)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # calcolo il rettangolo delle celle da esportare in coordinate scena
    rect = QRectF(minx * scene.cell_size,
                  miny * scene.cell_size,
                  w_beads * scene.cell_size,
                  h_beads * scene.cell_size)

    # scene.render(painter, target, source)
    # target: area della pagina PDF
    # source: area della scena
    target_rect = QRectF(0, 0, pdf.width(), pdf.height())
    painter.fillRect(target_rect, QColor(255, 255, 255))
    scene.render(painter, target_rect, rect)

    painter.end()

    if status_bar:
        status_bar.showMessage(f"Esportato PDF: {filename} ({width_cm:.2f}cm x {height_cm:.2f}cm)")
