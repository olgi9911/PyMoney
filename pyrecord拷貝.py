import sys
from datetime import date

class Record:
    """Represent a record"""
    def __init__(self, date, cat, description, amount):
        self._date = date
        self._cat = cat
        self._description = description
        self._amount = amount
    @property
    def date(self):
        return self._date
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

            print('Welcome back!')
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
            if len(split_record) == 4:
                input_date = date.fromisoformat(split_record[0])
                cat = split_record[1]
                description = split_record[2]
                amount = int(split_record[3])
            else:
                input_date = date.today()
                cat = split_record[0]
                description = split_record[1]
                amount = int(split_record[2])
        except ValueError:
            sys.stderr.write('Invalid value for money.\nFail to add a record.\n')  
        except:
            if len(split_record) == 4:
                sys.stderr.write('The format of date should be YYYY-MM-DD.\nFail to add a record.\n')
            else:
                sys.stderr.write('The format of a record should be like this:meal breakfast -50.\nFail to add a record.\n')
            
        if categories.is_category_valid(str(cat)) == True:
            self._records.append(Record(input_date, cat, description, amount))
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