from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QProgressBar, QDialog, QLineEdit,
    QComboBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
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

        # Stat 3: Target Minimum
        target_box = QVBoxLayout()
        self.stat_target_val = QLabel("75%")
        self.stat_target_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #FFFFFF; border: none;")
        target_box.addWidget(self.stat_target_val)
        target_lbl = QLabel("Target Minimum")
        target_lbl.setStyleSheet("font-size: 12px; color: #8F9CAE; border: none;")
        target_box.addWidget(target_lbl)
        stats_layout.addLayout(target_box)

        stats_layout.addStretch()

        # Stat 4: Standing status badge
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

        if total_happened > 0:
            pct = (total_attended / total_happened) * 100
            self.stat_overall_val.setText(f"{pct:.1f}%")
            if pct >= self.current_semester.min_attendance:
                self.stat_overall_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #2ECC71; border: none;")
                self.status_badge.setText("✓ In Good Standing")
                self.status_badge.setStyleSheet("background-color: #1E3A2F; color: #2ECC71; font-size: 12px; font-weight: bold; border-radius: 10px; padding: 6px 16px; border: none;")
            else:
                self.stat_overall_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #E74C3C; border: none;")
                self.status_badge.setText("⚠ Attention Needed")
                self.status_badge.setStyleSheet("background-color: #3D2323; color: #E74C3C; font-size: 12px; font-weight: bold; border-radius: 10px; padding: 6px 16px; border: none;")
        else:
            self.stat_overall_val.setText("—%")
            self.stat_overall_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #8F9CAE; border: none;")
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


class CourseCard(QFrame):
    def __init__(self, course: Course, parent_screen: SemesterScreen):
        super().__init__()
        self.course = course
        self.parent_screen = parent_screen

        self.setObjectName("CourseCard")
        self.setStyleSheet("""
            QFrame#CourseCard {
                background-color: #181C24;
                border: 1px solid #2C333D;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(20, 16, 20, 16)
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

        # Middle row: Percentage & Progress
        mid_row = QHBoxLayout()

        has_happened = course.classes_happened > 0
        min_target = course.min_attendance or 75
        if has_happened:
            pct = course.attendance_percentage(float)
            pct_text = f"{pct:.1f}%"
            is_above = pct >= min_target
            pct_color = "#2ECC71" if is_above else "#E74C3C"
            int_pct = int(min(100, max(0, pct)))
        else:
            pct_text = "—%"
            pct_color = "#8F9CAE"
            is_above = True
            int_pct = 0

        pct_lbl = QLabel(pct_text)
        pct_lbl.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {pct_color}; border: none;")
        pct_lbl.setFixedWidth(80)
        mid_row.addWidget(pct_lbl)

        prog_layout = QVBoxLayout()
        count_str = f"Attended: {course.classes_attended} / {course.classes_happened} periods"
        if course.total_classes > 0:
            count_str += f" (Est. Total: {course.total_classes})"
        count_lbl = QLabel(count_str)
        count_lbl.setStyleSheet("font-size: 12px; color: #8F9CAE; border: none;")
        prog_layout.addWidget(count_lbl)

        prog_bar = QProgressBar()
        prog_bar.setFixedHeight(8)
        prog_bar.setTextVisible(False)
        prog_bar.setRange(0, 100)
        prog_bar.setValue(int_pct)
        prog_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #2C333D;
                border: none;
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {pct_color if has_happened else "#373F4B"};
                border-radius: 4px;
            }}
        """)
        prog_layout.addWidget(prog_bar)
        mid_row.addLayout(prog_layout)

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
            if is_above:
                safe_leaves = course.calculate_safe_leaves()
                if safe_leaves > 0:
                    insight_text = f"✓ Safe Leaves: You can safely miss up to {safe_leaves} slot(s) and remain above {min_target}%."
                    insight_color = "#2ECC71"
                else:
                    insight_text = f"⚠ Borderline: Currently at or near {min_target}%. Missing the next class will lower your standing."
                    insight_color = "#F39C12"
            else:
                recovery = course.regain_min_attendance()
                if recovery is False:
                    insight_text = f"⚠ Critical: Mathematically impossible to reach {min_target}% with remaining classes."
                    insight_color = "#E74C3C"
                else:
                    insight_text = f"⚠ Recovery: You must attend the next {recovery} consecutive slot(s) to reach {min_target}%."
                    insight_color = "#E74C3C"

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

        adjust_btn = QPushButton("⚙ Adjust")
        adjust_btn.setCursor(QCursor(Qt.PointingHandCursor))
        adjust_btn.clicked.connect(self.open_edit_dialog)
        actions_row.addWidget(adjust_btn)

        card_layout.addLayout(actions_row)

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
            total = int(self.total_entry.text().strip() or "0")

            if happened < 0 or attended < 0 or total < 0:
                raise ValueError
            if attended > happened:
                self.error_lbl.setText("Attended periods cannot exceed happened periods.")
                return

            self.course.classes_happened = happened
            self.course.classes_attended = attended
            self.course.total_classes = total
            self.accept()
        except ValueError:
            self.error_lbl.setText("Please enter valid positive numbers.")


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
