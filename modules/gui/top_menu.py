from modules.tracker_logic.classes import *
import os
import sys
import tkinter as tk
from tkinter import messagebox

from modules.tracker_logic.languages import load_full_language_pack, extract_text_set_from_language_pack, LANGUAGE_NAMES, LANGUAGE_IDS
from modules.tracker_logic.fonts import FONTS

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
        self.file_menu.add_command(label=self.Text["New Journal"], command=empty_function)
        # ----- | ----- (Open Journal)
        self.file_menu.add_command(label=self.Text["Open Journal"], command=empty_function)
        # ----- | ----- |> [Recent Journals]
        self.recent_journals_menu = tk.Menu(self.file_menu, tearoff=0)
        # ----- | ----- | ----- | (path/to/recent/journal1.json)
        # ----- | ----- | ----- | (path/to/recent/journal2.json)
        # ----- | ----- | ----- | (path/to/recent/journal3.json)
        for i in range(len(self.settings.recent_journal_paths)):
            command_params = {
                'label': os.path.basename(self.settings.recent_journal_paths[i]),
                'command': empty_function,
            }

            if self.settings.recent_journal_paths[i] == self.settings.journal_path:
                command_params['background'] = 'orange'

            self.recent_journals_menu.add_command(**command_params)
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

