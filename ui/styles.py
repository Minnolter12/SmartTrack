DARK_THEME_QSS = """
QMainWindow, QWidget#MainContainer {
    background-color: #0E1217;
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

QScrollBar:vertical {
    border: none;
    background: #141820;
    width: 8px;
    margin: 0px 0px 0px 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #2C333D;
    min-height: 25px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #3B8ED0;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #141820;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background: #2C333D;
    min-width: 25px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background: #3B8ED0;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
    width: 0px;
}

/* Base Buttons */
QPushButton {
    background-color: #2C333D;
    color: #FFFFFF;
    border: 1px solid #373F4B;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #373F4B;
    border-color: #475569;
}

QPushButton:pressed {
    background-color: #232931;
}

QPushButton#PrimaryBtn {
    background-color: #3B8ED0;
    border: none;
    font-weight: bold;
}

QPushButton#PrimaryBtn:hover {
    background-color: #2A6F9E;
}

QPushButton#PrimaryBtn:pressed {
    background-color: #1E557A;
}

QPushButton#SuccessBtn {
    background-color: #27AE60;
    border: none;
    font-weight: bold;
}

QPushButton#SuccessBtn:hover {
    background-color: #1E8449;
}

QPushButton#DangerBtn {
    background-color: #C0392B;
    border: none;
    font-weight: bold;
}

QPushButton#DangerBtn:hover {
    background-color: #922B21;
}

QPushButton#DeleteSemBtn {
    background-color: #3D2323;
    color: #FFA4A4;
    border: 1px solid #5A2E2E;
}

QPushButton#DeleteSemBtn:hover {
    background-color: #5A2E2E;
    color: #FFFFFF;
}

/* Form Inputs */
QLineEdit, QSpinBox {
    background-color: #181C24;
    color: #FFFFFF;
    border: 1px solid #2C333D;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: #3B8ED0;
}

QLineEdit:focus, QSpinBox:focus {
    border: 1px solid #3B8ED0;
}

QComboBox {
    background-color: #181C24;
    color: #FFFFFF;
    border: 1px solid #2C333D;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
}

QComboBox:focus {
    border: 1px solid #3B8ED0;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #8F9CAE;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #181C24;
    color: #FFFFFF;
    border: 1px solid #2C333D;
    selection-background-color: #2C333D;
    outline: none;
    padding: 4px;
}

/* Dialog styling */
QDialog {
    background-color: #141820;
    color: #FFFFFF;
}
"""
