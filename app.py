import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SmartTrack")
        self.geometry("1000x800")

        # This is the top app frame
        self.top_frame = ctk.CTkFrame(
            self, corner_radius=5, height=60
        )
        self.top_frame.place(
            relx=0.5,
            relwidth=1.0,
            anchor="n"
        )

        self.name_icon = ctk.CTkLabel(
            self.top_frame,
            text="SmartTrack",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.name_icon.place(
            x=10, relx=0.01, rely=0.5, anchor="w"
        )

        self.dash_board = ctk.CTkFrame(
            self, corner_radius=10, height=250, width=800
        )
        self.dash_board.place(
            y=75, relx=1, anchor="n"
        )

        self.home_widget = ClickableHomeWidget(
            self, titleText="Home", 
            on_click=self.on_home_click
        )
        self.home_widget.place(
            x=200, y=200, 
        )

        self.course_widget = ClickableHomeWidget(
            self, titleText="Courses", frameHeight=50, frameWidth=70,
            on_click=self.on_courses_click
        )
        self.course_widget.place(       
            relx=0.5,
            rely=0.7,
            anchor="center"
        )

    def on_home_click(self):
        print("Home clicked!")

    def on_courses_click(self):
        print("Courses clicked!")


class ClickableHomeWidget(ctk.CTkFrame):

    def __init__(self, master, titleText, on_click=None, frameHeight=100, frameWidth=200):
        super().__init__(master, cursor="hand2", height=frameHeight, width=frameWidth, corner_radius=10)
        self.on_click = on_click

        self.title_label = ctk.CTkLabel(
            self,
            text=titleText,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.pack(pady=10)

        self.bind("<Button-1>", self._handle_click)
        self.title_label.bind("<Button-1>", self._handle_click)

    def _handle_click(self, event=None):
        if self.on_click:
            self.on_click()





        


       
