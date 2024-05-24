from modules.tracker_logic.classes import *
import os


class Settigns(TrackerObject):
    def __init__(self) -> None:
        self.journal_path: os.path = ""

    def __dict__(self) -> dict:
        return {
            "journal_path": self.journal_path
        }


class Application:
    def __init__(self) -> None:
        self.settigns: Settigns = Settigns()

        self.journal: Journal = None

        self.filtered_transaction_list = []

    def load_journal(self, path: os.path) -> None:
        self.journal
