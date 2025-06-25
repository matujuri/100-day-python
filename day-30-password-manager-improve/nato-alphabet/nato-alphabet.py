import pandas as pd
dataframe = pd.read_csv("nato_phonetic_alphabet.csv")
nato_dict = {row.letter:row.code for (index, row) in dataframe.iterrows()}

input_word = input("Enter a word: ").upper()
try:
    output_list = [nato_dict[letter] for letter in input_word]
except KeyError:
    print("Sorry, only letters in the alphabet please.")
else:
    print(output_list)