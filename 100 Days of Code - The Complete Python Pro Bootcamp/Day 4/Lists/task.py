fruits = ["Cherry", "Apple", "Pear"]

states_of_america = ["Delaware", "Pennsylvania", "New Jersey", "Georgia", "Connecticut",
                     "Massachusetts", "Maryland", "South Carolina", "New Hampshire", "Virginia",
                     "New York", "North Carolina", "Rhode Island", "Vermont", "Kentucky",
                     "Tennessee", "Ohio", "Louisiana", "Indiana", "Mississippi", "Illinois",
                     "Alabama", "Maine", "Missouri", "Arkansas", "Michigan", "Florida",
                     "Texas", "Iowa", "Wisconsin", "California", "Minnesota", "Oregon",
                     "Kansas", "West Virginia", "Nevada", "Nebraska", "Colorado",
                     "North Dakota", "South Dakota", "Montana", "Washington", "Idaho", "Wyoming",
                     "Utah", "Oklahoma", "New Mexico", "Arizona", "Alaska", "Hawaii"]

print(states_of_america[-4])
print(states_of_america[1])

fruits[1] = "orange"
print(fruits[1])

fruits.append("Dragonfruit")
print(fruits)

states_of_america.extend(["Brianland", "Canada"])
print(states_of_america)