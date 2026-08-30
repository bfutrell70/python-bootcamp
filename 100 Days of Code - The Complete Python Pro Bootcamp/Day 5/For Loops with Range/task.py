# starts at first number, goes up to the second number without including it in the results
# will print 1 through 9
# for number in range(1, 11):
#     print(number)
#
# print("--- range with step ---")
# for number in range(1, 10, 2):
#     print(number)

# Gauss challenge
number_sum = 0
for number in range(1, 101):
    number_sum += number
print(number_sum)