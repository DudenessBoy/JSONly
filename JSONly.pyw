#   JSONly is a GUI program for interacting with and manipulating JSON files
#     Copyright (C) 2024  Luke Moyer
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import json
import platform
import subprocess
import webbrowser
from plyer import filechooser
import tkinter as tk
import customtkinter as ctk
import JSONly.License
from JSONly.tooltip import Hovertip
from JSONly.image import image
from tkinter import ttk
if platform.system() != 'Linux':
    import pyperclip

# initialize some variables
file = {}# JSON data to be viewed
filename = None # filename to save to
saved = True # whether or not the data has been saved
findWord = ''# string in the find feature
buttons = []

# set the data folder depending on OS
dataDir = os.path.expanduser('~')
match platform.system():
    case'Linux':
        dataDir = os.path.join(dataDir, '.config', 'JSONly')
    case 'Darwin':
        dataDir = os.path.join(dataDir, 'Library', 'Preferences', 'JSONly')
    case 'Windows':
        dataDir = os.path.join(dataDir, 'AppData', 'Local', 'JSONly')

# check for unsaved work before closing the main window
def close() -> None:
    if not saved:
        ans = messagebox('Unsaved Work', 'Would you like to save your changes before loading a new file?', ('Save', 'Don\'t Save', 'Cancel'))
        if ans == 'Cancel':
            return
        elif ans == 'Save':
            if not save():
                return
    root.destroy()

# display messages in a pop-up
def messagebox(title, message, buttons=("OK",), callback=None, geometry = '300x150'):
    # Create a new window
    window = tk.Toplevel()
    window.configure(bg = color)
    window.title(title)
    window.geometry(geometry)
    window.resizable(False, False)

    # Add a message label
    label = ttk.Label(window, text=message, wraplength=250, anchor="center")
    label.pack(padx=20, pady=(20, 10))

    # Create a frame for the buttons
    button_frame = ttk.Frame(window)
    button_frame.pack(pady=10)

    # Callback function for buttons
    def on_button_click(btn_text):
        nonlocal endVal
        if callback:
            callback(btn_text)
        endVal = btn_text
        window.destroy()
    
    endVal = 'closed'

    # Add buttons
    for button_text in buttons:
        button = StyledButton(button_frame, text=button_text, command=lambda bt=button_text: on_button_click(bt), height=30, width = 100)
        button.pack(side=tk.LEFT, padx=5)

    # Center the window on the screen
    window.update_idletasks()

    # Prevent interaction with the main window
    window.transient()
    # window.grab_set()
    window.wait_window()
    return endVal

# load a file from the disk
def load(event = None) -> None:
    global filename, file, saved
    if not saved:
        ans = messagebox('Unsaved Work', 'Would you like to save your changes before loading a new file?', ('Save', 'Don\'t Save', 'Cancel'))
        if ans == 'Cancel':
            return
        elif ans == 'Save':
            if not save():
                return
    filename = filechooser.open_file(title = 'something', filters=[("JSON files", "*.json"), ('All files', '*.*')])
    if filename:
        try:
            with open(filename, 'r', encoding = 'utf-8') as f:
                file = json.load(f)
        except FileNotFoundError:
            messagebox('File Not Found', f'The file "{filename}" could not be found')
            filename = None
            return
        except json.JSONDecodeError:
            messagebox('JSON Decode Error', f'The file "{filename}" contains invalid JSON syntax')
            filename = None
            return
        except EOFError:
            messagebox('EOF Error', f'The file "{filename}" is corrupted')
            filename = None
            return
        except PermissionError:
            messagebox('Permission Denied', f'Permission to read the file "{filename}" could not be obtained')
            filename = None
            return
        except Exception as e:
            messagebox('Error', f'There was an error while attempting to read the file "{filename}": {e}')
            filename = None
            return
        else:
            refresh_listbox(listbox, file)
            saved = True
    else:
        filename = None

# save the file
def save(event = None, saveas: bool = False) -> bool:
    global filename, saved
    if filename is None or saveas:
        filename = filechooser.save_file(filters = [('JSON files', '*.json')])
        if not filename:
            filename = None
            return False
    try:
        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(file, f, indent = 2)
    except PermissionError:
        messagebox('Permission Denied', f'Permission to write to the file "{filename}" could not be obtained')
        filename = None
        return
    except IOError:
        messagebox('I/O Error', f'There was an error while attempting to write to the file "{filename}"')
        filename = None
        return
    except Exception as e:
        messagebox('Error', f'There was an error while attempting to write to the file "{dataFile}": {e}')
        return
    else:
        saved = True
        return True

