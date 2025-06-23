with open("./Input/Names/invited_names.txt") as file:
    names = file.readlines()

with open("./Input/Letters/starting_letter.txt") as file:
    letter = file.read()

for name in names:
    new_letter = letter.replace("[name]", name.strip())
    with open(f"./Output/ReadyToSend/letter_for_{name.strip()}.txt", mode="w") as file:
        file.write(new_letter)