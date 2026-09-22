import customtkinter as ctk
import src.courses as courses

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SmartTrack")
        self.geometry("1000x800")

        self.top_frame = ctk.CTkFrame(self, corner_radius=5, height=60)
        self.top_frame.place(relx=0.5, relwidth=1.0, anchor="n")

        self.name_icon = ctk.CTkLabel(
            self.top_frame,
            text="SmartTrack",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.name_icon.place(x=20, rely=0.5, anchor="w")

        self.dash_board = ctk.CTkFrame(self, corner_radius=20, height=250)
        self.dash_board.place(
            y=70,
            relx=0.5,
            relwidth=0.96,
            anchor="n",
        )

        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.place(y=350, relx=0.5, anchor="n")

        self.home_widget = ClickableHomeWidget(
            self.cards_frame,
            titleText="Home",
            frameHeight=180,
            frameWidth=220,
            bgColor="#2C333D",
            on_click=self.on_home_click,
        )
        self.home_widget.grid(row=0, column=0, padx=25, pady=10)

        self.course_widget = ClickableHomeWidget(
            self.cards_frame,
            titleText="Courses",
            frameHeight=180,
            frameWidth=220,
            bgColor="#28363D",
            on_click=self.on_courses_click,
        )
        self.course_widget.grid(row=0, column=1, padx=25, pady=10)

    def on_home_click(self) -> None:
        print("Home clicked!")

    def on_courses_click(self) -> None:
        print("Courses clicked!")


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

    
