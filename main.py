# For correct recognizing name in word
import nltk
import numpy

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk import word_tokenize, pos_tag, ne_chunk
# For fast searching str in line
import linecache

# For loading animation
import itertools
import sys
import time
import threading


def read_data(filename, tt_file, inputed_gnr):
    """
    (str, str, str) -> dict

    Reads the file (filename, title filename, inputted_gnr)
    And returns dictionary with names of character
    And quantity of occurrence their in titles
    Genres: Short         Action      Crime       Sport
            Drama         Romance     Adventure   History
            Comedy        Music       Fantasy     Musical
            Documentary   Animation   Sci-Fi      War
            Adult         Horror      Mystery     Reality-TV
            Thriller      Family      Biography   Western

    >>> read_data()
    """
    with open(filename, encoding='utf-8', errors='ignore', mode="r") as f:
        dct = {}
        proff_cnst = ["actress", "actor"]  # We use only actor and actress
        for line in f:
            line = line.strip().split("\t")

            profession = line[3]  # Human profession
            tt_numb = line[0]  # Unique number of title
            nm_numb = line[2]  # Unique number of actor
            name_ch = line[-1]  # Character`s name

            if profession in proff_cnst and name_ch != '\\N':

                name_ch = name_ch[2:-2]  # Making str from lst-str
                gnr_lst = genres_fu(tt_file, tt_numb)
                if gnr_lst != -1:
                    if inputed_gnr in gnr_lst:
                        key = inputed_gnr
                        count = 0
                        # Making dictionary of dictionaries where
                        # not frozen set is quantity of name in genre
                        if key not in dct:
                            count = 1
                            dct[key] = {name_ch: count}
                        else:
                            if name_ch not in dct[key]:
                                count = 1
                                dct[key][name_ch] = count
                            else:
                                dct[key][name_ch] += 1
    return dct


def popular(dct):
    """
    {tuple(str,str):int} ->
          [tuple(str:int), tuple(str:int), ..., tuples(str: int)]

    Function clearing all str that not seems to be names
    And checking is all char in str is alpha or spaces
    Return list of 5 most popular key by value in that key.

    >>> popular({"John": 4, "Clara": 3, "fdsal;": 56, \
"Narrator": 8, "Peter": 2, "Daniel": 1, "Cris": 5})
    [('John', 4), ('Peter', 2), ('Daniel', 1)]

    """
    values = []
    final_lst = []
    list_of_keys = list(dct.keys())
    for key in list_of_keys:
        # Clearing all trash names that not in first or second name view
        if key.isalpha():
            if "PERSON" not in str(ne_chunk(pos_tag(word_tokenize(key)))):
                # Is not name
                dct.pop(key)
        else:
            # Is not alpha sentence
            dct.pop(key)
    number = 50
    if number > len(dct):
        number = len(dct)
    for i in range(number):
        values = []
        for quantity in dct.values():
            values.append(quantity)
        max_ind = values.index(max(values))
        max_name = list(dct.keys())[max_ind]
        name_numb = max_name, dct[max_name]
        final_lst.append(name_numb)
        dct.pop(max_name)
    return final_lst


def genres_fu(filename, tt_numb):
    """
    (str,str) -> list

    Function open title_filename and binary search
    the line were tt_numb is on lin[0] position
    than returns list of line[-1] element which is the genres
    that separated by ","


    """

    min = 2
    max = 5479070
    while True:
        if max < min:
            return -1
        m = (min + max) // 2
        line = linecache.getline(filename, m).strip().split("\t")
        tt_compare = line[0]
        if tt_compare < tt_numb:
            min = m + 1
        elif tt_compare > tt_numb:
            max = m - 1
        else:
            line = linecache.getline(filename, m).strip().split("\t")
            title_gen = line[-1]  # Title genres
            genres = title_gen.split(",")
            return genres


def starter_prog(inputed_genre):
    """
    (str) -> lst

    Function starts reading file, and search
    the most popular name

    """

    dct = read_data('data/castIMDB.tsv', 'data/TITLE.tsv', inputed_genre)
    fin_lst = popular(dct[inputed_genre])
    fin_lst1 = fin_lst + []
    write_csv(fin_lst1)
    return fin_lst


def animate():
    """
    Function illustrate animation of loading
    and will close when starter_prog() finish process
    """
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading' + c)
        sys.stdout.flush()
        time.sleep(0.1)


def write_csv(lst):
    """
    lst -> None
    Writing csv file for statistic data
    >>> write_csv(["John"])

    """
    with open("statistic_Horror.csv", "w+", encoding="utf-8") as out_file:
        for tpl in lst:
            line = str(tpl[0]) + "," + str(tpl[1]) + "\n"
            out_file.write(line)


def main():
    """
    The main function of the module.
    Calls for input genre to user
    Than calls read_data().
    Searching the most popular name in dct that was returned by read_data()
    And writes file by f

    """
    # User greeting
    print("Starting program...")

    # User could choose one genre from this genres
    print("""
    Genres: Short         Action      Crime       Sport
            Drama         Romance     Adventure   History
            Comedy        Music       Fantasy     Musical
            Documentary   Animation   Sci-Fi      War
            Adult         Horror      Mystery     Reality-TV
            Thriller      Family      Biography   Western
                                                            """)
    # Variable for Animation loading
    global done
    done = False
    genres_lst = ["Short", "Drama", "Comedy", "Documentary", "Adult",
                  "Thriller", "Action", "Romance", "Music", "Animation",
                  "Horror", "Family", "Crime", "Adventure", "Fantasy",
                  "Sci-Fi", "Mystery", "Biography", "History", "Sport",
                  "Musical", "War", "Reality-TV", "Western"]

    inputted_genre = input("Please input genre: ")
    ch = True
    while ch:
        if inputted_genre not in genres_lst:
            inputted_genre = input("Please input genre: ")
        else:
            ch = False
    # Animation part start
    t1 = time.time()
    t = threading.Thread(target=animate)
    t.start()
    names_lst = starter_prog(inputted_genre)
    done = True
    print("\n")
    # Animation part ended
    # Inputting amount of names
    names_amount = input("Please input amount of names less 50: ")
    ch = True
    while ch:
        if not names_amount.isdigit():
            names_amount = input("Please input valid number: ")
        else:
            if int(names_amount) > 50:
                names_amount = input("Please input valid number: ")
            else:
                ch = False
    # Printing names
    for tpl in names_lst[:int(names_amount)]:
        line = str(tpl[0]) + " : " + str(tpl[1]) + " times"
        print(line)
    t2 = time.time()
    print(t2 - t1)


if __name__ == "__main__":
    main()