# edit the value, using a dedicated window
def edit_value(parent, val, typeVar: tk.StringVar, valVar: tk.StringVar, key=None, index=None) -> None:
    def save_value(event = None):
        new_value = value_entry.get()
        if typeVar.get() == 'integer':
            try:
                new_value = int(float(new_value))
            except ValueError:
                new_value = 1
        elif typeVar.get() == 'floating point number':
            try:
                new_value = float(new_value)
            except ValueError:
                new_value = 1.0
        elif typeVar.get() == 'boolean':
            if new_value.lower() != 'true' and new_value.lower() != 'false':
                if new_value == '0' or new_value == '':
                    new_value = 'false'
                else:
                    new_value = 'true'
            new_value = new_value.lower() == 'true'
        elif typeVar.get() == 'null':
            new_value = None

        if key is not None:
            val[key] = new_value
        elif index is not None:
            val[index] = new_value
        
        edit_window.destroy()
        parent.event_generate("<<ValueEdited>>")

    edit_window = tk.Toplevel(parent)
    edit_window.configure(bg = color)
    edit_window.title("Edit Value")
    edit_window.focus()
    # edit_window.grab_set()
    current_row = 0

    ttk.Label(edit_window, text="Type:").grid(row=current_row, column=0, padx=5, pady=5)
    value = str(type(val[key] if index is None else val[index]))
    if 'str' in  value:
        num = 0
    elif 'int' in value:
        num = 1
    elif 'float' in value:
        num = 2
    elif 'bool' in value:
        num = 3
    else:
        num = 4

    typeBox = ctk.CTkOptionMenu(edit_window, variable = typeVar, values=('string', 'integer', 'floating point number', 'boolean', 'null'), fg_color='#646cff', button_color='#646cff', button_hover_color='#4b50d8')
    typeBox.grid(row=current_row, column=1, padx=5, pady=5)
    typeBox.set(typeBox._values[num])
    current_row += 1

    ttk.Label(edit_window, text="Value:").grid(row=current_row, column=0, padx=5, pady=5)
    value_entry = ctk.CTkEntry(edit_window, width = 800, fg_color=color, border_color='#646cff', bg_color=color, text_color = fore)
    value_entry._entry.config(insertbackground=fore)
    value_entry.insert(0, str(val[key]).lower() if index is None else str(val[index]).lower())
    value_entry.select_range(0, tk.END)
    value_entry.focus()
    value_entry.bind('<Return>', save_value)
    value_entry.grid(row=current_row, column=1, padx=5, pady=5)
    current_row += 1

    StyledButton(edit_window, text="Save", command=save_value, cursor = 'hand2', height=30, width = 150)

# edit the value directly from the entry widget
def directEdit(parent, val, typeVar: tk.StringVar, value, key=None, index=None) -> None:
    new_value = value
    if typeVar.get() == 'integer':
        try:
            new_value = int(float(new_value))
        except ValueError:
            new_value = 1
    elif typeVar.get() == 'floating point number':
        try:
            new_value = float(new_value)
        except ValueError:
            new_value = 1.0
    elif typeVar.get() == 'boolean':
        if new_value.lower() != 'true' and new_value.lower() != 'false':
            if new_value == '0' or new_value == '':
                new_value = 'false'
            else:
                new_value = 'true'
        new_value = new_value.lower() == 'true'
    elif typeVar.get() == 'null':
        new_value = None

    if key is not None:
        val[key] = new_value
    elif index is not None:
        val[index] = new_value

# remove an item
def remove_item(parent, val, key=None, index=None) -> None:
    if key is not None:
        del val[key]
    elif index is not None:
        del val[index]
    parent.event_generate("<<ItemRemoved>>")

def configure(event=None) -> None:
    setIndex(listbox)
    if listbox.curselection():
        key = listbox.get(listbox.curselection()[0])
        value = file[key]
        update_value_display(value, typeVar, valVar)
        
        if isinstance(value, (dict, list)):
            view.configure(state='normal', command=lambda: display(value))
            edit.configure(state='disabled')
            valueEntry.configure(state='readonly')
        else:
            view.configure(state='disabled')
            edit.configure(state='normal', command=lambda: edit_value(root, file, typeVar, valVar, key=key))
            valueEntry.configure(state='normal')
        
        remove_button.configure(state='normal')
    else:
        remove_button.configure(state='disabled')

