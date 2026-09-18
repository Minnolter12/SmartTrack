import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    counter: int = 0

    def __init__(self):
        super().__init__()

        self.title("SmartTrack")
        self.geometry("1000x800")

        self.card = ctk.CTkFrame(
            self, width=200,
            height=50, corner_radius=10
         )
        self.card.place(
            relx=0.5, rely=0.07,
            anchor="center"
        )

        self.title_label = ctk.CTkLabel(
            self.card, text="SmartTrack",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=10, padx=10)

        self.button_frame = ctk.CTkFrame(
            self, width=200,
            height=50, corner_radius=10
        )
        self.button_frame.place(
            relx=0.5, rely=0.2,
            anchor="center"
        )

        self.button = ctk.CTkButton(
            self.button_frame, text="Click Me",
            command=self.on_button_click
        )
        self.button.pack(pady=10, padx=10)  

        self.button_counter_label = ctk.CTkLabel(
            self.button_frame, text=f"Button clicked: {self.counter} times",
            font=ctk.CTkFont(size=14)
        )
        self.button_counter_label.pack(pady=10, padx=10)

        self.reset_button = ctk.CTkButton(
            self.button_frame, text="Reset Counter",
            command=self.reset_counter
        )
        self.reset_button.pack(pady=10, padx=10)

    def on_button_click(self) -> None:
        self.counter += 1

        self.button_counter_label.configure(
            text=f"Button clicked: {self.counter} times"
        )

    def reset_counter(self) -> None:
        self.counter = 0

        self.button_counter_label.configure(
            text=f"Button clicked: {self.counter} times"
        )


def main():
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()