# # import another_module
# # print(another_module.another_variable)
#
# from turtle import Turtle, Screen
#
# # Turtle is a class, timmy is an object
# timmy = Turtle()
# print(timmy)
# timmy.shape("turtle")
# timmy.color("cyan2")
# timmy.forward(100)
# my_screen = Screen()
# print(my_screen.canvheight)
#
# # will keep the program running until it is clicked
# my_screen.exitonclick()

from prettytable import PrettyTable
table = PrettyTable()
# table.align = "l"
# it appears columns default to center alignment
table.add_column(fieldname="Pokemon Name", column= ['Pikachu', 'Squirtle', 'Caramander'])
table.add_column(fieldname="Type", column= ['Electric', 'Water', 'Fire'])
# if table alignment is done _after_ columns are added, it overrides the column's alignment
table.align = "l"
print(table.align)
print(table)


