from modules.tracker_logic.classes import *
import os
import tkinter as tk

def empty_function() -> None:
    raise NotImplementedError()

class GUITopMenu:
    def __init__(self, root, settigns: Settigns) -> None:
        self.root = root
        self.settigns = settigns

        # > [Menu bar]
        self.menu_bar = tk.Menu(self.root, tearoff=0)

        # ----- |> [File menu]
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        # ----- | ----- (New Journal)
        self.file_menu.add_command(label="New Journal", command=empty_function)
        # ----- | ----- (Open Journal)
        self.file_menu.add_command(label="Open Journal", command=empty_function)
        # ----- | ----- |> [Recent Journals]
        self.recent_journals_menu = tk.Menu(self.file_menu, tearoff=0)
        # ----- | ----- | ----- | (path/to/recent/journal1.json)
        # ----- | ----- | ----- | (path/to/recent/journal2.json)
        # ----- | ----- | ----- | (path/to/recent/journal3.json)
        for i in range(len(self.settigns.recent_journal_paths)):
            self.recent_journals_menu.add_command(label=os.path.basename(self.settigns.recent_journal_paths[i]), command=empty_function)
        self.file_menu.add_cascade(label="Recent Journals", menu=self.recent_journals_menu)
        # ----- | ----- (_____________)
        self.file_menu.add_separator()
        # ----- | ----- (Exit)
        self.file_menu.add_command(label="Exit", command=empty_function)

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # -----|> Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)

        root.config(menu=self.menu_bar)


