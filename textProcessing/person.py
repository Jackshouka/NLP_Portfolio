import sys
import pathlib
import re
import csv
import pickle

# method 2 of using sysarg on GitHub
def setfilepath(filepath):
    with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
        text_in = f.read()
   # print(text_in)


def process(filepath):
    csv_file = csv.reader(filepath)
    #delete header row, skip when reading and write to new

    with open(filepath, 'r') as in_file:
        reader = csv.reader(in_file)
        next(reader) # Skipping the header row
        text_csv = []
        for row in reader: #iterate thru reader
            for entry in row:
                text_csv.append(entry.lower())#append text to text list as lowercase to capitalize later
    #break down pure data list into new lists based on original columns we overlooked
    last_list = [text_csv[0], text_csv[5], text_csv[10], text_csv[15], text_csv[20]]
    first_list = [text_csv[1], text_csv[6], text_csv[11], text_csv[16], text_csv[21]]
    mi_list = [text_csv[2], text_csv[7], text_csv[12], text_csv[17], text_csv[22]]
    id_list = [text_csv[3], text_csv[8], text_csv[13], text_csv[18], text_csv[23]]
    phone_list = [text_csv[4], text_csv[9], text_csv[14], text_csv[19], text_csv[24]]

    #captialize first/last names in first_list and last_list
    #acheive this by copying lists and making edits.
    first_list[:] = [i.capitalize() for i in first_list]
    last_list[:] = [j.capitalize() for j in last_list]
    mi_list[:] = [k.capitalize() for k in mi_list]
    #capitalize ID alphabet characters
    id_list[:] = [l.upper() for l in id_list]
    #check for no mi
    for i in range(len(mi_list)):
        if mi_list[i] == '': #find empty cell
            mi_list[i] = 'X' #replcae w/ X

    #regex to format id section
    id_pattern = re.compile(r"^[A-Z]{2}\d{4}$")
    for i in range(len(id_list)):
        if id_pattern.match(id_list[i]):
            pass #id matches pattern, so we don't return error
        else:
            print("Invalid ID: Enter a two letter/four digit ID.")

    #regex for phone num
    phone_pattern = re.compile(r"^\d{3}-\d{3}-\d{4}$")
    for i in range(len(phone_list)):
        if phone_pattern.match(phone_list[i]):
            pass
        else:
            print("Invalid Phone Number: Enter a number in the format 123-456-7890.")

    #data to person obj
    pers1 = Person(first_list[0], last_list[0], mi_list[0], id_list[0], phone_list[0])
    pers2 = Person(first_list[1], last_list[1], mi_list[1], id_list[1], phone_list[1])
    pers3 = Person(first_list[2], last_list[2], mi_list[2], id_list[2], phone_list[2])
    pers4 = Person(first_list[3], last_list[3], mi_list[3], id_list[3], phone_list[3])
    pers5 = Person(first_list[4], last_list[4], mi_list[4], id_list[4], phone_list[4])

    #dict for person
    emp_dict = {
        pers1.id: pers1,
        pers2.id: pers2,
        pers3.id: pers3,
        pers4.id: pers4,
        pers4.id: pers5,
    }

    #pickle dict from process()
    pickle.dump(emp_dict, open('dict.p', 'wb'))
    return emp_dict


def main():
    # prompt file path
    print("Please enter in a filepath as a sysarg. ('data/data.csv')\n")
    if len(sys.argv) > 1:
        arg_input = sys.argv[1]
      #  print('Filepath: ', arg_input)
        setfilepath(arg_input)
    else:
        print('No sys.arg detected. Terminating.')
        sys.exit()

    process(arg_input)
    dict_in = pickle.load(open('dict.p', 'rb'))

# person class

class Person:
    def __init__(self, first, last, mi, id, phone):
        self.first = first
        self.last = last
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("Employee ID: ", self.id, "\n")
        print('{} {} {}'.format(self.first, self.mi, self.last), "\n")
        print(self.phone, "\n")


if __name__ == "__main__":
    main()
