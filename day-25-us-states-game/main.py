import turtle
import pandas  # type: ignore

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)

# display the image added to the screen object
turtle.shape(image)
turtle.penup()


# # test code - sets up click event handler
# # gets the coordinate of click and prints it
# def get_mouse_click_coor(x, y):
#     print(x, y)

# turtle.onscreenclick(get_mouse_click_coor)
# turtle.mainloop()

# TODO:
# 1 - DONE - Convert the guess to Title case
# 2 - Check if the guess is among the 50 states
# 3 - Write correct guesses onto the map
# 4 - DONE - Use a loop to allow the user to keep guessing
# 5 - Record the correct guesses in a list
# 6 - keep track of the score

score = 0
states_list = pandas.read_csv("50_states.csv")


def check_guess(guess):
    """
    checks the user's guess against the list of states
    if a match was found will return the x and y coordinates
    if a match was not found will return None
    """
    matching_state = states_list[states_list.state == guess]

    if len(matching_state) != 0:
        # Angela used matching_state.x.item()
        x = matching_state.iloc[0].x
        y = matching_state.iloc[0].y
        return x, y
    else:
        return None

keep_playing = True
state_turtle = turtle.Turtle()
state_turtle.penup()
state_turtle.hideturtle()
correct_states = []

while keep_playing:
    answer_state = screen.textinput(
        title=f"States {len(correct_states)}/50", prompt="What's another state's name?"
    )
    if answer_state == "Exit":
        # write states that weren't guessed to a CSV file
        missed_states = [state for state in states_list.state if state not in correct_states]
        new_data = pandas.DataFrame(missed_states)
        new_data.to_csv("states_to_learn.csv")
        # with open("states_to_learn.csv", mode="w") as output:
        #     for index, state in states_list.iterrows():
        #         if state.state not in correct_states:
        #             output.write(f"{state.state}\n")
        break

    if answer_state is not None:
        answer_state = answer_state.title()

        if answer_state in correct_states:

            print(f"{answer_state} was previously guessed and was correct!")

        result = check_guess(answer_state)
        if result is None:
            print(f"'{answer_state}' was not in the list of states")
        else:
            # write the state name to the screen
            state_turtle.goto(result)
            state_turtle.write(answer_state)
            score += 1
            correct_states.append(answer_state)
    else:
        keep_playing = False

    if len(correct_states) == 50:
        keep_playing = False
