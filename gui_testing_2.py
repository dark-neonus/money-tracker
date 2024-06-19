import tkinter as tk
from tkinter import filedialog, Menu
import json
import os
from datetime import datetime


def write_to_file(path: os.path, content) -> None:
    with open(path, "w") as file:
        json.dump(content, file, indent="\t")

def create_journal():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json", 
        filetypes=[("JSON files", "*.json")],
        title="Create Journal"
    )
    
    if file_path:
        if not file_path.endswith(".json"):
            file_path += ".json"

        file_name_with_extension = os.path.basename(file_path)
        file_name, _ = os.path.splitext(file_name_with_extension)
        
        journal_content = {
            "title": file_name,
            "description": "Journal created on " + datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "entries": []
        }
        
        write_to_file(file_path, journal_content)
        
        print(f"Journal '{file_name}' created at {file_path}")

def open_journal():
    file_path = filedialog.askopenfilename(
        defaultextension=".json", 
        filetypes=[("JSON files", "*.json")],
        title="Open Journal"
    )
    
    if file_path:
        with open(file_path, 'r') as file:
            journal_content = json.load(file)
        
        print(f"Journal loaded from {file_path}")
        print("Journal content:", json.dumps(journal_content, indent=4))

        # You can also display the content in a Tkinter widget
        # Here is an example of displaying it in a Text widget
        text_widget.delete('1.0', tk.END)  # Clear previous content
        text_widget.insert(tk.END, json.dumps(journal_content, indent=4))

# Initialize the Tkinter window
root = tk.Tk()
root.title("Journal App")

# Create a Text widget to display journal content
text_widget = tk.Text(root, wrap='word', width=80, height=20)
text_widget.pack(padx=10, pady=10)

# Create a menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create a 'File' menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add 'Create Journal' option to the 'File' menu
file_menu.add_command(label="Create Journal", command=create_journal)

# Add 'Open Journal' option to the 'File' menu
file_menu.add_command(label="Open Journal", command=open_journal)

# Run the Tkinter event loop
root.mainloop()
