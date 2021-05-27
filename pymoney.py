import sys
#class definitions
class Record:
    """Represent a record"""
    def __init__(self, cat, description, amount):
        self._cat = cat
        self._description = description
        self._amount = amount
    @property
    def cat(self):
        return self._cat
    @property
    def description(self):
        return self._description
    @property
    def amount(self):
        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        self._records = []
        try:
            fh = open('records.txt', 'r')
            try:
                self._initial_money = int(fh.readline())
            except ValueError:
                sys.stderr.write('Money not being read correctly. Set to 0 by default.\n')
                self._initial_money = 0
            
            read_list = fh.read().splitlines()
            for i in read_list:
                tmp = i.split(',')
                self._records.append(Record(tmp[0], tmp[1], int(tmp[2])))
        except FileNotFoundError:
            try:
                self._initial_money = int(input("How much money do you have?"))
            except:
                sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
                self._initial_money = 0
    
    def add(self, record, categories):
        """Function to add single record, with some excetion handling features."""
        try:
            split_record = record.split() # split str "cat record val" into ["cat, "record", "val"]
            amount = int(split_record[2])
        except ValueError:
            sys.stderr.write('Invalid value for money.\nFail to add a record.\n')  
        except:
            sys.stderr.write('The format of a record should be like this:meal breakfast -50.\nFail to add a record.\n')
            
        if categories.is_category_valid(str(split_record[0])) == True:
            self._records.append(Record(split_record[0], split_record[1], amount))
        else:
            print('Category is not valid.')

    def view(self):
        """Print out all records and remaining money at the end."""
        print("       Category       Description     Amount")
        print("   --------------- ----------------- --------")
        money_display = self._initial_money
        idx = 1
        for i in self._records:
            print(f'{idx}.  {i.cat : <14}  {i.description : <14} {i.amount : 8}')
            money_display += i.amount
            idx = idx + 1
        print('-- ------------------------------------------')
        print(f'Now you have {money_display} dollars.')
    
    def delete(self, records):
        """Delete a single record by its index."""
        delete_idx = int(records) - 1 #conversion: 1, 2, 3... to 0, 1, 2...
        try:
            del self._records[delete_idx]
        except:            
            print(f"There's no record that matches. Failed to delete a record.")

    def find(self, desired_categories):
        """Find an existing category, and print all records under it."""
        print_records = []
        print_records = list(filter(lambda n : n.cat in desired_categories, self._records))
        print("       Category       Description     Amount")
        print("   --------------- ----------------- --------")
        money_display = 0
        idx = 1
        for i in print_records:
            print(f'{idx}.  {i.cat : <14}  {i.description : <14} {i.amount : 8}')
            money_display += i.amount
            idx = idx + 1
        print('-- ------------------------------------------')
        print(f'The total amount above is {money_display}.')

    def save(self):
        """Save money and all records to records.txt."""
        #self._records = [str(line) + "\n" for line in self._records] #.writelines() doesn't add new lines by default
        save_records = []
        for record in self._records:
            line = str(record.cat) + "," + str(record.description) + "," + str(record.amount)
            save_records.append(line + "\n")
        with open('records.txt', 'w') as fh:     
            fh.write(str(self._initial_money) + "\n")
            fh.writelines(save_records)
   
class Categories:
    def __init__(self):
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'train', 'texi']], \
        'income', ['salary', 'bonus']]
    
    def view(self):
        """Print out all categories with indentation."""
        def view_inner(cats, level = -1):
            if cats == None:
                return
            if type(cats) == list:
                for child in cats:
                    view_inner(child, level + 1)
            else:
                print(f'{" " * 2 * level}・{cats}')
        view_inner(self._categories)
    
    def is_category_valid(self, desired_category):
        """Check if the user-input category is valid."""
        def is_category_valid_inner(category, categories):
            if type(categories) == list:
                for child in categories:
                    ret =  is_category_valid_inner(category, child)
                    if ret == True:
                        return is_category_valid_inner(category, child) # exit this function
            elif type(categories) == str:
                return str(category) == str(categories)
        return is_category_valid_inner(desired_category, self._categories)

    def find_subcategories(self, desired_categories):
        """Find sub categories of a specific category."""
        def flatten(L):
            """Flatten an irregular list."""
            if type(L) == list:
                result = []
                for child in L:
                    result.extend(flatten(child))
                return result
            else:
                return [L]

        def find_subcategories_inner(category, categories):
            if type(categories) == list:
                for val in categories:
                    part = find_subcategories_inner(category, val)
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

        return find_subcategories_inner(desired_categories, self._categories)
 
#main program starts here
records = Records()
categories = Categories()

while True:
    command = input("\nWhat do you want to do \
(add / view / delete / view categories / find / exit) ? ")
    if command == "add":
        record = input('Add an expense or income record with ...:\n')
        records.add(record, categories)
    elif command == "view":
        records.view()
    elif command == "delete":
        records.view()
        delete_record = input('\nWhich record do you want to delete? ')
        records.delete(delete_record)
    elif command == "view categories":
        categories.view()
    elif command == "find":
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        records.find(target_categories)
    elif command == "exit":
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
