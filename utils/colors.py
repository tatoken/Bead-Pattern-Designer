from PyQt6.QtGui import QColor

def color_to_hex(color: QColor) -> str:
    """Converte un QColor in stringa esadecimale #RRGGBB"""
    return f"#{color.red():02x}{color.green():02x}{color.blue():02x}"

def hex_to_color(hex_str: str) -> QColor:
    """Converte una stringa #RRGGBB in QColor"""
    return QColor(hex_str)
