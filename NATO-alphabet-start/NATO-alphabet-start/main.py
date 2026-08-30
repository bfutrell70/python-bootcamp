import pandas

# student_dict = {
#     "student": ["Angela", "James", "Lily"],
#     "score": [56, 76, 98]
# }
#
# #Looping through dictionaries:
# for (key, value) in student_dict.items():
#     #Access key and value
#     pass
#
# student_data_frame = pandas.DataFrame(student_dict)
#
# #Loop through rows of a data frame
# for (index, row) in student_data_frame.iterrows():
#     #Access index and row
#     #Access row.student or row.score
#     pass

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

data = pandas.read_csv("nato_phonetic_alphabet.csv")
letter_words = {row.letter: row.code for (index, row) in data.iterrows()}

# TODO: Add error handling to display a message if the word contains numbers
#       Prompt the user to enter the word again until it only has letters.

# my code (then again I haven't done much in the way of recursive functions
# only_letters = False
#
# while not only_letters:
#     word = input("Enter a word: ").upper()
#     try:
#         code_list = [letter_words[letter] for letter in word]
#     except KeyError:
#         print("Only letters in the alphabet please.")
#     else:
#         only_letters = True
#         print(code_list)

# Angela's code - uses a recursive function instead of a while loop.
def generate_phonetic():
    word = input("Enter a word: ").upper()
    try:
        code_list = [letter_words[letter] for letter in word]
    except KeyError:
        print("Only letters in the alphabet please.")
        generate_phonetic()
    else:
        print(code_list)

generate_phonetic()