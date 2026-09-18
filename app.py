import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    counter: int = 0

    def __init__(self):
        super().__init__()

        self.title("SmartTrack")
        self.geometry("1000x800")

        # 1. Instantiate without hardcoded pixel width/height
        self.display_info_card = ctk.CTkFrame(
            self, corner_radius=20
        )

        self.display_info_card.place(
            relx=0.5,
            rely=0.5,
            relwidth=0.6,  # 60% of the window's current width
            relheight=0.4,  # 40% of the window's current height
            anchor="center",
        )

        


def main():
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()