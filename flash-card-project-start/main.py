from tkinter import *
import random
import pandas
from pandas.core.interchange.dataframe_protocol import DataFrame

BACKGROUND_COLOR = "#B1DDC6"
ORIGINAL_DATA_PATH = "data/french_words.csv"
WORDS_TO_LEARN_PATH = "data/words_to_learn.csv"
word = {}
timer = None



# ------------------------- Data Preparation ------------------------------
def read_data():
    """
    read the word list from the appropriate data file
    :return: a list of dictionary entries containing a French word and its
            English equivalent
    """
    try:
        word_list = pandas.read_csv(WORDS_TO_LEARN_PATH)
    except FileNotFoundError:
        word_list = pandas.read_csv(ORIGINAL_DATA_PATH)
        # write entire list to the new CSV file
        word_list.to_csv(WORDS_TO_LEARN_PATH, index=False)

    # without orient="records", would be structured like this:
    # {"French": {0: "French word 1", 1: "French word 2", ... }, "English": {... } }
    return word_list.to_dict(orient="records")


def remove_word():
    """
    removes a word from the list and write the updated list to a file
    """
    # remove word from dictionary
    item_to_remove = [item for (_, item) in enumerate(word_dict) if item["French"] == language_word]
    # item_to_remove is a list of one item containing a dictionary
    print(item_to_remove)
    print(type(item_to_remove))

    # only remove the word and update words_to_learn.csv it the
    # word to remove was found
    if len(item_to_remove) > 0:
        word_dict.remove(item_to_remove[0])

        # convert the dictionary to a DataFrame
        data_set = pandas.DataFrame(word_dict)

        # write the DataFrame to a CSV file
        data_set.to_csv(WORDS_TO_LEARN_PATH, index=False)

    # display the next French word
    next_card()


# ------------------------- User Interface Functions ------------------------------------
word_dict = read_data()
print(word_dict)
language_word = ""

def flip_card():
    global  language_word
    """
    flip the flash card from the French side to the English side
    """
    language_word = word["English"]

    flash_card.itemconfig(card_background, image=card_back)
    flash_card.itemconfig(language_text, text="English", fill="white")
    flash_card.itemconfig(word_text, text=language_word, fill="white")


def next_card():
    """
    prepare the next French word to be displayed as a flash card
    """
    global word, timer, language_word

    # cancel the timer in case the user clicked either button before the card was flipped
    if timer is not None:
        window.after_cancel(timer)

    random_index = random.Random()
    word = random_index.choice(word_dict)

    # get the key name and word so the canvas objects can be refreshed
    language_word = word["French"]
    # language_name = [key for key, val in word.items() if val == language_word]

    flash_card.itemconfig(card_background, image=card_front)
    flash_card.itemconfig(language_text, text="French", fill="black")
    flash_card.itemconfig(word_text, text=language_word, fill="black")

    # set a timer to flip the card after 3 seconds
    timer = window.after(3000, flip_card)


# ------------------------- User Interface Setup --------------------------
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")

# flash card
flash_card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_background = flash_card.create_image(400, 263, image=card_front)
language_text = flash_card.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
word_text = flash_card.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
flash_card.grid(column=0, row=0, columnspan=2)

# x button
x_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=x_image, highlightthickness=0,
                        bg=BACKGROUND_COLOR, borderwidth=0, command=next_card)
unknown_button.grid(column=0, row=1)

# check button
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0,
                      bg=BACKGROUND_COLOR, borderwidth=0, command=remove_word)
known_button.grid(column=1, row=1)

next_card()
window.mainloop()
