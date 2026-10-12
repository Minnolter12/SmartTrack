import customtkinter as ctk
from src.courses import Semester, Course, TheoryCourses, LabCourses

class SemesterScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.current_semester: Semester | None = None

        # --- Top Navigation & Header Bar ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(side="top", fill="x", pady=(0, 15))

        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="← Back to Home",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2C333D",
            hover_color="#373F4B",
            corner_radius=8,
            width=130,
            height=36,
            command=self.go_back
        )
        self.back_button.pack(side="left", padx=(0, 15))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Semester Overview",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left")

        # Right side action buttons
        self.header_actions = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.header_actions.pack(side="right")

        self.add_course_button = ctk.CTkButton(
            self.header_actions,
            text="+ Add Course",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3B8ED0",
            hover_color="#2A6F9E",
            corner_radius=8,
            width=120,
            height=36,
            command=self.open_add_course_dialog
        )
        self.add_course_button.pack(side="left", padx=5)

        self.delete_sem_button = ctk.CTkButton(
            self.header_actions,
            text="Delete Semester",
            font=ctk.CTkFont(size=12),
            fg_color="#5A2E2E",
            hover_color="#7A3636",
            text_color="#FFA4A4",
            corner_radius=8,
            width=120,
            height=36,
            command=self.confirm_delete_semester
        )
        self.delete_sem_button.pack(side="left", padx=5)

        # --- Semester Summary Stats Bar ---
        self.stats_bar = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E232B", border_width=1, border_color="#2C333D")
        self.stats_bar.pack(side="top", fill="x", pady=(0, 15), ipady=10)

        self.stats_content = ctk.CTkFrame(self.stats_bar, fg_color="transparent")
        self.stats_content.pack(fill="both", expand=True, padx=20, pady=10)

        # Stat 1: Overall Attendance
        self.stat_overall_val = ctk.CTkLabel(self.stats_content, text="0.0%", font=ctk.CTkFont(size=22, weight="bold"))
        self.stat_overall_val.grid(row=0, column=0, sticky="w", padx=(0, 30))
        self.stat_overall_lbl = ctk.CTkLabel(self.stats_content, text="Overall Attendance", text_color="#8F9CAE", font=ctk.CTkFont(size=12))
        self.stat_overall_lbl.grid(row=1, column=0, sticky="w", padx=(0, 30))

        # Stat 2: Total Courses
        self.stat_courses_val = ctk.CTkLabel(self.stats_content, text="0", font=ctk.CTkFont(size=22, weight="bold"))
        self.stat_courses_val.grid(row=0, column=1, sticky="w", padx=30)
        self.stat_courses_lbl = ctk.CTkLabel(self.stats_content, text="Enrolled Courses", text_color="#8F9CAE", font=ctk.CTkFont(size=12))
        self.stat_courses_lbl.grid(row=1, column=1, sticky="w", padx=30)

        # Stat 3: Target Minimum
        self.stat_target_val = ctk.CTkLabel(self.stats_content, text="75%", font=ctk.CTkFont(size=22, weight="bold"))
        self.stat_target_val.grid(row=0, column=2, sticky="w", padx=30)
        self.stat_target_lbl = ctk.CTkLabel(self.stats_content, text="Target Minimum", text_color="#8F9CAE", font=ctk.CTkFont(size=12))
        self.stat_target_lbl.grid(row=1, column=2, sticky="w", padx=30)

        # Stat 4: Standing status pill
        self.status_pill = ctk.CTkLabel(
            self.stats_content,
            text="No Data",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2C333D",
            text_color="#CBD5E1",
            corner_radius=12,
            padx=16,
            pady=6
        )
        self.status_pill.grid(row=0, column=3, rowspan=2, sticky="e", padx=(40, 0))
        self.stats_content.grid_columnconfigure(3, weight=1)

        # --- Courses Scrollable Container ---
        self.courses_scroll = ctk.CTkScrollableFrame(
            self,
            corner_radius=15,
            fg_color="transparent"
        )
        self.courses_scroll.pack(fill="both", expand=True)

    def set_semester(self, semester: Semester) -> None:
        """Load and display the given Semester."""
        self.current_semester = semester
        self.title_label.configure(text=f"Semester {semester.sem_number}")
        self.stat_target_val.configure(text=f"{semester.min_attendance}%")
        self.refresh_view()

    def go_back(self) -> None:
        """Return to the HomeScreen."""
        if hasattr(self.controller, "frames") and "HomeScreen" in self.controller.frames:
            self.controller.frames["HomeScreen"].refresh_semester_row()
        self.controller.show_page("HomeScreen")

    def refresh_view(self) -> None:
        """Redraw all courses and update statistics."""
        if not self.current_semester:
            return

        # Clear existing course cards
        for widget in self.courses_scroll.winfo_children():
            widget.destroy()

        courses = self.current_semester.courses
        self.stat_courses_val.configure(text=str(len(courses)))

        # Calculate overall stats
        total_attended_periods = sum(c.classes_attended for c in courses)
        total_happened_periods = sum(c.classes_happened for c in courses)

        if total_happened_periods > 0:
            overall_pct = (total_attended_periods / total_happened_periods) * 100
            self.stat_overall_val.configure(text=f"{overall_pct:.1f}%")
            if overall_pct >= self.current_semester.min_attendance:
                self.stat_overall_val.configure(text_color="#2ECC71")
                self.status_pill.configure(text="✓ In Good Standing", fg_color="#1E3A2F", text_color="#2ECC71")
            else:
                self.stat_overall_val.configure(text_color="#E74C3C")
                self.status_pill.configure(text="⚠ Attention Needed", fg_color="#3D2323", text_color="#E74C3C")
        else:
            self.stat_overall_val.configure(text="—%", text_color="#CBD5E1")
            self.status_pill.configure(text="New Semester", fg_color="#2C333D", text_color="#8F9CAE")

        # Empty state display if no courses
        if not courses:
            empty_frame = ctk.CTkFrame(self.courses_scroll, corner_radius=15, fg_color="#1E232B", border_width=1, border_color="#2C333D")
            empty_frame.pack(fill="x", pady=40, padx=20, ipady=30)
            
            ctk.CTkLabel(
                empty_frame,
                text="No courses added to this semester yet",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#E1E4E8"
            ).pack(pady=(20, 8))
            
            ctk.CTkLabel(
                empty_frame,
                text="Click the '+ Add Course' button in the top right to start tracking attendance.",
                font=ctk.CTkFont(size=13),
                text_color="#8F9CAE"
            ).pack(pady=(0, 20))
            return

        # Render course cards
        for course in courses:
            self._render_course_card(course)

    def _render_course_card(self, course: Course) -> None:
        """Create a card widget for a single course."""
        card = ctk.CTkFrame(
            self.courses_scroll,
            corner_radius=15,
            fg_color="#1E232B",
            border_width=1,
            border_color="#2C333D"
        )
        card.pack(fill="x", pady=8, padx=5, ipady=8)

        # Top line: Title, Badges, and Delete Button
        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=16, pady=(10, 6))

        # Course Name
        name_lbl = ctk.CTkLabel(
            top_row,
            text=course.name,
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#FFFFFF"
        )
        name_lbl.pack(side="left")

        # Course Type Badge
        is_lab = isinstance(course, LabCourses) or course.periods > 1
        type_text = f"Lab ({course.periods} periods/slot)" if is_lab else f"Theory ({course.periods} period/slot)"
        type_badge = ctk.CTkLabel(
            top_row,
            text=type_text,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#263345",
            text_color="#64B5F6",
            corner_radius=6,
            padx=8,
            pady=2
        )
        type_badge.pack(side="left", padx=10)

        # Credits Badge
        credits_badge = ctk.CTkLabel(
            top_row,
            text=f"{course.credits} Credits",
            font=ctk.CTkFont(size=11),
            fg_color="#2C333D",
            text_color="#CBD5E1",
            corner_radius=6,
            padx=8,
            pady=2
        )
        credits_badge.pack(side="left")

        # Delete Course Button
        del_btn = ctk.CTkButton(
            top_row,
            text="✕",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="transparent",
            text_color="#8F9CAE",
            hover_color="#3D2323",
            width=28,
            height=28,
            corner_radius=6,
            command=lambda c=course: self.delete_course(c)
        )
        del_btn.pack(side="right")

        # Middle Section: Metrics, Progress Bar, and Smart Insights
        mid_row = ctk.CTkFrame(card, fg_color="transparent")
        mid_row.pack(fill="x", padx=16, pady=4)

        has_happened = course.classes_happened > 0
        if has_happened:
            pct = course.attendance_percentage(float)
            pct_text = f"{pct:.1f}%"
            is_above_target = pct >= (course.min_attendance or 75)
            pct_color = "#2ECC71" if is_above_target else "#E74C3C"
            ratio_val = min(1.0, max(0.0, pct / 100.0))
        else:
            pct_text = "—%"
            pct_color = "#8F9CAE"
            is_above_target = True
            ratio_val = 0.0

        # Percentage label
        pct_lbl = ctk.CTkLabel(
            mid_row,
            text=pct_text,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=pct_color,
            width=70,
            anchor="w"
        )
        pct_lbl.pack(side="left", padx=(0, 15))

        # Progress bar & period counts container
        progress_container = ctk.CTkFrame(mid_row, fg_color="transparent")
        progress_container.pack(side="left", fill="x", expand=True, padx=(0, 20))

        count_text = f"Attended: {course.classes_attended} / {course.classes_happened} periods"
        if course.total_classes > 0:
            count_text += f" (Est. Total: {course.total_classes})"
        count_lbl = ctk.CTkLabel(
            progress_container,
            text=count_text,
            font=ctk.CTkFont(size=12),
            text_color="#8F9CAE",
            anchor="w"
        )
        count_lbl.pack(fill="x")

        prog_bar = ctk.CTkProgressBar(
            progress_container,
            height=8,
            corner_radius=4,
            progress_color=pct_color if has_happened else "#373F4B",
            fg_color="#2C333D"
        )
        prog_bar.set(ratio_val)
        prog_bar.pack(fill="x", pady=(4, 0))

        # Smart Insights Banner
        insight_frame = ctk.CTkFrame(card, corner_radius=8, fg_color="#242B35")
        insight_frame.pack(fill="x", padx=16, pady=8, ipady=4)

        if not has_happened:
            insight_text = "ℹ No classes have occurred yet. Use '+ Present' or '- Absent' when classes take place."
            insight_color = "#8F9CAE"
        else:
            if is_above_target:
                safe_leaves = course.calculate_safe_leaves()
                if safe_leaves > 0:
                    insight_text = f"✓ Safe Leaves: You can safely miss up to {safe_leaves} slot(s) and stay above {course.min_attendance or 75}%."
                    insight_color = "#2ECC71"
                else:
                    insight_text = f"⚠ Borderline: Currently at or near {course.min_attendance or 75}%. Missing the next class will lower your standing."
                    insight_color = "#F39C12"
            else:
                recovery = course.regain_min_attendance()
                if recovery is False:
                    insight_text = f"⚠ Critical: Mathematically impossible to reach {course.min_attendance or 75}% with remaining classes."
                    insight_color = "#E74C3C"
                else:
                    insight_text = f"⚠ Recovery: You must attend the next {recovery} consecutive slot(s) to reach {course.min_attendance or 75}%."
                    insight_color = "#E74C3C"

        insight_lbl = ctk.CTkLabel(
            insight_frame,
            text=insight_text,
            font=ctk.CTkFont(size=12, weight="bold" if has_happened else "normal"),
            text_color=insight_color,
            anchor="w"
        )
        insight_lbl.pack(fill="x", padx=12, pady=4)

        # Action Buttons Row
        actions_row = ctk.CTkFrame(card, fg_color="transparent")
        actions_row.pack(fill="x", padx=16, pady=(4, 8))

        present_btn = ctk.CTkButton(
            actions_row,
            text="+ Present",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#27AE60",
            hover_color="#1E8449",
            corner_radius=8,
            width=90,
            height=32,
            command=lambda c=course: self.log_presence(c, True)
        )
        present_btn.pack(side="left", padx=(0, 8))

        absent_btn = ctk.CTkButton(
            actions_row,
            text="- Absent",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#C0392B",
            hover_color="#922B21",
            corner_radius=8,
            width=90,
            height=32,
            command=lambda c=course: self.log_presence(c, False)
        )
        absent_btn.pack(side="left", padx=(0, 8))

        undo_btn = ctk.CTkButton(
            actions_row,
            text="↺ Undo Last",
            font=ctk.CTkFont(size=12),
            fg_color="#2C333D",
            hover_color="#373F4B",
            text_color="#CBD5E1",
            corner_radius=8,
            width=95,
            height=32,
            command=lambda c=course: self.undo_last(c)
        )
        undo_btn.pack(side="left", padx=(0, 8))

        edit_btn = ctk.CTkButton(
            actions_row,
            text="⚙ Adjust",
            font=ctk.CTkFont(size=12),
            fg_color="#2C333D",
            hover_color="#373F4B",
            text_color="#CBD5E1",
            corner_radius=8,
            width=80,
            height=32,
            command=lambda c=course: self.open_edit_course_dialog(c)
        )
        edit_btn.pack(side="right")

    def log_presence(self, course: Course, attended: bool) -> None:
        """Log presence or absence for a course and persist."""
        course.log_attendance(attended)
        self.controller.save_data()
        self.refresh_view()

    def undo_last(self, course: Course) -> None:
        """Attempt to undo the most recent attendance logged."""
        if course.classes_happened < course.periods:
            return
        
        # Determine if last was present or absent by asking or attempting present first
        dialog = UndoChoiceDialog(self, course)
        self.wait_window(dialog)
        self.refresh_view()

    def delete_course(self, course: Course) -> None:
        """Delete a course from the current semester."""
        if not self.current_semester:
            return
        self.current_semester.remove_course(course)
        self.controller.save_data()
        self.refresh_view()

    def confirm_delete_semester(self) -> None:
        """Confirm and delete the current semester."""
        if not self.current_semester:
            return
        dialog = ConfirmDialog(
            self,
            title="Delete Semester",
            message=f"Are you sure you want to delete Semester {self.current_semester.sem_number}? All its courses will be permanently removed."
        )
        self.wait_window(dialog)
        if dialog.confirmed:
            if self.current_semester in self.controller.semesters:
                self.controller.semesters.remove(self.current_semester)
            self.controller.save_data()
            self.go_back()

    def open_add_course_dialog(self) -> None:
        """Open the Add Course modal."""
        if not self.current_semester:
            return
        dialog = AddCourseDialog(self, self.current_semester)
        self.wait_window(dialog)
        self.refresh_view()

    def open_edit_course_dialog(self, course: Course) -> None:
        """Open the Adjust Course modal."""
        dialog = EditCourseDialog(self, course)
        self.wait_window(dialog)
        self.refresh_view()


