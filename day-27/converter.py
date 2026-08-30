import tkinter

MILES_TO_KM = 1.60934

def calculate_kilometers():
    # miles_value = tkinter.DoubleVar()
    # miles_value.set(float(distance_entry.get()) * MILES_TO_KM)
    # kilometer_label.config(text=str(int(miles_value.get())))

    # Angela's code
    # distance_entry.get() returns a string - have to convert to do math on it
    miles = float(distance_entry.get())
    km = miles * MILES_TO_KM
    kilometer_label.config(text=f"{km}")


def key_released(e):
    # print(f"character: [{e.char}]")
    calculate_kilometers()

window = tkinter.Tk()
window.title("Miles to Km Converter")
# window sizes itself to accommodate the widgets placed on it
# window.minsize(width=300, height=200)
window.config(padx=25, pady=25)

# binds pressing the return key in the window to the key_released function
# the function calls the calculate_kilometers() function
window.bind('<Return>', key_released)
# use grid placement

# distance input
distance_entry = tkinter.Entry(width=10)
distance_entry.grid(column=1, row=0)

# miles label
miles_label = tkinter.Label(text="Miles")
miles_label.grid(column=2, row=0)

# 'is equal to' label
is_equal_to_label = tkinter.Label(text="is equal to")
is_equal_to_label.grid(column=0, row=1)

# converted value (km) label
kilometer_label = tkinter.Label(text="0", font=('Arial', 24))
kilometer_label.grid(column=1, row=1)

km_label = tkinter.Label(text="Km")
km_label.grid(column=2, row=1)



calculate_button = tkinter.Button(text="Calculate", command=calculate_kilometers)
calculate_button.grid(column=1, row=2)


# must be the last line in the program
window.mainloop()