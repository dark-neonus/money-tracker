import tkinter as tk

from modules.gui.basic_elements import GUIElement, GUIFrame, GUIButton
from modules.gui.listbox import GUIListBox

class GUIListToList(GUIElement):
    def __init__(
        self,
        source_dict: dict[str, str],
        asset_dict: dict[str, str] = {},
        assets_header: str = "",
        source_header: str = "",
        row_count: int = 5,
    ) -> None:
        super().__init__(
            side="top",
            expand=True,
            fill="both",
            relief="raised",
            borderwidth=2,
            padx=10,
            pady=10,
        )
        # { id1 : text1, id2 : text2, ...}
        self.items_list: list[dict] = [
            self.__create_items_list_item(key, False, value)
            for key, value in source_dict.items()
        ]

        for key, value in asset_dict.items():
            self.items_list.append(self.__create_items_list_item(key, True, value))

        self.source_header: str = source_header
        self.assets_header: str = assets_header

        self.source_listbox: GUIListBox = None
        self.assets_listbox: GUIListBox = None

        self.row_count = row_count

        self.is_packed = False

    def __create_items_list_item(self, id: str, in_assets: bool, text: str) -> dict:
        return {"id": id, "in_assets": in_assets, "text": text}

    def add_source(self, id: str, text: str) -> None:
        self.items_list.append(self.__create_items_list_item(id, False, text))
        self.update_lists()

    def update_lists(self) -> None:
        if self.is_packed:
            self.assets_listbox.listbox.delete("0", "end")
            self.source_listbox.listbox.delete("0", "end")

            for item in self.items_list:
                if item["in_assets"]:
                    self.assets_listbox.listbox.insert(tk.END, item["text"])
                else:
                    self.source_listbox.listbox.insert(tk.END, item["text"])

    def source_to_asset(self, index: int) -> None:
        self.items_list[index]["in_assets"] = True
        self.update_lists()

    def assets_to_source(self, index: int) -> None:
        self.items_list[index]["in_assets"] = False
        self.update_lists()

    def selected_source_to_asset(self) -> None:
        selected_index = self.source_listbox.listbox.curselection()
        if len(selected_index) > 0:
            target_text = self.source_listbox.listbox.get(selected_index[0])
            ind = 0
            for ind in range(len(self.items_list)):
                if self.items_list[ind]["text"] == target_text:
                    break
            self.source_to_asset(ind)
            self.update_lists()

    def selected_assets_to_source(self) -> None:
        selected_index = self.assets_listbox.listbox.curselection()
        if len(selected_index) > 0:
            target_text = self.assets_listbox.listbox.get(selected_index[0])
            ind = 0
            for ind in range(len(self.items_list)):
                if self.items_list[ind]["text"] == target_text:
                    break
            self.assets_to_source(ind)
            self.update_lists()

    def pack(self, root: tk.Frame) -> None:
        self.is_packed = True

        self.main_frame = GUIFrame(
            root,
            relief=self.relief,
            borderwidth=self.borderwidth,
            expand=self.expand,
            fill=self.fill,
            side=self.side,
            padx=self.padx,
            pady=self.pady,
            width=self.width,
            height=self.height,
        )

        self.assets_listbox = GUIListBox(self.row_count, self.assets_header)
        self.assets_listbox.side = "left"
        self.assets_listbox.relief = "raised"
        self.assets_listbox.borderwidth = 5
        self.main_frame.add(self.assets_listbox)

        self.source_listbox = GUIListBox(self.row_count, self.source_header)
        self.source_listbox.side = "right"
        self.main_frame.add(self.source_listbox)

        self.button_frame = GUIFrame(
            self.main_frame.frame, side="bottom", relief="flat"
        )

        self.source_to_assets_button = GUIButton(
            "<", self.selected_source_to_asset)
        self.assets_to_source_button = GUIButton(
            ">", self.selected_assets_to_source)
        self.button_frame.add(self.source_to_assets_button)
        self.button_frame.add(self.assets_to_source_button)

        self.main_frame.add(self.button_frame)

        self.main_frame.pack()

        self.update_lists()

    def get_assets(self) -> dict[str, str]:
        out = {}
        for item in self.items_list:
            if item["in_assets"]:
                out[item["id"]] = item["text"]
        return out
