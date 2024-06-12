import tkinter as tk
from tkinter import ttk

from modules.gui.basic_elements import GUIElement

class GUILabelAndEntry(GUIElement):
    def __init__(
        self,
        label_text: str,
        edible: bool = True,
        default_text: str = "",
        row_count: int = 1,
        row_width: int = 30,
        only_numbers: bool = False,
    ) -> None:

        super().__init__(side="top", fill="x", expand=True, padx=10, pady=10)

        self.label_text = label_text
        self.edible = edible
        self.default_text = default_text
        self.row_count = row_count
        self.row_width = row_width

        self.entry_side = "left"
        self.entry_left_offset = 10

        self.only_numbers = only_numbers

    def pack(self, root: tk.Frame) -> None:

        self.frame: tk.Frame = tk.Frame(
            root,
            relief=self.relief,
            borderwidth=self.borderwidth,
            width=self.width,
            height=self.height,
        )
        self.frame.pack(
            side=self.side,
            fill=self.fill,
            expand=self.expand,
            padx=self.padx,
            pady=self.pady,
        )

        self.label: ttk.Label = ttk.Label(self.frame, text=self.label_text)
        self.label.pack(side="left")

        if self.only_numbers:
            self.entry: tk.Entry = tk.Entry(
                self.frame, width=self.row_width
            )
            self.entry.insert("0", self.default_text)
        else:
            self.entry: tk.Text = tk.Text(
                self.frame, height=self.row_count, width=self.row_width
            )
            self.entry.insert("1.0", self.default_text)

        
        self.entry.configure(state="normal" if self.edible else "disable")

        if self.edible and self.only_numbers:
            validate_command = (
            self.entry.register(self.__validate),
            '%P',
            '%d',
            )
            self.entry.configure(validate="key", validatecommand=validate_command)

        self.entry.pack(
            side=self.entry_side, padx=10 if self.entry_side == "left" else 0
        )

    def update_text(self, new_text : str) -> None:
        edible = bool(self.edible)

        self.entry.configure(state="normal")
        if self.only_numbers:
            self.entry.delete("0", "end")
            self.entry.insert("0", new_text)
        else:
            self.entry.delete("1.0", "end")
            self.entry.insert("1.0", new_text)

        self.entry.configure(state="normal" if edible else "disable")

    def __validate(self, text, action):
        if (
            all(char in "0123456789.-" for char in text) and  # all characters are valid
            "-" not in text[1:] and # "-" is the first character or not present
            text.count(".") <= 1): # only 0 or 1 periods
                return True
        else:
            return False

        return False
