from modules.tracker_logic.general_functions import write_to_file, read_from_file

from modules.tracker_logic.classes import Settings

import os

LANGUAGE_JSON_PATH = os.path.join(Settings.DATA_PATH, "language.json") 

EN_INDEX = 0
UA_INDEX = 1

EN_ID = "EN"
UA_ID = "UA"

LANGUAGE_NAMES = ["English", "Ukrainian"]

LANGUAGE_IDS = [EN_ID, UA_ID]

__TEXT_SET = [
    #______________Top Menu_____________
    {EN_ID: "File",
     UA_ID: "Файл"},

    {EN_ID: "New Journal",
     UA_ID: "Новий Журнал"},

    {EN_ID: "Open Journal",
     UA_ID: "Відкрити Журнал"},

    {EN_ID: "Recent Journals",
     UA_ID: "Нещодавні Журнали"},

    {EN_ID: "Exit",
     UA_ID: "Вийти"},

    {EN_ID: "Settings",
     UA_ID: "Налаштування"},

    {EN_ID: "Language",
     UA_ID: "Мова"},

    {EN_ID: "English",
     UA_ID: "Англійська"},

    {EN_ID: "Ukrainian",
     UA_ID: "Українська"},

    {EN_ID: "Font",
     UA_ID: "Шрифт"},

    {EN_ID: "Font Size",
     UA_ID: "Розмір шрифту"},

    {EN_ID: "Text Example",
     UA_ID: "Приклад тексту"},
    #______________Messages_____________
    {EN_ID: "Restart application?",
     UA_ID: "Перезавантажити додаток?"},

    {EN_ID: "In order for the language change to take effect, you need to reload the application. Do you want to reload application now?",
     UA_ID: "Щоб змінити мову, потрібно перезавантажити додаток. Ви хочете перезавантажити додаток зараз?"},

    {EN_ID: "In order for the font change to take effect, you need to reload the application. Do you want to reload application now?",
     UA_ID: "Щоб змінити шрифт, потрібно перезавантажити додаток. Ви хочете перезавантажити додаток зараз?"},

    {EN_ID: "In order for the font size change to take effect, you need to reload the application. Do you want to reload application now?",
     UA_ID: "Щоб змінити розмір шрифту, потрібно перезавантажити додаток. Ви хочете перезавантажити додаток зараз?"},
]
def __get_test_set_for_saving(text_set : list[dict[str, str]]) -> dict[str, dict[str, str]]:
    processed_text_set = {}
    for i in range(len(text_set)):
        processed_text_set[text_set[i][EN_ID]] = text_set[i]
    return processed_text_set

def save_text_set() -> None:
    write_to_file(LANGUAGE_JSON_PATH, __get_test_set_for_saving(__TEXT_SET))

def load_full_language_pack() -> list[dict[str, dict[str, str]]]:
    if not os.path.exists(LANGUAGE_JSON_PATH):
        save_text_set()
    
    return read_from_file(LANGUAGE_JSON_PATH)

def extract_text_set_from_language_pack(language_index, language_pack) -> dict[str, str]:
    text_set = {}
    for text, dictionary in language_pack.items():
        text_set[text] = dictionary[LANGUAGE_IDS[language_index]] 
    return text_set
        