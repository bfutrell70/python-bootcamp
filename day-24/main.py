# file = open('my_file.txt')
#
# contents = file.read()
# print(contents)
#
# file.close()

# same as the above file
# with open('my_file.txt') as file:
#     contents = file.read()
#     print(contents)


# # 'w' overwrites the contents of the file
# with open('my_file.txt', mode='w') as file:
#     contents = file.write('New Text.')
#     print(contents)
#
# with open('my_file.txt', mode='a') as file:
#     contents = file.write('\nMore Text.')
#     print(contents)

# # if file doesn't exist in write mode, will create a new file
# with open('new_file.txt', mode='w') as file:
#     contents = file.write('New Text.')
#     print(contents)

# with open('C:/Users/wfutr/OneDrive/Desktop/my_file.txt') as file:
#     contents = file.read()
#     print(contents)

with open('../../my_file.txt') as file:
    contents = file.read()
    print(contents)