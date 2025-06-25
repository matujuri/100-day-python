from tkinter import Tk, Label, Button, Entry, Canvas, PhotoImage, END
import random
import string
import json

symbols = "!#$%&()*+"
file_path = "data.json"     

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_list = random.choices(string.ascii_letters, k=random.randint(8, 10))
    password_list += random.choices(string.digits, k=random.randint(2, 4))
    password_list += random.choices(symbols, k=random.randint(2, 4))
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    password_entry.clipboard_clear()
    password_entry.clipboard_append(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email" : email,
            "password" : password
        }
    }

    warning_label.config(text="")
    if len(website) == 0 or len(password) == 0:
        warning_label.config(text="Please don't leave any fields empty!", fg="red")
        return
    
    # Clear the entries
    website_entry.delete(0, END)
    password_entry.delete(0, END) 

    # Update the data.json file
    try:
        with open(file_path, "r") as data_file:
            data = json.load(data_file) # load the data from the file
    except FileNotFoundError: # if the file does not exist, create it
        with open(file_path, "w") as data_file:
            json.dump(new_data, data_file, indent=4)
    else: # if the file exists, update it
        data.update(new_data) # update the data with the new data
        with open(file_path, "w") as data_file:
            json.dump(data, data_file, indent=4)
    finally:
        website_entry.focus()

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open(file_path, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        warning_label.config(text="No data file found.", fg="red")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            email_entry.delete(0, END)
            email_entry.insert(0, email)
            password_entry.delete(0, END)
            password_entry.insert(0, password)
        else:
            warning_label.config(text="No details for the website exists.", fg="red")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.grid_columnconfigure(1, weight=1)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=0, row=0, columnspan=3)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

website_entry = Entry()
website_entry.grid(column=1, row=1, sticky="ew")
website_entry.focus()

search_button = Button(text="Search", width=12, command=find_password)
search_button.grid(column=2, row=1, sticky="e", padx=(0,0))

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "test@test.com")

password_entry = Entry()
password_entry.grid(column=1, row=3, sticky="ew")

generate_password_button = Button(text="Generate Password", width=12, command=generate_password)
generate_password_button.grid(column=2, row=3, sticky="e", padx=(0,0))

add_button = Button(text="Add", width=32, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

warning_label = Label(text="", fg="red")
warning_label.grid(column=1, row=5, columnspan=2)

window.mainloop()   