import tkinter as tk

window = tk.Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)

# label
my_label = tk.Label(text="Hello World", font=("Arial", 24, "bold"))
my_label.pack() # adds the label to the top center of the window

# entry
input = tk.Entry(width=10)
input.insert(tk.END, string="Some text to begin with.")
input.pack()

# button
def button_clicked():
    my_label.config(text=input.get())
    
button = tk.Button(text="Click Me", command=button_clicked)
button.pack()

# text
text = tk.Text(height=5, width=30)
text.focus()
text.insert(tk.END,"Example of multi-line text entry.")
# get current value in textbox at line 1, character 0
print(text.get("1.0", tk.END))
text.pack()

# spinbox
def spinbox_used():
    # get current value in spinbox
    print(spinbox.get())
spinbox = tk.Spinbox(from_=1, to=10, command=spinbox_used)
spinbox.pack()

# scale
def scale_used(value):
    print(value)
scale = tk.Scale(from_=1, to=100, command=scale_used)
scale.pack()

# checkbutton
def checkbutton_used():
    # print 1 if checkbox is checked, otherwise print 0
    print(checked_state.get())
# IntVar() is used to store integer values
checked_state = tk.BooleanVar()
checkbutton = tk.Checkbutton(text="Is On?", variable=checked_state, command=checkbutton_used)
checkbutton.pack()

# radio button
def radio_used():
    print(radio_state.get())
radio_state = tk.IntVar()
radio1 = tk.Radiobutton(text="Option1", value=1, variable=radio_state, command=radio_used)
radio2 = tk.Radiobutton(text="Option2", value=2, variable=radio_state, command=radio_used)
radio1.pack()
radio2.pack()

# listbox
def listbox_used(event):
    # get current selection from listbox
    print(listbox.get(listbox.curselection()))
listbox = tk.Listbox(height=4)
fruits = ["Apple", "Pear", "Orange", "Banana"]
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.pack()

# canvas
canvas = tk.Canvas(width=200, height=200)
canvas.create_line(0, 0, 200, 200, fill="red")
canvas.create_oval(100, 100, 200, 200, fill="blue")
canvas.create_rectangle(200, 200, 300, 300, fill="green")
canvas.pack()

window.mainloop()
