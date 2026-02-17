from tkinter import Tk, Entry, Label, Button, Canvas, PhotoImage, filedialog, simpledialog
from visualization import visualize_and_save
from show_data_excel import show_data
from dynamodb_to_mysql import main as sync_dynamodb

root = Tk()
root.title("Real Estate Index UI")
canvas = Canvas(root, width=300, height=200)
canvas.grid()

success_label = Label(root, text="")
success_label.grid(row=3, column=0, columnspan=2)

insert_button = Button(root, text="Show data", command= show_data)
insert_button.grid(row=0, column=0, padx=(0, 10), pady=10)

def visualize_and_update_label():
    message = visualize_and_save(success_label)
    success_label.config(text=message)

display_button = Button(root, text="Visualize and save data", command= visualize_and_update_label)
display_button.grid(row=1, column=0, padx=(0,10), pady=10)

def sync_and_update_label():
    success_label.config(text="Syncing DynamoDB to MySQL...")
    root.update()  # Force UI update
    success = sync_dynamodb()
    if success:
        success_label.config(text="DynamoDB sync completed successfully!")
    else:
        success_label.config(text="DynamoDB sync failed. Check console for errors.")

sync_button = Button(root, text="Sync DynamoDB to MySQL", command=sync_and_update_label)
sync_button.grid(row=2, column=0, padx=(0,10), pady=10)

root.mainloop()