def update_value_display(value, typeVar: tk.StringVar, valVar: tk.StringVar) -> None:
    if value is None:
        valVar.set('null')
        typeVar.set('null')
    elif isinstance(value, list):
        typeVar.set('array')
        valVar.set('(complex value)')
    elif isinstance(value, dict):
        typeVar.set('object')
        valVar.set('(complex value)')
    else:
        valVar.set(str(value))
        if isinstance(value, str):
            typeVar.set('string')
        elif isinstance(value, bool):
            typeVar.set('boolean')
            valVar.set(valVar.get().lower())
        elif isinstance(value, int):
            typeVar.set('integer')
        elif isinstance(value, float):
            typeVar.set('floating point number')

# display the file as JSON plain text
def plainText() -> None:
    win = tk.Toplevel(root)
    win.configure(bg = color)
    win.title('JSONly (plain text)')
    win.focus()
    # win.grab_set()
    text = tk.Text(win, width = 100, height = 20, bg = color, insertbackground = fore, fg = fore)
    text.pack()
    text.insert(0.0, json.dumps(file, indent = 2))
    text.configure(state = 'disabled')
    if platform.system() == 'Linux':
        copy = StyledButton(win, text = 'Copy', cursor = 'hand2', command = lambda: subprocess.run(["xsel", "-b"], input=json.dumps(file, indent = 2).encode('utf-8'), check=True))
    else:
        copy = StyledButton(win, text = 'Copy', cursor = 'hand2', command = lambda: pyperclip.copy(json.dumps(file, indent = 2)))
    copy.pack()

# add a new item to the listbox
def add_new_item(parent, val) -> None:
    def save_item(event = None):
        new_value = value_entry.get()
        if type_var.get() == 'integer':
            try:
                new_value = int(float(new_value))
            except ValueError:
                new_value = 1
        elif type_var.get() == 'floating point number':
            try:
                new_value = float(new_value)
            except ValueError:
                new_value = 1.0
        elif type_var.get() == 'boolean':
            if new_value.lower() != 'true' and new_value.lower() != 'false':
                if new_value == '0' or new_value == '':
                    new_value = 'false'
                else:
                    new_value = 'true'
            new_value = new_value.lower() == 'true'
        elif type_var.get() == 'null':
            new_value = None
        elif type_var.get() == 'array':
            new_value = []
        elif type_var.get() == 'object':
            new_value = {}

        if isinstance(val, dict):
            new_key = key_entry.get().strip()
            if not new_key:
                messagebox("Error", "Key cannot be empty")
                return
            if new_key in val:
                messagebox("Error", "Key already exists")
                return
            val[new_key] = new_value
        elif isinstance(val, list):
            val.append(new_value)
        
        add_window.destroy()
        parent.event_generate("<<ItemAdded>>")

    add_window = tk.Toplevel(parent)
    add_window.geometry('900x150')
    add_window.configure(bg = color)
    add_window.title("Add New Item")
    add_window.focus()
    # add_window.grab_set()

    current_row = 0

    if isinstance(val, dict):
        ttk.Label(add_window, text="Key:").grid(row=current_row, column=0, padx=5, pady=5)
        key_entry = ctk.CTkEntry(add_window, width = 200, fg_color=color, border_color='#646cff', bg_color=color, text_color = fore)
        key_entry._entry.config(insertbackground=fore)
        key_entry.bind('<Return>', lambda e: value_entry.focus())
        key_entry.grid(row=current_row, column=1, padx=5, pady=5)
        key_entry.focus()
        current_row += 1

    ttk.Label(add_window, text="Type:").grid(row=current_row, column=0, padx=5, pady=5)
    type_var = tk.StringVar(value='string')
    ctk.CTkOptionMenu(add_window, variable = type_var, values=['string', 'integer', 'floating point number', 'boolean', 'null', 'array', 'object'], fg_color='#646cff', button_color='#646cff', button_hover_color='#4b50d8').grid(row=current_row, column=1, padx=5, pady=5)
    current_row += 1

    ttk.Label(add_window, text="Value:").grid(row=current_row, column=0, padx=5, pady=5)
    value_entry = ctk.CTkEntry(add_window, width = 800, fg_color=color, border_color='#646cff', bg_color=color, text_color = fore)
    value_entry._entry.config(insertbackground=fore)
    value_entry.bind('<Return>', save_item)
    value_entry.grid(row=current_row, column=1, padx=5, pady=5)
    current_row += 1

    StyledButton(add_window, text="Save", command=save_item, cursor = 'hand2', height=30, width = 150).grid(row=current_row, column=0, columnspan=2, pady=10)

