import sys
import tkinter
from datetime import date
from tkinter import ttk
from pycategory import *
from pyrecord import *
#main program starts here
records = Records()
categories = Categories()

def add_record(date, category, description, amount):
    addRecord = date + ' ' + category + ' ' + description + '  ' + amount
    records.add(addRecord, categories)
def delete():
    description_entry.delete(0, 'end')
    amount_entry.delete(0, 'end')
    date_str.set(str(date.today()))
    cat_box.set('')
def update():
    money_display = records._initial_money
    entry.delete(0, 'end')
    listbox.delete(0, 'end')
    idx = 1
    for i in records._records:
        listbox.insert(idx, f'{str(i.date.strftime("%Y-%m-%d"))}  {i.cat :<10}{i.description :<10}{i.amount : 8}')
        idx = idx + 1
        money_display += i.amount
    curr_money_str.set(f'Now you have {money_display} dollars.')
    records.save()
def find(category):
    money_display = 0
    desired_categories = categories.find_subcategories(category)
    print_records = list(filter(lambda n : n.cat in desired_categories, records._records))
    listbox.delete(0, 'end')
    idx = 1
    for i in print_records:
        listbox.insert(idx, f'{str(i.date.strftime("%Y-%m-%d"))}  {i.cat :<8}{i.description :<8}{i.amount : 8}')
        idx = idx + 1
        money_display += i.amount
    curr_money_str.set(f'The total amount above is {money_display}.')
###################
root = tkinter.Tk()
root.title('PyMoney')
f = tkinter.Frame(root, width=680, height=240, borderwidth=5)
f.grid_propagate(False)
f.grid(row=0, column=0)
find_label = tkinter.Label(f, text='Find category:')
find_label.grid(row = 0)
find_str = tkinter.StringVar()
entry = tkinter.Entry(f, textvariable=find_str)
entry.grid(row = 0, column = 1)
find_button = tkinter.Button(f, text='Find', command = lambda:find(find_str.get()))
find_button.grid(row = 0, column=2)
all_button = tkinter.Button(f, text='All', command = lambda : update())
all_button.grid(row = 0, column=3)
listbox = tkinter.Listbox(f, width=45, height=10, font='courier')
listbox.grid(row=1, column=0, rowspan=6, columnspan=4, sticky=tkinter.W)
money_label = tkinter.Label(f, text='Initial money:')
money_label.grid(row = 1, column=4)
money_str = tkinter.StringVar()
money_str.set(str(records._initial_money))
money_entry = tkinter.Entry(f, textvariable=money_str)
money_entry.grid(row = 1, column = 5,sticky=tkinter.E)
update_button = tkinter.Button(f, text='Update', command = lambda: [records.set_initial_money(money_str.get()), update()])
update_button.grid(row=2,column=5,sticky=tkinter.E)
date_label = tkinter.Label(f, text='Date:')
date_label.grid(row = 3, column=4)
date_str = tkinter.StringVar()
date_str.set(str(date.today()))
date_entry = tkinter.Entry(f, textvariable=date_str)
date_entry.grid(row = 3, column = 5,sticky=tkinter.E)
cat_label = tkinter.Label(f, text='Category:')
cat_label.grid(row = 4, column = 4)
cat_box = ttk.Combobox(f, values=['expense', 'food', 'meal', 'snack', 'drink', 'transportation', 'bus', 'train', 'texi', \
        'income', 'salary', 'bonus'])
cat_box.grid(row = 4, column = 5,sticky=tkinter.E)
description_label = tkinter.Label(f, text='Description:')
description_label.grid(row = 5, column=4)
description_str = tkinter.StringVar()
description_entry = tkinter.Entry(f, textvariable=description_str)
description_entry.grid(row = 5, column = 5,sticky=tkinter.E)
amount_label = tkinter.Label(f, text='Amount:')
amount_label.grid(row = 6, column=4)
amount_str = tkinter.StringVar()
amount_entry = tkinter.Entry(f, textvariable=amount_str)
amount_entry.grid(row = 6, column = 5,sticky=tkinter.E)
add_button = tkinter.Button(f, text='Add', command = lambda:[add_record(date_str.get(), str(cat_box.get()), description_str.get(), amount_str.get()), delete(), update()])
add_button.grid(row=7,column=5,sticky=tkinter.E)
curr_money_str = tkinter.StringVar()
curr_money_label = tkinter.Label(f, textvariable= curr_money_str)
curr_money_label.grid(row = 7, column = 0, columnspan=3, sticky=tkinter.W)
delete_button = tkinter.Button(f, text='Delete', command=lambda:[records.delete(listbox.curselection()), update()])
delete_button.grid(row = 7, column = 3)
##################
update()
##################
tkinter.mainloop()
############

