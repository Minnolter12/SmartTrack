import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QStackedWidget, QGridLayout
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

        # 2. Section Header & Add Semester Action
        header_actions_row = QHBoxLayout()
        section_title = QLabel("Your Semesters")
        sec_title_font = QFont()
        sec_title_font.setPointSize(16)
        sec_title_font.setBold(True)
        section_title.setFont(sec_title_font)
        section_title.setStyleSheet("color: #FFFFFF; border: none;")
        header_actions_row.addWidget(section_title)

        header_actions_row.addStretch()

        self.add_sem_button = QPushButton("+ Add Semester")
        self.add_sem_button.setObjectName("PrimaryBtn")
        self.add_sem_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_sem_button.setFixedHeight(38)
        self.add_sem_button.clicked.connect(self.add_semester)
        header_actions_row.addWidget(self.add_sem_button)

        layout.addLayout(header_actions_row)

        # 3. Scrollable Grid Container of Hero Semester Cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")

        self.grid_container = QWidget()
        self.grid_container.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.scroll_area.setWidget(self.grid_container)
        layout.addWidget(self.scroll_area)

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
        # Clear existing grid widgets
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not self.controller:
            return

        self.semesters_list = [f"Sem {s.sem_number}" for s in self.controller.semesters]

        total_sems = len(self.controller.semesters)
        total_courses = sum(len(s.courses) for s in self.controller.semesters)
        self.dash_stats_lbl.setText(
            f"{total_sems} Active Semester{'s' if total_sems != 1 else ''} • {total_courses} Course{'s' if total_courses != 1 else ''} Tracked"
        )

        if not self.controller.semesters:
            empty_frame = QFrame()
            empty_frame.setStyleSheet("""
                QFrame {
                    background-color: #181C24;
                    border: 1px dashed #2C333D;
                    border-radius: 14px;
                }
            """)
            empty_layout = QVBoxLayout(empty_frame)
            empty_layout.setContentsMargins(40, 50, 40, 50)
            empty_layout.setAlignment(Qt.AlignCenter)

            empty_title = QLabel("No semesters added yet")
            empty_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF; border: none;")
            empty_layout.addWidget(empty_title, alignment=Qt.AlignCenter)

            empty_sub = QLabel("Create your first semester to begin organizing courses and attendance.")
            empty_sub.setStyleSheet("font-size: 13px; color: #8F9CAE; border: none; margin-top: 6px;")
            empty_layout.addWidget(empty_sub, alignment=Qt.AlignCenter)

            add_btn = QPushButton("+ Create Semester 1")
            add_btn.setObjectName("PrimaryBtn")
            add_btn.setCursor(QCursor(Qt.PointingHandCursor))
            add_btn.setFixedHeight(38)
            add_btn.setStyleSheet("margin-top: 14px;")
            add_btn.clicked.connect(self.add_semester)
            empty_layout.addWidget(add_btn, alignment=Qt.AlignCenter)

            self.grid_layout.addWidget(empty_frame, 0, 0, 1, 3)
            return

        cols = 3  # 3 columns responsive grid
        for i, sem in enumerate(self.controller.semesters):
            row = i // cols
            col = i % cols
            card = HeroSemesterCard(
                sem,
                on_click=lambda s=sem: self.controller.open_semester(s)
            )
            self.grid_layout.addWidget(card, row, col)

    def on_semester_select(self, name: str) -> None:
        print(f"User navigated context directly into: {name}")
        for sem in self.controller.semesters:
            if f"Sem {sem.sem_number}" == name:
                self.controller.open_semester(sem)
                break


class HeroSemesterCard(QFrame):
    """Modern Hero card representing a semester with attendance health, stats, and quick-launch."""
    def __init__(self, semester: Semester, on_click=None, parent=None):
        super().__init__(parent)
        self.semester = semester
        self.on_click = on_click
        self.setProperty("class", "HeroSemesterCard")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumWidth(280)
        self.setMinimumHeight(170)

        # Calculate metrics
        courses = semester.courses
        total_courses = len(courses)
        total_happened = sum(c.classes_happened for c in courses)
        total_attended = sum(c.classes_attended for c in courses)
        has_data = total_happened > 0

        pct = (total_attended / total_happened * 100) if has_data else 0.0
        min_target = semester.min_attendance

        if not has_data:
            health_mode = "nodata"
            accent_color = "#475569"
            badge_text = "No Classes Yet"
            badge_bg = "#222A35"
            badge_fg = "#94A3B8"
        elif pct >= min_target:
            health_mode = "safe"
            accent_color = "#10B981"
            badge_text = f"✓ {pct:.1f}% Safe"
            badge_bg = "#132D24"
            badge_fg = "#34D399"
        else:
            health_mode = "alert"
            accent_color = "#EF4444"
            badge_text = f"⚠ {pct:.1f}% Low"
            badge_bg = "#3A1B1D"
            badge_fg = "#F87171"

        self.setStyleSheet(f"""
            QFrame.HeroSemesterCard {{
                background-color: #161A22;
                border: 1px solid #28303C;
                border-top: 3px solid {accent_color};
                border-radius: 14px;
            }}
            QFrame.HeroSemesterCard:hover {{
                background-color: #1D232F;
                border-color: #4B5563;
                border-top: 3px solid {accent_color};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        # Header row: Sem title + Badge
        header_row = QHBoxLayout()
        sem_num_lbl = QLabel(f"Semester {semester.sem_number}")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        sem_num_lbl.setFont(font)
        sem_num_lbl.setStyleSheet("color: #FFFFFF; border: none;")
        header_row.addWidget(sem_num_lbl)

        header_row.addStretch()

        badge_lbl = QLabel(badge_text)
        badge_lbl.setStyleSheet(f"""
            background-color: {badge_bg};
            color: {badge_fg};
            font-size: 11px;
            font-weight: bold;
            border-radius: 8px;
            padding: 4px 10px;
            border: none;
        """)
        header_row.addWidget(badge_lbl)
        layout.addLayout(header_row)

        # Middle stats row
        stats_row = QHBoxLayout()
        courses_lbl = QLabel(f"📚 {total_courses} Course{'s' if total_courses != 1 else ''}")
        courses_lbl.setStyleSheet("color: #94A3B8; font-size: 13px; border: none;")
        stats_row.addWidget(courses_lbl)

        stats_row.addStretch()

        target_lbl = QLabel(f"Target: {min_target}%")
        target_lbl.setStyleSheet("color: #64748B; font-size: 12px; border: none;")
        stats_row.addWidget(target_lbl)
        layout.addLayout(stats_row)

        layout.addStretch()

        # Bottom row: Action link hint
        bottom_row = QHBoxLayout()
        if has_data:
            summary_lbl = QLabel(f"{total_attended}/{total_happened} periods attended")
        else:
            summary_lbl = QLabel("Ready for courses")
        summary_lbl.setStyleSheet("color: #64748B; font-size: 11px; border: none;")
        bottom_row.addWidget(summary_lbl)

        bottom_row.addStretch()

        open_btn = QLabel("Open View ➔")
        open_btn.setStyleSheet(f"color: {accent_color}; font-size: 12px; font-weight: bold; border: none;")
        bottom_row.addWidget(open_btn)
        layout.addLayout(bottom_row)

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click()


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