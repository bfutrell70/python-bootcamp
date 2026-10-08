# # functions inputs/functionality/output
# def add(n1, n2):
#     return n1 + n2
#
# def subtract(n1, n2):
#     return n1 - n2
#
# def multiply(n1, n2):
#     return n1 * n2
#
# def divide(n1, n2):
#     return n1 / n2
#
# # first-class objects, can be passed around as arguments e.g.
# # int/string/float/etc.
# def calculate(calc_function, n1, n2):
#     return calc_function(n1, n2)
#
#
# result = calculate(add, 2, 3)
# print(result)
#
# # nested functions
def outer_function():
    print("I'm the outer function")

    # only accessible from outer_function
    def nested_function():
        print("\tI'm the inner function")

    # can return function
    return nested_function

# functions can be returned from other functions
inner_function = outer_function()
inner_function()