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
import platform
import sys
# set the data and configuration folders depending on OS, needs to be above the other import statements to work properly
match platform.system():
    case'Linux':
        configDir = os.getenv('XDG_CONFIG_HOME', os.path.join(os.getenv('HOME', ''), '.config')) # get $XDG_CONFIG_HOME, if not set default to $HOME/.config
        dataDir = os.getenv('XDG_DATA_HOME', os.path.join(os.getenv('HOME', ''), '.local', 'share')) # seperate data directory to comply with XDG Base Directory Specification
        sys.path.insert(0, "/usr/share/JSONly/lib/")
        import subprocess
    case 'Darwin': # MacOS
        configDir = os.path.join(os.getenv("HOME", ""), "Library", "Application Support") # data stored in $HOME/Library/Application Support (why is there a space in the folder name?)
        dataDir = configDir
    case 'Windows':
        configDir = os.getenv("LOCALAPPDATA", os.path.join(os.getenv("USERPROFILE", ""), "AppData", "Local")) # data stored in %LOCALAPPDATA%, if it isn't set, default to %USERPROFILE\AppData\Local
        dataDir = configDir
    case 'FreeBSD':
        configDir = os.path.join(os.getenv('HOME'), '.config')
        dataDir = os.path.join(os.getenv('HOME'), '.local/share')
    case _:
        configDir = '.' # attempt to store data in same directory as the program if the OS is something other than Windows, MacOS or Linux
        dataDir = configDir
configDir = os.path.join(configDir, 'JSONly')
dataDir = os.path.join(dataDir, 'JSONly')
import json
import subprocess
import webbrowser
from plyer import filechooser
import tkinter as tk
import customtkinter as ctk
from CTkListbox import CTkListbox # customtkinter doesn't have a native listbox
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
isEnabled = True

# check for unsaved work before closing the main window
def close() -> None:
    if not isEnabled:
        print('closing blocked by popup')
        return
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
    buttonFrame = ttk.Frame(window)
    buttonFrame.pack(pady=10)

    # Callback function for buttons
    def onButtonClick(btn_text):
        nonlocal endVal
        if callback:
            callback(btn_text)
        endVal = btn_text
        enableWidgets(root)
        window.destroy()
    
    endVal = 'closed'

    # Add buttons
    for button_text in buttons:
        button = StyledButton(buttonFrame, text=button_text, command=lambda bt=button_text: onButtonClick(bt), height=30, width = 100)
        button.pack(side=tk.LEFT, padx=5)

    # Center the window on the screen
    window.update_idletasks()

    # Prevent interaction with the main window
    window.transient()
    # window.grab_set()
    window.attributes('-topmost', True)
    disableWidgets(root)
    window.protocol('WM_DELETE_WINDOW', lambda: onButtonClick(buttons[-1]))
    window.wait_window()
    return endVal

def disableWidgets(parent):
    """Disable all interactive widgets in the parent window."""
    global isEnabled
    print('disabled main window')
    isEnabled = False
    for widget in parent.winfo_children():
        if isinstance(widget, (StyledButton, ResizableListbox, ctk.CTkEntry, ctk.CTkOptionMenu)):
            widget.configure(state=tk.DISABLED)

def enableWidgets(parent):
    """Re-enable all widgets in the parent window."""
    global isEnabled
    print('enabled main window')
    isEnabled = True
    for widget in parent.winfo_children():
        if isinstance(widget, (StyledButton, ResizableListbox, ctk.CTkEntry, ctk.CTkOptionMenu)):
            widget.configure(state=tk.NORMAL)
    configure()

