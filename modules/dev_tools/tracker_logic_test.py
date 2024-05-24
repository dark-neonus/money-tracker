if __name__ == "__main__":
    import sys
    import os.path

    print(sys.path[0])
    sys.path[0] = os.path.join(sys.path[0], "..", "..")
    print(sys.path[0])

from modules.tracker_logic.classes import *
from modules.tracker_logic.general_functions import nice_dict_


"""
def Tag_test():
    tag  = Tag("test_tag", "This tag was created for testing", "#tg001")
    
    print("\nOriginal:")
    print(nice_dict_(tag.__dict__()))
    
    with open("tag.json", "w") as file:
        json.dump(tag.__dict__(), file, indent="\t")
        
    with open("tag.json", "r") as file:
        tag1 = Tag.from_dict(json.load(file))
        
        
    print("\nLoaded:")
    print(nice_dict_(tag1.__dict__()))
    print("\n")

def TagList_test():
    tag1  = Tag("test_tag_1", "This tag was created for testing", "#tg001")
    tag2  = Tag("test_tag_2", "This tag was created for testing", "#tg002")
    tag3  = Tag("test_tag_3", "This tag was created for testing", "#tg003")

    tag_list = TagList([tag1, tag2, tag3])

    print("\nOriginal:")
    print(nice_dict_(tag_list.__dict__()))

    with open("tag_list.json", "w") as file:
        json.dump(tag_list.__dict__(), file, indent="\t")

    with open("tag_list.json", "r") as file:
        tag_list1 = TagList.from_dict(json.load(file))


    print("\nLoaded:")
    print(nice_dict_(tag_list1.__dict__()))
    print("\n")
    
def Transaction_test():
    transaction  = Transaction("test_transaction", "This transaction was created for testing", "#tr000000", 500.0, ["#tg001", "#tg003"])
    
    print("\nOriginal:")
    print(nice_dict_(transaction.__dict__()))
    
    with open("transaction.json", "w") as file:
        json.dump(transaction.__dict__(), file, indent="\t")
        
    with open("transaction.json", "r") as file:
        transaction1 = Transaction.from_dict(json.load(file))
        
        
    print("\nLoaded:")
    print(nice_dict_(transaction1.__dict__()))
    print("\n")
    
"""

def Journal_test():
    tag1  = Tag("test_tag_1", "This tag was created for testing", "#tg001")
    tag2  = Tag("test_tag_2", "This tag was created for testing", "#tg002")
    tag3  = Tag("test_tag_3", "This tag was created for testing", "#tg003")

    tag_list = TagList([tag1, tag2, tag3])
    
    transaction1  = Transaction("test_transaction_1", "This transaction was created for testing", "#tr000001", 500.0, ["#tg001", "#tg003"])
    transaction2  = Transaction("test_transaction_2", "This transaction was created for testing", "#tr000002", -700.0, ["#tg002", "#tg001"])
    transaction3  = Transaction("test_transaction_3", "This transaction was created for testing", "#tr000003", 120.5, [])
    
    journal  = Journal("test_journal", "This journal was created for testing", "#jr000", tag_list, [transaction1, transaction2, transaction3])
    
    print("\nOriginal:")
    print(nice_dict_(journal.__dict__()))
    
    # with open("journal.json", "w") as file:
    #     json.dump(journal.__dict__(), file, indent="\t")
    journal.save("jsons/new_journal.json")
        
    journal1 = Journal.get_from_file("jsons/new_journal.json")
        
        
    print("\nLoaded:")
    print(nice_dict_(journal1.__dict__()))
    print("\n")
    print(journal1.get_balance())
    
tests : Dict[type, callable] = {
    # Tag : Tag_test,
    # TagList : TagList_test,
    # Transaction : Transaction_test,
    Journal : Journal_test,
}



if __name__ == "__main__":
    tests[Journal]()