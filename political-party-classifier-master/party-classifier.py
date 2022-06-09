import math


# Lyndsey Brandon
# Travis Parks

# http://www.opentextbooks.org.hk/ditatopic/6731
# Travis Parks wrote the file_test function.
def file_test(file):
    try:
        file = open(file)
        file = file.close()
    except:
        return False
    return True

# Lyndsey Brandon wrote the initial phase_menu function.
# Travis Parks edited the function with user input for the file,
# calling the appropriate function, and added validation.
def phase_menu():
    fname = input('What file would you like to edit? ')

    if ".txt" not in fname:
        fname = fname + ".txt"

    is_valid = file_test(fname)

    if is_valid:

        print("Which phase would you like to run?")
        print("1. Phase 1: Clean (the Document).")
        print("2. Phase 2: Parse (the Document) for Tokens and Frequencies.")
        print("3. Phase 3: Classify (the Document).")

        menu_choice = input()

        if (menu_choice == '1'):
            print("Cleaning the document...")
            write_file(fname)
            print("Look for 'cleanedfile.txt' in your directory.")
        elif (menu_choice == '2'):
            print("Parsing the document...")
            d_file(fname)
        elif (menu_choice == '3'):
            print("Classifying the document...")
            Classify.con_dict(Classify, fname, 'legendD.txt', 'legendR.txt')
        else:
            print("You didn't make a choice!")
    else:
        print(fname, " is not a valid filename.")
        phase_menu()

# https://www.pythontutorial.net/python-basics/python-read-text-file/
# https://stackoverflow.com/questions/16922214/reading-a-text-file-and-splitting-it-into-single-words-in-python

# write_file function initially written as two separate functions by
# Lyndsey Brandon. Takes in user-defined text file, makes everything lowercase,
# parses each word onto its own line, then cleans the file.
# Travis Parks properly spliced the two functions together.
def write_file(file):
    with open(file, 'r') as f, open('cleanedfile.txt', 'w') as fout:
        for line in f:
            line = line.lower()
            for word in line.split():
                fout.writelines(word + '\n')
    with open('cleanedfile.txt', 'r') as f:
        data = f.read()
    with open('cleanedfile.txt', 'w+') as f:
        f.write(remove_punc(data))

# Basically the same thing that was given to us...Like, exactly.
# When read, files become strings so this works without error when
# called in the correct place.
# "Written" by Lyndsey Brandon.
# https://www.pythonpool.com/remove-punctuation-python/#How_to_Remove_Punctuation_From_a_File_in_Python
def remove_punc(string):
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in string:
        if ele in punc:
            string = string.replace(ele, "")
    return string

# Lyndsey Brandon wrote this just because phase 2 didn't do anything.
# All it does is do the same thing as con_dict but it just
# makes an (unused) dictionary for the file being tested.
def d_file(fname):
    file_dict = {}
    with open(fname, 'r') as f:
        for line in f:
            for word in line.split():
                if word in file_dict:
                    file_dict[word].a = file_dict[word].a + 1
                else:
                    i = Token(word)
                    file_dict[word] = i
    
    for (key, value) in file_dict.items:
        print(key, value)

# Travis Parks wrote the Token class and magic methods.
# Holds the number of times words will appear in either class of speech.
class Token:

    def __init__(self, word):
        self.word = word
        self.a = 1
        self.b = 1

    def __str__(self):
        return self.word + ", " + str(self.a) + ", " + str(self.b)

# Travis Parks initially compiled everything into the class and
# added the Token counting to the con_dict function.
# Lyndsey Brandon wrote the con_dict function, and
# the classify_party function.
class Classify:

    # Makes the frequency table from two "legends" that supply
    # speeches that are known to be democrat or republican in nature.
    def con_dict(self, fname, dem_legend, repub_legend):
        d = {}
        with open(dem_legend, 'r') as f:
            for line in f:
                for file in line.split():
                    with open(file, 'r') as f3:
                        for line2 in f3:
                            for word in line2.split():
                                if word in d:
                                    d[word].a = d[word].a + 1
                                else:
                                    i = Token(word)
                                    d[word] = i

        with open(repub_legend, 'r') as f:
            for line in f:
                for file in line.split():
                    with open(file, 'r') as f3:
                        for line in f3:
                            for word in line.split():
                                if word in d:
                                    d[word].b = d[word].b + 1
                                else:
                                    i = Token(word)
                                    d[word] = i

        # EXTRA CREDIT, removes the stop words.
        with open('stopwords.txt', 'r') as f:
            for line in f:
                for word in line.split():
                    if word in d:
                        d.pop(word)

        # All this does is place the training dictionary in "diction_file.txt"
        # if you want to manually look at it.
        with open("diction_file.txt", 'w') as f:
            for key, value in d.items():
                f.write('%s:%s\n' % (key, value))

        # Prints the frequency table.
        for key, value in d.items():
            print(key, value)

        # I had some difficulty with placing this, so I found it easier to
        # call it within this function!
        self.classify_party(fname, d)

    # Takes another count to test whether or not the provided
    # test speech is dem or repub. Formatted to two decimal places.
    def classify_party(test_file, d):
        classA_count = 1
        classB_count = 1

        with open(test_file, 'r') as f:
            for line in f:
                for word in line.split():
                    if word not in d:
                        continue
                    elif word in d:
                        classA_count += math.log(d[word].a)
                        classB_count += math.log(d[word].b)

        if classA_count >= classB_count:
            return print(format(classA_count, '.2f'), "Leans Democrat.")
        else:
            return print(format(classB_count, '.2f'), "Leans Republican.")

# Main function to make everything nice and clean. (:
def main():
    phase_menu()


main()