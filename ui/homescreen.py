import customtkinter as ctk
from src.courses import Semester, Course
from src.storage import load_semesters, save_semesters
from ui.semester_screen import SemesterScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SmartTrack")
        self.geometry("1000x800")

        self.semesters: list[Semester] = load_semesters()

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="top", fill="both", expand=True, padx=20, pady=20)

        self.frames = {}

        home_frame = HomeScreen(parent=self.container, controller=self)
        self.frames["HomeScreen"] = home_frame

        semester_frame = SemesterScreen(parent=self.container, controller=self)
        self.frames["SemesterScreen"] = semester_frame

        self.show_page("HomeScreen")

    def show_page(self, page_name: str):
        for frame in self.frames.values():
            frame.pack_forget()
        
        self.frames[page_name].pack(fill="both", expand=True)

    def save_data(self) -> None:
        save_semesters(self.semesters)

    def open_semester(self, semester: Semester) -> None:
        self.frames["SemesterScreen"].set_semester(semester)
        self.show_page("SemesterScreen")


class HomeScreen(ctk.CTkFrame): 
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.semesters_list = [f"Sem {s.sem_number}" for s in self.controller.semesters]

        dash_board = ctk.CTkFrame(self, corner_radius=20, height=250)
        dash_board.pack(side="top", fill="x", pady=(0, 20))
        
        dash_lbl = ctk.CTkLabel(dash_board, text="Welcome back!", font=ctk.CTkFont(size=22, weight="bold"))
        dash_lbl.pack(pady=(35, 5))

        self.dash_stats_lbl = ctk.CTkLabel(
            dash_board,
            text="Manage your courses, periods, and attendance smartly.",
            font=ctk.CTkFont(size=13),
            text_color="#8F9CAE"
        )
        self.dash_stats_lbl.pack(pady=(0, 35))

        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(side="top", fill="x")

        self.add_sem_button = ctk.CTkButton(
            cards_frame, 
            text="Add Semester", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3B8ED0", 
            hover_color="#2A6F9E",   
            corner_radius=10, 
            height=40, 
            command=self.add_semester # 
        )
        self.add_sem_button.pack(pady=10)

        self.semester_row = LazyRowFrame(cards_frame, height=80, width=800)
        self.semester_row.pack(pady=20, fill="x", expand=True)

        self.refresh_semester_row()

    def add_semester(self) -> None:
        existing_nums = [s.sem_number for s in self.controller.semesters]
        next_sem_number = max(existing_nums, default=0) + 1
        
        new_sem = Semester(next_sem_number)
        self.controller.semesters.append(new_sem)
        self.controller.save_data()

        self.semesters_list.append(f"Sem {next_sem_number}")
        
        # Trigger the layout synchronization loop to update the monitor view
        self.refresh_semester_row()
        self.on_semester_select(f"Sem {next_sem_number}")

    def refresh_semester_row(self) -> None:
        for child in self.semester_row.winfo_children():
            child.destroy()

        self.semesters_list = [f"Sem {s.sem_number}" for s in self.controller.semesters]

        total_sems = len(self.controller.semesters)
        total_courses = sum(len(s.courses) for s in self.controller.semesters)
        self.dash_stats_lbl.configure(
            text=f"{total_sems} Active Semester{'s' if total_sems != 1 else ''} • {total_courses} Course{'s' if total_courses != 1 else ''} Tracked"
        )

        if not self.semesters_list:
            no_sem = ctk.CTkLabel(
                self.semester_row,
                text="No semesters added yet. Click 'Add Semester' above to begin!",
                font=ctk.CTkFont(size=13),
                text_color="#8F9CAE"
            )
            no_sem.pack(side="left", padx=20, pady=20)
            return

        for sem_name in self.semesters_list:
            sem_btn = ctk.CTkButton(
                self.semester_row, 
                text=sem_name, 
                corner_radius=10, 
                height=35,
                width=100,
                hover_color="#2A6F9E",
                command=lambda name=sem_name: self.on_semester_select(name)
            )
            sem_btn.pack(side="left", padx=10, pady=10)

    def on_semester_select(self, name: str) -> None:
        print(f"User navigated context directly into: {name}")
        for sem in self.controller.semesters:
            if f"Sem {sem.sem_number}" == name:
                self.controller.open_semester(sem)
                break

class LazyRowFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, height: int = 150, width: int = 600, **kwargs):
        super().__init__(
            master, 
            orientation="horizontal", 
            width=width, 
            height=height, 
            corner_radius=15,
            fg_color="#1E232B",          
            border_width=1,
            border_color="#2C333D",
            **kwargs
        )

class ClickableHomeWidget(ctk.CTkFrame):

    def __init__(self,
        master, titleText="Card", frameWidth=200, hover_color="#373F4B",
        frameHeight=200, on_click=None, bgColor="#2B2B2B", corner_radius=30, **kwargs
    ):
        super().__init__(master, width=frameWidth, height=frameHeight, cursor="hand2",
            corner_radius=corner_radius, fg_color=bgColor, **kwargs
        )
        self.on_click = on_click
        self.bg_color = bgColor
        self.hover_color = hover_color

        self.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self, text=titleText,
            font=ctk.CTkFont(size=15, weight="bold"),
            cursor="hand2",
        )
        self.title_label.pack(side="bottom", pady=(0, 16))

        self.bind("<Button-1>", self._handle_click)
        self.title_label.bind("<Button-1>", self._handle_click)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.title_label.bind("<Enter>", self._on_enter)
        self.title_label.bind("<Leave>", self._on_leave)

    def _handle_click(self, event=None) -> None:
        if self.on_click:
            self.on_click()

    def _on_enter(self, event=None) -> None:
        self.configure(fg_color=self.hover_color)

    def _on_leave(self, event=None) -> None:
        x, y = self.winfo_pointerxy()
        widget_x = self.winfo_rootx()
        widget_y = self.winfo_rooty()
        widget_w = self.winfo_width()
        widget_h = self.winfo_height()

        if not (
            widget_x <= x <= widget_x + widget_w 
            and widget_y <= y <= widget_y + widget_h
        ):
            self.configure(fg_color=self.bg_color)


