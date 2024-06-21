if __name__ == "__main__":
    import sys
    import os.path

    sys.path[0] = os.path.join(sys.path[0], "..", "..")

from modules.tracker_logic.classes import Settings
from modules.gui.basic_elements import GUIFrame, GUIButton
from modules.gui.label_and_entry import GUILabelAndEntry
from modules.gui.listbox import GUIListBox
from modules.gui.list_to_list import GUIListToList
from modules.tracker_logic.classes import Transaction, Tag
from modules.tracker_logic.fonts import FONTS 

from typing import Dict

from datetime import date
from modules.tracker_logic.languages import load_full_language_pack, extract_text_set_from_language_pack

import tkinter as tk
from tkinter import ttk, font
from tkinter import messagebox 

# MONEY_LEVELS = [100, 500, 1000, 2500, 5000]

LEVEL_MARK = "."

def create_window(title: str, width: int, height: int, min_width: int = None, min_height: int = None, resizable: bool = True) -> tk.Toplevel:
    """
    Creates a new window with the given title, width, height, and optional minimum width and height.

    Args:
        title (str): The title of the window.
        width (int): The width of the window.
        height (int): The height of the window.
        min_width (int, optional): The minimum width of the window. Defaults to None.
        min_height (int, optional): The minimum height of the window. Defaults to None.
        resizable (bool, optional): Indicates whether the window is resizable. Defaults to True.

    Returns:
        tk.Toplevel: The newly created window.

    Raises:
        None
    """
    window = tk.Toplevel()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    if min_width is not None and min_height is not None:
        window.minsize(width=min_width, height=min_height)
    
    window.title(title)
    window.resizable(resizable, resizable)

    return window



