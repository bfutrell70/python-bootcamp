alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))


# TODO-1: Create a function called 'decrypt()' that takes 'original_text' and 'shift_amount' as inputs.
# TODO-2: Inside the 'decrypt()' function, shift each letter of the 'original_text' *backwards* in the alphabet
#  by the shift amount and print the decrypted text.

def decrypt(original_text, shift_amount):
    cipher_text = ""
    for letter in original_text:
        shifted_position = alphabet.index(letter) - shift_amount

        # Angela's code
        shifted_position %= len(alphabet)
        # my code - didn't get cute with modulo (%) :)
        # if shifted_position is less than 0 add the length of the alphabet to it
        # to wrap the value to the other side of the alphabet
        # if shifted_position < 0:
        #     shifted_position += len(alphabet)
        cipher_text += alphabet[shifted_position]
    print(f"Here is the decoded result: {cipher_text}")

# TODO-3: Combine the 'encrypt()' and 'decrypt()' functions into one function called 'caesar()'.
#  Use the value of the user chosen 'direction' variable to determine which functionality to use.

def caesar(original_text, shift_amount, encode_or_decode):
    cipher_text = ""
    if encode_or_decode == "decode":
        # reverse the sign of shift_amount
        shift_amount *= -1

    for letter in original_text:
        shifted_position = alphabet.index(letter) + shift_amount

        # Angela's code
        shifted_position %= len(alphabet)
        # my code
        # adjust shifted_position to ensure that its value is within
        # the index range of the alphabet list
        # if direction == "encode":
        #     shifted_position %= len(alphabet)
        # else:
        #     if shifted_position < 0:
        #         shifted_position += len(alphabet)

        cipher_text += alphabet[shifted_position]

    print(f"Here is the {encode_or_decode}d result: {cipher_text}")

def encrypt(original_text, shift_amount):
    cipher_text = ""
    for letter in original_text:
        shifted_position = alphabet.index(letter) + shift_amount
        shifted_position %= len(alphabet)
        cipher_text += alphabet[shifted_position]
    print(f"Here is the encoded result: {cipher_text}")


#encrypt(original_text=text, shift_amount=shift)
#decrypt(original_text=text, shift_amount=shift)
caesar(original_text=text, shift_amount=shift, encode_or_decode=direction)


