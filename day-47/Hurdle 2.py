def turn_right():
    turn_left()
    turn_left()
    turn_left()
    
def turn_around():
    turn_left()
    turn_left()

def jump_hurdle():
    move()
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()
   
#for step in range(6):
#    jump_hurdle()

while not at_goal():
    jump_hurdle()
################################################################
# WARNING: Do not change this comment.
# Library Code is below.
################################################################