class CustomDropdown(ctk.CTkFrame):
    def __init__(self, master, options: list[str], default_text: str = "Select Option", 
                 width: int = 200, height: int = 40, on_select=None, **kwargs):
        # Base frame setup mimicking a clean slate input layout
        super().__init__(master, width=width, height=height, corner_radius=10, 
                         fg_color="#2C333D", border_width=1, border_color="#373F4B", **kwargs)
        
        self.options = options
        self.on_select = on_select
        self.is_open = False
        self.pack_propagate(False)

        # 1. Main Header Button Layout (The clickable top bar)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", cursor="hand2")
        self.header_frame.pack(fill="both", expand=True)

        # Label displaying current state selection text
        self.selection_label = ctk.CTkLabel(
            self.header_frame, text=default_text,
            font=ctk.CTkFont(size=14, weight="normal"), fg_color="transparent"
        )
        self.selection_label.pack(side="left", padx=15, rely=0.5, anchor="w")

        # Custom small chevron arrow icon indicator (using simple text characters)
        self.arrow_label = ctk.CTkLabel(
            self.header_frame, text="▼",
            font=ctk.CTkFont(size=11), text_color="#7F8C8D"
        )
        self.arrow_label.pack(side="right", padx=15, rely=0.5, anchor="e")

        # 2. Dropdown Floating Context List Window
        self.menu_window = None

        # Bind interface click event behaviors directly onto layout components
        for widget in (self.header_frame, self.selection_label, self.arrow_label):
            widget.bind("<Button-1>", self._toggle_menu)
            widget.bind("<Enter>", self._on_header_enter)
            widget.bind("<Leave>", self._on_header_leave)

    def _toggle_menu(self, event=None):
        if self.is_open:
            self._close_menu()
        else:
            self._open_menu()

    def _open_menu(self):
        self.is_open = True
        self.arrow_label.configure(text="▲", text_color="#3B8ED0") # Highlight arrow configuration
        self.configure(border_color="#3B8ED0") # Highlight container focus ring

        # Calculate coordinates directly underneath the selection boundary
        self.update_idletasks()
        root_x = self.winfo_rootx()
        root_y = self.winfo_rooty()
        widget_height = self.winfo_height()
        widget_width = self.winfo_width()

        # Create a borderless popup subwindow overlay stack
        self.menu_window = ctk.CTkToplevel(self)
        self.menu_window.withdraw() # Hide temporarily to prevent frame rendering flash
        self.menu_window.overrideredirect(True) # Remove OS native task titlebar wrap
        self.menu_window.attributes("-topmost", True)
        
        # Position panel seamlessly dropping down from baseline axis
        self.menu_window.geometry(f"{widget_width}x{len(self.options) * 35 + 10}+{root_x}+{root_y + widget_height + 4}")
        
        # Menu content box layer implementation
        menu_frame = ctk.CTkFrame(self.menu_window, fg_color="#232931", 
                                  corner_radius=8, border_width=1, border_color="#373F4B")
        menu_frame.pack(fill="both", expand=True)

        # Dynamic loop sequence generating entry options lists fields rows structures
        for index, option in enumerate(self.options):
            opt_btn = ctk.CTkButton(
                menu_frame, text=option, height=30, anchor="w",
                fg_color="transparent", text_color="#E1E4E8",
                hover_color="#2C333D", font=ctk.CTkFont(size=13),
                corner_radius=5,
                command=lambda opt=option: self._select_option(opt)
            )
            opt_btn.pack(fill="x", padx=5, pady=(5 if index == 0 else 2, 2))

        self.menu_window.deiconify() # Reveal popup
        
        # Safety binding to auto-close layout elements if user clicks anywhere outside the menu field area bounds box
        self.menu_window.bind("<FocusOut>", lambda e: self._close_menu())
        self.menu_window.focus_set()

    def _close_menu(self):
        self.is_open = False
        self.arrow_label.configure(text="▼", text_color="#7F8C8D")
        self.configure(border_color="#373F4B")
        if self.menu_window:
            self.menu_window.destroy()
            self.menu_window = None

    def _select_option(self, value: str):
        self.selection_label.configure(text=value)
        self._close_menu()
        if self.on_select:
            self.on_select(value)

    # Styling feedback behaviors routing handlers hooks execution
    def _on_header_enter(self, event=None):
        if not self.is_open:
            self.configure(fg_color="#323A45")

    def _on_header_leave(self, event=None):
        if not self.is_open:
            self.configure(fg_color="#2C333D")

    def get(self) -> str:
        return self.selection_label.cget("text")

    def set(self, value: str) -> None:
        self.selection_label.configure(text=value)