# new_list = [new_item for item in list if test]

numbers = [1, 2, 3, 4, 5]
new_numbers = [n % 2 for n in numbers]
print(new_numbers)

name = "lijingjing"
letters = [letter for letter in name]
print(letters)

numbers = [n for n in range(1,100) if n % 7 == 0]
print(len(numbers))

names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]
short_names = [name for name in names if len(name) < 5]
print(short_names)

long_names = [name.upper() for name in names if len(name) > 5]
print(long_names)

# new_dict = {new_key:new_value for item in list if test}
# new_dict = {new_key:new_value for (key, value) in dict.items() if test}
import random
names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]
scores = {name:random.randint(1, 100) for name in names}
print(scores)

passed_students = {student:score for (student, score) in scores.items() if score >= 60}
print(passed_students)

# iterrows
student_dict = {
    "student": ["Angela", "James", "Lily"],
    "score": [56, 76, 98]
}

import pandas as pd
student_data_frame = pd.DataFrame(student_dict)
print(student_data_frame)

# for (key, value) in student_data_frame.items():
#     print(value)
    
for (index,row) in student_data_frame.iterrows():
    if row.student == "Lily":
        print(row.score)