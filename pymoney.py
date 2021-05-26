#!/usr/bin/env python
# coding: utf-8
import sys
import re
#function declarations start here
def initialize():
    """Open and read in records.txt if existed, 
    or prompt user to input money they have.
    """
    total_record = []
    try:
        fh = open('records.txt', 'r')
        try:
            money = int(fh.readline())
        except ValueError:
            sys.stderr.write('Money not being read correctly. Set to 0 by default.\n')
            
        read_list = fh.read().splitlines()
        for i in read_list:
            temp = re.split("[('',)]", i) # split str"('record', val)" into ["", "", "record", "", " val", ""]
            total_record.append((temp[2], temp[5], int(temp[7])))
    except FileNotFoundError:
        try:
            money = int(input("How much money do you have?"))
        except:
            sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
            money = 0
    return money, total_record
############################
def initialize_categories():
    """Initialize a list of default categories.
    """
    return ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'train']], \
        'income', ['salary', 'bonus']]
######################
def add(total_record, categories):
    """Function to add single record, with some excetion handling features.
    """
    record = input("Add an expense or income record with categories, description and amount:\n")
    try:
        split_record = record.split() # split str"record val" into ["record", "val"]
        amount = int(split_record[2])
    except ValueError:
        sys.stderr.write('Invalid value for money.\nFail to add a record.\n')
        return total_record
    except:
        sys.stderr.write('The format of a record should be like this: breakfast -50.\nFail to add a record.\n')
        return total_record
    if is_category_valid(str(split_record[0]), categories) == True:
        total_record.append((split_record[0], split_record[1], amount)) #tuple in a list
    else:
        print('Category is not valid.')
    return total_record
#########################
def view(money, records):
    """Print out all records and remaining money at the end.
    """
    print("       Category       Description     Amount")
    print("   --------------- ----------------- --------")
    money_display = money
    idx = 1
    for i in records:
        print(f'{idx}.  {i[0] : <14}  {i[1] : <14} {i[2] : 8}')
        money_display += i[2]
        idx = idx + 1
    print('-- ------------------------------------------')
    print(f'Now you have {money_display} dollars.')
####################
def delete(records):
    """Delete a single record by its index.
    """
    try:
        delete_idx = int(input("Input the record index you want to delete: "))
    except:
        sys.stderr.write('Invalid format. Fail to delete a record.\n')
        return records
    delete_idx = delete_idx - 1 #conversion: 1, 2, 3... to 0, 1, 2...
    try:
        del records[delete_idx]
    except:            
        print(f"There's no record that matches. Fail to delete a record.")
        return records 
    
    return records
######################
def view_categories(cats, level = -1):
    """Print out all categories with indentation.
    """
    if cats == None:
        return
    if type(cats) == list:
        for child in cats:
            view_categories(child, level + 1)
    else:
        print(f'{" " * 2 * level}・{cats}')
############################################
def is_category_valid(category, categories):
    """Check if the user-input category is valid.
    """
    if type(categories) == list:
        for child in categories:
            ret =  is_category_valid(category, child)
            if ret == True:
                return is_category_valid(category, child) # exit this function
    elif type(categories) == str:
        return str(category) == str(categories)
##############################
def find(records, categories):
    """Find an existing category, and print all records under it.
    """
    to_find = input('Which category do you want to find? ')
    found_records = find_subcategories(to_find, categories)
    print_records = []
    print_records = list((filter(lambda n : n[0] in found_records, records)))
    print("       Category       Description     Amount")
    print("   --------------- ----------------- --------")
    money_display = 0
    idx = 1
    for i in print_records:
        print(f'{idx}.  {i[0] : <14}  {i[1] : <14} {i[2] : 8}')
        money_display += i[2]
        idx = idx + 1
    print('-- ------------------------------------------')
    print(f'The total amount above is {money_display}.')
#############################################
def find_subcategories(category, categories):
    """Find sub categories of a specific category.
    """
    if type(categories) == list:
        for val in categories:
            part = find_subcategories(category, val)
            if part == True:
                index = categories.index(val)
                if index + 1 < len(categories) and \
                    type(categories[index + 1]) == list:
                    return flatten(categories[index:index + 2])
                else:
                    return [val]
            if part != []:
                return part
    return True if categories == category else []
###############
def flatten(L):
    """Flatten an irregular list.
    """
    if type(L) == list:
        result = []
        for child in L:
            result.extend(flatten(child))
        return result
    else:
        return [L]
#########################
def save(money, records):
    """Save money and all records to records.txt.
    """
    records = [str(line) + "\n" for line in records] #.writelines() doesn't add new lines by default
        
    with open('records.txt', 'w') as fh:     
        fh.write(str(money) + "\n")
        fh.writelines(records)
#########################       
#main program starts here
initial_money, records = initialize()
categories = initialize_categories()
while True:
    command = input("\nWhat do you want to do (add / view / delete / view categories / find / exit)? ")
    if command == "add":
        records = add(records, categories)
    elif command == "view":
        view(initial_money, records)
    elif command == "delete":
        records = delete(records)
    elif command == "view categories":
        view_categories(categories)
    elif command == "find":
        find(records, categories)
    elif command == "exit":
        save(initial_money, records)
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
