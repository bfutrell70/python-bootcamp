class User:
    # allows the "indent expected" error to be bypassed
    #pass

    def __init__(self, user_id = "000", username = "test user"):
        # initialize attributes
        # called every time an object is initialized
        self.id = user_id
        self.username = username
        self.followers = 0
        self.following = 0

    def follow(self, user):
        user.followers += 1
        self.following += 1


user1 = User(user_id="001", username="Angela")

# print(user1.id)
# print(user1.username)
# print(user1.followers)
# print(user1)

user2 = User()
# print(user2.id)
# print(user2.username)

user1.follow(user2)

print(user1.followers)
print(user1.following)
print(user2.followers)
print(user2.following)