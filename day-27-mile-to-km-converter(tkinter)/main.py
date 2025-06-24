from tkinter import Tk, Label, Entry, Button

FONT = ("Arial", 24, "bold")

def button_clicked():
    miles = float(input.get())
    km = miles * 1.60934
    km_result_label.config(text=f"{km:.2f}")

window = Tk()
window.title("Miles to Kilometers Converter")
window.config(padx=50, pady=50)

# label
miles_label = Label(text="Miles", font=FONT)
miles_label.grid(column=2, row=0)

equal_label = Label(text="is equal to", font=FONT)
equal_label.grid(column=0, row=1)

km_result_label = Label(text="0", font=FONT)
km_result_label.grid(column=1, row=1)

km_label = Label(text="Km", font=FONT)
km_label.grid(column=2, row=1)

# entry
input = Entry(width=15, font=FONT)
input.grid(column=1, row=0)

# button
button = Button(text="Calculate", command=button_clicked, width=10, font=FONT)
button.grid(column=1, row=2)

window.mainloop()