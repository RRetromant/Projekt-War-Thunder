import unittest
import customtkinter as ctk

class TestWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Test Window")
        self.geometry("800x600")  # Fenster größe
        self.button_test()

    def button_test(self):
        self.fenster = ctk.CTkFrame(master=self, width=200)
        self.fenster.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.button = ctk.CTkButton(master=self.fenster, command=self.ausgabe)
        self.button.configure(text="Button")
        self.button.pack(pady=20)

    def ausgabe(self):
        print("Test")

class TestButtonFunctionality(unittest.TestCase):
    def test_ausgabe(self):
        # Hier kannst du Tests für die Funktionalität der GUI schreiben
        self.assertEqual(1, 1)  # Beispiel-Test

if __name__ == "__main__":
    app = TestWindow()
    app.mainloop()  # Starte die GUI
    unittest.main()  # Führe die Tests aus