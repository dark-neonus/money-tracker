from tracker_logic import *
import os

class Settigns:
    def __init__(self) -> None:
        self.journal_path : os.path = ""


class Application:
    def __init__(self) -> None:
        self.settigns : Settigns = Settigns()

        self.journal : Journal = None

    def load_journal(self, path : os.path) -> None:
        self.journal


