from tkinter import Tk, Entry, Label, Button, Canvas, PhotoImage, filedialog, simpledialog
from visualization import visualize_and_save
from show_data_excel import show_data

root = Tk()
root.title("Real Estate Index UI")
canvas = Canvas(root, width=300, height=200)
canvas.grid()

success_label = Label(root, text="")
success_label.grid(row=2, column=0, columnspan=2)

insert_button = Button(root, text="Show data", command= show_data)
insert_button.grid(row=0, column=0, padx=(0, 10), pady=10)

def visualize_and_update_label():
    message = visualize_and_save(success_label)
    success_label.config(text=message)

display_button = Button(root, text="Visualize and save data", command= visualize_and_update_label)
display_button.grid(row=1, column=0, padx=(0,10), pady=10)

root.mainloop()