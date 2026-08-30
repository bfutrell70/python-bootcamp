from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    password_list += [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)

    # clear existing password and set it to the newly generated password
    password_entry.delete(0, END)
    password_entry.insert(0, password)

    # copy the password to the clipboard
    pyperclip.copy(password)

# ----------------------------- FIND PASSWORD -------------------------------------
# search for the website in the JSON data,
# display the results in a popup
def find_password():
    # get the website from the website_entry widget
    website = website_entry.get()

    try:
        # open JSON file
        with open('data.json', 'r') as data_file:
            # read data into a Python dictionary
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found")
    else:
        # search for website key
        if website in data:
            # if found display a popup
            # - website is the title
            # - email and password are displayed as the message
            message_to_display = f"Email: {data[website]["email"]} \nPassword: {data[website]["password"]}"
            messagebox.showinfo(title=website, message=message_to_display)
        else:
            # website was not found - inform the user
            messagebox.showwarning(title="Error", message=f"No details for {website} exist.")



# ---------------------------- SAVE PASSWORD ------------------------------- #
# take data from website entry, email entry, and password entry and write it to a file
# in JSON format
def save_data():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Validation error", message="Please enter data for all fields.")
    else:
        new_data = {
            website: {
                "email": email,
                "password": password
            }
        }

        # FileNotFoundError occurs if a non-existent file is opened for reading
        try:
            with open('data.json', 'r') as data_file:
                # read old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # updating old data with new data
            # if the key exists, will update the existing data for the key
            data.update(new_data)

            with open('data.json', 'w') as data_file:
                # saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            # clear all fields except for email
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# --- row 0
# logo image
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# --- row 1
# website label
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

# website entry
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1, sticky="w")
# sets the focus to the website entry
website_entry.focus()

# search button
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="ew")

# --- row 2
# email/username label
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

# email/username entry
email_entry = Entry()
email_entry.grid(column=1, row=2, columnspan=2, sticky="ew")
email_entry.insert(index=0, string="bfutrel@gmail.com")

# --- row 3
# password label
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# password entry
password_entry = Entry(width=21, show="*")
password_entry.grid(column=1, row=3, sticky="w")

# generate password button
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

# add button
add_button = Button(text="Add", width=36, command=save_data)
add_button.grid(column=1, row=4, columnspan=2, sticky="ew")

window.mainloop()