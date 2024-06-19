import os
import sys

from modules.tracker_logic.classes import *
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

from modules.tracker_logic.languages import load_full_language_pack, extract_text_set_from_language_pack, LANGUAGE_NAMES, LANGUAGE_IDS
from modules.tracker_logic.fonts import FONTS
from modules.tracker_logic.classes import Journal



def empty_function() -> None:
    raise NotImplementedError()

class GUITopMenu:
    def __init__(self, root, settings: Settings, fv_close_app) -> None:
        self.root = root
        self.settings = settings

        self.fv_close_app  = fv_close_app

        self.lang_pack = load_full_language_pack()
        self.Text = extract_text_set_from_language_pack(self.settings.language_index, self.lang_pack)

        # > [Menu bar]
        self.menu_bar = tk.Menu(self.root, tearoff=0)

        # ----- |> [File menu]
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        # ----- | ----- (New Journal)
        self.file_menu.add_command(label=self.Text["New Journal"], command=self.create_journal)
        # ----- | ----- (Open Journal)
        self.file_menu.add_command(label=self.Text["Open Journal"], command=self.open_journal_with_filewindow)
        # ----- | ----- |> [Recent Journals]
        self.recent_journals_menu = tk.Menu(self.file_menu, tearoff=0)
        # ----- | ----- | ----- | (path/to/recent/journal1.json)
        # ----- | ----- | ----- | (path/to/recent/journal2.json)
        # ----- | ----- | ----- | (path/to/recent/journal3.json)
        rec_j_iter = 0
        while rec_j_iter < len(self.settings.recent_journal_paths):
            if self.can_open_journal(self.settings.recent_journal_paths[rec_j_iter]):

                command_params = {
                    'label': os.path.basename(self.settings.recent_journal_paths[rec_j_iter]),
                    'command': lambda path=self.settings.recent_journal_paths[rec_j_iter]: self.open_journal(path=path),
                }

                if self.settings.recent_journal_paths[rec_j_iter] == self.settings.journal_path:
                    command_params['background'] = 'orange'
                
                self.recent_journals_menu.add_command(**command_params)
                rec_j_iter += 1
            else:
                self.settings.recent_journal_paths.remove(self.settings.recent_journal_paths[rec_j_iter])
                self.settings.save(Settings.DEFAULT_SETTINGS_PATH)
        del rec_j_iter
        
        self.file_menu.add_cascade(label=self.Text["Recent Journals"], menu=self.recent_journals_menu)
        # ----- | ----- (_____________)
        self.file_menu.add_separator()
        # ----- | ----- (Exit)
        self.file_menu.add_command(label=self.Text["Exit"], command=self.fv_close_app)
        self.menu_bar.add_cascade(label=self.Text["File"], menu=self.file_menu)
        # -----|> [Settings]
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        # ----- | ----- |> [Language]
        self.select_language_menu = tk.Menu(self.settings_menu, tearoff=0)
        # ----- | ----- | ----- (English)
        # ----- | ----- | ----- (Ukrainian)
        for i in range(len(LANGUAGE_NAMES)):
            command_params = {
                'label': self.lang_pack[LANGUAGE_NAMES[i]][LANGUAGE_IDS[self.settings.language_index]],
                'command': lambda index=i: self.set_language_index(index),
            }

            if i == self.settings.language_index:
                command_params['background'] = 'orange'

            self.select_language_menu.add_command(**command_params)
            
        self.settings_menu.add_cascade(label=self.Text["Language"], menu=self.select_language_menu)
        # ----- | ----- |> [Font]
        self.select_font_menu = tk.Menu(self.settings_menu, tearoff=0)
        # ----- | ----- | ----- (Font1)
        # ----- | ----- | ----- (Font2)
        # ----- | ----- | ----- (Font3)
        for i in range(len(FONTS)):
            command_params = {
                'label': FONTS[i] + " | " + self.Text["Text Example"],
                'command': lambda index=i: self.set_font_index(index),
                'font': (FONTS[i], self.settings.font_size)
            }
            if i == self.settings.font_index:
                command_params['background'] = 'orange'
                
            self.select_font_menu.add_command(**command_params)

        self.settings_menu.add_cascade(label=self.Text["Font"], menu=self.select_font_menu)
        # ----- | ----- |> [Font Size]
        self.font_size_menu = tk.Menu(self.settings_menu, tearoff=0)
        # ----- | ----- | ----- (6 | "Text Example")
        # ----- | ----- | ----- ...
        # ----- | ----- | ----- (20 | "Text Example")
        for i in range(6, 20):
            command_params = {
                'label': str(i) + self.Text["Text Example"] + (" [Default]" if i == Settings.DEFAULT_FONT_SIZE else ""),
                'command': lambda index=i: self.set_font_size(index),
                'font': (FONTS[self.settings.font_index], i)
            }

            if i == self.settings.font_size:
                command_params['background'] = 'orange'

            self.font_size_menu.add_command(**command_params)
        self.settings_menu.add_cascade(label=self.Text["Font Size"], menu=self.font_size_menu)
        self.menu_bar.add_cascade(label=self.Text["Settings"], menu=self.settings_menu)

        root.config(menu=self.menu_bar)

    def set_language_index(self, index: int) -> None:
        self.settings.set_language_index(index)

        want_to_restart = messagebox.askyesno(
            self.Text["Restart application?"],
            self.Text["In order for the language change to take effect, you need to reload the application. Do you want to reload application now?"],
            parent=self.root)
        
        if want_to_restart:
            self.__restart_app()

    def set_font_index(self, index: int) -> None:
        self.settings.set_font_index(index)

        want_to_restart = messagebox.askyesno(
            self.Text["Restart application?"],
            self.Text["In order for the font change to take effect, you need to reload the application. Do you want to reload application now?"],
            parent=self.root)
        
        if want_to_restart:
            self.__restart_app()

    def set_font_size(self, size: int) -> None:
        self.settings.set_font_size(size)

        want_to_restart = messagebox.askyesno(
            self.Text["Restart application?"],
            self.Text["In order for the font size change to take effect, you need to reload the application. Do you want to reload application now?"],
            parent=self.root)
        
        if want_to_restart:
            self.__restart_app()

    def __restart_app(self) -> None:
        os.execv(sys.executable, ['python'] + sys.argv)

    def create_journal(self) -> None:
        file_path = filedialog.asksaveasfilename(
            initialdir=os.path.join(sys.path[0], Settings.DEFAULT_JOURNALS_PATH),
            defaultextension=".json", 
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Create Journal"
        )
        
        if file_path:
            file_name, _ = os.path.splitext(os.path.basename(file_path))

            new_journal = Journal(
                name=file_name,
                description="Journal created on " + datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                id=Journal.generate_journal_id(),
                tag_list=TagList([]),
                transaction_list=[]
            )

            self.settings.journal_path = file_path
            self.settings.save(Settings.DEFAULT_SETTINGS_PATH)

            new_journal.save(file_path)

            self.__restart_app()

            # self.fv_load_journal(file_path, create_if_not_exist=False)

    def open_journal_with_filewindow(self) -> None:
        print(os.path.join(sys.path[0], Settings.DEFAULT_JOURNALS_PATH))
        file_path = filedialog.askopenfilename(
            initialdir=os.path.join(sys.path[0], Settings.DEFAULT_JOURNALS_PATH),
            defaultextension=".json", 
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Open Journal"
        )
        
        if file_path:
            if not os.path.exists(file_path):
                messagebox.showerror(self.Text["Error"], self.Text["File not found!"], parent=self.root)
                return
            
            self.open_journal(file_path)

    def open_journal(self, path : os.path) -> None:
        if self.can_open_journal(path):
            self.settings.journal_path = path
            self.settings.save(Settings.DEFAULT_SETTINGS_PATH)

            self.__restart_app()
        else:
            messagebox.showerror(self.Text["Error"], self.Text["Something went wrong. Could not load journal."], parent=self.root)

    def can_open_journal(self, path : os.path) -> bool:
        if not os.path.exists(path):
            return False
        
        try:
            test_journal = Journal.get_from_file(path)
        except:
            return False

        return True
