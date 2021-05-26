#!/usr/bin/env python
# coding: utf-8
import sys
import re
#function declarations start here
def initialize():
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
            total_record.append((temp[2], int(temp[4])))
    except FileNotFoundError:
        try:
            money = int(input("How much money do you have?"))
        except:
            sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
            money = 0
    return money, total_record
############################
def initialize_categories():
    return ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'train']], \
        'income', ['salary', 'bonus']]
######################
def add(total_record):
    record = input("Add an expense or income record with description and amount:\n")
    try:
        split_record = record.split() # split str"record val" into ["record", "val"]
        amount = int(split_record[1])
    except ValueError:
        sys.stderr.write('Invalid value for money.\nFail to add a record.\n')
        return total_record
    except:
        sys.stderr.write('The format of a record should be like this: breakfast -50.\nFail to add a record.\n')
        return total_record
    
    total_record.append((split_record[0], amount)) #tuple in a list
    return total_record
#########################
def view(money, records):
    print("   Description     Amount")
    print("----------------- --------")
    money_display = money
    idx = 1
    for i in records:
        print(f'{idx}. {i[0] : <14} {i[1] : 8}')
        money_display += i[1]
        idx = idx + 1
            
    print(f'Now you have {money_display} dollars.')
####################
def delete(records):
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
def view_categories():
    print("")
#########################
def save(money, records):
    records = [str(line) + "\n" for line in records] #.writelines() doesn't add new lines by default
        
    with open('records.txt', 'w') as fh:     
        fh.write(str(money) + "\n")
        fh.writelines(records)

#main program starts here
initial_money, records = initialize()
categories = initialize_categories()
while True:
    command = input("\nWhat do you want to do (add / view / delete / view categories / find / exit)? ")
    if command == "add":
        records = add(records)
    elif command == "view":
        view(initial_money, records)
    elif command == "delete":
        records = delete(records)
    elif command == "view categories":
        view_categories()
    elif command == "exit":
        save(initial_money, records)
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
