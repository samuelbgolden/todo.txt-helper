import os
import pickle
from datetime import datetime, timedelta

### initials ###

datafile_path = os.path.relpath('./.helperdata')
datetime_format = '%Y-%m-%d'

### function definitions ###

class Func:
    def __init__(self, name, desc, callback):
        self.name = name
        self.desc = desc
        self.callback = callback

def add_many():
    text = input("content of todo item (exclude due date): ").strip()
    first = last = None
    while not first:
        try:
            first = datetime.strptime(input("first day (yyyy-mm-dd): ").strip(), datetime_format)
        except ValueError:
            print('> could not parse date, try again')

    while not last:
        try:
            last = datetime.strptime(input("last day (yyyy-mm-dd, exclusive): ").strip(), datetime_format)
        except ValueError:
            print('> could not parse date, try again')

    tasks = []
    while first != last:
        tasks.append(f"{text} due:{first.strftime(datetime_format)}\n")
        first = first + timedelta(days=1)
    
    with open(data['todo_path'], 'a') as todo:
        for task in tasks:
            todo.write(task)
    
    print('> Done!')

functions = [
    Func('add-many', 'adds one task many times across a date range', add_many),
]

### MAIN ###

if __name__ == "__main__":
    # find data file or create it
    if os.path.exists(datafile_path):
        with open(datafile_path, 'rb') as f:
            data = pickle.load(f)
    else: 
        data = {}
        data['todo_path'] = os.path.abspath(input("path to todo.txt file: "))
        data['done_path'] = os.path.abspath(input("path to done.txt file: "))

    while not os.path.isfile(data['todo_path']):
        print(f"> could not find todo.txt at {data['todo_path']}")
        data['todo_path'] = os.path.abspath(input("path to todo.txt file: "))

    while not os.path.isfile(data['done_path']):
        print(f"> could not find done.txt at {data['done_path']}")
        data['done_path'] = os.path.abspath(input("path to done.txt file: "))

    with open(datafile_path, 'wb') as f:
        pickle.dump(data, f, pickle.DEFAULT_PROTOCOL)

    # print menu
    print("~~~~~~~~~~~~~~~ TODO.TXT HELPER ~~~~~~~~~~~~~~~")
    print(f"  TODO PATH: {data['todo_path']}\n  DONE PATH: {data['done_path']}")
    print("Functions:")
    for i,f in enumerate(functions):
        print(f"\t{i}) {f.name}: {f.desc}")

    # get user choice and call appropriate function
    choice = str(input("\nEnter function name or number: ")).strip()
    chosen = None
    for f in functions:
        if f.name == choice:
            chosen = f.callback

    if not chosen:
        try:
            func_num = int(choice)
            if func_num in range(0,len(functions)):
                chosen = functions[func_num].callback
            else:
                print(f"Only function numbers 0 to {len(functions)-1} are valid; exiting...")
        except ValueError:
            print(f"Could not figure out which function '{choice}' is; exiting...")

    chosen()


