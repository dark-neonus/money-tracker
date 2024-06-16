import tkinter as tk
from tkinter import messagebox

def on_new():
    messagebox.showinfo("New", "New File")

def on_open():
    messagebox.showinfo("Open", "Open File")

def on_save():
    messagebox.showinfo("Save", "Save File")

def on_exit():
    root.quit()

def on_cut():
    messagebox.showinfo("Cut", "Cut")

def on_copy():
    messagebox.showinfo("Copy", "Copy")

def on_paste():
    messagebox.showinfo("Paste", "Paste")

def on_preferences():
    messagebox.showinfo("Preferences", "Preferences")

def on_help():
    messagebox.showinfo("Help", "Help")

def on_about():
    messagebox.showinfo("About", "About")

def on_recent_files(file):
    messagebox.showinfo("Recent File", f"Opening {file}")

def on_tools(tool):
    messagebox.showinfo("Tool", f"Using {tool}")

# Create the main application window
root = tk.Tk()
root.title("Tkinter Menu Example with Submenus")
root.geometry("400x300")

# Create the menu bar
menu_bar = tk.Menu(root)

# Create the File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=on_new)
file_menu.add_command(label="Open", command=on_open)

# Create a submenu for Recent Files
recent_files_menu = tk.Menu(file_menu, tearoff=0)
recent_files_menu.add_command(label="File1.txt", command=lambda: on_recent_files("File1.txt"))
recent_files_menu.add_command(label="File2.txt", command=lambda: on_recent_files("File2.txt"))
recent_files_menu.add_command(label="File3.txt", command=lambda: on_recent_files("File3.txt"))
file_menu.add_cascade(label="Recent Files", menu=recent_files_menu)

file_menu.add_command(label="Save", command=on_save)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_exit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create the Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=on_cut)
edit_menu.add_command(label="Copy", command=on_copy)
edit_menu.add_command(label="Paste", command=on_paste)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Create the Preferences menu
preferences_menu = tk.Menu(menu_bar, tearoff=0)
preferences_menu.add_command(label="Preferences", command=on_preferences)

# Create a submenu for Tools
tools_menu = tk.Menu(preferences_menu, tearoff=0)
tools_menu.add_command(label="Tool1", command=lambda: on_tools("Tool1"))
tools_menu.add_command(label="Tool2", command=lambda: on_tools("Tool2"))
tools_menu.add_command(label="Tool3", command=lambda: on_tools("Tool3"))
preferences_menu.add_cascade(label="Tools", menu=tools_menu)

menu_bar.add_cascade(label="Preferences", menu=preferences_menu)

# Create the View menu
view_menu = tk.Menu(menu_bar, tearoff=0)
# You can add more commands or options to the View menu here
menu_bar.add_cascade(label="View", menu=view_menu)

# Create the Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help", command=on_help)
help_menu.add_command(label="About", command=on_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Configure the menu bar
root.config(menu=menu_bar)

# Run the main event loop
root.mainloop()
