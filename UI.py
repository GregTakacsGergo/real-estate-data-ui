from tkinter import Tk, Entry, Label, Button, Canvas, PhotoImage, filedialog, simpledialog
from visualization2 import visualize

root = Tk()
root.title("Real Estate Index UI")
canvas = Canvas(root, width=300, height=200)
canvas.grid()

success_label = Label(root, text="")
success_label.grid(row=2, column=0, columnspan=2)

insert_button = Button(root, text="Show data")
insert_button.grid(row=0, column=0, padx=(0, 10), pady=10)

display_button = Button(root, text="Visualize data", command= visualize)
display_button.grid(row=1, column=0, padx=(0,10), pady=10)

root.mainloop()