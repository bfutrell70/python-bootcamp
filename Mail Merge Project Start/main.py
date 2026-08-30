# TODO: Create a letter using starting_letter.txt
# for each name in invited_names.txt
# Replace the [name] placeholder with the actual name.
# Save the letters in the folder "ReadyToSend".

# Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp

# Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp

# Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

LETTER_PATH = "Input/Letters/starting_letter.txt"
NAMES_PATH = "Input/Names/invited_names.txt"
OUTPUT_PATH = "Output/ReadyToSend/"
PLACEHOLDER = "[name]"

# open the file with the list of names
with open(NAMES_PATH) as names:
    # read the names from the file as a list

    # iterating through the list of names and stripping the
    #  newline character from each one before assigning the result
    # to a list
    names_list = names.readlines()

# open the source letter file
with open(LETTER_PATH) as letter:
    # read the contents of the letter
    letter_contents = letter.read()

# loop through the names in the list
for name in names_list:
    # strip the newline character from the end of the name
    name = name.strip("\n")

    # replace the text '[name]' in the letter with the name from the list
    personalized_letter = letter_contents.replace(PLACEHOLDER, name)

    # build the output path with the filename
    personalized_letter_path = f"{OUTPUT_PATH}letter_for_{name}.txt"

    # open the file in write mode and write the personalized letter
    # to the file
    with open(personalized_letter_path, mode="w") as output:
        output.write(personalized_letter)
