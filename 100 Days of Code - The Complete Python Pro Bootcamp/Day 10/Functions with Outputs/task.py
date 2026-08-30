def format_name(f_name, l_name):
    formatted_f_name = f_name.title()
    formatted_l_name = l_name.title()
    return f"{formatted_f_name} {formatted_l_name}"


#print(format_name("brian", "futrell"))
print(format_name("bRiaN", "FUTRELL"))

def function_1(text):
    return text + text

def function_2(text: str):
    return text.title()

output = function_2(function_1("hello"))
print(output)