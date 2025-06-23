from turtle import Turtle, Screen
import pandas as pd

screen = Screen()
screen.title("U.S. States Game")
screen.setup(width=725, height=491)
image = "blank_states_img.gif"
screen.addshape(image)
t = Turtle()
t.shape(image)

data = pd.read_csv("50_states.csv")
writer = Turtle()
writer.penup()
writer.hideturtle()

guessed_states = []
states_to_learn = []
while len(guessed_states) < 50:
    input_state = screen.textinput(title=f"{len(guessed_states)}/50 Guess the State", prompt="What's another state's name? Type 'exit' to finish the game.")
    if input_state.title() == "Exit":
        for state in data.state.values:
            if state not in guessed_states:
                states_to_learn.append(state)
        pd.DataFrame(states_to_learn).to_csv("states_to_learn.csv")
        break

    if input_state.title() in data.state.values:
        writer.goto(data[data.state == input_state.title()].x.item(), data[data.state == input_state.title()].y.item())
        writer.write(input_state.title())
        guessed_states.append(input_state.title())

screen.exitonclick()


# def get_mouse_click_coor(x, y):
#     print(x, y)

# screen.onscreenclick(get_mouse_click_coor)

# screen.mainloop()