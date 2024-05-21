import tkinter as tk
from tkinter import ttk

class GUIElement:
    def __init__(self, side : str = "top", expand : bool = True, fill : str = "none", relief : str = "flat", borderwidth=0, padx : int = 0, pady = 0, width : int = -1, height : int = -1) -> None:
        self.side = side
        self.expand = expand
        self.fill = fill

        self.relief = relief
        self.borderwidth = borderwidth

        self.padx = padx
        self.pady = pady

        self.width = width
        self.height = height

class GUIFrame(GUIElement):
    def __init__(self, root, side : str = "top", expand : bool = True, fill : str = "none", relief : str = "raised", borderwidth : int = 2, padx : int = 0, pady : int = 0, width : int = -1, height : int = -1) -> None:
        super().__init__(side=side, expand=expand, fill=fill, relief=relief, borderwidth=borderwidth, padx=padx, pady=pady, width=width, height=height)
        self.root = root
        if isinstance(root, tk.Frame):
            self.frame = tk.Frame(self.root, relief=self.relief, borderwidth=self.borderwidth, width=self.width, height=self.height)
        elif isinstance(root, GUIFrame):
            self.frame = tk.Frame(self.root.frame, relief=self.relief, borderwidth=self.borderwidth, width=self.width, height=self.height)
        else:
            raise TypeError(f"Root must be tk.Frame or GUIFrame, {type(root)} was given!")
        self.elements = []
        
    def add(self, element) -> None:
        self.elements.append(element)
        
    def pack(self, root="") -> None:
        if root != "":
            self.root = root
        if isinstance(self.root, tk.Frame):
            self.frame = tk.Frame(self.root, relief=self.relief, borderwidth=self.borderwidth, width=self.width, height=self.height)
        elif isinstance(self.root, GUIFrame):
            self.frame = tk.Frame(self.root.frame, relief=self.relief, borderwidth=self.borderwidth, width=self.width, height=self.height)
        else:
            raise TypeError(f"Root must be tk.Frame or GUIFrame, {type(self.root)} was given!")
        self.frame.pack(expand=self.expand, fill=self.fill, side=self.side, padx=self.padx, pady=self.pady)
        for i in range(len(self.elements)):
            self.elements[i].pack(self.frame)
            
            

class GUILabelAndInput(GUIElement):
    def __init__(self, label_text : str, edible : bool = True, default_text : str = "", row_count : int = 1, row_width : int = 30) -> None:
        super().__init__(side="top", fill="x", expand=True, padx=10, pady=10)
        self.label_text = label_text
        self.edible = edible
        self.default_text = default_text
        self.row_count = row_count
        self.row_width = row_width

        self.entry_side = "left"
        self.entry_left_offset = 10
        
    def pack(self, root : tk.Frame) -> None:
        
        self.frame : tk.Frame = tk.Frame(root, relief=self.relief, borderwidth=self.borderwidth, width=self.width, height=self.height)
        self.frame.pack(side=self.side, fill=self.fill, expand=self.expand, padx=self.padx, pady=self.pady)
        
        self.label : ttk.Label = ttk.Label(self.frame, text=self.label_text)
        self.label.pack(side="left")
        
        self.entry : tk.Text = tk.Text(self.frame, height=self.row_count, width=self.row_width)
        
        self.entry.insert("1.0", self.default_text)
        self.entry.configure(state="normal" if self.edible else "disable")
        self.entry.pack(side=self.entry_side, padx=10 if self.entry_side == "left" else 0)
        
class GUIButton(GUIElement):
    def __init__(self, text : str, function, color : str = "#FFFFFF") -> None:
        super().__init__(side="left", expand=True, fill="none", relief="raised", borderwidth=2, padx=10, pady=10)
        self.text : str = text
        self.function = function
        self.color = color
        
    def pack(self, root : tk.Frame) -> None:
        self.button : tk.Button = tk.Button(root, text=self.text, command=self.function, bg=self.color, relief=self.relief, borderwidth=self.borderwidth, width=self.width, height=self.height)
        self.button.pack(side=self.side, expand=self.expand, fill=self.fill, padx=self.padx, pady=self.pady)
        
