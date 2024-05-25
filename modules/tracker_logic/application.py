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
        for transaction in self.filtered_transaction_list:
            self.gui.add_transaction_to_display(transaction)

        self.gui.fv_delete_selected_transaction = self.delete_selected_transaction
        
    def delete_selected_transaction(self) -> None:
        selected_index = self.gui.transaction_listbox.listbox.curselection()
        if selected_index:
            self.journal.transaction_list.pop(
                self.index_filtered_to_normal(selected_index[0])
            )
            self.filtered_transaction_list.pop(selected_index[0])
            self.gui.transaction_listbox.remove_item(selected_index[0])


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
    
    def run(self) -> None:
        self.gui.run()

if __name__ == "__main__":
    app = Application()
    app.init_app()
    app.run()