# load a file from the disk
def load(event = None, filePath = None) -> None:
    global filename, file, saved
    if not saved:
        ans = messagebox('Unsaved Work', 'Would you like to save your changes before loading a new file?', ('Save', 'Don\'t Save', 'Cancel'))
        if ans == 'Cancel':
            return
        elif ans == 'Save':
            if not save():
                return
    if filePath is None:
        filename = filechooser.open_file(title = 'something', filters=[("JSON files", "*.json"), ('All files', '*.*')])
    else:
        filename = [filePath]
    if filename:
        filename = filename[0]
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
            refreshListbox(listbox, file)
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
def editValue(parent, val, typeVar: tk.StringVar, valVar: tk.StringVar, key=None, index=None) -> None:
    def saveValue(event = None):
        newValue = valueEntry.get()
        if typeVar.get() == 'integer':
            try:
                newValue = int(float(newValue))
            except ValueError:
                newValue = 1
        elif typeVar.get() == 'floating point number':
            try:
                newValue = float(newValue)
            except ValueError:
                newValue = 1.0
        elif typeVar.get() == 'boolean':
            if newValue.lower() != 'true' and newValue.lower() != 'false':
                if newValue == '0' or newValue == '':
                    newValue = 'false'
                else:
                    newValue = 'true'
            newValue = newValue.lower() == 'true'
        elif typeVar.get() == 'null':
            newValue = None

        if key is not None:
            val[key] = newValue
        elif index is not None:
            val[index] = newValue
        
        enableWidgets(root)
        editWindow.destroy()
        parent.event_generate("<<ValueEdited>>")

    editWindow = tk.Toplevel(parent)
    disableWidgets(root)
    editWindow.protocol('WM_DELETE_WINDOW', lambda: [enableWidgets(root), editWindow.destroy()])
    editWindow.configure(bg = color)
    editWindow.title("Edit Value")
    editWindow.focus()
    # editWindow.grab_set()
    currentRow = 0

    ttk.Label(editWindow, text="Type:").grid(row=currentRow, column=0, padx=5, pady=5)
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

    typeBox = ctk.CTkOptionMenu(editWindow, variable = typeVar, values=('string', 'integer', 'floating point number', 'boolean', 'null'), fg_color='#646cff', button_color='#646cff', button_hover_color='#4b50d8')
    typeBox.grid(row=currentRow, column=1, padx=5, pady=5)
    typeBox.set(typeBox._values[num])
    currentRow += 1

    ttk.Label(editWindow, text="Value:").grid(row=currentRow, column=0, padx=5, pady=5)
    valueEntry = ctk.CTkEntry(editWindow, width = 800, fg_color=color, border_color='#646cff', bg_color=color, text_color = fore)
    valueEntry._entry.config(insertbackground=fore)
    valueEntry.insert(0, str(val[key]).lower() if index is None else str(val[index]).lower())
    valueEntry.select_range(0, tk.END)
    valueEntry.focus()
    valueEntry.bind('<Return>', saveValue)
    valueEntry.grid(row=currentRow, column=1, padx=5, pady=5)
    currentRow += 1

    StyledButton(editWindow, text="Save", command=saveValue, cursor = 'hand2', height=30, width = 150)

# edit the value directly from the entry widget
def directEdit(parent, val, typeVar: tk.StringVar, value, key=None, index=None) -> None:
    newValue = value
    if typeVar.get() == 'integer':
        try:
            newValue = int(float(newValue))
        except ValueError:
            newValue = 1
    elif typeVar.get() == 'floating point number':
        try:
            newValue = float(newValue)
        except ValueError:
            newValue = 1.0
    elif typeVar.get() == 'boolean':
        if newValue.lower() != 'true' and newValue.lower() != 'false':
            if newValue == '0' or newValue == '':
                newValue = 'false'
            else:
                newValue = 'true'
        newValue = newValue.lower() == 'true'
    elif typeVar.get() == 'null':
        newValue = None

    if key is not None:
        val[key] = newValue
    elif index is not None:
        val[index] = newValue

# remove an item
def removeItem(parent, val, key=None, index=None) -> None:
    if key is not None:
        del val[key]
    elif index is not None:
        del val[index]
    parent.event_generate("<<ItemRemoved>>")

def configure(event=None) -> None:
    setIndex(listbox)
    if listbox.curselection() != None:
        key = listbox.get(listbox.curselection())
        value = file[key]
        updateValueDisplay(value, typeVar, valVar)
        
        if isinstance(value, (dict, list)):
            view.configure(state='normal', command=lambda: display(value))
            edit.configure(state='disabled')
            valueEntry.configure(state='readonly')
        else:
            view.configure(state='disabled')
            edit.configure(state='normal', command=lambda: editValue(root, file, typeVar, valVar, key=key))
            valueEntry.configure(state='normal')
        
        removeButton.configure(state='normal')
    else:
        removeButton.configure(state='disabled')
        view.configure(state='disabled')
        edit.configure(state='disabled')
        valueEntry.configure(state='readonly')