# general preferences
def settings() -> None:
    def configNumLabel(val) -> None:
        number.config(text = int(val))
    def close() -> None:
        data['preferences']['indent'] = int(indent.get())
        extension = ext.get().strip()
        if not extension.startswith('.'):
            extension = '.' + extension
        data['preferences']['extension'] = extension
        saveData(data)
        win.destroy()
    win = tk.Toplevel(root)
    win.title('Preferences - JSONly')
    win.config(bg = color)
    win.protocol('WM_DELETE_WINDOW', close)
    ttk.Label(win, text = 'Indent when saving', font = 1).pack()
    number = ttk.Label(win, text = data['preferences']['indent'])
    number.pack()
    indent = ctk.CTkSlider(win, to = 10, from_ = 0, number_of_steps = 10, command = configNumLabel, button_color='#646cff', button_hover_color='#4b50d8')
    indent.set(data['preferences']['indent'])
    indent.pack()
    ttk.Label(win, text = 'Default file extension to save', font = 1).pack()
    ext = ctk.CTkEntry(win, width = 200, fg_color=color, border_color='#646cff', bg_color=color, text_color = fore)
    ext._entry.config(insertbackground=fore)
    ext.pack()
    ext.insert(0, data['preferences']['extension'])
    ttk.Label

# WIP change color while running
# def changeTheme() -> None:
#     global color, fore
#     if data['theme']['global']:
#         color = fore
#         fore = 'black'
#     else:
#         color = color
#         fore = fore
#     root.config(bg = color)
#     listbox.config(bg = color)
#     style.configure('TLabel', background = color, foreground = fore)

# theme settings
def theme() -> None:
    def close() -> None:
        data['theme']['global'] = globalTheme.get()
        # changeTheme()
        saveData(data)
        win.destroy()
    win = tk.Toplevel()
    win.title('Theme - JSONly')
    win.grab_set()
    win.config(bg = color)
    ttk.Label(win, text = 'Global theme', font = 1).pack()
    globalTheme = tk.IntVar(value = data['theme']['global'])
    dark = ctk.CTkRadioButton(win, variable = globalTheme, value = 0, text = 'Dark')
    dark.pack()
    light = ctk.CTkRadioButton(win, variable = globalTheme, value = 1, text = 'Light')
    light.pack()
    ttk.Label(win, text = 'Note: requires app restart').pack()
    win.protocol('WM_DELETE_WINDOW', close)

# construct the main window with all of it's widgets
def main_window() -> None:
    global root, listbox, typeVar, valVar, view, edit, add_button, remove_button, file, valueEntry

    root = tk.Tk()
    root.configure(bg = color)
    root.title('JSONly')
    if platform.system() == 'Windows':
        root.state('zoomed')
    else:
        root.attributes('-zoomed', True)
    root.focus()

    listbox = ResizableListbox(root, height=20, width=100, bg = color, fg = fore, highlightbackground='#4b50d8', highlightcolor='#646cff')
    listbox.pack()
    for i in file:
        listbox.insert(tk.END, i)
    listbox.bind('<<ListboxSelect>>', configure)

    ttk.Label(root, text='Type').pack()
    typeVar = tk.StringVar()
    type_ = ctk.CTkEntry(root, state='readonly', textvariable=typeVar, justify = 'center', width = 200, fg_color=color, border_color='#646cff', bg_color=color, text_color=fore)
    type_.pack()

    ttk.Label(root, text='Value').pack()
    valVar = tk.StringVar()
    valueEntry = ctk.CTkEntry(root, state='readonly', textvariable=valVar, width = 800, justify = 'center', fg_color=color, border_color='#646cff', bg_color=color, text_color = fore)
    valueEntry.pack()
    valueEntry.bind('<Return>', lambda e: directEdit(root, file, typeVar, valueEntry.get(), key=listbox.get(index)))
    valueEntry.bind('<FocusOut>', lambda e: directEdit(root, file, typeVar, valueEntry.get(), key=listbox.get(index)))

    view = StyledButton(root, text='View complex value', cursor='hand2', state='disabled')
    view.pack()
    Hovertip(view, 'look at complex values (arrays and objects)')

    edit = StyledButton(root, text='Edit simple value', cursor='hand2', state='disabled', 
                      command=lambda: edit_value(root, file, key=listbox.get(listbox.curselection()[0])))
    edit.pack()
    Hovertip(edit, 'edit the properties of simple values (strings, integers, etc.)')

    add_button = StyledButton(root, text='Add new item', cursor='hand2', 
                            command=lambda: add_new_item(root, file))
    add_button.pack()
    Hovertip(add_button, 'add a new item')

    remove_button = StyledButton(root, text='Remove item', cursor='hand2', state='disabled',
                               command=lambda: remove_item(root, file, key=listbox.get(listbox.curselection()[0])))
    remove_button.pack()
    Hovertip(remove_button, 'remove items')

    # menu bar
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff = 0)
    filemenu.add_command(label = 'Open', command = load)
    filemenu.add_command(label = 'Save', command = save)
    filemenu.add_command(label = 'Save as…', command = lambda: save(saveas = True))
    filemenu.add_separator()
    filemenu.add_command(label = 'Exit', command = close)
    menubar.add_cascade(label = 'File', menu = filemenu)
    editmenu = tk.Menu(menubar, tearoff = 0)
    editmenu.add_command(label = 'Add new item', command = add_button.invoke)
    editmenu.add_command(label = 'Show plain text', command = plainText)
    menubar.add_cascade(label = 'Edit', menu=editmenu)
    about = tk.Menu(menubar, tearoff = 0)
    about.add_command(label = 'Website', command = lambda: webbrowser.open('https://dudenessboy.github.io/JSONly'))
    about.add_command(label = 'Github repository', command = lambda: webbrowser.open('https://github.com/DudenessBoy/JSONly'))
    about.add_command(label = 'License', command = JSONly.License.showLicense)
    menubar.add_cascade(label = 'About', menu = about)
    settingmenu = tk.Menu(menubar, tearoff = 0)
    settingmenu.add_command(label = 'Theme', command = theme)
    settingmenu.add_command(label = 'Preferences', command = settings)
    menubar.add_cascade(label = 'Settings', menu = settingmenu)
    if platform.system() != 'Windows':
        for menu in (menubar, filemenu, editmenu, about, settingmenu):
            menu.configure(bg = color, fg = fore, activebackground='#646cff', activeforeground='#cccccc')
    root.configure(menu = menubar)

    root.bind("<<ValueEdited>>", lambda e: configure())
    root.bind("<<ItemAdded>>", lambda e: refresh_listbox(listbox, file))
    root.bind("<<ItemRemoved>>", lambda e: refresh_listbox(listbox, file))
    root.bind('<Control-o>', load)
    root.bind('<Control-s>', save)
    root.bind('<Control-Shift-KeyPress-s>', lambda: save(saveas = True))
    root.protocol('WM_DELETE_WINDOW', close)
    root.bind('<Control-f>', lambda e: findWindow(listbox))
    root.bind('<Button-3>', context)
    listbox.bind('<Delete>', lambda e: remove_button.invoke())

    return root