class GUI:
    def __init__(self, font_index : int, font_size : int, settings : Settings) -> None:

        self.settings = settings

        # Root init
        self.root = tk.Tk()

        # Title
        self.root.title("Money Tracker")

        # self.root.update_idletasks()
        # self.root.attributes('-zoomed', True)

        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))

        # Window size and position
        # window_width = 800
        # window_height = 600
        # screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()
        # x_coordinate = (screen_width // 2) - (window_width // 2)
        # y_coordinate = (screen_height // 2) - (window_height // 2)
        # self.root.geometry(
        #     f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.root.minsize(width=800, height=600)
        
        self.lang_pack = load_full_language_pack()
        self.Text = extract_text_set_from_language_pack(self.settings.language_index, self.lang_pack)

        # Notebook creation
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.fv_delete_selected_transaction = lambda: None
        self.fv_edit_selected_transaction = lambda: None
        self.fv_create_transaction = lambda: None

        self.fv_sort_transactions_by_date = lambda: None
        self.fv_sort_transactions_by_balance = lambda: None
        self.fv_filter_transactions = lambda: None
        self.fv_clear_filter = lambda: None

        self.fv_get_current_transaction = lambda: None
        self.fv_get_current_tag = lambda: None

        self.fv_delete_selected_tag = lambda: None
        self.fv_edit_selected_tag = lambda: None
        self.fv_create_tag = lambda: None

        self.font_index = font_index
        self.font_size = font_size

        self.tag_list_holder : Dict[str, Tag] = None

        self.init_font()

        self.create_main_tab()
        self.create_tag_tab()

        

    def f_add_transaction_button(self) -> None:

        new_window = create_window(
            self.Text["Create transaction"],
            700,
            500,
            min_width=700,
            min_height=500,
            resizable=False
        )

        window_fr = tk.Frame(new_window)
        window_fr.pack(side="top", expand=True, fill="both")

        window_frame = GUIFrame(window_fr, side="top",
                                expand=True, fill="both")

        info_name = GUILabelAndEntry(self.Text["Name"], edible=True)
        info_name.side = "top"
        info_name.entry_side = "left"

        info_description = GUILabelAndEntry(
            self.Text["Description"], edible=True, row_count=3)
        info_description.side = "top"
        info_description.entry_side = "left"

        info_balance = GUILabelAndEntry(self.Text["Balance"], edible=True, only_numbers=True, default_text="0.0")
        info_balance.side = "top"
        info_balance.entry_side = "left"

        info_date = GUILabelAndEntry(self.Text["Date(YYYY-MM-DD)"], edible=True, default_text=date.today().isoformat())
        info_date.side = "top"
        info_date.entry_side = "left"

        window_frame.add(info_name)
        window_frame.add(info_description)
        window_frame.add(info_balance)
        window_frame.add(info_date)

        tag_list = {key : value.name for key, value in self.tag_list_holder.items()}

        info_tags = GUIListToList(
            source_dict=tag_list, assets_header=self.Text["Transaction tags"], source_header=self.Text["Available tags"], row_count=6)
        info_tags.fill = "both"
        info_tags.expand = True
        info_tags.relief = "flat"

        def tmp_f() -> None:
            if info_name.entry.get("1.0", "end-1c"):

                try:
                    transaction_date = date.fromisoformat(info_date.entry.get("1.0", "end-1c"))
                except:
                    messagebox.showerror(self.Text["Error"], self.Text["Invalid date!"], parent=new_window)
                    return

                try:
                    balance : float = float(info_balance.entry.get())
                except:
                    balance : float = 0

                self.fv_create_transaction(
                    name=info_name.entry.get("1.0", "end-1c"),
                    description=info_description.entry.get("1.0", "end-1c"),
                    balance=balance,
                    tags_id=info_tags.get_assets().keys(),
                    date_=transaction_date
                )
                new_window.destroy()
            else:
                messagebox.showinfo(self.Text["Error"], self.Text["Please enter name"], parent=new_window)

        window_frame.add(info_tags)

        buttons_frame = GUIFrame(window_frame, "bottom", relief="flat")

        create_button = GUIButton(self.Text["Create"], function=tmp_f)
        cancel_button = GUIButton(self.Text["Cancel"], function=new_window.destroy)

        buttons_frame.add(cancel_button)
        buttons_frame.add(create_button)

        window_frame.add(buttons_frame)

        window_frame.pack()

    def f_edit_transaction_button(self) -> None:
        current_transaction : Transaction = self.fv_get_current_transaction()

        if current_transaction == None:
            messagebox.showinfo(self.Text["Error"], self.Text["Please select transaction first!"], parent=self.root)
            return
        
        tmp_name = self.Text["Edit transaction"]
        new_window = create_window(
            f"{tmp_name} {current_transaction.id}",
            700,
            500,
            min_width=700,
            min_height=500,
            resizable=False
        )

        window_fr = tk.Frame(new_window)
        window_fr.pack(side="top", expand=True, fill="both")

        window_frame = GUIFrame(window_fr, side="top",
                                expand=True, fill="both")

        info_name = GUILabelAndEntry(
            label_text=self.Text["Name"],
            edible=True,
            default_text=current_transaction.name
            )
        info_name.side = "top"
        info_name.entry_side = "left"

        info_description = GUILabelAndEntry(
            self.Text["Description"],
            edible=True,
            default_text=current_transaction.description,
            row_count=3
            )
        info_description.side = "top"
        info_description.entry_side = "left"

        info_balance = GUILabelAndEntry(
            self.Text["Balance"],
            edible=True,
            only_numbers=True,
            default_text=current_transaction.balance
            )
        info_balance.side = "top"
        info_balance.entry_side = "left"

        info_date = GUILabelAndEntry(self.Text["Date(YYYY-MM-DD)"], edible=True, default_text=current_transaction.date.isoformat())
        info_date.side = "top"
        info_date.entry_side = "left"

        window_frame.add(info_name)
        window_frame.add(info_description)
        window_frame.add(info_date)
        window_frame.add(info_balance)

        current_tags = {}
        available_tags = {}

        for tag in self.tag_list_holder.items():
            if tag[0] in current_transaction.tags_id:
                current_tags[tag[0]] = tag[1].name
            else:
                available_tags[tag[0]] = tag[1].name

        info_tags = GUIListToList(
            source_dict=available_tags,
            asset_dict=current_tags,
            assets_header=self.Text["Transaction tags"],
            source_header=self.Text["Available tags"],
            row_count=6
            )
        info_tags.fill = "both"
        info_tags.expand = True
        info_tags.relief = "flat"

        def tmp_f() -> None:
            if info_name.entry.get("1.0", "end-1c"):

                try:
                    transaction_date = date.fromisoformat(info_date.entry.get("1.0", "end-1c"))
                except:
                    messagebox.showerror(self.Text["Error"], self.Text["Invalid date!"], parent=new_window)
                    return

                try:
                    balance : float = float(info_balance.entry.get())
                except:
                    balance : float = current_transaction.balance

                self.fv_edit_selected_transaction(
                    transaction=current_transaction,
                    name=info_name.entry.get("1.0", "end-1c"),
                    description=info_description.entry.get("1.0", "end-1c"),
                    balance=balance,
                    tags_id=info_tags.get_assets().keys(),
                    date_=transaction_date
                )
                new_window.destroy()
            else:
                messagebox.showinfo(self.Text["Error"], self.Text["Please enter name"], parent=new_window)

        window_frame.add(info_tags)

        buttons_frame = GUIFrame(window_frame, "bottom", relief="flat")

        create_button = GUIButton(self.Text["Save"], function=tmp_f)
        cancel_button = GUIButton(self.Text["Cancel"], function=new_window.destroy)

        buttons_frame.add(cancel_button)
        buttons_frame.add(create_button)

        window_frame.add(buttons_frame)

        window_frame.pack()

    def f_remove_transaction_button(self) -> None:

        selected_index = self.transaction_listbox.listbox.curselection()
        if not selected_index:
            messagebox.showinfo(self.Text["Error"], self.Text["Please select transaction first!"], parent=self.root)
            return
        
        want_to_delete = messagebox.askyesno(self.Text["Are you sure?"], self.Text["Do you realy want to delete selected transaction?"], parent=self.root)
        
        if want_to_delete:
            self.fv_delete_selected_transaction()

    def f_filter_transaction_button(self) -> None:

        new_window = create_window(
            self.Text["Filter transactions"],
            700,
            500,
            min_width=700,
            min_height=500,
            resizable=False
        )

        window_fr = tk.Frame(new_window)
        window_fr.pack(side="top", expand=True, fill="both")

        window_frame = GUIFrame(window_fr, side="top",
                                expand=True, fill="both")

        info_tag_to_look = GUIListBox(
            row_count=10,
            label_text=self.Text["Select tag to look for (optional)"],
            vscrollbar=True
            )
        info_tag_to_look.side = "top"
        

        info_date_from = GUILabelAndEntry(self.Text["Date from <YYYY-MM-DD> (optional)"], row_count=1)
        info_date_from.side = "top"
        info_date_to = GUILabelAndEntry(self.Text["Date to <YYYY-MM-DD> (optional)"], row_count=1)
        info_date_to.side = "top"

        window_frame.add(info_tag_to_look)
        window_frame.add(info_date_from)
        window_frame.add(info_date_to)

        def tmp_f() -> None:
            # Tag
            selected_tag_index = info_tag_to_look.listbox.curselection() 
            if selected_tag_index:
                selected_tag = list(self.tag_list_holder.keys())[selected_tag_index[0]]
            else:
                selected_tag = None
            # Date from
            date_from = info_date_from.entry.get("1.0", "end-1c")
            if date_from:
                try:
                    date_from = date.fromisoformat(date_from)
                except:
                    messagebox.showerror("Error", self.Text["Invalid date from!"], parent=new_window)
                    return
            else:
                date_from = None
            # Date to
            date_to = info_date_to.entry.get("1.0", "end-1c")
            if date_to:
                try:
                    date_to = date.fromisoformat(date_to)
                except:
                    messagebox.showerror("Error", self.Text["Invalid date to!"], parent=new_window)
                    return
            else:
                date_to = None

            self.fv_filter_transactions(
                tag_to_look=selected_tag,
                date_from=date_from,
                date_to=date_to
            )
            new_window.destroy()

        buttons_frame = GUIFrame(window_frame, "bottom", relief="flat")

        filter_button = GUIButton(self.Text["Filter"], function=tmp_f)
        cancel_button = GUIButton(self.Text["Cancel"], function=new_window.destroy)

        buttons_frame.add(cancel_button)
        buttons_frame.add(filter_button)

        window_frame.add(buttons_frame)

        window_frame.pack()

        for tag in self.tag_list_holder.values():
            info_tag_to_look.add_item(tag.name)

    def create_main_tab(self) -> None:
        # Tab frame
        self.transaction_tab = tk.Frame(self.notebook)
        self.main_tab_frame = GUIFrame(
            self.transaction_tab, fill="both", expand=True)

        # Transaction history frame
        self.transaction_list_frame = GUIFrame(
            self.main_tab_frame.frame, side="left", fill="both")

        self.transaction_listbox = GUIListBox(
            row_count=30,
            label_text=self.Text["Transaction History"],
            vscrollbar=True,
            hscrollbar=True
            )
        self.transaction_listbox.listbox_width = 70

        self.bottom_panel_frame = GUIFrame(
            self.transaction_list_frame, side="bottom", fill="both", expand=True, relief="flat"
            )
        
        self.info_final_balance = GUILabelAndEntry(self.Text["Sum"], edible=False, row_width=15)
        self.info_final_balance.side = "left"

        self.sort_buttons_frame = GUIFrame(self.bottom_panel_frame, side="left", fill="none", expand=True, relief="flat")
        def sort_date_f_holder() -> None:
            self.fv_sort_transactions_by_date()
        def sort_balance_f_holder() -> None:
            self.fv_sort_transactions_by_balance()
        self.sort_date_button = GUIButton(self.Text["Sort by date"], function=sort_date_f_holder)
        self.sort_date_button.side = "top"
        self.sort_balance_button = GUIButton(self.Text["Sort by balance"], function=sort_balance_f_holder)
        self.sort_balance_button.side = "top"

        self.sort_buttons_frame.add(self.sort_date_button)
        self.sort_buttons_frame.add(self.sort_balance_button)

        self.filter_buttons_frame = GUIFrame(self.bottom_panel_frame, side="left", fill="none", expand=True, relief="flat")

        def clear_filter_f_holder() -> None:
            self.fv_clear_filter()
        self.filter_button = GUIButton(self.Text["Filter"], function=self.f_filter_transaction_button)
        self.filter_button.side = "top"
        self.clear_filter_button = GUIButton(self.Text["Clear filter"], function=clear_filter_f_holder)
        self.clear_filter_button.side = "top"

        self.filter_buttons_frame.add(self.filter_button)
        self.filter_buttons_frame.add(self.clear_filter_button)

        self.bottom_panel_frame.add(self.info_final_balance)
        self.bottom_panel_frame.add(self.sort_buttons_frame)
        self.bottom_panel_frame.add(self.filter_buttons_frame)

        self.transaction_list_frame.add(self.transaction_listbox)
        self.transaction_list_frame.add(self.bottom_panel_frame)

        self.main_tab_frame.add(self.transaction_list_frame)

        # Information and buttons frmae
        self.info_and_buttons_frame = GUIFrame(
            self.main_tab_frame, side="right", fill="both", padx=30, pady=30)

        # Info frame
        self.info_frame = GUIFrame(
            self.info_and_buttons_frame, side="top", expand=True, fill="both", relief="flat")

        self.info_name = GUILabelAndEntry(self.Text["Name"], edible=False)
        self.info_balance = GUILabelAndEntry(self.Text["Balance"], edible=False)
        # self.info_balance.relief = "raised"
        self.info_balance.borderwidth = 2
        self.info_description = GUILabelAndEntry(
            self.Text["Description"], edible=False, row_count=4)
        
        self.info_date = GUILabelAndEntry(self.Text["Date(YYYY-MM-DD)"], edible=False)
        
        self.info_tags = GUIListBox(row_count=3, label_text=self.Text["Tags"])
        self.info_tags.listbox_width = 20
        
        self.info_id = GUILabelAndEntry(self.Text["ID"], edible=False)

        self.info_frame.add(self.info_name)
        self.info_frame.add(self.info_balance)
        self.info_frame.add(self.info_description)
        self.info_frame.add(self.info_date)
        self.info_frame.add(self.info_tags)
        self.info_frame.add(self.info_id)

        self.info_and_buttons_frame.add(self.info_frame)

        # Button frame
        self.button_frame = GUIFrame(
            self.info_and_buttons_frame, side="bottom", fill="none", padx=30, pady=30, relief="flat")

        self.add_transaction_button = GUIButton(
            self.Text["Add"], function=self.f_add_transaction_button, color="#9ED689")
        self.add_transaction_button.width = 10
        self.add_transaction_button.height = 2
        self.add_transaction_button.padx = 2
        self.edit_transaction_button = GUIButton(
            self.Text["Edit"], function=self.f_edit_transaction_button)
        self.edit_transaction_button.width = 10
        self.edit_transaction_button.height = 2
        self.edit_transaction_button.padx = 2
        self.remove_transaction_button = GUIButton(
            self.Text["Remove"], function=self.f_remove_transaction_button, color="#DD8D75")
        self.remove_transaction_button.width = 10
        self.remove_transaction_button.height = 2
        self.remove_transaction_button.padx = 2

        self.button_frame.add(self.add_transaction_button)
        self.button_frame.add(self.edit_transaction_button)
        self.button_frame.add(self.remove_transaction_button)

        self.info_and_buttons_frame.add(self.button_frame)

        self.main_tab_frame.add(self.info_and_buttons_frame)

        self.main_tab_frame.pack()

        self.notebook.add(self.transaction_tab, text=self.Text["Transactions"])

    def f_add_tag_button(self) -> None:

        new_window = create_window(
            title=self.Text["Create tag"],
            width=300,
            height=300,
            min_width=300,
            min_height=300,
            resizable=False
        )

        window_fr = tk.Frame(new_window)
        window_fr.pack(side="top", expand=True, fill="both")

        window_frame = GUIFrame(window_fr, side="top",
                                expand=True, fill="both")

        info_name = GUILabelAndEntry(self.Text["Name"], edible=True)
        info_name.side = "top"
        info_name.entry_side = "left"
        info_description = GUILabelAndEntry(
            self.Text["Description"], edible=True, row_count=3)
        info_description.side = "top"
        info_description.entry_side = "left"

        window_frame.add(info_name)
        window_frame.add(info_description)

        def tmp_f() -> None:
            if info_name.entry.get("1.0", "end-1c"):
                self.fv_create_tag(
                    name=info_name.entry.get("1.0", "end-1c"),
                    description=info_description.entry.get("1.0", "end-1c")
                )
                new_window.destroy()
            else:
                messagebox.showinfo(self.Text["Error"], self.Text["Please enter name!"], parent=new_window)

        buttons_frame = GUIFrame(window_frame, "bottom", relief="flat")

        create_button = GUIButton(self.Text["Create"], function=tmp_f)
        cancel_button = GUIButton(self.Text["Cancel"], function=new_window.destroy)

        buttons_frame.add(cancel_button)
        buttons_frame.add(create_button)

        window_frame.add(buttons_frame)

        window_frame.pack()

    def f_edit_tag_button(self) -> None:

        current_tag = self.fv_get_current_tag()

        if current_tag == None:
            messagebox.showinfo(self.Text["Error"], self.Text["Please select tag first!"], parent=self.root)
            return

        new_window = create_window(
            title=self.Text["Edit tag"],
            width=300,
            height=300,
            min_width=300,
            min_height=300,
            resizable=False
        )

        window_fr = tk.Frame(new_window)
        window_fr.pack(side="top", expand=True, fill="both")

        window_frame = GUIFrame(window_fr, side="top",
                                expand=True, fill="both")

        info_name = GUILabelAndEntry(self.Text["Name"], edible=True, default_text=current_tag.name)
        info_name.side = "top"
        info_name.entry_side = "left"
        info_description = GUILabelAndEntry(
            self.Text["Description"],
            edible=True,
            row_count=3,
            default_text=current_tag.description
            )
        info_description.side = "top"
        info_description.entry_side = "left"

        window_frame.add(info_name)
        window_frame.add(info_description)

        def tmp_f() -> None:
            if info_name.entry.get("1.0", "end-1c"):
                self.fv_edit_selected_tag(
                    tag=current_tag,
                    name=info_name.entry.get("1.0", "end-1c"),
                    description=info_description.entry.get("1.0", "end-1c")
                )
                new_window.destroy()
            else:
                messagebox.showinfo(self.Text["Error"], self.Text["Please enter name!"], parent=new_window)

        buttons_frame = GUIFrame(window_frame, "bottom", relief="flat")

        create_button = GUIButton(self.Text["Create"], function=tmp_f)
        cancel_button = GUIButton(self.Text["Cancel"], function=new_window.destroy)

        buttons_frame.add(cancel_button)
        buttons_frame.add(create_button)

        window_frame.add(buttons_frame)

        window_frame.pack()

    def f_remove_tag_button(self) -> None:

        selected_index = self.tags_listbox.listbox.curselection()
        if not selected_index:
            messagebox.showinfo(self.Text["Error"], self.Text["Please select tag first!"], parent=self.root)
            return
        
        want_to_delete = messagebox.askyesno(self.Text["Are you sure?"], self.Text["Do you realy want to delete selected tag?"], parent=self.root)
        
        if want_to_delete:
            self.fv_delete_selected_tag()


    def create_tag_tab(self) -> None:
        # Tab frame
        self.tag_tab = tk.Frame(self.notebook)
        self.tag_tab_frame = GUIFrame(self.tag_tab, fill="both", expand=True)

        # Transaction history frame
        self.tag_list_frame = GUIFrame(
            self.tag_tab_frame.frame, side="left", fill="both")

        self.tags_listbox = GUIListBox(30, self.Text["Tag list"])
        self.tag_list_frame.add(self.tags_listbox)

        self.tag_tab_frame.add(self.tag_list_frame)

        # Information and buttons frmae
        self.tag_info_and_buttons_frame = GUIFrame(
            self.tag_tab_frame, side="right", fill="both", padx=30, pady=30)

        # Info frame
        self.tag_info_frame = GUIFrame(
            self.tag_info_and_buttons_frame, side="top", expand=True, fill="both", relief="flat")

        self.tag_info_name = GUILabelAndEntry(self.Text["Name"], edible=False)
        self.tag_info_description = GUILabelAndEntry(
            self.Text["Description"], edible=False, row_count=3)
        self.tag_info_id = GUILabelAndEntry(self.Text["ID"], edible=False)

        self.tag_info_frame.add(self.tag_info_name)
        self.tag_info_frame.add(self.tag_info_description)
        self.tag_info_frame.add(self.tag_info_id)

        self.tag_info_and_buttons_frame.add(self.tag_info_frame)

        # Button frame
        self.tag_button_frame = GUIFrame(
            self.tag_info_and_buttons_frame, side="bottom", fill="none", padx=30, pady=30, relief="flat")

        self.add_tag_button = GUIButton(
            self.Text["Add"], function=self.f_add_tag_button, color="#9ED689")
        self.add_tag_button.width = 10
        self.add_tag_button.height = 2
        self.add_tag_button.padx = 2
        self.edit_tag_button = GUIButton(
            self.Text["Edit"], function=self.f_edit_tag_button)
        self.edit_tag_button.width = 10
        self.edit_tag_button.height = 2
        self.edit_tag_button.padx = 2
        self.remove_tag_button = GUIButton(
            self.Text["Remove"], function=self.f_remove_tag_button, color="#DD8D75")
        self.remove_tag_button.width = 10
        self.remove_tag_button.height = 2
        self.remove_tag_button.padx = 2

        self.tag_button_frame.add(self.add_tag_button)
        self.tag_button_frame.add(self.edit_tag_button)
        self.tag_button_frame.add(self.remove_tag_button)

        self.tag_info_and_buttons_frame.add(self.tag_button_frame)

        self.tag_tab_frame.add(self.tag_info_and_buttons_frame)

        self.tag_tab_frame.pack()

        self.notebook.add(self.tag_tab, text=self.Text["Tags tab"])

    def add_transaction_to_display(self, transaction: Transaction) -> None:
        
        

        self.transaction_listbox.add_item(transaction.__str__())

        if transaction.balance > 0:
            self.transaction_listbox.listbox.itemconfig(
                index=self.transaction_listbox.listbox.size() - 1,
                foreground="green"
            )
        elif transaction.balance < 0:
            self.transaction_listbox.listbox.itemconfig(
                index=self.transaction_listbox.listbox.size() - 1,
                foreground="red"
            )
        else:
            self.transaction_listbox.listbox.itemconfig(
                index=self.transaction_listbox.listbox.size() - 1,
                foreground="grey"
            )
        

    def add_tag_to_display(self, tag: Tag) -> None:
        self.tags_listbox.add_item(tag.__str__())

 
    def init_font(self) -> None:
        default_font = tk.font.nametofont("TkDefaultFont")

        default_font.configure(
            # family="Comic Sans MS",
            family=FONTS[self.font_index],
            size=self.font_size, 
            weight=font.NORMAL,
        )

        self.root.option_add("*Font", default_font)

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app = GUI()
    app.run()

