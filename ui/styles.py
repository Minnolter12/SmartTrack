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

QPushButton#SimulatorBtn {
    background-color: #242B35;
    color: #64B5F6;
    border: 1px solid #364457;
    font-weight: 600;
}

QPushButton#SimulatorBtn:hover {
    background-color: #2F3B4A;
    border-color: #64B5F6;
    color: #90CAF9;
}

QSlider::groove:horizontal {
    border: none;
    height: 6px;
    background: #2C333D;
    border-radius: 3px;
}

QSlider::sub-page:horizontal {
    background: #3B8ED0;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #FFFFFF;
    border: 2px solid #3B8ED0;
    width: 16px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background: #E0E0E0;
    border-color: #64B5F6;
}

/* Preset Chips for Simulator */
QPushButton.PresetChip {
    background-color: #1E2530;
    color: #94A3B8;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton.PresetChip:hover {
    background-color: #2D3748;
    color: #60A5FA;
    border-color: #60A5FA;
}

QPushButton.PresetChip:pressed {
    background-color: #1E3A5F;
}

/* Stepper buttons */
QPushButton.StepperBtn {
    background-color: #242C38;
    color: #E2E8F0;
    border: 1px solid #3B4758;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    min-width: 38px;
    max-width: 38px;
    min-height: 38px;
    max-height: 38px;
    padding: 0px;
}

QPushButton.StepperBtn:hover {
    background-color: #323E50;
    border-color: #60A5FA;
    color: #60A5FA;
}

QPushButton.StepperBtn:pressed {
    background-color: #1E2633;
}

/* Hero Cards on HomeScreen */
QFrame.HeroSemesterCard {
    background-color: #151921;
    border: 1px solid #28303C;
    border-radius: 14px;
}

QFrame.HeroSemesterCard:hover {
    background-color: #1A202A;
    border: 1px solid #3E4C60;
}

/* Course Tab Buttons */
QPushButton.CourseTabBtn {
    background-color: transparent;
    color: #8F9CAE;
    border: none;
    border-bottom: 2px solid transparent;
    border-radius: 0px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton.CourseTabBtn:hover {
    color: #CBD5E1;
}

QPushButton.CourseTabBtn[active="true"] {
    color: #60A5FA;
    border-bottom: 2px solid #60A5FA;
}

/* Mini pill counters for OD / ML */
QLabel.PillBadge {
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 11px;
    font-weight: bold;
}
"""