def updateValueDisplay(value, typeVar: tk.StringVar, valVar: tk.StringVar) -> None:
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
def addNewItem(parent, val) -> None:
    def saveItem(event = None):
        newValue = valueEntry.get()
        if type_var.get() == 'integer':
            try:
                newValue = int(float(newValue))
            except ValueError:
                newValue = 1
        elif type_var.get() == 'floating point number':
            try:
                newValue = float(newValue)
            except ValueError:
                newValue = 1.0
        elif type_var.get() == 'boolean':
            if newValue.lower() != 'true' and newValue.lower() != 'false':
                if newValue == '0' or newValue == '':
                    newValue = 'false'
                else:
                    newValue = 'true'
            newValue = newValue.lower() == 'true'
        elif type_var.get() == 'null':
            newValue = None
        elif type_var.get() == 'array':
            newValue = []
        elif type_var.get() == 'object':
            newValue = {}

        if isinstance(val, dict):
            new_key = key_entry.get().strip()
            if not new_key:
                messagebox("Error", "Key cannot be empty")
                return
            if new_key in val:
                messagebox("Error", "Key already exists")
                return
            val[new_key] = newValue
        elif isinstance(val, list):
            val.append(newValue)
        
        enableWidgets(root)
        addWindow.destroy()
        parent.event_generate("<<ItemAdded>>")

    addWindow = tk.Toplevel(parent)
    disableWidgets(root)
    addWindow.protocol('WM_DELETE_WINDOW', lambda: [enableWidgets(root), addWindow.destroy()])
    addWindow.geometry('900x150')
    addWindow.configure(bg = color)
    addWindow.title("Add New Item")
    addWindow.focus()
    # addWindow.grab_set()

    currentRow = 0

    if isinstance(val, dict):
        ttk.Label(addWindow, text="Key:").grid(row=currentRow, column=0, padx=5, pady=5)
        key_entry = ctk.CTkEntry(addWindow, width = 200, fg_color=color, border_color='#646cff', bg_color=color, text_color = fore)
        key_entry._entry.config(insertbackground=fore)
        key_entry.bind('<Return>', lambda e: valueEntry.focus())
        key_entry.grid(row=currentRow, column=1, padx=5, pady=5)
        key_entry.focus()
        currentRow += 1

    ttk.Label(addWindow, text="Type:").grid(row=currentRow, column=0, padx=5, pady=5)
    type_var = tk.StringVar(value='string')
    ctk.CTkOptionMenu(addWindow, variable = type_var, values=['string', 'integer', 'floating point number', 'boolean', 'null', 'array', 'object'], fg_color='#646cff', button_color='#646cff', button_hover_color='#4b50d8').grid(row=currentRow, column=1, padx=5, pady=5)
    currentRow += 1

    ttk.Label(addWindow, text="Value:").grid(row=currentRow, column=0, padx=5, pady=5)
    valueEntry = ctk.CTkEntry(addWindow, width = 800, fg_color=color, border_color='#646cff', bg_color=color, text_color = fore)
    valueEntry._entry.config(insertbackground=fore)
    valueEntry.bind('<Return>', saveItem)
    valueEntry.grid(row=currentRow, column=1, padx=5, pady=5)
    currentRow += 1

    StyledButton(addWindow, text="Save", command=saveItem, cursor = 'hand2', height=30, width = 150).grid(row=currentRow, column=0, columnspan=2, pady=10)

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
        enableWidgets(root)
        win.destroy()
    win = tk.Toplevel(root)
    disableWidgets(root)
    win.protocol('WM_DELETE_WINDOW', lambda: [enableWidgets(root), win.destroy()])
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

def writeFile(path: str, data: str) -> bool:
    try:
        with open(path, 'w') as f:
            f.write(data)
        return True
    except PermissionError:
        messagebox('Permission Denied', f'Permission to write to the file "{path}" could not be obtained.')
        return False
    except Exception as e:
        messagebox('Error', f'There was an error while attempting to write to the file "{path}": {e}.')
        return False

