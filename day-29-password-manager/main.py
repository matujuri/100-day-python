from tkinter import Tk, Label, Button, Entry, Canvas, PhotoImage, END, messagebox

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
        return
    
    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} \nPassword: {password} \nIs it ok to save?")
    
    if is_ok:
        # Clear the entries
        website_entry.delete(0, END)
        password_entry.delete(0, END) 

        # Save the data to a CSV file
        with open("data.csv", "a") as data_file:
            data_file.write(f"{website},{email},{password}\n")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
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

website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, columnspan=2)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "test@test.com")

password_entry = Entry()
password_entry.grid(column=1, row=3, sticky="ew")

generate_password_button = Button(text="Generate Password", width=12)
generate_password_button.grid(column=1, row=3, sticky="e", padx=(0,0))

add_button = Button(text="Add", width=32, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()   