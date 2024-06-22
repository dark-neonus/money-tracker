from typing import List, Dict
import os
import abc
from datetime import date, datetime
import random

from modules.tracker_logic.general_functions import write_to_file, read_from_file

MONEY_LEVELS = [50, 100, 200, 300, 400, 500, 750, 1000, 1500, 2500, 5000, 10000, 15000, 25000]


class TrackerObject(metaclass=abc.ABCMeta):
    def __init__(
            self,
            name: str,
            description: str,
            id: str | None
    ) -> None:

        if not isinstance(name, str):
            raise TypeError(
                f"Name of TrackerObject must be a str, not a {type(name)}!")
        self.name: str = name

        if not isinstance(description, str):
            raise TypeError(
                f"Description of TrackerObject must be a str, not a {type(description)}!")
        self.description: str = description

        if not isinstance(id, str) and id != None:
            raise TypeError(
                f"ID of TrackerObject must be a str, not a {type(id)}!")
        self.id: str = id

    @abc.abstractmethod
    def __dict__(self) -> dict:
        pass

    @abc.abstractmethod
    def from_dict(self, dict_) -> None:
        pass

    @staticmethod
    @abc.abstractmethod
    def create_from_dict(dict_) -> 'TrackerObject':
        pass

    def save(self, path: os.path) -> None:
        write_to_file(path, self.__dict__())

    def load(self, path: os.path) -> None:
        self.from_dict(read_from_file(path))

    @staticmethod
    @abc.abstractmethod
    def get_from_file(path: os.path) -> 'TrackerObject':
        pass

 
class Tag(TrackerObject):
    def __init__(
            self,
            name: str,
            description: str,
            id: str | None = None
    ) -> None:

        TrackerObject.__init__(self, name, description, id)

    def __dict__(self):
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id
        }

    def from_dict(self, dict_) -> None:
        self.name = dict_["name"]
        self.description = dict_["description"]
        self.id = dict_["id"]

    @staticmethod
    def create_from_dict(dict_) -> 'Tag':
        return Tag(
            dict_["name"],
            dict_["description"],
            dict_["id"]
        )

    @staticmethod
    def get_from_file(path: os.path) -> 'Tag':
        new_tag = Tag("", "", "")
        new_tag.load(path)
        return new_tag
    
    def __str__(self) -> str:
        return self.name


class TagList():
    def __init__(
            self,
            tags: List[Tag],
            __id_counter : int = 0
    ) -> None:
        
        self.__id_counter = __id_counter

        self.tags: Dict[str, Tag] = {}
        for tag in tags:
            self.add_tag(tag)


    def add_tag(self, tag: Tag, change_id_counter : bool = True) -> None:
        if not isinstance(tag, Tag):
            raise TypeError(f"Tag must be Tag, not {type(tag)}!")
        new_id = self.generate_tag_id(change_id_counter)
        self.tags[new_id] = Tag(tag.name, tag.description, new_id)

    def __add_exact_tag(self, tag: Tag) -> None:
        """Add tag and dont manage its id, but use existing one instead. Dont use if it isn't necessary!!!"""
        if not isinstance(tag, Tag):
            raise TypeError(f"Tag must be Tag, not {type(tag)}!")
        self.tags[tag.id] = Tag(tag.name, tag.description, tag.id)

    def remove_tag(self, tag_id: str) -> None:
        if not isinstance(tag_id, str):
            raise TypeError(f"Tags id must be a str, not {type(tag_id)}!")
        self.tags.pop(tag_id)

    def __getitem__(self, tag_id: str) -> Tag:
        if not isinstance(tag_id, str):
            raise TypeError(f"ID must be a str, not {type(tag_id)}!")
        return self.tags[tag_id]

    def __dict__(self) -> dict:
        tmp: dict = {}
        for tag in self.tags.values():
            tmp[tag.id] = tag.__dict__()
        tmp["__id_counter"] = self.__id_counter
        return tmp
    
    def get_tag_by_name(self, name : str) -> Tag | None:
        for tag in self.tags.values():
            if tag.name == name:
                return tag
        return None

    def from_dict(self, dict_) -> None:
        for tag_dict in dict_.values():
            if isinstance(tag_dict, dict):
                self.__add_exact_tag(Tag.create_from_dict(tag_dict))
        self.__id_counter = dict_["__id_counter"]

    @staticmethod
    def from_dict(dict_: dict) -> 'TagList':
        tmp = TagList([])
        for tag_dict in dict_.values():
            if isinstance(tag_dict, dict):
                tmp.__add_exact_tag(Tag.create_from_dict(tag_dict))
        tmp.__id_counter = dict_["__id_counter"]
        return tmp

    def generate_tag_id(self, change_id_counter : bool = True) -> str:
        index = str(self.__id_counter).zfill(4)
        new_id = f"#tg{index}"
        
        if change_id_counter:
            self.__id_counter += 1
            
        return new_id

