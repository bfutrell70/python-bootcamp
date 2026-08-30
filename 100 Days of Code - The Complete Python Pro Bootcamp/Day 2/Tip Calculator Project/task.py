print("Welcome to the tip calculator!")
bill = float(input("What was the total bill? $"))
tip = int(input("What percentage tip would you like to give?\n(Enter as a whole number) :"))
people = int(input("How many people to split the bill? "))

to_pay_per_person = (bill / people) * (1 + (tip/100))

print(f"Amount to pay per person: ${to_pay_per_person:.2f}")

# given inputs of 150, 12, and 5, the number shown in the code below is '33.6'
# print(f"Amount to pay per person: ${round(to_pay_per_person, 2)}")
