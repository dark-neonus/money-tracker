from modules.tracker_logic.classes import *
from modules.tracker_logic.general_functions import nice_dict_
import json

tag1  = Tag("Car", "Money spent on car repairment, fuel and other needs", "#tg001")
tag2  = Tag("Food", "Money spent to brought food", "#tg002")
tag3  = Tag("Bills", "Bills payment", "#tg003")
tag4  = Tag("Salary", "Salary", "#tg004")
tag_list = TagList([tag1, tag2, tag3, tag4])

transaction1  = Transaction("Trip", "Money spent on family trip", "#tr000001", -2500.0, ["#tg001", "#tg002"])
transaction2  = Transaction("Salary 2024.07", "Salary that was get on July 2024", "#tr000002", 14000.0, ["#tg004"])
transaction3  = Transaction("Charity", "For poor childrens", "#tr000003", -120.5, [])

journal  = Journal("MyMainJournal", "This journal was created for testing", "#jr000", tag_list, [transaction1, transaction2, transaction3])

print("\nOriginal:")
print(nice_dict_(journal.__dict__()))

with open("test-journal.json", "w") as file:
    json.dump(journal.__dict__(), file, indent="\t")
    
with open("test-journal.json", "r") as file:
    journal1 = Journal.from_dict(json.load(file))
    
    
print("\nLoaded:")
print(nice_dict_(journal1.__dict__()))
print("\n")
print(journal1.balance())