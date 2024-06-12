if __name__ == "__main__":
    import sys
    import os.path

    sys.path[0] = os.path.join(sys.path[0], "..", "..")

from modules.tracker_logic.classes import *
from modules.gui.window import GUI
import os

from modules.tracker_logic.classes import TrackerObject

DATA_PATH = "data"
JOURNALS_PATH = os.path.join(DATA_PATH, "journals")
SETTINGS_PATH = os.path.join(DATA_PATH, "settigns.json")

DEFAULT_JOURNAL_NAME = "journal_01"
DEFAULT_JOURNAL_PATH = os.path.join(
    JOURNALS_PATH, f"{DEFAULT_JOURNAL_NAME}.json")


class Settigns(TrackerObject):
    def __init__(self) -> None:
        super().__init__("", "", "")
        self.journal_path: os.path = ""

    def __dict__(self) -> dict:
        return {
            "journal_path": self.journal_path
        }

    def from_dict(self, dict_) -> None:
        self.journal_path = dict_["journal_path"]

    @staticmethod
    def create_from_dict(dictionary) -> TrackerObject:
        settigns = Settigns()
        settigns.journal_path = dictionary["journal_path"]
        return settigns

    @staticmethod
    def get_from_file(path: os.path) -> 'Settigns':
        settigns = Settigns()
        settigns.load(path)

        return settigns

    @staticmethod
    def generate_default_settings() -> 'Settigns':
        settings = Settigns()
        settings.journal_path = DEFAULT_JOURNAL_PATH

        return settings


class Application:
    def __init__(self) -> None:
        self.settigns: Settigns = None

        self.journal: Journal = None
        self.filtered_transaction_list = []

        self.gui: GUI = None

        

    def init_app(self) -> None:

        # Check if journals folder exists (it will automatically create data folder if needed)
        if not os.path.exists(JOURNALS_PATH):
            os.mkdir(JOURNALS_PATH)
        
        self.load_settings(
            path=SETTINGS_PATH,
            create_if_not_exist=True
        )

        self.load_journal(
            path=self.settigns.journal_path,
            create_if_not_exist=True
        )

        self.gui = GUI()
        self.init_gui()

    def init_gui(self) -> None:
        self.load_transaction_list_to_display(self.filtered_transaction_list)

        self.load_tag_list_to_display(self.journal.tag_list)

        self.gui.fv_delete_selected_transaction = self.delete_selected_transaction
        self.gui.fv_edit_selected_transaction = self.edit_transaction
        self.gui.fv_create_transaction = self.create_transaction

        self.gui.fv_create_tag = self.create_tag
        self.gui.fv_edit_selected_tag = self.edit_tag
        self.gui.fv_delete_selected_tag = self.delete_selected_tag

        self.gui.fv_get_current_transaction = self.get_selected_transaction
        self.gui.fv_get_current_tag = self.get_selected_tag

        self.gui.transaction_listbox.listbox.bind("<<ListboxSelect>>", self.transaction_info_on_selection)
        self.gui.tags_listbox.listbox.bind("<<ListboxSelect>>", self.tag_info_on_selection)

        self.gui.tag_list_holder = self.journal.tag_list.tags

        self.update_filtered_sum_text()
        
    def journal_changes(func) -> None:
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.journal.save(self.settigns.journal_path)
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
        if os.path.exists(path):
            self.settigns = Settigns.get_from_file(path)
        elif(create_if_not_exist):
            Settigns.generate_default_settings().save(path)

    def load_journal(self, path: os.path, create_if_not_exist: bool = False) -> None:
        if os.path.exists(self.settigns.journal_path):
            self.journal = Journal.get_from_file(self.settigns.journal_path)
        elif (create_if_not_exist):
            self.journal = Journal(
                DEFAULT_JOURNAL_NAME, "This journal was created automatically", "#jr000", TagList([]), [])
            self.journal.save(self.settigns.journal_path)

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
        total_sum = sum(transaction.balance for transaction in self.filtered_transaction_list)
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

    
if __name__ == "__main__":
    app = Application()
    app.init_app()
    app.run()