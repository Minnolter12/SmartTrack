import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QStackedWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor

from src.courses import Semester, Course
from src.storage import load_semesters, save_semesters
from ui.semester_screen import SemesterScreen
from ui.styles import DARK_THEME_QSS

class MainApp(QMainWindow):
    _qapp = None

    def __init__(self):
        if not QApplication.instance():
            MainApp._qapp = QApplication(sys.argv)

        super().__init__()
        self.setWindowTitle("SmartTrack")
        self.resize(1000, 800)
        self.setStyleSheet(DARK_THEME_QSS)

        self.semesters: list[Semester] = load_semesters()

        # Central container
        central_widget = QWidget()
        central_widget.setObjectName("MainContainer")
        self.setCentralWidget(central_widget)

        container_layout = QVBoxLayout(central_widget)
        container_layout.setContentsMargins(20, 20, 20, 20)

        # Multi-page switcher
        self.stacked_widget = QStackedWidget()
        container_layout.addWidget(self.stacked_widget)

        # Screens
        self.home_screen = HomeScreen(parent=self, controller=self)
        self.stacked_widget.addWidget(self.home_screen)

        self.semester_screen = SemesterScreen(parent=self, controller=self)
        self.stacked_widget.addWidget(self.semester_screen)

        self.show_home()

    def mainloop(self):
        """Preserves compatibility with app.mainloop() pattern."""
        self.show()
        app = QApplication.instance() or MainApp._qapp
        if app:
            sys.exit(app.exec())

    def save_data(self) -> None:
        save_semesters(self.semesters)

    def open_semester(self, semester: Semester) -> None:
        self.semester_screen.set_semester(semester)
        self.stacked_widget.setCurrentWidget(self.semester_screen)

    def show_home(self) -> None:
        self.home_screen.refresh_semester_row()
        self.stacked_widget.setCurrentWidget(self.home_screen)


class HomeScreen(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.semesters_list = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(25)

        # 1. Dashboard Banner Card
        dash_board = QFrame()
        dash_board.setStyleSheet("""
            QFrame {
                background-color: #181C24;
                border: 1px solid #2C333D;
                border-radius: 16px;
            }
        """)
        dash_layout = QVBoxLayout(dash_board)
        dash_layout.setContentsMargins(30, 40, 30, 40)
        dash_layout.setSpacing(10)

        dash_lbl = QLabel("Welcome back!")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        dash_lbl.setFont(title_font)
        dash_lbl.setStyleSheet("color: #FFFFFF; border: none;")
        dash_layout.addWidget(dash_lbl, alignment=Qt.AlignCenter)

        self.dash_stats_lbl = QLabel("Manage your courses, periods, and attendance smartly.")
        self.dash_stats_lbl.setStyleSheet("font-size: 13px; color: #8F9CAE; border: none;")
        dash_layout.addWidget(self.dash_stats_lbl, alignment=Qt.AlignCenter)

        layout.addWidget(dash_board)

        # 2. Add Semester Button
        actions_frame = QWidget()
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(0, 0, 0, 0)

        self.add_sem_button = QPushButton("Add Semester")
        self.add_sem_button.setObjectName("PrimaryBtn")
        self.add_sem_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_sem_button.setFixedHeight(42)
        self.add_sem_button.clicked.connect(self.add_semester)
        actions_layout.addWidget(self.add_sem_button, alignment=Qt.AlignCenter)

        layout.addWidget(actions_frame)

        # 3. Horizontal Semester Row
        self.semester_row = LazyRowFrame(self)
        layout.addWidget(self.semester_row)

        layout.addStretch()

        self.refresh_semester_row()

    def add_semester(self) -> None:
        existing_nums = [s.sem_number for s in self.controller.semesters]
        next_sem_number = max(existing_nums, default=0) + 1

        new_sem = Semester(next_sem_number)
        self.controller.semesters.append(new_sem)
        self.controller.save_data()

        self.semesters_list.append(f"Sem {next_sem_number}")

        self.refresh_semester_row()
        self.on_semester_select(f"Sem {next_sem_number}")

    def refresh_semester_row(self) -> None:
        self.semester_row.clear()

        if not self.controller:
            return

        self.semesters_list = [f"Sem {s.sem_number}" for s in self.controller.semesters]

        total_sems = len(self.controller.semesters)
        total_courses = sum(len(s.courses) for s in self.controller.semesters)
        self.dash_stats_lbl.setText(
            f"{total_sems} Active Semester{'s' if total_sems != 1 else ''} • {total_courses} Course{'s' if total_courses != 1 else ''} Tracked"
        )

        if not self.controller.semesters:
            empty_lbl = QLabel("No semesters added yet. Click 'Add Semester' above to begin!")
            empty_lbl.setStyleSheet("color: #8F9CAE; font-size: 13px; padding: 20px;")
            self.semester_row.add_widget(empty_lbl)
            return

        for sem in self.controller.semesters:
            sem_name = f"Sem {sem.sem_number}"
            sem_btn = QPushButton(sem_name)
            sem_btn.setObjectName("PrimaryBtn")
            sem_btn.setCursor(QCursor(Qt.PointingHandCursor))
            sem_btn.setFixedHeight(38)
            sem_btn.setMinimumWidth(110)
            sem_btn.clicked.connect(lambda checked, name=sem_name: self.on_semester_select(name))
            self.semester_row.add_widget(sem_btn)

    def on_semester_select(self, name: str) -> None:
        print(f"User navigated context directly into: {name}")
        for sem in self.controller.semesters:
            if f"Sem {sem.sem_number}" == name:
                self.controller.open_semester(sem)
                break


class LazyRowFrame(QScrollArea):
    """Horizontal scrollable container for row items."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFixedHeight(95)
        self.setStyleSheet("""
            QScrollArea {
                background-color: #1E232B;
                border: 1px solid #2C333D;
                border-radius: 12px;
            }
        """)

        self.container_widget = QWidget()
        self.container_widget.setStyleSheet("background: transparent;")
        self.row_layout = QHBoxLayout(self.container_widget)
        self.row_layout.setContentsMargins(15, 10, 15, 10)
        self.row_layout.setSpacing(12)
        self.row_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setWidget(self.container_widget)

    def clear(self):
        while self.row_layout.count():
            item = self.row_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_widget(self, widget: QWidget):
        self.row_layout.addWidget(widget)


class ClickableHomeWidget(QFrame):
    """Card widget maintained for backward compatibility."""
    def __init__(self, master=None, titleText="Card", on_click=None, **kwargs):
        super().__init__(master)
        self.on_click = on_click
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet("""
            QFrame {
                background-color: #2B2B2B;
                border-radius: 16px;
            }
            QFrame:hover {
                background-color: #373F4B;
            }
        """)
        layout = QVBoxLayout(self)
        lbl = QLabel(titleText)
        lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(lbl, alignment=Qt.AlignCenter)

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click()


class CustomDropdown(QWidget):
    """Dropdown component maintained for backward compatibility."""
    def __init__(self, master=None, options: list[str] = None, default_text: str = "Select Option", **kwargs):
        super().__init__(master)
        from PySide6.QtWidgets import QComboBox
        self.combo = QComboBox(self)
        if options:
            self.combo.addItems(options)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.combo)

    def get(self) -> str:
        return self.combo.currentText()

    def set(self, value: str) -> None:
        self.combo.setCurrentText(value)