if __name__ == "__main__":
    import sys
    import os.path

    sys.path[0] = os.path.join(sys.path[0], "..", "..")

from modules.tracker_logic.classes import *
from modules.tracker_logic.general_functions import nice_dict_
import json



tag_list = TagList([
    Tag("Car", "Money spent on car repairment, fuel and other needs"),
    Tag("Food", "Money spent to brought food"),
    Tag("Bills", "Bills payment"),
    Tag("Salary", "Salary"),
    Tag("Ahaha", "Tag for super testing\n\nhaha\n\nsome tag text\n.\n."),
    Tag("Cool stuff", "Litteraly not drugs, but cool stuff"),
    Tag("Other", ""),
     ])

transaction_list = [
    Transaction("Car", "Money spent on car repairment", -100.0, [
        tag_list.get_tag_by_name("Car").id,
        tag_list.get_tag_by_name("Bills").id
    ],
        date_=date(2024, 6, 12)
    ),
    Transaction("Food", "Money spent on food", -50.0, [
        tag_list.get_tag_by_name("Food").id,
        tag_list.get_tag_by_name("Cool stuff").id
    ],
        date_=date(2024, 2, 1)
    ),
    Transaction("Bills", "Money spent on bills", -100.0, [
        tag_list.get_tag_by_name("Bills").id,
        tag_list.get_tag_by_name("Ahaha").id
    ],
        date_=date(2023, 12, 29)
    ),
    Transaction("Salary", "Salary that was get on July 2024", 14000.0, [
        tag_list.get_tag_by_name("Salary").id
    ],
        date_=date(2024, 7, 1)
    ),
    Transaction("Charity", "For poor childrens", -120.5, [
        tag_list.get_tag_by_name("Other").id
    ]),
    Transaction("Trip", "Money spent on family trip", -2500.0, [
        tag_list.get_tag_by_name("Car").id,
        tag_list.get_tag_by_name("Ahaha").id,
        tag_list.get_tag_by_name("Other").id,
        tag_list.get_tag_by_name("Cool stuff").id
    ],
        date_=date(2024, 7, 27)
    ),
    Transaction("Empty transaction", "", 0.0, [

    ]),
    Transaction("Ahaha", "Tester transaction", -12.78, [
        tag_list.get_tag_by_name("Ahaha").id
    ]),
    Transaction("Luccky poker game", "Won soe games", 1000.0, [
        tag_list.get_tag_by_name("Other").id,
        tag_list.get_tag_by_name("Salary").id
    ],
        date_=date(2024, 1, 1)
    ),
    Transaction("Blablalba", ".", 274.2, [
        tag_list.get_tag_by_name("Other").id
    ]),
    Transaction("Fuel", "Bought fuel at gas station", -2400.0, [
        tag_list.get_tag_by_name("Car").id
    ],
        date_=date(2024, 3, 21)
    )
]

journal  = Journal("MyMainJournal", "This journal was created for testing", "#jr000", tag_list, transaction_list)

print("\nOriginal:")
print(nice_dict_(journal.__dict__()))

with open(os.path.join("data", "journals", "test-journal.json"), "w") as file:
    json.dump(journal.__dict__(), file, indent="\t")
    
with open(os.path.join("data", "journals", "test-journal.json"), "r") as file:
    journal1 = Journal.create_from_dict(json.load(file))
    
    
print("\nLoaded:")
print(nice_dict_(journal1.__dict__()))
print("\n")
print(journal1.get_balance())