class GUIListBox(GUIElement):
    def __init__(self, row_count : int, label_text : str = "") -> None:
        super().__init__(side="top", expand=True, fill="both", padx=10, pady=10)
        self.row_count = row_count
        self.label_text : str = label_text
        self.listbox : tk.Listbox = None
        
    def add_item(self, item : str) -> None:
        self.listbox.insert(tk.END, item)
        
    def remove_item(self, index : int) -> None:
        self.listbox.delete(index)
        
    def remove_selected_item(self) -> None:
        selected_index = self.listbox.curselection()
        if selected_index:
            self.remove_item(selected_index)
            
    def set_item(self, index : int, item : str) -> None:
        self.listbox.delete(index)
        self.listbox.insert(index, item)
        
    def set_selected_item(self, item : str) -> None:
        selected_index = self.listbox.curselection()
        if selected_index:
            self.set_item(selected_index, item)
        
    def pack(self, root : tk.Frame) -> None:
        self.main_frame : tk.Frame = tk.Frame(root, relief=self.relief, borderwidth=self.borderwidth, width=self.width, height=self.height)
        self.main_frame.pack(side=self.side, fill=self.fill, expand=self.expand, padx=self.padx, pady=self.pady)
        
        self.listbox : tk.Listbox = tk.Listbox(self.main_frame, height=self.row_count)
        self.listbox.pack(side="bottom", expand=True, fill="both")

        self.label = tk.Label(self.main_frame, text=self.label_text)
        self.label.pack(side="bottom", expand=False, fill="both")
        
        
        
class GUIListToList(GUIElement):
    def __init__(self, source_dict : dict[str, str], assets_header : str = "", source_header : str = "", row_count : int = 5) -> None:
        super().__init__(side="top", expand=True, fill="both", relief="raised", borderwidth=2, padx=10, pady=10)
        # { id1 : text1, id2 : text2, ...}
        self.items_list : list[dict] = [self.__create_items_list_item(key, False, value) for key, value in source_dict.items()]
        
        self.source_header : str = source_header
        self.assets_header : str = assets_header
        
        self.source_listbox : GUIListBox = None
        self.assets_listbox : GUIListBox = None
        
        self.row_count = row_count
        
        self.is_packed = False
        
    def __create_items_list_item(self, id : str, in_assets : bool, text : str) -> dict:
        return {"id" : id, "in_assets" : in_assets, "text" : text}
        
    def add_source(self, id : str, text : str) -> None:
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
        
    def source_to_asset(self, index : int) -> None:
        self.items_list[index]["in_assets"] = True
        self.update_lists()
        
    def assets_to_source(self, index : int) -> None:
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
        
    def pack(self, root : tk.Frame) -> None:
        self.is_packed = True
        
        self.main_frame = GUIFrame(root, relief=self.relief, borderwidth=self.borderwidth, expand=self.expand, fill=self.fill, side=self.side, padx=self.padx, pady=self.pady, width=self.width, height=self.height)        
        
        self.assets_listbox = GUIListBox(self.row_count, self.assets_header)
        self.assets_listbox.side = "left"
        self.assets_listbox.relief = "raised"
        self.assets_listbox.borderwidth = 5
        self.main_frame.add(self.assets_listbox)

        self.source_listbox = GUIListBox(self.row_count, self.source_header)
        self.source_listbox.side = "right"
        self.main_frame.add(self.source_listbox)
        
        
        self.button_frame = GUIFrame(self.main_frame.frame, side="bottom", relief="flat")
        
        self.source_to_assets_button = GUIButton("<", self.selected_source_to_asset)
        self.assets_to_source_button = GUIButton(">", self.selected_assets_to_source)
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


