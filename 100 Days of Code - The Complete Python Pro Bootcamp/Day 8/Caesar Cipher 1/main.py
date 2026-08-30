alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))


# TODO-1: Create a function called 'encrypt()' that takes 'original_text' and 'shift_amount' as 2 inputs.
def encrypt(original_text, shift_amount):
    # TODO-2: Inside the 'encrypt()' function, shift each letter of the 'original_text' forwards in the alphabet
    #  by the shift amount and print the encrypted text.
    cipher_text = ""

    for letter in original_text:
        if letter in alphabet:
            original_index = alphabet.index(letter)
            index = original_index + shift_amount

            # TODO-4: What happens if you try to shift z forwards by 9? Can you fix the code?
            # check if the index is greater than the last index value of the alphabet list
            # if it is the subtract the length of the alphabet list from the index

            # Angela used Modulo - doesn't need if statement to check if the index is greater than
            # the length of the alphabet list
            index %= len(alphabet)

            # my code
            #if index > (len(alphabet) - 1):
            #    index -= len(alphabet)

            cipher_text += alphabet[index]
        else:
            cipher_text += letter

    print(f"Here is the encoded result: {cipher_text}")

# TODO-3: Call the 'encrypt()' function and pass in the user inputs. You should be able to test the code and encrypt a
#  message.

encrypt(original_text = text, shift_amount = shift)