class AddCourseDialog(ctk.CTkToplevel):
    def __init__(self, parent, semester: Semester):
        super().__init__(parent)
        self.semester = semester
        self.parent_screen = parent
        
        self.title("Add New Course")
        self.geometry("480x640")
        self.minsize(440, 520)
        self.resizable(True, True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#181C24")

        self.transient(parent)
        self.grab_set()

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=25, pady=20)

        # 1. Pinned bottom action buttons (ALWAYS visible at the bottom)
        btn_row = ctk.CTkFrame(container, fg_color="transparent")
        btn_row.pack(side="bottom", fill="x", pady=(15, 0))

        cancel_btn = ctk.CTkButton(
            btn_row,
            text="Cancel",
            font=ctk.CTkFont(size=13),
            fg_color="#2C333D",
            hover_color="#373F4B",
            height=40,
            corner_radius=8,
            command=self.destroy
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        save_btn = ctk.CTkButton(
            btn_row,
            text="✓ Confirm & Add Course",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3B8ED0",
            hover_color="#2A6F9E",
            height=40,
            corner_radius=8,
            command=self._save_course
        )
        save_btn.pack(side="right", fill="x", expand=True)

        # 2. Scrollable form area
        form_frame = ctk.CTkScrollableFrame(container, fg_color="transparent")
        form_frame.pack(side="top", fill="both", expand=True)

        ctk.CTkLabel(
            form_frame,
            text="Add Course Details",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(0, 15))

        # Course Name
        ctk.CTkLabel(form_frame, text="Course Name", font=ctk.CTkFont(size=12, weight="bold"), text_color="#8F9CAE").pack(anchor="w")
        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g. Signals and Systems", height=35, corner_radius=8)
        self.name_entry.pack(fill="x", pady=(4, 12))

        # Course Type
        ctk.CTkLabel(form_frame, text="Course Type", font=ctk.CTkFont(size=12, weight="bold"), text_color="#8F9CAE").pack(anchor="w")
        self.type_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["Theory (1 period/slot)", "Lab (3 periods/slot)"],
            height=35,
            corner_radius=8,
            command=self._on_type_change
        )
        self.type_menu.set("Theory (1 period/slot)")
        self.type_menu.pack(fill="x", pady=(4, 12))

        # Credits & Periods row
        row1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 12))

        c_col = ctk.CTkFrame(row1, fg_color="transparent")
        c_col.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(c_col, text="Credits (1-6)", font=ctk.CTkFont(size=12, weight="bold"), text_color="#8F9CAE").pack(anchor="w")
        self.credits_entry = ctk.CTkEntry(c_col, height=35, corner_radius=8)
        self.credits_entry.insert(0, "4")
        self.credits_entry.pack(fill="x", pady=(4, 0))

        p_col = ctk.CTkFrame(row1, fg_color="transparent")
        p_col.pack(side="right", fill="x", expand=True)
        ctk.CTkLabel(p_col, text="Periods per Slot", font=ctk.CTkFont(size=12, weight="bold"), text_color="#8F9CAE").pack(anchor="w")
        self.periods_entry = ctk.CTkEntry(p_col, height=35, corner_radius=8)
        self.periods_entry.insert(0, "1")
        self.periods_entry.pack(fill="x", pady=(4, 0))

        # Target Min Attendance
        ctk.CTkLabel(form_frame, text="Minimum Attendance Target (%)", font=ctk.CTkFont(size=12, weight="bold"), text_color="#8F9CAE").pack(anchor="w")
        self.min_att_entry = ctk.CTkEntry(form_frame, height=35, corner_radius=8)
        self.min_att_entry.insert(0, str(self.semester.min_attendance))
        self.min_att_entry.pack(fill="x", pady=(4, 12))

        # Semester Duration Planning (Optional)
        ctk.CTkLabel(form_frame, text="Estimated Semester Duration (Optional)", font=ctk.CTkFont(size=12, weight="bold"), text_color="#8F9CAE").pack(anchor="w")
        row2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(4, 15))

        m_col = ctk.CTkFrame(row2, fg_color="transparent")
        m_col.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.months_entry = ctk.CTkEntry(m_col, placeholder_text="Months (e.g. 4)", height=35, corner_radius=8)
        self.months_entry.insert(0, "4")
        self.months_entry.pack(fill="x")

        w_col = ctk.CTkFrame(row2, fg_color="transparent")
        w_col.pack(side="right", fill="x", expand=True)
        self.weeks_entry = ctk.CTkEntry(w_col, placeholder_text="Weeks (e.g. 0)", height=35, corner_radius=8)
        self.weeks_entry.insert(0, "0")
        self.weeks_entry.pack(fill="x")

        # Error label
        self.error_lbl = ctk.CTkLabel(form_frame, text="", text_color="#E74C3C", font=ctk.CTkFont(size=12))
        self.error_lbl.pack(pady=(0, 10))

        # Bind Enter to save and set focus to name
        self.bind("<Return>", lambda event: self._save_course())
        self.name_entry.focus_set()

    def _on_type_change(self, value: str) -> None:
        if "Lab" in value:
            self.periods_entry.delete(0, "end")
            self.periods_entry.insert(0, "3")
        else:
            self.periods_entry.delete(0, "end")
            self.periods_entry.insert(0, "1")

    def _save_course(self) -> None:
        name = self.name_entry.get().strip()
        if not name:
            self.error_lbl.configure(text="Please enter a course name.")
            return

        try:
            credits = int(self.credits_entry.get().strip())
            if not (1 <= credits <= 6):
                raise ValueError
        except ValueError:
            self.error_lbl.configure(text="Credits must be an integer between 1 and 6.")
            return

        try:
            periods = int(self.periods_entry.get().strip())
            if periods <= 0:
                raise ValueError
        except ValueError:
            self.error_lbl.configure(text="Periods per slot must be a positive integer.")
            return

        try:
            min_att = int(self.min_att_entry.get().strip())
            if not (0 <= min_att <= 100):
                raise ValueError
        except ValueError:
            self.error_lbl.configure(text="Target attendance must be between 0 and 100.")
            return

        # Check type
        is_lab = "Lab" in self.type_menu.get()
        if is_lab:
            course = LabCourses(
                name=name,
                credits=credits,
                periods_per_lab=periods,
                min_attendance=min_att
            )
        else:
            course = TheoryCourses(
                name=name,
                credits=credits,
                periods_per_theory_class=periods,
                min_attendance=min_att
            )

        # Calculate estimated total classes if months/weeks provided
        try:
            months = int(self.months_entry.get().strip() or "0")
            weeks = int(self.weeks_entry.get().strip() or "0")
            if months > 0 or weeks > 0:
                course.calculate_total_classes(months=months, weeks=weeks)
        except ValueError:
            pass

        self.semester.add_course(course)
        self.parent_screen.controller.save_data()
        self.destroy()