# refresh the listbox in case of new values
def refresh_listbox(listbox, val) -> None:
    global saved
    saved = False
    listbox.delete(0, tk.END)
    if isinstance(val, dict):
        for key in val:
            listbox.insert(tk.END, key)
    elif isinstance(val, list):
        for i, item in enumerate(val):
            listbox.insert(tk.END, f"[{i}]")

def setIndex(listbox: tk.Listbox):
    global index
    if listbox.curselection():
        index = listbox.curselection()[0]
    else:
        index = 0

# display complex value, hopefully replaced with a tree view soon
def display(val) -> None:
    index = 0
    disp = tk.Toplevel(root)
    disp.configure(bg = color)
    disp.title('JSONly (complex value)')
    # disp.grab_set()
    disp.focus()
    
    listbox = ResizableListbox(disp, height=20, width=100, fg = fore, bg = color, highlightbackground='#4b50d8', highlightcolor='#646cff')
    listbox.pack()
    
    def refresh_listbox():
        global saved
        saved = False
        listbox.delete(0, tk.END)
        if isinstance(val, dict):
            for key in val:
                listbox.insert(tk.END, key)
        elif isinstance(val, list):
            for i, item in enumerate(val):
                listbox.insert(tk.END, f"[{i}]")

    refresh_listbox()

    def configure(event=None):
        setIndex(listbox)
        if listbox.curselection():
            index = listbox.curselection()[0]
            if isinstance(val, dict):
                key = listbox.get(index)
                value = val[key]
            else:
                value = val[index]
            
            update_value_display(value, typeVar, valVar)
            
            if isinstance(value, (dict, list)):
                view.configure(state='normal', command=lambda: display(value))
                valueEntry.configure(state = 'readonly')
                edit.configure(state='disabled')
            else:
                view.configure(state='disabled')
                valueEntry.configure(state = 'normal')
                edit.configure(state='normal', command=lambda: edit_value(disp, val, typeVar, valVar, key=key))
            
            remove_button.configure(state='normal')
        else:
            remove_button.configure(state='disabled')

    def directEdit(parent, otherVal, typeVar: tk.StringVar, value, key=None, index=None) -> None:
        new_value = value
        if typeVar.get() == 'integer':
            try:
                new_value = int(float(new_value))
            except ValueError:
                new_value = 1
        elif typeVar.get() == 'floating point number':
            try:
                new_value = float(new_value)
            except ValueError:
                new_value = 1.0
        elif typeVar.get() == 'boolean':
            if new_value.lower() != 'true' and new_value.lower() != 'false':
                if new_value == '0' or new_value == '':
                    new_value = 'false'
                else:
                    new_value = 'true'
            new_value = new_value.lower() == 'true'
        elif typeVar.get() == 'null':
            new_value = None

        if key is not None:
            val[key] = new_value
        elif index is not None:
            val[index] = new_value

    listbox.bind('<<ListboxSelect>>', configure)
    ttk.Label(disp, text='Type').pack()
    typeVar = tk.StringVar()
    type_ = ctk.CTkEntry(disp, state='readonly', textvariable=typeVar, justify = 'center', width = 200, fg_color=color, border_color='#646cff', bg_color=color, text_color=fore)
    type_.pack()
    ttk.Label(disp, text='Value').pack()
    valVar = tk.StringVar()
    valueEntry = ctk.CTkEntry(disp, state='readonly', textvariable=valVar, justify = 'center', width = 800, fg_color=color, border_color='#646cff', bg_color=color, text_color = fore)
    valueEntry._entry.config(insertbackground=fore)
    valueEntry.pack()
    if isinstance(val, dict):
        valueEntry.bind('<Return>', lambda e: directEdit(disp, file, typeVar, valueEntry.get(), key=listbox.get(index)))
        valueEntry.bind('<FocusOut>', lambda e: directEdit(disp, file, typeVar, valueEntry.get(), key=listbox.get(index)))
    else:
        valueEntry.bind('<Return>', lambda e: directEdit(disp, file, typeVar, valueEntry.get(), index=index))
        valueEntry.bind('<FocusOut>', lambda e: directEdit(disp, file, typeVar, valueEntry.get(), index=index))
    view = StyledButton(disp, text='View complex value', cursor='hand2', state='disabled')
    view.pack()
    Hovertip(view, 'look at complex values (arrays and objects)')
    edit = StyledButton(disp, text='Edit simple value', cursor='hand2', state='disabled',)
    edit.pack()
    Hovertip(edit, 'edit the properties of simple values (strings, integers, etc.)')
    add_button = StyledButton(disp, text='Add new item', cursor='hand2', 
                            command=lambda: add_new_item(disp, val))
    add_button.pack()
    Hovertip(add_button, 'add a new item')

    remove_button = StyledButton(disp, text='Remove item', cursor='hand2', state='disabled',
                               command=lambda: remove_item(disp, val, 
                                                           key=listbox.get(listbox.curselection()[0]) if isinstance(val, dict) else None,
                                                           index=listbox.curselection()[0] if isinstance(val, list) else None))
    remove_button.pack()
    Hovertip(remove_button, 'remove items')

    disp.bind("<<ValueEdited>>", lambda e: configure())
    disp.bind("<<ItemAdded>>", lambda e: refresh_listbox())
    disp.bind("<<ItemRemoved>>", lambda e: refresh_listbox())

