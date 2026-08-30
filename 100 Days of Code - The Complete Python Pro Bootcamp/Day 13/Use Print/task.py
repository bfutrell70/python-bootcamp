#word_per_page = 0
pages = int(input("Number of pages: "))

print("after pages input")

word_per_page = int(input("Number of words per page: "))

print(f"word_per_page: {word_per_page}")

total_words = pages * word_per_page
print(f"Total words: {total_words}")