def loadData(path: str, default: str) -> str:
    try:
        with open(path, 'r') as f:
            ret = f.read()
            return ret
    except FileNotFoundError:
        writeFile(path, default)
        return default
    except PermissionError:
        messagebox('Permission Denied', f'Permission to read the file "{path}" could not be obtained. Data cannot be read.')
        return default
    except json.JSONDecodeError:
        messagebox('JSON Decode Error', f'The file "{path}" contains invalid JSON syntax. JSONly will overwrite the data.')
        writeFile(path, default)
        return default
    except Exception as e:
        messagebox('Error', f'There was an error while attempting to read the file "{path}": {e}. JSONly will attempt to overwrite the data.')
        writeFile(path, default)
        return default

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
        enableWidgets(root)
        win.destroy()
    win = tk.Toplevel()
    disableWidgets(root)
    win.protocol('WM_DELETE_WINDOW', lambda: [enableWidgets(root), win.destroy()])
    win.title('Theme - JSONly')
    # win.grab_set()
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
def mainWindow() -> None:
    global root, listbox, typeVar, valVar, view, edit, addButton, removeButton, file, valueEntry

    root = tk.Tk()
    root.configure(bg = color)
    root.title('JSONly')
    root.geometry('1000x800')
    if platform.system() == 'Windows':
        root.state('zoomed')
    elif platform.system() == 'Linux':
        root.attributes('-zoomed', True)
    root.focus()

    listbox = ResizableListbox(root, width=800, fg_color = color, hover_color = '#646cff', highlight_color='#4b50d8', text_color=fore)
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
                      command=lambda: editValue(root, file, key=listbox.get(listbox.curselection())))
    edit.pack()
    Hovertip(edit, 'edit the properties of simple values (strings, integers, etc.)')

    addButton = StyledButton(root, text='Add new item', cursor='hand2', 
                            command=lambda: addNewItem(root, file))
    addButton.pack()
    Hovertip(addButton, 'add a new item')

    removeButton = StyledButton(root, text='Remove item', cursor='hand2', state='disabled',
                               command=lambda: removeItem(root, file, key=listbox.get(listbox.curselection())))
    removeButton.pack()
    Hovertip(removeButton, 'remove items')

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
    editmenu.add_command(label = 'Add new item', command = addButton.invoke)
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
    root.bind("<<ItemAdded>>", lambda e: refreshListbox(listbox, file))
    root.bind("<<ItemRemoved>>", lambda e: refreshListbox(listbox, file))
    root.bind('<Control-o>', load)
    root.bind('<Control-s>', save)
    root.bind('<Control-Shift-KeyPress-s>', lambda: save(saveas = True))
    root.protocol('WM_DELETE_WINDOW', close)
    root.bind('<Control-f>', lambda e: findWindow(listbox))
    root.bind('<Button-3>', context)
    listbox.bind('<Delete>', lambda e: removeButton.invoke())

    return root

# refresh the listbox in case of new values
def refreshListbox(listbox, val) -> None:
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
        index = listbox.curselection()
    else:
        index = 0

