import tkinter as tk

from modules.gui.basic_elements import GUIElement


class GUIListBox(GUIElement):
    def __init__(
            self,
            row_count: int,
            label_text:
            str = ""
    ) -> None:

        super().__init__(
            side="top",
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        self.row_count = row_count
        self.label_text: str = label_text
        self.listbox: tk.Listbox = None

    def add_item(self, item: str) -> None:
        self.listbox.insert(tk.END, item)

    def remove_item(self, index: int) -> None:
        self.listbox.delete(index)

    def remove_selected_item(self) -> None:
        selected_index = self.listbox.curselection()
        if selected_index:
            self.remove_item(selected_index)

    def set_item(self, index: int, item: str) -> None:
        self.listbox.delete(index)
        self.listbox.insert(index, item)

    def set_selected_item(self, item: str) -> None:
        selected_index = self.listbox.curselection()
        if selected_index:
            self.set_item(selected_index, item)

    def pack(self, root: tk.Frame) -> None:
        self.main_frame: tk.Frame = tk.Frame(
            root,
            relief=self.relief,
            borderwidth=self.borderwidth,
            width=self.width,
            height=self.height,
        )
        self.main_frame.pack(
            side=self.side,
            fill=self.fill,
            expand=self.expand,
            padx=self.padx,
            pady=self.pady,
        )

        self.listbox: tk.Listbox = tk.Listbox(
            self.main_frame, height=self.row_count)
        self.listbox.pack(side="bottom", expand=True, fill="both")

        self.label = tk.Label(self.main_frame, text=self.label_text)
        self.label.pack(side="bottom", expand=False, fill="both")
