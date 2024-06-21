from modules.tracker_logic.general_functions import write_to_file, read_from_file

from modules.tracker_logic.classes import Settings

import os

LANGUAGE_JSON_PATH = os.path.join(Settings.DEFAULT_DATA_PATH, "language.json") 

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

    {EN_ID: "Error",
     UA_ID: "Помилка"},

    {EN_ID: "File not found!",
     UA_ID: "Файл не знайдено!"},

    {EN_ID: "Something went wrong. Could not load journal.",
     UA_ID: "Щось пішло не так. Не вдалося завантажити журнал."},

    {EN_ID: "Invalid date!",
     UA_ID: "Некоректна дата!"},

    {EN_ID: "Invalid date from!",
     UA_ID: "Некоректна дата від!"},

    {EN_ID: "Invalid date to!",
     UA_ID: "Некоректна дата до!"},

    {EN_ID: "Please enter name!",
     UA_ID: "Будь ласка, введіть назву!"},

    {EN_ID: "Please select transaction first!",
     UA_ID: "Будь ласка, виберіть транзакцію!"},

    {EN_ID: "Please select tag first!",
     UA_ID: "Будь ласка, виберіть тег!"},

    {EN_ID: "Are you sure?",
     UA_ID: "Ви впевнені?"},

    {EN_ID: "Do you realy want to delete selected transaction?",
     UA_ID: "Ви дійсно хочете видалити вибрану транзакцію?"},

    {EN_ID: "Do you realy want to delete selected tag?",
     UA_ID: "Ви дійсно хочете видалити вибраний тег?"},

    # _____________Window content_____________
    {EN_ID: "Transactions",
     UA_ID: "Транзакції"},

    {EN_ID: "Create tag",
     UA_ID: "Створити тег"},

    {EN_ID: "Edit tag",
     UA_ID: "Редагувати тег"},

    {EN_ID: "Tag list",
     UA_ID: "Список тегів"},

    {EN_ID: "Tags tab",
     UA_ID: "Вкладка тегів"},

    {EN_ID: "Create transaction",
     UA_ID: "Створити транзакцію"},

    {EN_ID: "Edit transaction",
     UA_ID: "Редагувати транзакцію"},

    {EN_ID: "Filter transactions",
     UA_ID: "Фільтрувати транзакції"},

    {EN_ID: "Select tag to look for (optional)",
     UA_ID: "Виберіть тег для пошуку (опціонально)"},

    {EN_ID: "Date from <YYYY-MM-DD> (optional)",
     UA_ID: "Дата від <YYYY-MM-DD> (опціонально)"},

    {EN_ID: "Date to <YYYY-MM-DD> (optional)",
     UA_ID: "Дата до <YYYY-MM-DD> (опціонально)"},

    {EN_ID: "Transaction History",
     UA_ID: "Історія транзакцій"},

    {EN_ID: "Sum",
     UA_ID: "Сума"},

    {EN_ID: "Name",
     UA_ID: "Назва"},

    {EN_ID: "Description",
     UA_ID: "Опис"},

    {EN_ID: "Balance",
     UA_ID: "Баланс"},

    {EN_ID: "Date(YYYY-MM-DD)",
     UA_ID: "Дата(YYYY-MM-DD)"},

    {EN_ID: "Transaction tags",
     UA_ID: "Теги транзакції"},

    {EN_ID: "Tags",
     UA_ID: "Теги"},

    {EN_ID: "ID",
     UA_ID: "ID"},

    {EN_ID: "Available tags",
     UA_ID: "Доступні теги"},

    {EN_ID: "Create",
     UA_ID: "Створити"},

    {EN_ID: "Save",
     UA_ID: "Зберегти"},

    {EN_ID: "Add",
     UA_ID: "Додати"},

    {EN_ID: "Edit",
     UA_ID: "Редагувати"},

    {EN_ID: "Filter",
     UA_ID: "Фільтрувати"},

    {EN_ID: "Clear filter",
     UA_ID: "Очистити фільтр"},

    {EN_ID: "Remove",
     UA_ID: "Видалити"},

    {EN_ID: "Cancel",
     UA_ID: "Скасувати"},

    {EN_ID: "Sort by date",
     UA_ID: "Сортувати за датою"},

    {EN_ID: "Sort by balance",
     UA_ID: "Сортувати за балансом"},
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
        