# display complex value, hopefully replaced with a tree view soon
def display(val) -> None:
    index = 0
    disp = tk.Toplevel(root)
    disp.configure(bg = color)
    disp.geometry('1000x800')
    disp.title('JSONly (complex value)')
    # disp.grab_set()
    disp.focus()
    
    listbox = ResizableListbox(disp, width=800, fg_color = color, hover_color = '#646cff', highlight_color='#4b50d8', text_color=fore)
    listbox.pack()
    
    def refreshListbox():
        global saved
        saved = False
        listbox.delete(0, tk.END)
        if isinstance(val, dict):
            for key in val:
                listbox.insert(tk.END, key)
        elif isinstance(val, list):
            for i, item in enumerate(val):
                listbox.insert(tk.END, f"[{i}]")

    refreshListbox()

    def configure(event=None):
        setIndex(listbox)
        if listbox.curselection() != None:
            index = listbox.curselection()
            if isinstance(val, dict):
                key = listbox.get(index)
                value = val[key]
            else:
                value = val[index]
            
            updateValueDisplay(value, typeVar, valVar)
            
            if isinstance(value, (dict, list)):
                view.configure(state='normal', command=lambda: display(value))
                valueEntry.configure(state = 'readonly')
                edit.configure(state='disabled')
            else:
                view.configure(state='disabled')
                valueEntry.configure(state = 'normal')
                edit.configure(state='normal', command=lambda: editValue(disp, val, typeVar, valVar, key=key))
            
            removeButton.configure(state='normal')
        else:
            removeButton.configure(state='disabled')
            view.configure(state='disabled')
            edit.configure(state='disabled')
            valueEntry.configure(state='readonly')

    def directEdit(parent, otherVal, typeVar: tk.StringVar, value, key=None, index=None) -> None:
        newValue = value
        if typeVar.get() == 'integer':
            try:
                newValue = int(float(newValue))
            except ValueError:
                newValue = 1
        elif typeVar.get() == 'floating point number':
            try:
                newValue = float(newValue)
            except ValueError:
                newValue = 1.0
        elif typeVar.get() == 'boolean':
            if newValue.lower() != 'true' and newValue.lower() != 'false':
                if newValue == '0' or newValue == '':
                    newValue = 'false'
                else:
                    newValue = 'true'
            newValue = newValue.lower() == 'true'
        elif typeVar.get() == 'null':
            newValue = None

        if key is not None:
            val[key] = newValue
        elif index is not None:
            val[index] = newValue

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
    addButton = StyledButton(disp, text='Add new item', cursor='hand2', 
                            command=lambda: addNewItem(disp, val))
    addButton.pack()
    Hovertip(addButton, 'add a new item')

    removeButton = StyledButton(disp, text='Remove item', cursor='hand2', state='disabled',
                               command=lambda: removeItem(disp, val, 
                                                           key=listbox.get(listbox.curselection()) if isinstance(val, dict) else None,
                                                           index=listbox.curselection() if isinstance(val, list) else None))
    removeButton.pack()
    Hovertip(removeButton, 'remove items')

    disp.bind("<<ValueEdited>>", lambda e: configure())
    disp.bind("<<ItemAdded>>", lambda e: refreshListbox())
    disp.bind("<<ItemRemoved>>", lambda e: refreshListbox())

# next three functions are for finding objects
def findWindow(listbox: tk.Listbox) -> None:
    def close() -> None:
        global findmode, findWord
        findWord = findEntry.get()
        enableWidgets(root)
        findWin.destroy()
    findWin = tk.Toplevel(root)
    disableWidgets(root)
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
    contextMenu.add_command(label='Add new item', command=addButton.invoke)
    contextMenu.add_command(label='Remove selected item', command=removeButton.invoke)
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
class ResizableListbox(CTkListbox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._master = master
        self._resize_timer = None

        self._master.bind('<Configure>', self.debounce_resize)

    def debounce_resize(self, event):
        if self._resize_timer is not None:
            self._master.after_cancel(self._resize_timer)
        self._resize_timer = self._master.after(150, self.auto_resize, event)

    def auto_resize(self, event):
        """
        Dynamically resize listbox based on parent window height.
        Leaves room for other UI components (like buttons).
        """
        if self._master:
            padding = 300 # padding for buttons
            available = max(self._master.winfo_height() - padding, 1) # Prevent negative or zero height
            super().configure(height = available)

# load save data
dataFile = os.path.join(configDir, 'settings.json')
os.makedirs(configDir, exist_ok=True)
os.makedirs(dataDir, exist_ok=True)
try:
    data = json.loads(loadData(dataFile, r'{}'))
except json.JSONDecodeError:
    messagebox('JSON Decode Error', f'The file "{dataFile}" contains invalid JSON syntax. Persistant data will be overwritten.')
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

root = mainWindow()
img = tk.PhotoImage(data = image)
root.iconphoto(True, img)
# styling ttk widgets
style = ttk.Style()
style.theme_use('alt')
style.configure('TLabel', background = color, foreground = fore)
style.configure('TFrame', background = color)
del img, image

if len(sys.argv) > 1:
    print('opened:', sys.argv[1])
    load(filePath = sys.argv[1])

root.mainloop()