class Application:
    def __init__(self) -> None:
        
        # Root init
        self.root = tk.Tk()
        
        # Title
        self.root.title("Money Tracker")
        
        # Window size and position
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        self.root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
        self.root.minsize(width=600, height=500)
        
        # Notebook creation
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_main_tab()
        self.create_transaction_tab()
        
    def delete_selected_transaction(self) -> None:
        pass
    
    def create_transaction(self, name : str, description : str, tags : list) -> None:
        pass
        
    def f_add_transaction_button(self) -> None:
        new_window = tk.Toplevel()
        
        window_width = 500
        window_height = 500
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        new_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
        
        new_window.title("Create transaction")
        new_window.resizable(False, False)
        
        window_fr = tk.Frame(new_window)
        window_fr.pack(side="top", expand=True, fill="both")
        
        window_frame = GUIFrame(window_fr, side="top", expand=True, fill="both")


        info_frame = GUIFrame(window_frame, side="top", expand=True, fill="both", relief="flat")
        
        info_name = GUILabelAndInput("Name", edible=True)
        info_name.side = "top"
        info_name.entry_side = "left"
        info_description = GUILabelAndInput("Description", edible=True, row_count=3)
        info_description.side = "top"
        info_description.entry_side = "left"


        info_frame.add(info_name)
        info_frame.add(info_description)

        window_frame.add(info_frame)

        tag_list = {"000" : "Food", "001" : "Car", "002" : "Unexpected", "003" : "Fun/Relax"}

        info_tags = GUIListToList(source_dict=tag_list, assets_header="Transaction tags", source_header="Available tags", row_count=6)
        info_tags.fill = "both"
        info_tags.expand = True
        info_tags.relief = "flat"
        
        def tmp_f() -> None:
            self.create_transaction(name=info_name.entry.get("1.0", "end-1c"),
                                    description=info_description.entry.get("1.0", "end-1c"), 
                                    tags=info_tags.get_assets().keys())
            new_window.destroy()
        
        
        window_frame.add(info_tags)
        
        buttons_frame = GUIFrame(window_frame, "bottom", relief="flat")
        
        create_button = GUIButton("Create", function=tmp_f)
        cancel_button = GUIButton("Cancel", function=new_window.destroy)
        
        buttons_frame.add(cancel_button)
        buttons_frame.add(create_button)
        
        window_frame.add(buttons_frame)
        
        window_frame.pack()  
    
    def f_edit_transaction_button(self) -> None:
        pass
    
    def f_remove_transaction_button(self) -> None:
        new_window = tk.Toplevel()
        
        window_width = 300
        window_height = 100
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        new_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

        new_window.resizable(False, False)
        
        new_window.title("Are you sure?")
        
        window_fr = tk.Frame(new_window)
        window_fr.pack()
        
        label = tk.Label(window_fr, text="Do you realy want to delete selected transaction?")
        label.pack(side="top", fill="both", pady=10)
        
        window_frame = GUIFrame(window_fr, "bottom", relief="flat")
        
        def tmp_f() -> None:
            self.delete_selected_transaction()
            new_window.destroy()
        
        yes_button = GUIButton("Yes", function=tmp_f)
        no_button = GUIButton("No", function=new_window.destroy)
        
        window_frame.add(no_button)
        window_frame.add(yes_button)
        
        
        window_frame.pack()


    
    def create_main_tab(self) -> None:
        # Tab frame
        self.transaction_tab = tk.Frame(self.notebook)
        self.main_tab_frame = GUIFrame(self.transaction_tab, fill="both", expand=True)
        
        # Transaction history frame
        self.tag_list_frame = GUIFrame(self.main_tab_frame.frame, side="left", fill="both")
        
        self.tags_listbox = GUIListBox(30, "Transaction History")
        self.tag_list_frame.add(self.tags_listbox)
        
        self.main_tab_frame.add(self.tag_list_frame)
        
        
        
        # Information and buttons frmae
        self.info_and_buttons_frame = GUIFrame(self.main_tab_frame, side="right", fill="both", padx=30, pady=30)
        
        # Info frame
        self.info_frame = GUIFrame(self.info_and_buttons_frame, side="top", expand=True, fill="both", relief="flat")
        
        self.info_name = GUILabelAndInput("Name", edible=False)
        self.info_balance = GUILabelAndInput("Balance", edible=False)
        self.info_balance.relief = "raised"
        self.info_balance.borderwidth = 2
        self.info_description = GUILabelAndInput("Description", edible=False, row_count=3)
        self.info_tags = GUIListBox(row_count=3, label_text="Tags")
        self.info_id = GUILabelAndInput("ID", edible=False)
        
        self.info_frame.add(self.info_name)
        self.info_frame.add(self.info_balance)
        self.info_frame.add(self.info_description)
        self.info_frame.add(self.info_tags)
        self.info_frame.add(self.info_id)
        
        self.info_and_buttons_frame.add(self.info_frame)
        
        # Button frame
        self.button_frame = GUIFrame(self.info_and_buttons_frame, side="bottom", fill="none", padx=30, pady=30, relief="flat")
        
        self.add_transaction_button = GUIButton("Add", function=self.f_add_transaction_button, color="#9ED689")
        self.add_transaction_button.width = 10
        self.add_transaction_button.height = 2
        self.add_transaction_button.padx = 2
        self.edit_transaction_button = GUIButton("Edit", function=self.f_edit_transaction_button)
        self.edit_transaction_button.width = 10
        self.edit_transaction_button.height = 2
        self.edit_transaction_button.padx = 2
        self.remove_transaction_button = GUIButton("Remove", function=self.f_remove_transaction_button, color="#DD8D75")
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



    def create_tag(self, name : str, description : str) -> None:
        pass

    def f_add_tag_button(self) -> None:
        new_window = tk.Toplevel()
        
        window_width = 300
        window_height = 300
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        new_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
        
        new_window.title("Create tag")
        new_window.resizable(False, False)
        
        window_fr = tk.Frame(new_window)
        window_fr.pack(side="top", expand=True, fill="both")
        
        window_frame = GUIFrame(window_fr, side="top", expand=True, fill="both")


        info_frame = GUIFrame(window_frame, side="top", expand=True, fill="both", relief="flat")
        
        info_name = GUILabelAndInput("Name", edible=True)
        info_name.side = "top"
        info_name.entry_side = "left"
        info_description = GUILabelAndInput("Description", edible=True, row_count=3)
        info_description.side = "top"
        info_description.entry_side = "left"


        info_frame.add(info_name)
        info_frame.add(info_description)

        window_frame.add(info_frame)
        
        def tmp_f() -> None:
            self.create_tag(name=info_name.entry.get("1.0", "end-1c"), description=info_description.entry.get("1.0", "end-1c"))
            new_window.destroy()
        
        
        buttons_frame = GUIFrame(window_frame, "bottom", relief="flat")
        
        create_button = GUIButton("Create", function=tmp_f)
        cancel_button = GUIButton("Cancel", function=new_window.destroy)
        
        buttons_frame.add(cancel_button)
        buttons_frame.add(create_button)
        
        window_frame.add(buttons_frame)
        
        window_frame.pack()  
    
    def f_edit_tag_button(self) -> None:
        pass
    
    def f_remove_tag_button(self) -> None:
        new_window = tk.Toplevel()
        
        window_width = 300
        window_height = 100
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        new_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
        
        new_window.resizable(False, False)

        new_window.title("Are you sure?")
        
        window_fr = tk.Frame(new_window)
        window_fr.pack()
        
        label = tk.Label(window_fr, text="Do you realy want to delete selected tag?")
        label.pack(side="top", fill="both", pady=10)
        
        window_frame = GUIFrame(window_fr, "bottom", relief="flat")
        
        def tmp_f() -> None:
            self.delete_selected_tag()
            new_window.destroy()
        
        yes_button = GUIButton("Yes", function=tmp_f)
        no_button = GUIButton("No", function=new_window.destroy)
        
        window_frame.add(no_button)
        window_frame.add(yes_button)
        
        
        window_frame.pack()
 
        
    def create_transaction_tab(self) -> None:
        # Tab frame
        self.tag_tab = tk.Frame(self.notebook)
        self.tag_tab_frame = GUIFrame(self.tag_tab, fill="both", expand=True)
        
        # Transaction history frame
        self.tag_list_frame = GUIFrame(self.tag_tab_frame.frame, side="left", fill="both")
        
        self.tags_listbox = GUIListBox(30, "Tag list")
        self.tag_list_frame.add(self.tags_listbox)
        
        self.tag_tab_frame.add(self.tag_list_frame)
        
        
        
        # Information and buttons frmae
        self.tag_info_and_buttons_frame = GUIFrame(self.tag_tab_frame, side="right", fill="both", padx=30, pady=30)
        
        # Info frame
        self.tag_info_frame = GUIFrame(self.tag_info_and_buttons_frame, side="top", expand=True, fill="both", relief="flat")
        
        self.tag_info_name = GUILabelAndInput("Name", edible=False)
        self.tag_info_description = GUILabelAndInput("Description", edible=False, row_count=3)
        self.tag_info_id = GUILabelAndInput("ID", edible=False)
        
        self.tag_info_frame.add(self.tag_info_name)
        self.tag_info_frame.add(self.tag_info_description)
        self.tag_info_frame.add(self.tag_info_id)
        
        self.tag_info_and_buttons_frame.add(self.tag_info_frame)
        
        # Button frame
        self.tag_button_frame = GUIFrame(self.tag_info_and_buttons_frame, side="bottom", fill="none", padx=30, pady=30, relief="flat")
        
        self.add_tag_button = GUIButton("Add", function=self.f_add_tag_button, color="#9ED689")
        self.add_tag_button.width = 10
        self.add_tag_button.height = 2
        self.add_tag_button.padx = 2
        self.edit_tag_button = GUIButton("Edit", function=self.f_edit_tag_button)
        self.edit_tag_button.width = 10
        self.edit_tag_button.height = 2
        self.edit_tag_button.padx = 2
        self.remove_tag_button = GUIButton("Remove", function=self.f_remove_tag_button, color="#DD8D75")
        self.remove_tag_button.width = 10
        self.remove_tag_button.height = 2
        self.remove_tag_button.padx = 2
        
        self.tag_button_frame.add(self.add_tag_button)
        self.tag_button_frame.add(self.edit_tag_button)
        self.tag_button_frame.add(self.remove_tag_button)
        
        self.tag_info_and_buttons_frame.add(self.tag_button_frame)
        
        self.tag_tab_frame.add(self.tag_info_and_buttons_frame)
        
        
        
        self.tag_tab_frame.pack()
        
        self.notebook.add(self.tag_tab, text="Transactions")  
    
    def run(self) -> None:
        self.root.mainloop()
    

app = Application()
app.run()
