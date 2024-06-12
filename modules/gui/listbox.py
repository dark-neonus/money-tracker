import tkinter as tk

from modules.gui.basic_elements import GUIElement


class GUIListBox(GUIElement):
    def __init__(
            self,
            row_count: int,
            label_text: str = "",
            vscrollbar: bool = False,
            hscrollbar: bool = False,
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

        self.__vscrollbar = vscrollbar
        self.__hscrollbar = hscrollbar
        self.v_scrollbar_side = "right"
        self.h_scrollbar_side = "bottom"

        self.listbox_width = None

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

    def clear(self) -> None:
        self.listbox.delete(0, tk.END)

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

        self.label = tk.Label(self.main_frame, text=self.label_text)
        self.label.pack(side="top", expand=False, fill="both")

        self.listbox: tk.Listbox = tk.Listbox(self.main_frame, height=self.row_count)
        
        if self.__vscrollbar:
            self.v_scrollbar = tk.Scrollbar(
                self.main_frame,
                orient=tk.VERTICAL,
                command=self.listbox.yview
            )
            self.listbox.config(yscrollcommand=self.v_scrollbar.set)
            self.v_scrollbar.pack(side=self.v_scrollbar_side, fill="y")

        if self.__hscrollbar:
            self.h_scrollbar = tk.Scrollbar(
                self.main_frame,
                orient=tk.HORIZONTAL,
                command=self.listbox.xview
            )
            self.listbox.config(xscrollcommand=self.h_scrollbar.set)
            self.h_scrollbar.pack(side=self.h_scrollbar_side, fill="x")

        if self.listbox_width:
            self.listbox.config(width=self.listbox_width)

        self.listbox.pack(side="top", expand=True, fill="both")

        
