if __name__ == "__main__":
    import sys
    import os.path

    sys.path[0] = os.path.join(sys.path[0], "..", "..")

from modules.tracker_logic.classes import *
from modules.tracker_logic.general_functions import nice_dict_, write_to_file

import random
import string
from datetime import datetime, timedelta

random_char_set = string.ascii_letters + string.digits + string.punctuation + " "

def random_char() -> str:
    return random.choice(random_char_set)

def random_char_string(length : int) -> str:
    return "".join(random_char() for _ in range(length))

def random_date(start: datetime, end: datetime) -> datetime:
    """Generate a random datetime between `start` and `end`."""
    delta = end - start
    int_delta = delta.days
    random_day = random.randint(0, int_delta)
    return start + timedelta(days=random_day)

def gen_random_tag_list() -> list:
    global shadow_journal, tag_list
    __tag_list = []
    for i in range(random.randint(0, len(tag_list) - 1)):
        __tag_list.append(list(shadow_journal.tag_list.tags.keys())[i])
    return __tag_list


tags_amount = 50
transactions_amount = 100000

tag_list = [
    Tag(
        name=random_char_string(random.randint(3, 20)),
        description=random_char_string(random.randint(10, 150))
    ) for _ in range(tags_amount)
]

shadow_journal = Journal("Shadow Journal", "This journal was created for testing", "#jr999", TagList(tag_list), [])




transactions_list = [
    Transaction(
        name=random_char_string(random.randint(10, 40)),
        description=random_char_string(random.randint(10, 150)),
        balance=random.uniform(-50000, 50000),
        tags_id=gen_random_tag_list(),
        date_=None
    ) for _ in range(int(transactions_amount / 3))
] + [
    Transaction(
        name=random_char_string(random.randint(10, 40)),
        description=random_char_string(random.randint(10, 150)),
        balance=random.uniform(-10000, 10000),
        tags_id=gen_random_tag_list(),
        date_=None
    ) for _ in range(int(transactions_amount / 3))
] + [
    Transaction(
        name=random_char_string(random.randint(10, 40)),
        description=random_char_string(random.randint(10, 150)),
        balance=random.uniform(-1000, 1000),
        tags_id=gen_random_tag_list(),
        date_=None
    ) for _ in range(int(transactions_amount / 3))
]

while len(transactions_list) < transactions_amount:
    transactions_list.append(
        Transaction(
            name=random_char_string(random.randint(10, 40)),
            description=random_char_string(random.randint(10, 150)),
            balance=random.uniform(-1000, 1000),
            tags_id=gen_random_tag_list(),
            date_=None
        )
    )

while len(transactions_list) > transactions_amount:
    transactions_list.pop(0)

journal = Journal("Super big journal", "This journal was created for testing", "#jr003", TagList(tag_list), [])

for transaction in transactions_list:
    journal.add_transaction(transaction)
    journal.transaction_list[-1].date = random_date(datetime(2000, 1, 1), datetime(2027, 1, 1)).date()

write_to_file(os.path.join(Settings.DEFAULT_JOURNALS_PATH, "super_big_journal.json"), journal.__dict__())