class Transaction(TrackerObject):
    def __init__(
            self,
            name: str,
            description: str,
            balance: float,
            tags_id: List[str],
            id: str | None = None,
            date_: date | None = None
    ) -> None:

        TrackerObject.__init__(self, name, description, id)

        if not isinstance(balance, float):
            raise TypeError(
                f"Balance of transaction must be a float, not a {type(name)}!")
        self.balance: float = balance

        self.tags_id: List[str] = tags_id

        if date_ == None:
            self.date = date.today()
        else:
            self.date = date_

    def __dict__(self):
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "balance": self.balance,
            "tags_id": self.tags_id,
            "date": self.date.isoformat()
        }

    def from_dict(self, dict_) -> None:
        self.name = dict_["name"]
        self.description = dict_["description"]
        self.id = dict_["id"]
        self.balance = dict_["balance"]
        self.tags_id = dict_["tags_id"]
        self.date = date.fromisoformat(dict_["date"])

    @staticmethod
    def create_from_dict(dict_) -> 'Transaction':
        return Transaction(
            name=dict_["name"],
            description=dict_["description"],
            balance=dict_["balance"],
            tags_id=dict_["tags_id"],
            id=dict_["id"],
            date_=date.fromisoformat(dict_["date"])
        )

    @staticmethod
    def get_from_file(path: os.path) -> 'Transaction':
        new_transaction = Transaction("", "", "", 0, [])
        new_transaction.load(path)
        return new_transaction

    def __str__(self) -> str:
        # empty_char = "\u2591"
        empty_char = " "
        prefix = empty_char

        if self.balance > 0:
            prefix += empty_char * len(MONEY_LEVELS) + "\u2588"
            for level in MONEY_LEVELS:
                if self.balance >= level:
                    prefix += "\u2588"
                else:
                    prefix += empty_char
        else:
            for level in MONEY_LEVELS[::-1]:
                if self.balance <= -level:
                    prefix += "\u2588"
                else:
                    prefix += empty_char
            prefix += "\u2588" + empty_char * len(MONEY_LEVELS)

        balance_text = str(self.balance)

        balance_text = " " * max(0, 7 - len(balance_text)) + balance_text

        return f" {self.date.isoformat()} {prefix} < {balance_text} > {self.name}"

class Journal(TrackerObject):
    def __init__(
            self,
            name: str,
            description: str,
            id: str,
            tag_list: TagList,
            transaction_list: List[Transaction],
            id_counter: int = 0,
            backup_path = None
    ) -> None:

        TrackerObject.__init__(self, name, description, id)

        self.tag_list: TagList = tag_list

        self.__id_counter: int = id_counter

        self.transaction_list: List[Transaction] = []
        for i in range(len(transaction_list)):
            self.add_transaction(transaction_list[i])

        self.backup_path = backup_path

    def get_balance(self) -> float:
        bal: float = 0.0
        for transaction in self.transaction_list:
            bal += transaction.balance
        return bal
    
    def add_tag(self, tag: Tag) -> None:
        self.tag_list.add_tag(tag)

    def add_transaction(self, transaction: Transaction, change_id_counter : bool = True) -> None:
        if not isinstance(transaction, Transaction):
            raise TypeError(
                f"Transaction must be a Transaction, not {type(transaction)}!")
        self.transaction_list.append(
            Transaction(
                name=transaction.name,
                description=transaction.description,
                balance=transaction.balance,
                tags_id=transaction.tags_id,
                id=self.generate_transaction_id(change_id_counter),
                date_=transaction.date
            )
        )

    def remove_transaction(self, index: int) -> None:
        if not isinstance(index, int):
            raise TypeError(
                f"Index of transaction must be an int, not {type(id)}!")
        if index < 0:
            raise IndexError(
                f"Index of transaction cant be negative! Current index value: {index}")
        if index >= len(self.transaction_list):
            raise IndexError(
                f"Index of transaction cant be greater than amount of transactions! Current index value: {index}, transactions amount: {len(self.transaction_list)}")
        self.transaction_list.pop(index)

    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "tag_list": self.tag_list.__dict__(),
            "transaction_list": [transaction.__dict__() for transaction in self.transaction_list],
            "__id_counter": self.__id_counter,
            "backup_path": self.backup_path
        }

    def from_dict(self, dict_) -> None:
        self.name = dict_["name"]
        self.description = dict_["description"]
        self.id = dict_["id"]
        self.tag_list = TagList.from_dict(dict_["tag_list"])
        self.transaction_list = [Transaction.create_from_dict(tr_dict)
                                 for tr_dict in dict_["transaction_list"]]
        self.__id_counter = dict_["__id_counter"]
        self.backup_path = dict_["backup_path"]

    @staticmethod
    def create_from_dict(dict_: dict) -> 'Journal':
        journal = Journal(
            dict_["name"],
            dict_["description"],
            dict_["id"],
            TagList.from_dict(dict_["tag_list"]),
            [],
            dict_["__id_counter"],
            dict_["backup_path"]
        )
        for tr_dict in dict_["transaction_list"]:
            journal.add_transaction(Transaction.create_from_dict(tr_dict), False) 

        return journal

    @staticmethod
    def get_from_file(path: os.path) -> 'Journal':
        tag_list = TagList([])
        new_journal = Journal("", "", "", tag_list, [])
        new_journal.load(path)
        return new_journal
    
    def get_transactions_by_id(self, id: str) -> Transaction | None:
        for transaction in self.transaction_list:
            if transaction.id == id:
                return transaction
        return None

    def generate_transaction_id(self, change_id_counter: bool = True) -> str:
        index = str(self.__id_counter).zfill(10)
        new_id = f"#tr{index}"
        
        if change_id_counter:
            self.__id_counter += 1
            
        return new_id

    @staticmethod
    def generate_journal_id() -> str:
        index = str(random.randint(0, 10**8)).zfill(10)
        new_id = f"#jr{index}"
        return new_id
    

    def create_backup(self, backup_dir : os.path, file_name : str) -> None:
        backup_journal_name = file_name + datetime.now().strftime("[%Y-%m-%d_%H-%M]")
        if self.backup_path != None and os.path.exists(self.backup_path):
            os.remove(self.backup_path)

        self.backup_path = os.path.join(backup_dir, backup_journal_name + ".json" + Settings.BACKUP_EXTENSION)
        write_to_file(
            self.backup_path,
            self.__dict__()
            )
        

