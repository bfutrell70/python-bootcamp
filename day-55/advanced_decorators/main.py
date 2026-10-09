## Advanced Python Decorator Functions

class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False

def is_authenticated_decorator(function):
    def wrapper(*args, **kwargs):
        if args[0].is_logged_in == True:
            function(args[0])
    return wrapper

@is_authenticated_decorator
# attempted to specify the user parameter as type User, but it errored when running this file
# I think when specifying the parameter type, the parameter becomes a keyword argument (**kwargs)
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")

new_user = User("Brian")
new_user.is_logged_in = True

create_blog_post(new_user)