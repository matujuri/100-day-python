from tkinter import Tk, Label, Button, Entry, Canvas, PhotoImage, Frame

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=0)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=0, row=0, columnspan=3)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1, padx=5, pady=5)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2, padx=5, pady=5)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3, padx=5, pady=5)

website_entry = Entry()
website_entry.grid(column=1, row=1, columnspan=2, sticky="ew", padx=5, pady=5)

email_entry = Entry()
email_entry.grid(column=1, row=2, columnspan=2, sticky="ew", padx=5, pady=5)

pw_frame = Frame(window)
pw_frame.grid(column=1, row=3, columnspan=2, sticky="ew", pady=5)
pw_frame.grid_columnconfigure(0, weight=1)

password_entry = Entry(pw_frame)
password_entry.grid(column=0, row=0, sticky="ew")

generate_password_button = Button(pw_frame, text="Generate Password", width=15)
generate_password_button.grid(column=1, row=0, padx=(5, 0))

add_button = Button(text="Add", width=32)
add_button.grid(column=1, row=4, columnspan=2, padx=5, pady=5)

window.mainloop()  