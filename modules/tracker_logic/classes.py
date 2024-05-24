from typing import List, Dict
import os
import abc

from modules.tracker_logic.general_functions import write_to_file, read_from_file


class TrackerObject(metaclass=abc.ABCMeta):
    def __init__(
            self,
            name: str,
            description: str,
            id: str
    ) -> None:

        if not isinstance(name, str):
            raise TypeError(
                f"Name of TrackerObject must be a str, not a {type(name)}!")
        self.name: str = name

        if not isinstance(description, str):
            raise TypeError(
                f"Description of TrackerObject must be a str, not a {type(description)}!")
        self.description: str = description

        if not isinstance(id, str):
            raise TypeError(
                f"ID of TrackerObject must be a str, not a {type(id)}!")
        self.id: str = id

    @abc.abstractmethod
    def __dict__(self) -> dict:
        pass

    @staticmethod
    @abc.abstractmethod
    def from_dict(dictionary) -> 'TrackerObject':
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
            id: str
    ) -> None:

        TrackerObject.__init__(self, name, description, id)

    def __dict__(self):
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id
        }

    @staticmethod
    def from_dict(dict_) -> 'Tag':
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




class TagList():
    def __init__(
            self,
            tags: List[Tag]
    ) -> None:

        self.tags: Dict[str, Tag] = {}
        for tag in tags:
            self.add_tag(tag)

    def add_tag(self, tag: Tag) -> None:
        if not isinstance(tag, Tag):
            raise TypeError(f"Tag must be Tag, not {type(tag)}!")
        self.tags[tag.id] = tag

    def remove_tag(self, tag_id: str) -> None:
        if not isinstance(tag_id, str):
            raise TypeError(f"Tags id must be a str, not {type(tag_id)}!")
        self.tags.pop(tag_id)

    def __getitem__(self, tag_id: str) -> Tag:
        if not isinstance(tag_id, str):
            raise TypeError(f"ID must be a str, not {type(id)}!")
        return self.tags[tag_id]

    def __dict__(self) -> dict:
        tmp: dict = {}
        for tag in self.tags.values():
            tmp[tag.id] = tag.__dict__()
        return tmp

    @staticmethod
    def from_dict(dict_: dict) -> 'TagList':
        tmp = TagList([])
        for tag_dict in dict_.values():
            tmp.add_tag(Tag.from_dict(tag_dict))
        return tmp


class Transaction(TrackerObject):
    def __init__(
            self,
            name: str,
            description: str,
            id: str, balance: float,
            tags_id: List[str]
    ) -> None:

        TrackerObject.__init__(self, name, description, id)

        if not isinstance(balance, float):
            raise TypeError(
                f"Balance of transaction must be a float, not a {type(name)}!")
        self.balance: float = balance

        self.tags_id: List[str] = tags_id

    def __dict__(self):
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "balance": self.balance,
            "tags_id": self.tags_id,
        }

    @staticmethod
    def from_dict(dict_) -> 'Transaction':
        return Transaction(
            dict_["name"],
            dict_["description"],
            dict_["id"],
            dict_["balance"],
            dict_["tags_id"]
        )

    @staticmethod
    def get_from_file(path: os.path) -> 'Transaction':
        new_transaction = Transaction("", "", "", 0, [])
        new_transaction.load(path)
        return new_transaction


class Journal(TrackerObject):
    def __init__(
            self,
            name: str,
            description: str,
            id: str,
            tag_list: TagList,
            transaction_list: List[Transaction]
    ) -> None:

        TrackerObject.__init__(self, name, description, id)

        self.tag_list: TagList = tag_list

        self.transaction_list: List[Transaction] = transaction_list

    def get_balance(self) -> float:
        bal: float = 0.0
        for transaction in self.transaction_list:
            bal += transaction.balance
        return bal

    def add_transaction(self, transaction: Transaction) -> None:
        if not isinstance(transaction, Transaction):
            raise TypeError(
                f"Transaction must be a Transaction, not {type(id)}!")
        self.transaction_list.append(transaction)

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
        }

    @staticmethod
    def from_dict(dict_: dict) -> 'Journal':
        return Journal(
            dict_["name"],
            dict_["description"],
            dict_["id"],
            TagList.from_dict(dict_["tag_list"]),
            [Transaction.from_dict(tr_dict)
             for tr_dict in dict_["transaction_list"]]
        )

    @staticmethod
    def get_from_file(path: os.path) -> 'Journal':
        tag_list = TagList([])
        new_journal = Journal("", "", "", tag_list, [])
        new_journal.load(path)
        return new_journal
