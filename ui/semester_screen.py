from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QProgressBar, QDialog, QLineEdit,
    QComboBox, QMessageBox, QRadioButton, QButtonGroup,
    QSpinBox, QStackedWidget
)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QFont, QCursor, QPainter, QPen, QColor, QConicalGradient, QLinearGradient
from src.courses import Semester, Course, TheoryCourses, LabCourses

class SemesterScreen(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.current_semester: Semester | None = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 1. Top Header Bar
        header_layout = QHBoxLayout()

        self.back_btn = QPushButton("← Back to Home")
        self.back_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(self.back_btn)

        self.title_label = QLabel("Semester Overview")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #FFFFFF; margin-left: 10px;")
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        self.add_course_btn = QPushButton("+ Add Course")
        self.add_course_btn.setObjectName("PrimaryBtn")
        self.add_course_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_course_btn.clicked.connect(self.open_add_course_dialog)
        header_layout.addWidget(self.add_course_btn)

        self.delete_sem_btn = QPushButton("Delete Semester")
        self.delete_sem_btn.setObjectName("DeleteSemBtn")
        self.delete_sem_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.delete_sem_btn.clicked.connect(self.confirm_delete_semester)
        header_layout.addWidget(self.delete_sem_btn)

        main_layout.addLayout(header_layout)

        # 2. Stats Bar Frame
        self.stats_frame = QFrame()
        self.stats_frame.setStyleSheet("""
            QFrame {
                background-color: #181C24;
                border: 1px solid #2C333D;
                border-radius: 12px;
            }
        """)
        stats_layout = QHBoxLayout(self.stats_frame)
        stats_layout.setContentsMargins(25, 15, 25, 15)

        # Stat 1: Overall Attendance
        att_box = QVBoxLayout()
        self.stat_overall_val = QLabel("0.0%")
        self.stat_overall_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #FFFFFF; border: none;")
        att_box.addWidget(self.stat_overall_val)
        att_lbl = QLabel("Overall Attendance")
        att_lbl.setStyleSheet("font-size: 12px; color: #8F9CAE; border: none;")
        att_box.addWidget(att_lbl)
        stats_layout.addLayout(att_box)
        stats_layout.addSpacing(30)

        # Stat 2: Enrolled Courses
        courses_box = QVBoxLayout()
        self.stat_courses_val = QLabel("0")
        self.stat_courses_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #FFFFFF; border: none;")
        courses_box.addWidget(self.stat_courses_val)
        courses_lbl = QLabel("Enrolled Courses")
        courses_lbl.setStyleSheet("font-size: 12px; color: #8F9CAE; border: none;")
        courses_box.addWidget(courses_lbl)
        stats_layout.addLayout(courses_box)
        stats_layout.addSpacing(30)

        # Stat 3: Projected with OD / Medical Leave
        self.proj_overall_box = QVBoxLayout()
        self.stat_proj_val = QLabel("—%")
        self.stat_proj_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #60A5FA; border: none;")
        self.proj_overall_box.addWidget(self.stat_proj_val)
        self.proj_lbl = QLabel("Projected (w/ OD & ML)")
        self.proj_lbl.setStyleSheet("font-size: 12px; color: #8F9CAE; border: none;")
        self.proj_overall_box.addWidget(self.proj_lbl)
        stats_layout.addLayout(self.proj_overall_box)
        stats_layout.addSpacing(30)

        # Stat 4: Target Minimum
        target_box = QVBoxLayout()
        self.stat_target_val = QLabel("75%")
        self.stat_target_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #FFFFFF; border: none;")
        target_box.addWidget(self.stat_target_val)
        target_lbl = QLabel("Target Minimum")
        target_lbl.setStyleSheet("font-size: 12px; color: #8F9CAE; border: none;")
        target_box.addWidget(target_lbl)
        stats_layout.addLayout(target_box)

        stats_layout.addStretch()

        # Stat 5: Standing status badge
        self.status_badge = QLabel("No Data")
        self.status_badge.setStyleSheet("""
            QLabel {
                background-color: #2C333D;
                color: #CBD5E1;
                font-size: 12px;
                font-weight: bold;
                border-radius: 10px;
                padding: 6px 16px;
                border: none;
            }
        """)
        stats_layout.addWidget(self.status_badge)

        main_layout.addWidget(self.stats_frame)

        # 3. Scrollable courses container
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.courses_layout = QVBoxLayout(self.scroll_widget)
        self.courses_layout.setContentsMargins(0, 10, 10, 10)
        self.courses_layout.setSpacing(12)
        self.courses_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_widget)

        main_layout.addWidget(self.scroll_area)

    def set_semester(self, semester: Semester) -> None:
        self.current_semester = semester
        self.title_label.setText(f"Semester {semester.sem_number}")
        self.stat_target_val.setText(f"{semester.min_attendance}%")
        self.refresh_view()

    def go_back(self) -> None:
        if self.controller:
            self.controller.show_home()

    def refresh_view(self) -> None:
        if not self.current_semester:
            return

        # Clear existing course cards
        while self.courses_layout.count():
            item = self.courses_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        courses = self.current_semester.courses
        self.stat_courses_val.setText(str(len(courses)))

        total_attended = sum(c.classes_attended for c in courses)
        total_happened = sum(c.classes_happened for c in courses)
        total_effective = sum(min(c.classes_happened, c.classes_attended + c.od_periods + c.ml_periods) for c in courses)

        if total_happened > 0:
            pct = (total_attended / total_happened) * 100
            proj_pct = (total_effective / total_happened) * 100
            self.stat_overall_val.setText(f"{pct:.1f}%")
            self.stat_proj_val.setText(f"{proj_pct:.1f}%")

            if proj_pct >= self.current_semester.min_attendance:
                self.stat_proj_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #2ECC71; border: none;")
            else:
                self.stat_proj_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #E74C3C; border: none;")

            if pct >= self.current_semester.min_attendance:
                self.stat_overall_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #2ECC71; border: none;")
                self.status_badge.setText("✓ In Good Standing")
                self.status_badge.setStyleSheet("background-color: #1E3A2F; color: #2ECC71; font-size: 12px; font-weight: bold; border-radius: 10px; padding: 6px 16px; border: none;")
            elif proj_pct >= self.current_semester.min_attendance:
                self.stat_overall_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #F59E0B; border: none;")
                self.status_badge.setText("✓ Safe with OD/ML")
                self.status_badge.setStyleSheet("background-color: #2D2713; color: #F59E0B; font-size: 12px; font-weight: bold; border-radius: 10px; padding: 6px 16px; border: none;")
            else:
                self.stat_overall_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #E74C3C; border: none;")
                self.status_badge.setText("⚠ Attention Needed")
                self.status_badge.setStyleSheet("background-color: #3D2323; color: #E74C3C; font-size: 12px; font-weight: bold; border-radius: 10px; padding: 6px 16px; border: none;")
        else:
            self.stat_overall_val.setText("—%")
            self.stat_overall_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #8F9CAE; border: none;")
            self.stat_proj_val.setText("—%")
            self.stat_proj_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #8F9CAE; border: none;")
            self.status_badge.setText("New Semester")
            self.status_badge.setStyleSheet("background-color: #2C333D; color: #8F9CAE; font-size: 12px; font-weight: bold; border-radius: 10px; padding: 6px 16px; border: none;")

        if not courses:
            empty_frame = QFrame()
            empty_frame.setStyleSheet("background-color: #181C24; border: 1px solid #2C333D; border-radius: 12px;")
            empty_layout = QVBoxLayout(empty_frame)
            empty_layout.setContentsMargins(30, 40, 30, 40)
            empty_layout.setAlignment(Qt.AlignCenter)

            msg_title = QLabel("No courses added to this semester yet")
            msg_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF; border: none;")
            empty_layout.addWidget(msg_title, alignment=Qt.AlignCenter)

            msg_sub = QLabel("Click the '+ Add Course' button in the top right to start tracking attendance.")
            msg_sub.setStyleSheet("font-size: 13px; color: #8F9CAE; border: none; margin-top: 5px;")
            empty_layout.addWidget(msg_sub, alignment=Qt.AlignCenter)

            self.courses_layout.addWidget(empty_frame)
            return

        for course in courses:
            card = CourseCard(course, self)
            self.courses_layout.addWidget(card)

    def open_add_course_dialog(self) -> None:
        if not self.current_semester:
            return
        dialog = AddCourseDialog(self.current_semester, self)
        if dialog.exec():
            self.controller.save_data()
            self.refresh_view()

    def confirm_delete_semester(self) -> None:
        if not self.current_semester:
            return
        reply = QMessageBox.question(
            self,
            "Delete Semester",
            f"Are you sure you want to delete Semester {self.current_semester.sem_number}? All its courses will be permanently deleted.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.current_semester in self.controller.semesters:
                self.controller.semesters.remove(self.current_semester)
            self.controller.save_data()
            self.go_back()


class CircularProgressWidget(QWidget):
    """Modern circular ring progress gauge with smooth gradients and center percentage."""
    def __init__(self, parent=None, size: int = 76):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._percentage: float = 0.0
        self._has_data: bool = False
        self._color_start = QColor("#2ECC71")
        self._color_end = QColor("#27AE60")

    def set_data(self, percentage: float, has_data: bool, status_mode: str):
        """status_mode: 'safe', 'borderline', 'alert', 'nodata'"""
        self._percentage = max(0.0, min(100.0, percentage))
        self._has_data = has_data

        if not has_data:
            self._color_start = QColor("#64748B")
            self._color_end = QColor("#475569")
        elif status_mode == "safe":
            # Emerald green gradient
            self._color_start = QColor("#2ECC71")
            self._color_end = QColor("#10B981")
        elif status_mode == "borderline":
            # Amber / Warm Orange gradient
            self._color_start = QColor("#F59E0B")
            self._color_end = QColor("#D97706")
        else: # alert
            # Coral / Crimson red gradient
            self._color_start = QColor("#EF4444")
            self._color_end = QColor("#DC2626")

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        stroke_width = 7.0
        margin = stroke_width / 2.0 + 2.0
        rect = QRectF(margin, margin, w - 2 * margin, h - 2 * margin)

        # 1. Background Track Ring
        bg_pen = QPen(QColor("#252D38"), stroke_width)
        bg_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(rect, 0, 360 * 16)

        # 2. Foreground Progress Arc with Gradient
        if self._has_data and self._percentage > 0:
            gradient = QLinearGradient(0, 0, w, h)
            gradient.setColorAt(0.0, self._color_start)
            gradient.setColorAt(1.0, self._color_end)

            prog_pen = QPen(gradient, stroke_width)
            prog_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(prog_pen)

            start_angle = 90 * 16 # Start from top (12 o'clock)
            span_angle = -int(self._percentage * 3.6 * 16) # Clockwise
            painter.drawArc(rect, start_angle, span_angle)

        # 3. Inner text display
        painter.setPen(QColor("#FFFFFF") if self._has_data else QColor("#8F9CAE"))
        font = QFont()
        font.setBold(True)
        if self._has_data:
            font.setPointSize(11)
            painter.setFont(font)
            text = f"{self._percentage:.0f}%"
        else:
            font.setPointSize(11)
            painter.setFont(font)
            text = "—%"

        painter.drawText(self.rect(), Qt.AlignCenter, text)
        painter.end()


class CourseCard(QFrame):
    def __init__(self, course: Course, parent_screen: SemesterScreen):
        super().__init__()
        self.course = course
        self.parent_screen = parent_screen

        has_happened = course.classes_happened > 0
        min_target = course.min_attendance or 75
        pct = (course.classes_attended / course.classes_happened * 100) if has_happened else 0.0

        # Determine health mode and colors
        if not has_happened:
            health_mode = "nodata"
            accent_color = "#3A4454"
            border_glow = "rgba(58, 68, 84, 0.4)"
        elif pct >= min_target:
            # Check if borderline (within 3% of min_target or 0 safe leaves)
            safe_leaves = course.calculate_safe_leaves()
            if safe_leaves == 0 or (pct - min_target < 3.0):
                health_mode = "borderline"
                accent_color = "#F59E0B"
                border_glow = "rgba(245, 158, 11, 0.35)"
            else:
                health_mode = "safe"
                accent_color = "#10B981"
                border_glow = "rgba(16, 185, 129, 0.35)"
        else:
            health_mode = "alert"
            accent_color = "#EF4444"
            border_glow = "rgba(239, 68, 68, 0.35)"

        self.setObjectName("CourseCard")
        # 4px left accent strip with subtle glowing border
        self.setStyleSheet(f"""
            QFrame#CourseCard {{
                background-color: #181C24;
                border: 1px solid {border_glow};
                border-left: 4px solid {accent_color};
                border-radius: 12px;
            }}
        """)

        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(18, 16, 20, 16)
        card_layout.setSpacing(12)

        # Top row: Title, badges, delete button
        top_row = QHBoxLayout()

        name_lbl = QLabel(course.name)
        name_font = QFont()
        name_font.setPointSize(14)
        name_font.setBold(True)
        name_lbl.setFont(name_font)
        name_lbl.setStyleSheet("color: #FFFFFF; border: none;")
        top_row.addWidget(name_lbl)

        is_lab = isinstance(course, LabCourses) or course.periods > 1
        type_text = f"Lab ({course.periods} periods)" if is_lab else f"Theory ({course.periods} period)"
        type_badge = QLabel(type_text)
        type_badge.setStyleSheet("background-color: #263345; color: #64B5F6; font-size: 11px; font-weight: bold; border-radius: 6px; padding: 3px 8px; border: none;")
        top_row.addWidget(type_badge)

        credits_badge = QLabel(f"{course.credits} Credits")
        credits_badge.setStyleSheet("background-color: #2C333D; color: #CBD5E1; font-size: 11px; border-radius: 6px; padding: 3px 8px; border: none;")
        top_row.addWidget(credits_badge)

        top_row.addStretch()

        del_btn = QPushButton("✕")
        del_btn.setFixedSize(28, 28)
        del_btn.setCursor(QCursor(Qt.PointingHandCursor))
        del_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #8F9CAE;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3D2323;
                color: #FFA4A4;
            }
        """)
        del_btn.clicked.connect(self.delete_course)
        top_row.addWidget(del_btn)

        card_layout.addLayout(top_row)

        # Middle row: Circular Progress Gauge + Detailed Stats
        mid_row = QHBoxLayout()
        mid_row.setSpacing(16)

        # Circular Gauge
        self.circular_gauge = CircularProgressWidget(size=76)
        self.circular_gauge.set_data(pct, has_happened, health_mode)
        mid_row.addWidget(self.circular_gauge, alignment=Qt.AlignVCenter)

        # Stats Column
        stats_col = QVBoxLayout()
        stats_col.setSpacing(4)

        if has_happened:
            pct_formatted = f"{pct:.1f}%"
            val_lbl = QLabel(f"{pct_formatted} Attendance")
            val_lbl.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {accent_color}; border: none;")
        else:
            val_lbl = QLabel("No Classes Held Yet")
            val_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #8F9CAE; border: none;")
        stats_col.addWidget(val_lbl)

        count_str = f"Attended: {course.classes_attended} of {course.classes_happened} period{'s' if course.classes_happened != 1 else ''}"
        if course.total_classes > 0:
            count_str += f" • Estimated Semester Total: {course.total_classes}"
        count_lbl = QLabel(count_str)
        count_lbl.setStyleSheet("font-size: 12px; color: #8F9CAE; border: none;")
        stats_col.addWidget(count_lbl)

        target_info = QLabel(f"Minimum Requirement: {min_target}%")
        target_info.setStyleSheet("font-size: 11px; color: #64748B; border: none;")
        stats_col.addWidget(target_info)

        mid_row.addLayout(stats_col)
        mid_row.addStretch()

        card_layout.addLayout(mid_row)

        # Smart Insights Frame
        insight_frame = QFrame()
        insight_frame.setStyleSheet("background-color: #242B35; border: none; border-radius: 8px;")
        insight_layout = QHBoxLayout(insight_frame)
        insight_layout.setContentsMargins(12, 8, 12, 8)

        if not has_happened:
            insight_text = "ℹ No classes have occurred yet. Use '+ Present' or '- Absent' when classes take place."
            insight_color = "#8F9CAE"
        else:
            if pct >= min_target:
                safe_leaves = course.calculate_safe_leaves()
                if safe_leaves > 0:
                    insight_text = f"✓ Safe Leaves: You can safely miss up to {safe_leaves} slot(s) and remain above {min_target}%."
                    insight_color = "#10B981"
                else:
                    insight_text = f"⚠ Borderline: Currently at or near {min_target}%. Missing the next class will lower your standing."
                    insight_color = "#F59E0B"
            else:
                recovery = course.regain_min_attendance()
                if recovery is False:
                    insight_text = f"⚠ Critical: Mathematically impossible to reach {min_target}% with remaining classes."
                    insight_color = "#EF4444"
                else:
                    insight_text = f"⚠ Recovery: You must attend the next {recovery} consecutive slot(s) to reach {min_target}%."
                    insight_color = "#EF4444"

        insight_lbl = QLabel(insight_text)
        insight_lbl.setStyleSheet(f"font-size: 12px; font-weight: {'bold' if has_happened else 'normal'}; color: {insight_color}; border: none;")
        insight_layout.addWidget(insight_lbl)

        card_layout.addWidget(insight_frame)

        # Action buttons
        actions_row = QHBoxLayout()

        present_btn = QPushButton("+ Present")
        present_btn.setObjectName("SuccessBtn")
        present_btn.setCursor(QCursor(Qt.PointingHandCursor))
        present_btn.clicked.connect(lambda: self.log_presence(True))
        actions_row.addWidget(present_btn)

        absent_btn = QPushButton("- Absent")
        absent_btn.setObjectName("DangerBtn")
        absent_btn.setCursor(QCursor(Qt.PointingHandCursor))
        absent_btn.clicked.connect(lambda: self.log_presence(False))
        actions_row.addWidget(absent_btn)

        undo_btn = QPushButton("↺ Undo Last")
        undo_btn.setCursor(QCursor(Qt.PointingHandCursor))
        undo_btn.clicked.connect(self.undo_last)
        actions_row.addWidget(undo_btn)

        actions_row.addStretch()

        simulator_btn = QPushButton("⚡ Simulate")
        simulator_btn.setObjectName("SimulatorBtn")
        simulator_btn.setCursor(QCursor(Qt.PointingHandCursor))
        simulator_btn.clicked.connect(self.open_simulator_dialog)
        actions_row.addWidget(simulator_btn)

        adjust_btn = QPushButton("⚙ Adjust")
        adjust_btn.setCursor(QCursor(Qt.PointingHandCursor))
        adjust_btn.clicked.connect(self.open_edit_dialog)
        actions_row.addWidget(adjust_btn)

        card_layout.addLayout(actions_row)

    def open_simulator_dialog(self) -> None:
        dialog = WhatIfSimulatorDialog(self.course, self.parent_screen)
        dialog.exec()

    def log_presence(self, attended: bool) -> None:
        self.course.log_attendance(attended)
        self.parent_screen.controller.save_data()
        self.parent_screen.refresh_view()

    def undo_last(self) -> None:
        if self.course.classes_happened < self.course.periods:
            return
        dialog = UndoChoiceDialog(self.course, self.parent_screen)
        if dialog.exec():
            self.parent_screen.controller.save_data()
            self.parent_screen.refresh_view()

    def open_edit_dialog(self) -> None:
        dialog = EditCourseDialog(self.course, self.parent_screen)
        if dialog.exec():
            self.parent_screen.controller.save_data()
            self.parent_screen.refresh_view()

    def delete_course(self) -> None:
        self.parent_screen.current_semester.remove_course(self.course)
        self.parent_screen.controller.save_data()
        self.parent_screen.refresh_view()


class AddCourseDialog(QDialog):
    def __init__(self, semester: Semester, parent=None):
        super().__init__(parent)
        self.semester = semester
        self.setWindowTitle("Add New Course")
        self.setFixedSize(480, 560)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(14)

        title_lbl = QLabel("Add Course Details")
        title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF;")
        main_layout.addWidget(title_lbl)

        # Course name
        name_lbl = QLabel("Course Name")
        name_lbl.setStyleSheet("font-size: 12px; font-weight: bold; color: #8F9CAE;")
        main_layout.addWidget(name_lbl)
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("e.g. Operating Systems")
        main_layout.addWidget(self.name_entry)

        # Course type
        type_lbl = QLabel("Course Type")
        type_lbl.setStyleSheet("font-size: 12px; font-weight: bold; color: #8F9CAE;")
        main_layout.addWidget(type_lbl)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Theory (1 period/slot)", "Lab (3 periods/slot)"])
        self.type_combo.currentIndexChanged.connect(self._on_type_change)
        main_layout.addWidget(self.type_combo)

        # Credits & Periods row
        row1 = QHBoxLayout()
        credits_box = QVBoxLayout()
        credits_lbl = QLabel("Credits (1-6)")
        credits_lbl.setStyleSheet("font-size: 12px; font-weight: bold; color: #8F9CAE;")
        credits_box.addWidget(credits_lbl)
        self.credits_entry = QLineEdit("4")
        credits_box.addWidget(self.credits_entry)
        row1.addLayout(credits_box)

        periods_box = QVBoxLayout()
        periods_lbl = QLabel("Periods per Slot")
        periods_lbl.setStyleSheet("font-size: 12px; font-weight: bold; color: #8F9CAE;")
        periods_box.addWidget(periods_lbl)
        self.periods_entry = QLineEdit("1")
        periods_box.addWidget(self.periods_entry)
        row1.addLayout(periods_box)
        main_layout.addLayout(row1)

        # Target Min Attendance
        target_lbl = QLabel("Minimum Attendance Target (%)")
        target_lbl.setStyleSheet("font-size: 12px; font-weight: bold; color: #8F9CAE;")
        main_layout.addWidget(target_lbl)
        self.target_entry = QLineEdit(str(self.semester.min_attendance))
        main_layout.addWidget(self.target_entry)

        # Estimated duration (optional)
        dur_lbl = QLabel("Estimated Semester Duration (Optional)")
        dur_lbl.setStyleSheet("font-size: 12px; font-weight: bold; color: #8F9CAE;")
        main_layout.addWidget(dur_lbl)
        row2 = QHBoxLayout()
        self.months_entry = QLineEdit("4")
        self.months_entry.setPlaceholderText("Months (e.g. 4)")
        row2.addWidget(self.months_entry)
        self.weeks_entry = QLineEdit("0")
        self.weeks_entry.setPlaceholderText("Weeks (e.g. 0)")
        row2.addWidget(self.weeks_entry)
        main_layout.addLayout(row2)

        self.error_lbl = QLabel("")
        self.error_lbl.setStyleSheet("color: #E74C3C; font-size: 12px;")
        main_layout.addWidget(self.error_lbl)

        main_layout.addStretch()

        # Action buttons pinned at bottom
        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        confirm_btn = QPushButton("✓ Confirm & Add Course")
        confirm_btn.setObjectName("PrimaryBtn")
        confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))
        confirm_btn.clicked.connect(self._save_course)
        btn_layout.addWidget(confirm_btn)

        main_layout.addLayout(btn_layout)

    def _on_type_change(self, index: int) -> None:
        if index == 1: # Lab
            self.periods_entry.setText("3")
        else:
            self.periods_entry.setText("1")

    def _save_course(self) -> None:
        name = self.name_entry.text().strip()
        if not name:
            self.error_lbl.setText("Please enter a course name.")
            return

        try:
            credits = int(self.credits_entry.text().strip())
            if not (1 <= credits <= 6):
                raise ValueError
        except ValueError:
            self.error_lbl.setText("Credits must be an integer between 1 and 6.")
            return

        try:
            periods = int(self.periods_entry.text().strip())
            if periods <= 0:
                raise ValueError
        except ValueError:
            self.error_lbl.setText("Periods per slot must be a positive integer.")
            return

        try:
            target = int(self.target_entry.text().strip())
            if not (0 <= target <= 100):
                raise ValueError
        except ValueError:
            self.error_lbl.setText("Target attendance must be between 0 and 100.")
            return

        is_lab = self.type_combo.currentIndex() == 1
        if is_lab:
            course = LabCourses(name=name, credits=credits, periods_per_lab=periods, min_attendance=target)
        else:
            course = TheoryCourses(name=name, credits=credits, periods_per_theory_class=periods, min_attendance=target)

        try:
            months = int(self.months_entry.text().strip() or "0")
            weeks = int(self.weeks_entry.text().strip() or "0")
            if months > 0 or weeks > 0:
                course.calculate_total_classes(months=months, weeks=weeks)
        except ValueError:
            pass

        self.semester.add_course(course)
        self.accept()


class EditCourseDialog(QDialog):
    def __init__(self, course: Course, parent=None):
        super().__init__(parent)
        self.course = course
        self.setWindowTitle(f"Adjust - {course.name}")
        self.setFixedSize(400, 380)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title_lbl = QLabel(f"Adjust Attendance Data")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(title_lbl)

        sub_lbl = QLabel(course.name)
        sub_lbl.setStyleSheet("font-size: 12px; color: #8F9CAE;")
        layout.addWidget(sub_lbl)

        layout.addWidget(QLabel("Total Periods Held (Happened)"))
        self.happened_entry = QLineEdit(str(course.classes_happened))
        layout.addWidget(self.happened_entry)

        layout.addWidget(QLabel("Periods Attended"))
        self.attended_entry = QLineEdit(str(course.classes_attended))
        layout.addWidget(self.attended_entry)

        # On-Duty and Medical Leave Row
        od_ml_row = QHBoxLayout()
        od_box = QVBoxLayout()
        od_box.addWidget(QLabel("Approved OD Periods"))
        self.od_entry = QLineEdit(str(course.od_periods))
        od_box.addWidget(self.od_entry)
        od_ml_row.addLayout(od_box)

        ml_box = QVBoxLayout()
        ml_box.addWidget(QLabel("Medical Leave Periods"))
        self.ml_entry = QLineEdit(str(course.ml_periods))
        ml_box.addWidget(self.ml_entry)
        od_ml_row.addLayout(ml_box)
        layout.addLayout(od_ml_row)

        layout.addWidget(QLabel("Total Classes in Semester (Optional)"))
        self.total_entry = QLineEdit(str(course.total_classes))
        layout.addWidget(self.total_entry)

        self.error_lbl = QLabel("")
        self.error_lbl.setStyleSheet("color: #E74C3C; font-size: 12px;")
        layout.addWidget(self.error_lbl)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save Changes")
        save_btn.setObjectName("PrimaryBtn")
        save_btn.clicked.connect(self._save_changes)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def _save_changes(self) -> None:
        try:
            happened = int(self.happened_entry.text().strip())
            attended = int(self.attended_entry.text().strip())
            od = int(self.od_entry.text().strip() or "0")
            ml = int(self.ml_entry.text().strip() or "0")
            total = int(self.total_entry.text().strip() or "0")

            if happened < 0 or attended < 0 or od < 0 or ml < 0 or total < 0:
                raise ValueError
            if attended > happened:
                self.error_lbl.setText("Attended periods cannot exceed happened periods.")
                return

            self.course.classes_happened = happened
            self.course.classes_attended = attended
            self.course.od_periods = od
            self.course.ml_periods = ml
            self.course.total_classes = total
            self.accept()
        except ValueError:
            self.error_lbl.setText("Please enter valid non-negative numbers.")


class UndoChoiceDialog(QDialog):
    def __init__(self, course: Course, parent=None):
        super().__init__(parent)
        self.course = course
        self.setWindowTitle("Undo Attendance")
        self.setFixedSize(360, 200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title_lbl = QLabel("Undo Last Log")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(title_lbl)

        desc_lbl = QLabel(f"What was the last logged attendance for {course.name}?")
        desc_lbl.setStyleSheet("font-size: 12px; color: #8F9CAE;")
        layout.addWidget(desc_lbl)

        btn_layout = QHBoxLayout()
        present_btn = QPushButton("Undo Present (+)")
        present_btn.setObjectName("SuccessBtn")
        present_btn.setCursor(QCursor(Qt.PointingHandCursor))
        present_btn.clicked.connect(lambda: self._apply(True))
        btn_layout.addWidget(present_btn)

        absent_btn = QPushButton("Undo Absent (-)")
        absent_btn.setObjectName("DangerBtn")
        absent_btn.setCursor(QCursor(Qt.PointingHandCursor))
        absent_btn.clicked.connect(lambda: self._apply(False))
        btn_layout.addWidget(absent_btn)
        layout.addLayout(btn_layout)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

    def _apply(self, attended: bool) -> None:
        self.course.undo_attendance(attended)
        self.accept()


class WhatIfSimulatorDialog(QDialog):
    """Interactive simulator allowing students to test scenarios:
    'What if I attend the next N slots?' vs 'What if I miss the next N slots?'
    """
    def __init__(self, course: Course, parent=None):
        super().__init__(parent)
        self.course = course
        self.setWindowTitle(f"What-If Simulator • {course.name}")
        self.setFixedSize(500, 520)

        # Baseline metrics
        self.current_happened = course.classes_happened
        self.current_attended = course.classes_attended
        self.target_pct = course.min_attendance if course.min_attendance is not None else 75
        self.periods_per_slot = course.periods

        self.current_pct = (
            (self.current_attended / self.current_happened) * 100
            if self.current_happened > 0
            else 0.0
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(16)

        # 1. Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        title_lbl = QLabel("What-If Attendance Simulator")
        title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF;")
        header_layout.addWidget(title_lbl)

        sub_lbl = QLabel(f"Forecast your future attendance for {course.name}")
        sub_lbl.setStyleSheet("font-size: 12px; color: #8F9CAE;")
        header_layout.addWidget(sub_lbl)
        layout.addLayout(header_layout)

        # 2. Mode Selector: Attend vs Miss
        mode_frame = QFrame()
        mode_frame.setStyleSheet("""
            QFrame {
                background-color: #181C24;
                border: 1px solid #2C333D;
                border-radius: 10px;
            }
        """)
        mode_layout = QHBoxLayout(mode_frame)
        mode_layout.setContentsMargins(16, 10, 16, 10)

        self.btn_group = QButtonGroup(self)
        self.radio_attend = QRadioButton("Attend next classes (Boost)")
        self.radio_attend.setChecked(True)
        self.radio_attend.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_attend.setStyleSheet("color: #2ECC71; font-weight: bold; font-size: 13px;")

        self.radio_miss = QRadioButton("Miss / Bunk next classes (Drop)")
        self.radio_miss.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_miss.setStyleSheet("color: #E74C3C; font-weight: bold; font-size: 13px;")

        self.btn_group.addButton(self.radio_attend, 1)
        self.btn_group.addButton(self.radio_miss, 2)
        self.btn_group.idToggled.connect(self._recalculate)

        mode_layout.addWidget(self.radio_attend)
        mode_layout.addWidget(self.radio_miss)
        layout.addWidget(mode_frame)

        # 3. Interactive Stepper & Preset Chips Section (Replacing Slider)
        input_card = QFrame()
        input_card.setStyleSheet("""
            QFrame {
                background-color: #181C24;
                border: 1px solid #2C333D;
                border-radius: 12px;
            }
        """)
        input_card_layout = QVBoxLayout(input_card)
        input_card_layout.setContentsMargins(20, 16, 20, 16)
        input_card_layout.setSpacing(14)

        input_top_row = QHBoxLayout()
        input_label = QLabel("Number of upcoming slots:")
        input_label.setStyleSheet("color: #CBD5E1; font-size: 13px; font-weight: 500;")
        input_top_row.addWidget(input_label)

        self.periods_summary_lbl = QLabel(f"(1 slot = {self.periods_per_slot} period{'s' if self.periods_per_slot != 1 else ''})")
        self.periods_summary_lbl.setStyleSheet("color: #64748B; font-size: 12px;")
        input_top_row.addWidget(self.periods_summary_lbl)
        input_top_row.addStretch()
        input_card_layout.addLayout(input_top_row)

        # Stepper Row
        stepper_row = QHBoxLayout()
        stepper_row.setSpacing(12)

        self.dec_btn = QPushButton("−")
        self.dec_btn.setProperty("class", "StepperBtn")
        self.dec_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.dec_btn.clicked.connect(lambda: self._change_slots(-1))
        stepper_row.addWidget(self.dec_btn)

        self.slots_spin = QSpinBox()
        self.slots_spin.setRange(1, 100)
        self.slots_spin.setValue(1)
        self.slots_spin.setFixedHeight(38)
        self.slots_spin.setMinimumWidth(80)
        self.slots_spin.setAlignment(Qt.AlignCenter)
        self.slots_spin.setStyleSheet("""
            QSpinBox {
                background-color: #12151C;
                color: #FFFFFF;
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #3B4758;
                border-radius: 8px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
                border: none;
            }
        """)
        self.slots_spin.valueChanged.connect(self._on_slots_changed)
        stepper_row.addWidget(self.slots_spin)

        self.inc_btn = QPushButton("+")
        self.inc_btn.setProperty("class", "StepperBtn")
        self.inc_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.inc_btn.clicked.connect(lambda: self._change_slots(1))
        stepper_row.addWidget(self.inc_btn)

        self.slot_unit_lbl = QLabel("slot(s)")
        self.slot_unit_lbl.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: bold;")
        stepper_row.addWidget(self.slot_unit_lbl)

        stepper_row.addStretch()
        input_card_layout.addLayout(stepper_row)

        # Quick Preset Chips Row
        presets_row = QHBoxLayout()
        presets_row.setSpacing(8)
        preset_title = QLabel("Quick Presets:")
        preset_title.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 600;")
        presets_row.addWidget(preset_title)

        for val in [1, 2, 3, 5, 10]:
            btn = QPushButton(f"{val} slot{'s' if val > 1 else ''}")
            btn.setProperty("class", "PresetChip")
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.clicked.connect(lambda checked, v=val: self.slots_spin.setValue(v))
            presets_row.addWidget(btn)

        presets_row.addStretch()
        input_card_layout.addLayout(presets_row)

        layout.addWidget(input_card)

        # 4. Result Projection Card
        self.result_card = QFrame()
        self.result_card.setStyleSheet("""
            QFrame {
                background-color: #1A212D;
                border: 1px solid #2C3748;
                border-radius: 12px;
            }
        """)
        result_layout = QVBoxLayout(self.result_card)
        result_layout.setContentsMargins(20, 16, 20, 16)
        result_layout.setSpacing(10)

        proj_row = QHBoxLayout()
        # Current vs Projected
        curr_box = QVBoxLayout()
        curr_title = QLabel("Current Standing")
        curr_title.setStyleSheet("color: #8F9CAE; font-size: 11px;")
        curr_box.addWidget(curr_title)

        curr_text = f"{self.current_pct:.1f}%" if self.current_happened > 0 else "—%"
        self.curr_val_lbl = QLabel(curr_text)
        self.curr_val_lbl.setStyleSheet("color: #FFFFFF; font-size: 20px; font-weight: bold;")
        curr_box.addWidget(self.curr_val_lbl)
        proj_row.addLayout(curr_box)

        arrow_lbl = QLabel("➔")
        arrow_lbl.setStyleSheet("color: #64748B; font-size: 20px; font-weight: bold; margin: 0 10px;")
        proj_row.addWidget(arrow_lbl, alignment=Qt.AlignCenter)

        proj_box = QVBoxLayout()
        proj_title = QLabel("Projected Standing")
        proj_title.setStyleSheet("color: #8F9CAE; font-size: 11px;")
        proj_box.addWidget(proj_title)

        self.proj_val_lbl = QLabel("0.0%")
        self.proj_val_lbl.setStyleSheet("color: #2ECC71; font-size: 20px; font-weight: bold;")
        proj_box.addWidget(self.proj_val_lbl)
        proj_row.addLayout(proj_box)

        # Delta Badge
        self.delta_badge = QLabel("+0.0%")
        self.delta_badge.setStyleSheet("""
            background-color: #1E3A2F;
            color: #2ECC71;
            font-size: 12px;
            font-weight: bold;
            border-radius: 8px;
            padding: 5px 12px;
        """)
        proj_row.addWidget(self.delta_badge, alignment=Qt.AlignRight | Qt.AlignVCenter)

        result_layout.addLayout(proj_row)

        # Progress bar
        self.proj_progress = QProgressBar()
        self.proj_progress.setFixedHeight(8)
        self.proj_progress.setTextVisible(False)
        self.proj_progress.setRange(0, 100)
        result_layout.addWidget(self.proj_progress)

        # Status text explanation
        self.explanation_lbl = QLabel()
        self.explanation_lbl.setWordWrap(True)
        self.explanation_lbl.setStyleSheet("color: #CBD5E1; font-size: 12px; line-height: 1.4;")
        result_layout.addWidget(self.explanation_lbl)

        layout.addWidget(self.result_card)

        layout.addStretch()

        # 5. Close Button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Done")
        close_btn.setObjectName("PrimaryBtn")
        close_btn.setFixedWidth(100)
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        # Initial calculation
        self._recalculate()

    def _change_slots(self, delta: int) -> None:
        new_val = max(1, min(100, self.slots_spin.value() + delta))
        self.slots_spin.setValue(new_val)

    def _on_slots_changed(self, value: int) -> None:
        self._recalculate()

    def _recalculate(self) -> None:
        slots = self.slots_spin.value()
        additional_periods = slots * self.periods_per_slot
        sim_happened = self.current_happened + additional_periods

        is_attend_mode = self.radio_attend.isChecked()
        if is_attend_mode:
            sim_attended = self.current_attended + additional_periods
        else:
            sim_attended = self.current_attended

        sim_pct = (sim_attended / sim_happened) * 100 if sim_happened > 0 else 0.0

        # Delta calculation
        if self.current_happened > 0:
            diff = sim_pct - self.current_pct
            diff_str = f"+{diff:.1f}%" if diff >= 0 else f"{diff:.1f}%"
        else:
            diff_str = f"{sim_pct:.1f}%"

        # Safe / unsafe colors
        is_safe = sim_pct >= self.target_pct
        pct_color = "#2ECC71" if is_safe else "#E74C3C"

        self.proj_val_lbl.setText(f"{sim_pct:.1f}%")
        self.proj_val_lbl.setStyleSheet(f"color: {pct_color}; font-size: 20px; font-weight: bold;")

        if is_attend_mode:
            self.delta_badge.setText(diff_str)
            self.delta_badge.setStyleSheet("background-color: #1E3A2F; color: #2ECC71; font-size: 12px; font-weight: bold; border-radius: 8px; padding: 5px 12px;")
        else:
            self.delta_badge.setText(diff_str)
            self.delta_badge.setStyleSheet("background-color: #3D2323; color: #E74C3C; font-size: 12px; font-weight: bold; border-radius: 8px; padding: 5px 12px;")

        # Progress bar
        self.proj_progress.setValue(int(min(100, max(0, sim_pct))))
        self.proj_progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: #2C333D;
                border: none;
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {pct_color};
                border-radius: 4px;
            }}
        """)

        # Explanatory verdict
        unit_text = f"{slots} upcoming slot{'s' if slots > 1 else ''}"
        if is_attend_mode:
            if is_safe:
                self.explanation_lbl.setText(
                    f"✓ Attending {unit_text} will raise your attendance to <b>{sim_pct:.1f}%</b>, keeping you comfortably above the {self.target_pct}% threshold."
                )
            else:
                self.explanation_lbl.setText(
                    f"Attending {unit_text} will improve your attendance to <b>{sim_pct:.1f}%</b>, but you still need more classes to reach the {self.target_pct}% target."
                )
        else:
            if is_safe:
                self.explanation_lbl.setText(
                    f"✓ Missing {unit_text} will lower your attendance to <b>{sim_pct:.1f}%</b>. You will remain above your {self.target_pct}% requirement."
                )
            else:
                self.explanation_lbl.setText(
                    f"⚠ Missing {unit_text} will drop your attendance to <b>{sim_pct:.1f}%</b>, falling below your {self.target_pct}% target!"
                )
