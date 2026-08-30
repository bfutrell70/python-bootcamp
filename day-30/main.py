# # FileNotFoundError
# try:
#     file = open("a_file.txt")
#     a_dictionary = {"key": "value"}
#     print(a_dictionary["23432423"])
# except FileNotFoundError:
#     file = open("a_file.txt", "w")
#     file.write("Something")
# except TypeError as error_message:
#     print(f"The key {error_message} does not exist.")
# else:
#     # no exceptions occurred.
#     content = file.read()
#     print(content)
# finally:
#     file.close()
#     print("File was closed.")
#
#     # manually raise an error
#     raise KeyError("Just testing...")
#
# # KeyError
# # a_dictionary = { "key": "value"}
# # value = a_dictionary["non_existent_key"]
#
# # IndexError
# # fruit_list = ["Apple", "Banana", "Pear"]
# # fruit = fruit_list[3]
#
# # TypeError
# # text = 'abc'
# # print(text + 5)
#

# should not be over 3 meters
height = float(input("Height: "))
weight = int(input("Weight: "))

if height > 3:
    raise ValueError("Human height should not be over 3 meters.")

bmi = weight / height ** 2
print(bmi)