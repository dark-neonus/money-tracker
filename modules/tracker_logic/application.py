import sys
import os

if __name__ == "__main__":
    sys.path[0] = os.path.join(sys.path[0], "..", "..")

from modules.tracker_logic.classes import *
from modules.gui.window import GUI


from tkinter import messagebox

from modules.gui.top_menu import GUITopMenu

from modules.tracker_logic.languages import save_text_set, load_full_language_pack, extract_text_set_from_language_pack



    

class Application:
    def __init__(self) -> None:
        self.settings: Settings = None

        self.journal: Journal = None
        self.filtered_transaction_list = []

        self.gui: GUI = None
        self.top_menu = None

        self.__sort_date_from = None
        self.__sort_date_to = None
        self.__sort_tag_to_look = None

    def init_app(self) -> None:

        # Check if journals folder exists (it will automatically create data folder if needed)
        if not os.path.exists(Settings.JOURNALS_PATH):
            os.mkdir(Settings.JOURNALS_PATH)
        
        self.load_settings(
            path=Settings.SETTINGS_PATH,
            create_if_not_exist=True
        )

        save_text_set()

        self.lang_pack = load_full_language_pack()
        self.Text = extract_text_set_from_language_pack(self.settings.language_index, self.lang_pack)

        self.load_journal(
            path=self.settings.journal_path,
            create_if_not_exist=True
        )

        self.gui = GUI(self.settings.font_index, self.settings.font_size)
        self.init_gui()

    def init_gui(self) -> None:
        self.load_transaction_list_to_display(self.filtered_transaction_list)

        self.load_tag_list_to_display(self.journal.tag_list)

        self.gui.fv_delete_selected_transaction = self.delete_selected_transaction
        self.gui.fv_edit_selected_transaction = self.edit_transaction
        self.gui.fv_create_transaction = self.create_transaction

        self.gui.fv_filter_transactions = self.filter_transactions
        self.gui.fv_clear_filter = self.clear_filter
        self.gui.fv_sort_transactions_by_date = self.sort_transactions_by_date
        self.gui.fv_sort_transactions_by_balance = self.sort_transactions_by_balance

        self.gui.fv_create_tag = self.create_tag
        self.gui.fv_edit_selected_tag = self.edit_tag
        self.gui.fv_delete_selected_tag = self.delete_selected_tag

        self.gui.fv_get_current_transaction = self.get_selected_transaction
        self.gui.fv_get_current_tag = self.get_selected_tag

        self.gui.transaction_listbox.listbox.bind("<<ListboxSelect>>", self.transaction_info_on_selection)
        self.gui.tags_listbox.listbox.bind("<<ListboxSelect>>", self.tag_info_on_selection)

        self.gui.tag_list_holder = self.journal.tag_list.tags

        self.update_filtered_sum_text()

        self.top_menu = GUITopMenu(self.gui.root, self.settings, self.close_app)
        
    def journal_changes(func) -> None:
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.journal.save(self.settings.journal_path)
            self.update_filtered_sum_text()
        return wrapper



    @journal_changes
    def delete_selected_transaction(self) -> None:
        selected_index = self.gui.transaction_listbox.listbox.curselection()
        if selected_index:
            self.journal.transaction_list.pop(
                self.index_filtered_to_normal(selected_index[0])
            )
            self.filtered_transaction_list.pop(selected_index[0])
            self.gui.transaction_listbox.remove_item(selected_index[0])

    @journal_changes    
    def create_transaction(self, name : str, description : str, balance : float, tags_id : List[str], date_: date) -> None:
        self.journal.add_transaction(Transaction(name, description, balance, list(tags_id), date_=date_))
        self.filtered_transaction_list.append(self.journal.transaction_list[-1])
        self.gui.add_transaction_to_display(self.journal.transaction_list[-1])

    @journal_changes
    def edit_transaction(self, transaction : Transaction, name : str, description : str, balance : float, tags_id : List[str], date_: date) -> None:
        if transaction == None:
            self.create_transaction(name, description, balance, tags_id, date_)
        else:
            transaction.name = name
            transaction.description = description
            transaction.balance = balance
            transaction.tags_id = list(tags_id)
            transaction.date = date_
            self.load_transaction_list_to_display(self.filtered_transaction_list)

    @journal_changes
    def delete_selected_tag(self) -> None:
        selected_index = self.gui.tags_listbox.listbox.curselection()
        if selected_index:
            tag_to_delete = self.journal.tag_list.get_tag_by_name(self.gui.tags_listbox.listbox.get(selected_index[0]))

            # Delete all references to tag in transactions
            for transaction in self.journal.transaction_list:
                if tag_to_delete.id in transaction.tags_id:
                    transaction.tags_id.remove(tag_to_delete.id)

            self.journal.tag_list.remove_tag(tag_to_delete.id)

            self.gui.tags_listbox.remove_item(selected_index[0])

    @journal_changes
    def create_tag(self, name: str, description: str) -> None:
        self.journal.add_tag(Tag(name, description))
        self.gui.add_tag_to_display(self.journal.tag_list.get_tag_by_name(name))

    @journal_changes
    def edit_tag(self, tag: Tag, name: str, description: str) -> None:
        if tag == None:
            self.create_tag(name, description)
        else:
            tag.name = name
            tag.description = description
            self.load_tag_list_to_display(self.journal.tag_list)

    def transaction_info_on_selection(self, event) -> None:
        selected_index = self.gui.transaction_listbox.listbox.curselection()
        if selected_index:
            selected_transaction = self.filtered_transaction_list[selected_index[0]]
            self.gui.info_name.update_text(selected_transaction.name)
            self.gui.info_description.update_text(selected_transaction.description)
            self.gui.info_balance.update_text(selected_transaction.balance)
            self.gui.info_date.update_text(selected_transaction.date.isoformat())
            self.gui.info_id.update_text(selected_transaction.id)

            self.gui.info_tags.clear()
            for tag_id in selected_transaction.tags_id:
                self.gui.info_tags.add_item(self.journal.tag_list.tags[tag_id].name)


    def tag_info_on_selection(self, event) -> None:
        selected_index = self.gui.tags_listbox.listbox.curselection()
        if selected_index:
            key_list = list(self.journal.tag_list.tags.keys())
            names_list = list(tag.name for tag in self.journal.tag_list.tags.values())

            selected_key = key_list[names_list.index(self.gui.tags_listbox.listbox.get(selected_index[0]))]
            
            selected_tag = self.journal.tag_list.tags[selected_key]
            self.gui.tag_info_name.update_text(selected_tag.name)
            self.gui.tag_info_description.update_text(selected_tag.description)
            self.gui.tag_info_id.update_text(selected_tag.id)

    def load_settings(self, path: os.path, create_if_not_exist: bool = False) -> None:
        if not os.path.exists(path) and create_if_not_exist:
            Settings.generate_default_settings().save(path)
        try:
            self.settings = Settings.get_from_file(path)
        except:
            restart_settings = messagebox.askyesno("Error", "Error during reading settings.json. Do you want to use default settings?")
            if restart_settings:
                self.settings = Settings.generate_default_settings()
            else:
                print("Error during reading settings.json. Exiting...")
                sys.exit(0)
            

    def load_journal(self, path: os.path, create_if_not_exist: bool = False) -> None:
        if os.path.exists(self.settings.journal_path):
            self.journal = Journal.get_from_file(self.settings.journal_path)
        elif (create_if_not_exist):
            self.journal = Journal(
                Settings.DEFAULT_JOURNAL_NAME, "This journal was created automatically", "#jr000", TagList([]), [])
            self.journal.save(self.settings.journal_path)

        self.settings.add_recent_journal_path(self.settings.journal_path)

        self.filtered_transaction_list = self.journal.transaction_list[:]

    def index_filtered_to_normal(self, index: int) -> None:
        # Dont do search when not filtered
        if len(self.filtered_transaction_list) == len(self.journal.transaction_list):
            return index
        
        trg = self.filtered_transaction_list[index].id
        for i in range(len(self.journal.transaction_list)):
            if self.journal.transaction_list[i].id == trg:
                return i
    
    def load_transaction_list_to_display(self, transaction_list: List[Transaction]) -> None:
        self.gui.transaction_listbox.clear()
        for transaction in transaction_list:
            self.gui.add_transaction_to_display(transaction)

        self.update_filtered_sum_text()

    def load_tag_list_to_display(self, tag_list: TagList) -> None:
        self.gui.tags_listbox.clear()
        for tag in tag_list.tags.values():
            self.gui.add_tag_to_display(tag.name)

    def get_selected_transaction(self) -> Transaction | None:
        selected_index = self.gui.transaction_listbox.listbox.curselection()
        if selected_index:
            return self.filtered_transaction_list[self.index_filtered_to_normal(selected_index[0])]
        else:
            return None

    def get_selected_tag(self) -> Tag | None:
        selected_index = self.gui.tags_listbox.listbox.curselection()
        if selected_index:
            return self.journal.tag_list.get_tag_by_name(self.gui.tags_listbox.listbox.get(selected_index[0]))
        else:
            return None


    def update_filtered_sum_text(self) -> None:
        total_sum = round(sum(transaction.balance for transaction in self.filtered_transaction_list), 5)
        self.gui.info_final_balance.update_text(total_sum)

        color = "grey"
        if total_sum > 0:
            color = "green"
        elif total_sum < 0:
            color = "red"

        self.gui.info_final_balance.entry.config(foreground=color)
        self.gui.info_final_balance.label.config(foreground=color)

    def run(self) -> None:
        self.gui.run()

    def filter_transactions(self, date_from : date, date_to : date, tag_to_look : str) -> None:
        self.filtered_transaction_list = []

        self.__sort_date_from = date_from
        self.__sort_date_to = date_to
        self.__sort_tag_to_look = tag_to_look

        for transaction in self.journal.transaction_list:
            if (self.__sort_date_from == None or transaction.date >= self.__sort_date_from) and \
                    (self.__sort_date_to == None or transaction.date <= self.__sort_date_to) and \
                    (self.__sort_tag_to_look == None or self.__sort_tag_to_look in transaction.tags_id):
                self.filtered_transaction_list.append(transaction)
        
        
        self.load_transaction_list_to_display(self.filtered_transaction_list)
    
    def clear_filter(self) -> None:
        self.filter_transactions(None, None, None)

    @journal_changes
    def sort_transactions_by_date(self) -> None:
        self.journal.transaction_list.sort(key=lambda x: x.date, reverse=True)
        self.filter_transactions(self.__sort_date_from, self.__sort_date_to, self.__sort_tag_to_look)
        self.load_transaction_list_to_display(self.filtered_transaction_list)

    @journal_changes
    def sort_transactions_by_balance(self) -> None:
        self.journal.transaction_list.sort(key=lambda x: x.balance, reverse=True)
        self.filter_transactions(self.__sort_date_from, self.__sort_date_to, self.__sort_tag_to_look)
        self.load_transaction_list_to_display(self.filtered_transaction_list)

    @journal_changes
    def sort_transaction_random(self) -> None:
        import random
        random.shuffle(self.journal.transaction_list)
        self.filter_transactions(self.__sort_date_from, self.__sort_date_to, self.__sort_tag_to_look)
        self.load_transaction_list_to_display(self.filtered_transaction_list)

    def close_app(self) -> None:
        self.gui.root.quit()

if __name__ == "__main__":
    app = Application()
    app.init_app()
    app.run()

