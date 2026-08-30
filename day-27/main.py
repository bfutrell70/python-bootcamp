import tkinter

window = tkinter.Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)

# adds padding around all widgets
window.config(padx=20, pady=20)

def button_clicked():
    #print("I got clicked")
    text = entry.get()
    my_label["text"] = text


# pack is difficult to place an item precisely
# place is precise placing
# grid is similar to Bootstrap
#       can specify a row and column
#       how to specify number of rows and columns
#       can't use grid and pack together

# components

# label
# 1 - define component
my_label = tkinter.Label(text="I am a label", font=("Arial", 24, "italic"))
# 2 - place on window (defaults to top of window and centered)
my_label["text"] = "New Text"
my_label.config(text="New Text")
# my_label.pack()
# my_label.place(x=100, y=200)
my_label.grid(column=0, row=0)
# can pad individual widgets
my_label.config(padx=0, pady=50)

# Button
button = tkinter.Button(text="Click Me", command=button_clicked)
# button.pack()
button.grid(column=1, row=1)

# Entry
entry = tkinter.Entry(width=10)
# input.pack()
entry.grid(column=3, row = 2)
# get contents of input field
# input.get()

new_button = tkinter.Button(text="Click Me Too!", command=button_clicked)
new_button.grid(column=2, row=0)

# must be the last line in the program
window.mainloop()

