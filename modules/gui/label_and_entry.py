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
    ) -> None:

        super().__init__(side="top", fill="x", expand=True, padx=10, pady=10)

        self.label_text = label_text
        self.edible = edible
        self.default_text = default_text
        self.row_count = row_count
        self.row_width = row_width

        self.entry_side = "left"
        self.entry_left_offset = 10

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

        self.entry: tk.Text = tk.Text(
            self.frame, height=self.row_count, width=self.row_width
        )

        self.entry.insert("1.0", self.default_text)
        self.entry.configure(state="normal" if self.edible else "disable")
        self.entry.pack(
            side=self.entry_side, padx=10 if self.entry_side == "left" else 0
        )
