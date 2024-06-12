if __name__ == "__main__":
    import sys
    import os.path

    sys.path[0] = os.path.join(sys.path[0], "..", "..")

from modules.gui.basic_elements import GUIFrame, GUIButton
from modules.gui.label_and_entry import GUILabelAndEntry
from modules.gui.listbox import GUIListBox
from modules.gui.list_to_list import GUIListToList
from modules.tracker_logic.classes import Transaction, Tag

from typing import Dict

from datetime import date
import datetime

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
    def __init__(self) -> None:

        # Root init
        self.root = tk.Tk()

        # Title
        self.root.title("Money Tracker")

        self.root.update_idletasks()
        self.root.attributes('-zoomed', True)

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
        

        # Notebook creation
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.fv_delete_selected_transaction = lambda: None
        self.fv_edit_selected_transaction = lambda: None
        self.fv_create_transaction = lambda: None

        self.fv_get_current_transaction = lambda: None
        self.fv_get_current_tag = lambda: None

        self.fv_delete_selected_tag = lambda: None
        self.fv_edit_selected_tag = lambda: None
        self.fv_create_tag = lambda: None

        self.tag_list_holder : Dict[str, Tag] = None

        self.init_font()

        self.create_main_tab()
        self.create_tag_tab()

        

    def f_add_transaction_button(self) -> None:

        new_window = create_window(
            "Create transaction",
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

        info_frame = GUIFrame(window_frame, side="top",
                              expand=True, fill="both", relief="flat")

        info_name = GUILabelAndEntry("Name", edible=True)
        info_name.side = "top"
        info_name.entry_side = "left"

        info_description = GUILabelAndEntry(
            "Description", edible=True, row_count=3)
        info_description.side = "top"
        info_description.entry_side = "left"

        info_balance = GUILabelAndEntry("Balance", edible=True, only_numbers=True, default_text="0.0")
        info_balance.side = "top"
        info_balance.entry_side = "left"

        info_date = GUILabelAndEntry("Date(YYYY-MM-DD)", edible=True, default_text=date.today().isoformat())
        info_date.side = "top"
        info_date.entry_side = "left"

        info_frame.add(info_name)
        info_frame.add(info_description)
        info_frame.add(info_balance)
        info_frame.add(info_date)

        window_frame.add(info_frame)

        tag_list = {key : value.name for key, value in self.tag_list_holder.items()}

        info_tags = GUIListToList(
            source_dict=tag_list, assets_header="Transaction tags", source_header="Available tags", row_count=6)
        info_tags.fill = "both"
        info_tags.expand = True
        info_tags.relief = "flat"

        def tmp_f() -> None:
            if info_name.entry.get("1.0", "end-1c"):

                try:
                    transaction_date = date.fromisoformat(info_date.entry.get("1.0", "end-1c"))
                except:
                    messagebox.showerror("Error", "Invalid date!", parent=new_window)
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
                messagebox.showinfo("Error", "Please enter name", parent=new_window)

        window_frame.add(info_tags)

        buttons_frame = GUIFrame(window_frame, "bottom", relief="flat")

        create_button = GUIButton("Create", function=tmp_f)
        cancel_button = GUIButton("Cancel", function=new_window.destroy)

        buttons_frame.add(cancel_button)
        buttons_frame.add(create_button)

        window_frame.add(buttons_frame)

        window_frame.pack()

    def f_edit_transaction_button(self) -> None:
        current_transaction : Transaction = self.fv_get_current_transaction()

        if current_transaction == None:
            messagebox.showinfo("Error", "Please select transaction first", parent=self.root)
            return
        
        new_window = create_window(
            f"Edit transaction {current_transaction.id}",
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

        info_frame = GUIFrame(window_frame, side="top",
                              expand=True, fill="both", relief="flat")

        info_name = GUILabelAndEntry(
            label_text="Name",
            edible=True,
            default_text=current_transaction.name
            )
        info_name.side = "top"
        info_name.entry_side = "left"

        info_description = GUILabelAndEntry(
            "Description",
            edible=True,
            default_text=current_transaction.description,
            row_count=3
            )
        info_description.side = "top"
        info_description.entry_side = "left"

        info_balance = GUILabelAndEntry(
            "Balance",
            edible=True,
            only_numbers=True,
            default_text=current_transaction.balance
            )
        info_balance.side = "top"
        info_balance.entry_side = "left"

        info_date = GUILabelAndEntry("Date(YYYY-MM-DD)", edible=True, default_text=current_transaction.date.isoformat())
        info_date.side = "top"
        info_date.entry_side = "left"

        info_frame.add(info_name)
        info_frame.add(info_description)
        info_frame.add(info_date)
        info_frame.add(info_balance)

        window_frame.add(info_frame)

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
            assets_header="Transaction tags",
            source_header="Available tags",
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
                    messagebox.showerror("Error", "Invalid date!", parent=new_window)
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
                messagebox.showinfo("Error", "Please enter name", parent=new_window)

        window_frame.add(info_tags)

        buttons_frame = GUIFrame(window_frame, "bottom", relief="flat")

        create_button = GUIButton("Save", function=tmp_f)
        cancel_button = GUIButton("Cancel", function=new_window.destroy)

        buttons_frame.add(cancel_button)
        buttons_frame.add(create_button)

        window_frame.add(buttons_frame)

        window_frame.pack()

    def f_remove_transaction_button(self) -> None:

        selected_index = self.transaction_listbox.listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Error", "Please select transaction first", parent=self.root)
            return
        
        want_to_delete = messagebox.askyesno("Are you sure?", "Do you realy want to delete selected transaction?", parent=self.root)
        
        if want_to_delete:
            self.fv_delete_selected_transaction()

        return
        new_window = tk.Toplevel()

        window_width = 300
        window_height = 100
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        new_window.geometry("%dx%d+%d+%d" % (window_width,
                            window_height, x_coordinate, y_coordinate))

        new_window.resizable(False, False)

        new_window.title("Are you sure?")

        window_fr = tk.Frame(new_window)
        window_fr.pack()

        label = tk.Label(
            window_fr, text="Do you realy want to delete selected transaction?")
        label.pack(side="top", fill="both", pady=10)

        window_frame = GUIFrame(window_fr, "bottom", relief="flat")

        def tmp_f() -> None:
            self.fv_delete_selected_transaction()
            new_window.destroy()

        yes_button = GUIButton("Yes", function=tmp_f)
        no_button = GUIButton("No", function=new_window.destroy)

        window_frame.add(no_button)
        window_frame.add(yes_button)

        window_frame.pack()

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
            label_text="Transaction History",
            vscrollbar=True,
            hscrollbar=True
            )
        self.transaction_listbox.listbox_width = 70

        self.bottom_frame = GUIFrame(
            self.transaction_list_frame, side="bottom", fill="both", expand=True, relief="flat"
            )
        
        self.info_final_balance = GUILabelAndEntry("Sum", edible=False, row_width=15)
        

        self.bottom_frame.add(self.info_final_balance)

        self.transaction_list_frame.add(self.transaction_listbox)
        self.transaction_list_frame.add(self.bottom_frame)

        self.main_tab_frame.add(self.transaction_list_frame)

        # Information and buttons frmae
        self.info_and_buttons_frame = GUIFrame(
            self.main_tab_frame, side="right", fill="both", padx=30, pady=30)

        # Info frame
        self.info_frame = GUIFrame(
            self.info_and_buttons_frame, side="top", expand=True, fill="both", relief="flat")

        self.info_name = GUILabelAndEntry("Name", edible=False)
        self.info_balance = GUILabelAndEntry("Balance", edible=False)
        # self.info_balance.relief = "raised"
        self.info_balance.borderwidth = 2
        self.info_description = GUILabelAndEntry(
            "Description", edible=False, row_count=4)
        
        self.info_date = GUILabelAndEntry("Date(YYYY-MM-DD)", edible=False)
        
        self.info_tags = GUIListBox(row_count=3, label_text="Tags")
        self.info_tags.listbox_width = 20
        
        self.info_id = GUILabelAndEntry("ID", edible=False)

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
            "Add", function=self.f_add_transaction_button, color="#9ED689")
        self.add_transaction_button.width = 10
        self.add_transaction_button.height = 2
        self.add_transaction_button.padx = 2
        self.edit_transaction_button = GUIButton(
            "Edit", function=self.f_edit_transaction_button)
        self.edit_transaction_button.width = 10
        self.edit_transaction_button.height = 2
        self.edit_transaction_button.padx = 2
        self.remove_transaction_button = GUIButton(
            "Remove", function=self.f_remove_transaction_button, color="#DD8D75")
        self.remove_transaction_button.width = 10
        self.remove_transaction_button.height = 2
        self.remove_transaction_button.padx = 2

        self.button_frame.add(self.add_transaction_button)
        self.button_frame.add(self.edit_transaction_button)
        self.button_frame.add(self.remove_transaction_button)

        self.info_and_buttons_frame.add(self.button_frame)

        self.main_tab_frame.add(self.info_and_buttons_frame)

        self.main_tab_frame.pack()

        self.notebook.add(self.transaction_tab, text="Transactions")

    def f_add_tag_button(self) -> None:

        new_window = create_window(
            title="Create tag",
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

        info_frame = GUIFrame(window_frame, side="top",
                              expand=True, fill="both", relief="flat")

        info_name = GUILabelAndEntry("Name", edible=True)
        info_name.side = "top"
        info_name.entry_side = "left"
        info_description = GUILabelAndEntry(
            "Description", edible=True, row_count=3)
        info_description.side = "top"
        info_description.entry_side = "left"

        info_frame.add(info_name)
        info_frame.add(info_description)

        window_frame.add(info_frame)

        def tmp_f() -> None:
            if info_name.entry.get("1.0", "end-1c"):
                self.fv_create_tag(
                    name=info_name.entry.get("1.0", "end-1c"),
                    description=info_description.entry.get("1.0", "end-1c")
                )
                new_window.destroy()
            else:
                messagebox.showinfo("Error", "Please enter name", parent=new_window)

        buttons_frame = GUIFrame(window_frame, "bottom", relief="flat")

        create_button = GUIButton("Create", function=tmp_f)
        cancel_button = GUIButton("Cancel", function=new_window.destroy)

        buttons_frame.add(cancel_button)
        buttons_frame.add(create_button)

        window_frame.add(buttons_frame)

        window_frame.pack()

    def f_edit_tag_button(self) -> None:

        current_tag = self.fv_get_current_tag()

        if current_tag == None:
            messagebox.showinfo("Error", "Please select tag first", parent=self.root)
            return

        new_window = create_window(
            title="Edit tag",
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

        info_frame = GUIFrame(window_frame, side="top",
                              expand=True, fill="both", relief="flat")

        info_name = GUILabelAndEntry("Name", edible=True, default_text=current_tag.name)
        info_name.side = "top"
        info_name.entry_side = "left"
        info_description = GUILabelAndEntry(
            "Description",
            edible=True,
            row_count=3,
            default_text=current_tag.description
            )
        info_description.side = "top"
        info_description.entry_side = "left"

        info_frame.add(info_name)
        info_frame.add(info_description)

        window_frame.add(info_frame)

        def tmp_f() -> None:
            if info_name.entry.get("1.0", "end-1c"):
                self.fv_edit_selected_tag(
                    tag=current_tag,
                    name=info_name.entry.get("1.0", "end-1c"),
                    description=info_description.entry.get("1.0", "end-1c")
                )
                new_window.destroy()
            else:
                messagebox.showinfo("Error", "Please enter name", parent=new_window)

        buttons_frame = GUIFrame(window_frame, "bottom", relief="flat")

        create_button = GUIButton("Create", function=tmp_f)
        cancel_button = GUIButton("Cancel", function=new_window.destroy)

        buttons_frame.add(cancel_button)
        buttons_frame.add(create_button)

        window_frame.add(buttons_frame)

        window_frame.pack()


    def f_remove_tag_button(self) -> None:
        new_window = tk.Toplevel()

        window_width = 300
        window_height = 100
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        new_window.geometry("%dx%d+%d+%d" % (window_width,
                            window_height, x_coordinate, y_coordinate))

        new_window.resizable(False, False)

        new_window.title("Are you sure?")

        window_fr = tk.Frame(new_window)
        window_fr.pack()

        label = tk.Label(
            window_fr, text="Do you realy want to delete selected tag?")
        label.pack(side="top", fill="both", pady=10)

        window_frame = GUIFrame(window_fr, "bottom", relief="flat")

        def tmp_f() -> None:
            self.fv_delete_selected_tag()
            new_window.destroy()

        yes_button = GUIButton("Yes", function=tmp_f)
        no_button = GUIButton("No", function=new_window.destroy)

        window_frame.add(no_button)
        window_frame.add(yes_button)

        window_frame.pack()

    def create_tag_tab(self) -> None:
        # Tab frame
        self.tag_tab = tk.Frame(self.notebook)
        self.tag_tab_frame = GUIFrame(self.tag_tab, fill="both", expand=True)

        # Transaction history frame
        self.tag_list_frame = GUIFrame(
            self.tag_tab_frame.frame, side="left", fill="both")

        self.tags_listbox = GUIListBox(30, "Tag list")
        self.tag_list_frame.add(self.tags_listbox)

        self.tag_tab_frame.add(self.tag_list_frame)

        # Information and buttons frmae
        self.tag_info_and_buttons_frame = GUIFrame(
            self.tag_tab_frame, side="right", fill="both", padx=30, pady=30)

        # Info frame
        self.tag_info_frame = GUIFrame(
            self.tag_info_and_buttons_frame, side="top", expand=True, fill="both", relief="flat")

        self.tag_info_name = GUILabelAndEntry("Name", edible=False)
        self.tag_info_description = GUILabelAndEntry(
            "Description", edible=False, row_count=3)
        self.tag_info_id = GUILabelAndEntry("ID", edible=False)

        self.tag_info_frame.add(self.tag_info_name)
        self.tag_info_frame.add(self.tag_info_description)
        self.tag_info_frame.add(self.tag_info_id)

        self.tag_info_and_buttons_frame.add(self.tag_info_frame)

        # Button frame
        self.tag_button_frame = GUIFrame(
            self.tag_info_and_buttons_frame, side="bottom", fill="none", padx=30, pady=30, relief="flat")

        self.add_tag_button = GUIButton(
            "Add", function=self.f_add_tag_button, color="#9ED689")
        self.add_tag_button.width = 10
        self.add_tag_button.height = 2
        self.add_tag_button.padx = 2
        self.edit_tag_button = GUIButton(
            "Edit", function=self.f_edit_tag_button)
        self.edit_tag_button.width = 10
        self.edit_tag_button.height = 2
        self.edit_tag_button.padx = 2
        self.remove_tag_button = GUIButton(
            "Remove", function=self.f_remove_tag_button, color="#DD8D75")
        self.remove_tag_button.width = 10
        self.remove_tag_button.height = 2
        self.remove_tag_button.padx = 2

        self.tag_button_frame.add(self.add_tag_button)
        self.tag_button_frame.add(self.edit_tag_button)
        self.tag_button_frame.add(self.remove_tag_button)

        self.tag_info_and_buttons_frame.add(self.tag_button_frame)

        self.tag_tab_frame.add(self.tag_info_and_buttons_frame)

        self.tag_tab_frame.pack()

        self.notebook.add(self.tag_tab, text="Tag")

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
            family="Comic Sans MS", 
            size=10, 
            weight=font.NORMAL,
        )

        self.root.option_add("*Font", default_font)

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app = GUI()
    app.run()