class Settings(TrackerObject):
    DEFAULT_DATA_PATH = "data"

    DEFAULT_JOURNALS_PATH = os.path.join(DEFAULT_DATA_PATH, "journals")
    DEFAULT_BACKUPS_PATH = os.path.join(DEFAULT_DATA_PATH, "backups")
    DEFAULT_SETTINGS_PATH = os.path.join(DEFAULT_DATA_PATH, "settings.json")

    DEFAULT_JOURNAL_NAME = "default_journal"
    DEFAULT_JOURNAL_PATH = os.path.join(DEFAULT_JOURNALS_PATH, f"{DEFAULT_JOURNAL_NAME}.json")

    # ".backup"
    BACKUP_EXTENSION = ".backup"
    DEL_EXTENSION = ".del"

    DEFAULT_LANGUAGE_INDEX = 0
    DEFAULT_FONT_INDEX = 0
    DEFAULT_FONT_SIZE = 11

    def __init__(self) -> None:
        super().__init__("settings", "", "")
        self.journal_path: os.path = ""
        self.language_index = 0
        self.font_index = 0
        self.font_size = 0
        self.recent_journal_paths: List[str] = []

    def settings_changes(func) -> None:

        def wrapper(self, *args, **kwargs) -> None:
            func(self, *args, **kwargs)
            self.save(self.DEFAULT_SETTINGS_PATH)
        return wrapper

    @settings_changes
    def add_recent_journal_path(self, path : os.path) -> None:
        if path not in self.recent_journal_paths:
            self.recent_journal_paths.append(path)

    @settings_changes
    def set_language_index(self, index: int) -> None:
        self.language_index = index

    @settings_changes
    def set_font_index(self, index: int) -> None:
        self.font_index = index

    @settings_changes
    def set_font_size(self, size: int) -> None:
        self.font_size = size

    def __dict__(self) -> dict:
        return {
            "journal_path": self.journal_path,
            "language_index": self.language_index,
            "font_index": self.font_index,
            "font_size": self.font_size,
            "recent_journal_paths": self.recent_journal_paths
        }

    def from_dict(self, dict_) -> None:
        self.journal_path = dict_["journal_path"]
        self.language_index = dict_["language_index"]
        self.font_index = dict_["font_index"]
        self.font_size = dict_["font_size"]
        self.recent_journal_paths = dict_["recent_journal_paths"]

    @staticmethod
    def create_from_dict(dict_) -> TrackerObject:
        settings = Settings()
        settings.journal_path = dict_["journal_path"]
        settings.language_index = dict_["language_index"]
        settings.font_index = dict_["font_index"]
        settings.font_size = dict_["font_size"]
        settings.recent_journal_paths = dict_["recent_journal_paths"]
        return settings

    @staticmethod
    def get_from_file(path: os.path) -> 'Settings':
        settings = Settings()
        settings.load(path)

        return settings

    @staticmethod
    def generate_default_settings() -> 'Settings':
        settings = Settings()
        settings.journal_path = Settings.DEFAULT_JOURNAL_PATH
        settings.language_index = Settings.DEFAULT_LANGUAGE_INDEX
        settings.font_index = Settings.DEFAULT_FONT_INDEX
        settings.font_size = Settings.DEFAULT_FONT_SIZE
        settings.recent_journal_paths = []

        return settings