# next three functions are for finding objects
def findWindow(listbox: tk.Listbox) -> None:
    def close() -> None:
        global findmode, findWord
        findWord = findEntry.get()
        findWin.destroy()
    findWin = tk.Toplevel(root)
    findWin.configure(bg = color)
    findWin.focus()
    # findWin.grab_set()
    findWin.overrideredirect(True)
    # Calculate the center coordinates of the main window
    root.update_idletasks()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    x_center = root.winfo_rootx() + root_width // 2
    y_center = root.winfo_rooty() + root_height // 2
    
    # Calculate the offset to position the Toplevel window in the center of the main window
    findWin_width = findWin.winfo_width()
    findWin_height = findWin.winfo_height()
    x_offset = (x_center - findWin_width // 2 ) - 100
    y_offset = (y_center - findWin_height // 2) + 20
    
    findWin.geometry(f"+{x_offset}+{y_offset}")
    findEntry = ctk.CTkEntry(findWin, width = 200, fg_color=color, border_color='#646cff', bg_color=color, text_color = fore)
    findEntry._entry.config(insertbackground=fore)
    findEntry.pack(side = 'left')
    findEntry.focus()
    findEntry.insert(0, findWord)
    findEntry.select_range(0, tk.END)
    nextBtn = StyledButton(findWin, text = '↓', command = lambda: findNext(findEntry.get(), listbox), width = 5)
    nextBtn.pack(side = 'left')
    Hovertip(nextBtn, 'find next (enter, up)')
    prevBtn = StyledButton(findWin, text = '↑', command = lambda: findPrev(findEntry.get(), listbox), width = 5)
    prevBtn.pack(side = 'left')
    Hovertip(prevBtn, 'find previous (up)')
    closeBtn = StyledButton(findWin, text = '×', command = close, width = 5)
    closeBtn.pack(side = 'left')
    Hovertip(closeBtn, 'close')
    findWin.bind('<Return>', lambda event: findNext(findEntry.get(), listbox))
    findWin.bind('<Down>', lambda event: findNext(findEntry.get(), listbox))
    findWin.bind('<Up>', lambda event: findPrev(findEntry.get(), listbox))

def findNext(searchKey: str, listbox: tk.Listbox):
    if searchKey:
        items = listbox.get(0, 'end')
        current_selection = listbox.curselection()
        if current_selection:
            current_index = current_selection[0]
        else:
            current_index = -1  # Set a default index when nothing is selected
        
        found = False
        for i in range(current_index + 1, len(items)):
            if searchKey.lower() in items[i].lower():
                listbox.selection_clear(0, 'end')
                listbox.selection_set(i)
                listbox.see(i)
                found = True
                break
        
        if not found:
            for i in range(len(items)):
                if searchKey.lower() in items[i].lower():
                    listbox.selection_clear(0, 'end')
                    listbox.selection_set(i)
                    listbox.see(i)
                    break

def findPrev(searchKey: str, listbox: tk.Listbox):
    if searchKey:
        items = listbox.get(0, 'end')
        current_selection = listbox.curselection()
        if current_selection:
            current_index = current_selection[0]
        else:
            current_index = len(items)  # Set a default index when nothing is selected
        
        found = False
        for i in range(current_index - 1, -1, -1):
            if searchKey.lower() in items[i].lower():
                listbox.selection_clear(0, 'end')
                listbox.selection_set(i)
                listbox.see(i)
                found = True
                break
        
        if not found:
            for i in range(len(items) - 1, -1, -1):
                if searchKey.lower() in items[i].lower():
                    listbox.selection_clear(0, 'end')
                    listbox.selection_set(i)
                    listbox.see(i)
                    break

# save the program's persistant data
def saveData(data: dict) -> None:
    if os.path.exists(dataFile):
        operation = 'write to'
    else:
        operation = 'create'
    try:
        with open(dataFile, 'w') as f:
            json.dump(data, f, indent = 2)
    except PermissionError:
        messagebox('Permission Denied', f'Permission to {operation} the file "{dataFile}" could not be obtained')
    except IOError:
        messagebox('I/O Error', f'There was an error while attempting to {operation} the file "{dataFile}"')
    except Exception as e:
        messagebox('Error', f'There was an error while attempting to {operation} the file "{dataFile}": {e}')

# context menu
def context(event: tk.Event) -> None:
    contextMenu = tk.Menu(root, tearoff=0)
    contextMenu.add_command(label='Save', command=save)
    contextMenu.add_command(label='Save as', command=lambda: save(saveas=True))
    contextMenu.add_command(label='Open', command=load)
    contextMenu.add_separator()
    contextMenu.add_command(label='Add new item', command=add_button.invoke)
    contextMenu.add_command(label='Remove selected item', command=remove_button.invoke)
    contextMenu.add_separator()
    contextMenu.add_command(label='Show plain text', command=plainText)
    contextMenu.tk_popup(event.x_root, event.y_root)
    if platform.system() != 'Windows':
        contextMenu.configure(bg = color, fg = fore, activebackground='#646cff', activeforeground='#cccccc')

# a custom button class, useless outside of this program, pre-sets a lot of things that were causing repitition
class StyledButton(ctk.CTkButton):
    def __init__(self, master, width = 200, height=40, text = '', cursor = 'arrow', state = 'normal', command = None) -> None:
        self.master = master
        self.width = width
        self.text = text
        self.cursor = cursor
        self.state = state
        self.command = command
        match data['theme']['global']:
            case 0:
                border_color = '#1e1e2e'
                bg_color = '#1e1e2e'
            case 1:
                border_color = 'white'
                bg_color = 'white'
        self.border_color = border_color
        self.bg_color = bg_color
        super().__init__(master, width, height, fg_color = '#646cff', hover_color='#4b50d8', border_color=border_color, border_width=2, bg_color=bg_color, text=text, cursor=cursor, state=state, command=command)
    
    def changeTheme(self) -> None:
        match data['theme']['global']:
            case 0:
                self.border_color = color
                self.bg_color = color
            case 1:
                self.border_color = fore
                self.bg_color = fore
        super().configure(bg_color = self.bg_color, border_color = self.border_color)

# custom listbox class that will dynamically resize with the window
class ResizableListbox(tk.Listbox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._master = master
        
        # Wait for widget to be fully created before binding
        self.after_idle(self._setup_resize_binding)

    def _setup_resize_binding(self):
        if self._master:
            # Only respond to actual size changes, not moves
            self._master.bind('<Configure>', self._on_configure)
            # Force initial sizing
            self.update_idletasks()
            self.auto_resize(self._create_dummy_event())

    def _on_configure(self, event):
        # Only handle if size actually changed
        if hasattr(self, '_last_size'):
            if (event.width, event.height) == self._last_size:
                return
        self._last_size = (event.width, event.height)
        self.auto_resize(event)

    def auto_resize(self, event):
        """
        Dynamically resize listbox based on parent window height.
        Leaves room for other UI components (like buttons).
        Converts pixel height to number of rows.
        """
        if self._master:
            # Get the height of a single line in pixels
            font = self.cget('font')
            if isinstance(font, str):
                font_obj = tk.font.nametofont(font)
            else:
                font_obj = font
            line_height = font_obj.metrics('linespace')

            # Convert available pixels to number of rows
            total_rows = event.height // line_height
            
            # Don't let padding take more than 70% of the total height
            max_padding = int(total_rows * 0.7)
            padding_rows = 16
            padding_rows = min(padding_rows, max_padding)
            
            rows = total_rows - padding_rows
            
            # Limit maximum number of rows to 50
            rows = min(rows, 50)
            
            # Ensure a minimum of 5 rows, but don't let it exceed 80% of total height
            min_rows = 5#min(1, int(total_rows * 0.8))
            rows = max(rows, min_rows)
            
            self.config(height=int(rows))

    def _create_dummy_event(self):
        """Creates a dummy event with the correct height."""
        class DummyEvent:
            def __init__(self, height):
                self.height = height

        return DummyEvent(self._master.winfo_height())

# load save data
dataFile = os.path.join(dataDir, 'settings.json')
os.makedirs(dataDir, exist_ok=True)
try:
    with open(dataFile, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}
    saveData(data)
except PermissionError:
    messagebox('Permission Denied', f'Permission to read the file "{dataFile}" could not be obtained. Persistant data cannot be read.')
    data = {}
except json.JSONDecodeError:
    messagebox('JSON Decode Error', f'The file "{dataFile}" contains invalid JSON syntax. Persistant data will be overwritten.')
    data = {}
    saveData(data)
except Exception as e:
    messagebox('Error', f'There was an error while attempting to read the file "{dataFile}": {e}. JSONly will attempt to overwrite persistant data.')
    data = {}
    saveData(data)

# make sure all required keys exist and contain valid data
if 'preferences' not in data.keys():
    data['preferences'] = {}
    saveData(data)
if 'indent' not in data['preferences'].keys():
    data['preferences']['indent'] = 2
    saveData(data)
if 'extension' not in data['preferences'].keys():
    data['preferences']['extension'] = '.json'
    saveData(data)
if 'theme' not in data.keys():
    data['theme'] = {}
    saveData(data)
if 'global' not in data['theme'].keys():
    data['theme']['global'] = 0
    saveData(data)

if data['theme']['global']:
    color = 'white'
    fore = 'black'
else:
    color = '#1e1e2e'
    fore = 'white'

root = main_window()
img = tk.PhotoImage(data = image)
root.iconphoto(True, img)
# styling ttk widgets
style = ttk.Style()
style.theme_use('alt')
style.configure('TButton', background = color, foreground = fore, focuscolor = 'gray')
style.map('TButton', background = [('disabled', '#383846'), ('active', '#2a2a3a')])
style.configure('TLabel', background = color, foreground = fore)
style.configure('TEntry', foreground = fore, fieldbackground = color, insertcolor = fore)
style.map('TEntry', fieldbackground = [('readonly', '#2a2a3a')])
style.configure('TCombobox', foreground = fore, fieldbackground = color, background = color, arrowcolor = fore, insertcolor = fore)
style.map('TCombobox', fieldbackground = [('readonly', '#2a2a3a')], background = [('active', '!focus', '#2a2a3a')])
style.configure('Vertical.TScrollbar', background = color, troughcolor = color, arrowcolor = fore)
style.map('Vertical.TScrollbar', background = [('active', '!focus', '#2a2a3a')])
style.configure('TFrame', background = color)
root.option_add('*TCombobox*Listbox.background', color)
root.option_add('*TCombobox*Listbox.foreground', fore)
del img, image
root.mainloop()