class EditCourseDialog(ctk.CTkToplevel):
    def __init__(self, parent, course: Course):
        super().__init__(parent)
        self.course = course
        self.parent_screen = parent

        self.title(f"Adjust - {course.name}")
        self.geometry("440x450")
        self.minsize(400, 400)
        self.resizable(True, True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#181C24")

        self.transient(parent)
        self.grab_set()

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=25, pady=20)

        # Pin bottom action buttons
        btn_row = ctk.CTkFrame(container, fg_color="transparent")
        btn_row.pack(side="bottom", fill="x", pady=(15, 0))

        cancel_btn = ctk.CTkButton(
            btn_row,
            text="Cancel",
            fg_color="#2C333D",
            hover_color="#373F4B",
            height=38,
            corner_radius=8,
            command=self.destroy
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        save_btn = ctk.CTkButton(
            btn_row,
            text="Save Changes",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3B8ED0",
            hover_color="#2A6F9E",
            height=38,
            corner_radius=8,
            command=self._save_changes
        )
        save_btn.pack(side="right", fill="x", expand=True)

        ctk.CTkLabel(
            container,
            text=f"Adjust Attendance Data",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(0, 4))

        ctk.CTkLabel(
            container,
            text=course.name,
            font=ctk.CTkFont(size=13),
            text_color="#8F9CAE"
        ).pack(anchor="w", pady=(0, 15))

        # Classes happened
        ctk.CTkLabel(container, text="Total Periods Held (Happened)", font=ctk.CTkFont(size=12, weight="bold"), text_color="#8F9CAE").pack(anchor="w")
        self.happened_entry = ctk.CTkEntry(container, height=35, corner_radius=8)
        self.happened_entry.insert(0, str(course.classes_happened))
        self.happened_entry.pack(fill="x", pady=(4, 10))

        # Classes attended
        ctk.CTkLabel(container, text="Periods Attended", font=ctk.CTkFont(size=12, weight="bold"), text_color="#8F9CAE").pack(anchor="w")
        self.attended_entry = ctk.CTkEntry(container, height=35, corner_radius=8)
        self.attended_entry.insert(0, str(course.classes_attended))
        self.attended_entry.pack(fill="x", pady=(4, 10))

        # Estimated total classes
        ctk.CTkLabel(container, text="Total Classes in Semester (Optional)", font=ctk.CTkFont(size=12, weight="bold"), text_color="#8F9CAE").pack(anchor="w")
        self.total_entry = ctk.CTkEntry(container, height=35, corner_radius=8)
        self.total_entry.insert(0, str(course.total_classes))
        self.total_entry.pack(fill="x", pady=(4, 10))

        self.error_lbl = ctk.CTkLabel(container, text="", text_color="#E74C3C", font=ctk.CTkFont(size=12))
        self.error_lbl.pack(pady=(0, 8))

        self.bind("<Return>", lambda event: self._save_changes())

    def _save_changes(self) -> None:
        try:
            happened = int(self.happened_entry.get().strip())
            attended = int(self.attended_entry.get().strip())
            total = int(self.total_entry.get().strip() or "0")

            if happened < 0 or attended < 0 or total < 0:
                raise ValueError("Values cannot be negative.")
            if attended > happened:
                self.error_lbl.configure(text="Attended periods cannot exceed happened periods.")
                return

            self.course.classes_happened = happened
            self.course.classes_attended = attended
            self.course.total_classes = total
            self.parent_screen.controller.save_data()
            self.destroy()
        except ValueError as e:
            self.error_lbl.configure(text="Please enter valid positive numbers.")


class UndoChoiceDialog(ctk.CTkToplevel):
    def __init__(self, parent, course: Course):
        super().__init__(parent)
        self.course = course
        self.parent_screen = parent

        self.title("Undo Attendance")
        self.geometry("360x220")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#181C24")

        self.transient(parent)
        self.grab_set()

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            container,
            text="Undo Last Log",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(0, 4))

        ctk.CTkLabel(
            container,
            text=f"What was the last logged attendance for {course.name}?",
            font=ctk.CTkFont(size=12),
            text_color="#8F9CAE",
            wraplength=320,
            justify="left"
        ).pack(anchor="w", pady=(0, 16))

        btn_row = ctk.CTkFrame(container, fg_color="transparent")
        btn_row.pack(fill="x", pady=(0, 10))

        undo_present = ctk.CTkButton(
            btn_row,
            text="Undo Present (+)",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#27AE60",
            hover_color="#1E8449",
            height=36,
            corner_radius=8,
            command=lambda: self._apply_undo(True)
        )
        undo_present.pack(side="left", fill="x", expand=True, padx=(0, 8))

        undo_absent = ctk.CTkButton(
            btn_row,
            text="Undo Absent (-)",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#C0392B",
            hover_color="#922B21",
            height=36,
            corner_radius=8,
            command=lambda: self._apply_undo(False)
        )
        undo_absent.pack(side="right", fill="x", expand=True)

        cancel_btn = ctk.CTkButton(
            container,
            text="Cancel",
            fg_color="#2C333D",
            hover_color="#373F4B",
            height=32,
            corner_radius=8,
            command=self.destroy
        )
        cancel_btn.pack(fill="x")

    def _apply_undo(self, attended: bool) -> None:
        success = self.course.undo_attendance(attended)
        if success:
            self.parent_screen.controller.save_data()
        self.destroy()


class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, parent, title: str, message: str):
        super().__init__(parent)
        self.confirmed = False

        self.title(title)
        self.geometry("380x180")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#181C24")

        self.transient(parent)
        self.grab_set()

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            container,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(0, 8))

        ctk.CTkLabel(
            container,
            text=message,
            font=ctk.CTkFont(size=12),
            text_color="#CBD5E1",
            wraplength=340,
            justify="left"
        ).pack(anchor="w", pady=(0, 16))

        btn_row = ctk.CTkFrame(container, fg_color="transparent")
        btn_row.pack(fill="x")

        cancel_btn = ctk.CTkButton(
            btn_row,
            text="Cancel",
            fg_color="#2C333D",
            hover_color="#373F4B",
            height=34,
            corner_radius=8,
            command=self.destroy
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        confirm_btn = ctk.CTkButton(
            btn_row,
            text="Confirm Delete",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#C0392B",
            hover_color="#922B21",
            height=34,
            corner_radius=8,
            command=self._confirm
        )
        confirm_btn.pack(side="right", fill="x", expand=True)

    def _confirm(self) -> None:
        self.confirmed = True
        self.destroy()
