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

import json
import platform
import subprocess
import webbrowser
import tkinter as tk
from LicenseText import LICENSE
from tooltip import Hovertip
from tkinter import ttk

if platform.system() == 'Linux':
    import tkfilebrowser
else:
    from tkinter import filedialog as tkfilebrowser

file = {}
filename = None
saved = True
findWord = ''
image = 'iVBORw0KGgoAAAANSUhEUgAAAEIAAABWCAYAAAB7E0BlAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPfSURBVHhe7VzRcdswDM0o+XKG6BJZoSNkgNoeoAt0gA7g/0zQAbKAJ+gCTvGkx5wqg6ToCKB8wbt754sFCtAjAVoUo4dAIGCOy/7p+2W/O10OT3/eD0/vU8p3b3LsN02LeD/snnEOOd/f/84hfw/fH3Y/Lz9232i+HaTAp0HnCLHYLAuIprWdc6mwLhhEmPVciRL8LzbNQmuXI0Rjs36QQB5bRADXFgLsPjIkgJMWWInS5oXNs2gVF+xWM8T54zyYGllHHnmKLMTmeMNIO7G5L8T5cR7MlONF755p/inI+SB6URwco7kv5EJftYBACeosn9Web4Wcsyz+ghlpdfBiMwHVC+KtKI4K+X1BMz9ogSRa9kx5JDrPHqjQWiCJNDMBRpvmE0RdopkP0ONaICCGLs1MID6ydWJbQhgH09P3FTYrhPcUulUhQJr5IIQgcL+gBQF+NSG6TWEhBBFCECEEEUIQIQQRQhAhBBFCEPckxCvNTHA/QsgxmplgW0LI8NeCAM2F6Lg6dgXpldLCbfUBzmeh+Z1w9dVzFbUeWetZRgm635FIHZrZolwffFaIKqlpv5ItjooPfSUIl8dulc4408wOuFDNeaLXg9haekIomq6PqgjOD2FL6QGuKgaVx8PX7CwBMl18qjWB2EppCiJuCCKftxVQNKw5SRzt7GcKDc27dVp/9dbSIFFO/NZLhIRhZFTSZMqmOlbNv/FB7JHmm8A4incn+ayl8fI0uUchJB6Z2od6sKIQ8qNEO8mcIkj31ABYK4oCJDalRksRGu36idEU661LBA3TJ467Tp8AfFZjkzSXEb7ejWBtJkE60dQNC1LYpo6xSGoOBzbl3yfB0arGAZp2jDio3XS5jYrSaEC60MwOEkDfOz+iUhvsp/bqkHRID8wUmu8JnVapCr0hx8xXiLCfUvMN3jxF3oJS0UTq0MwM4iM7g3n4/0C5TjgIUbgF8BiRH6gIYb5Ao/lN3I4Q0ls0M4PmN5EmPgghiJ5CYOhrfhNp5oMQggghiBCCCCGIEIIIIYgQggghiBCCKAUTQpAhBBlCkD2FEN++L9XYsBCmvq9QDGb/lf4TuLKkTzMTVKZuvxXsBC2QRIwYmq0OXKzmE4RINPODXGz+2YbhexyQeppP0n/zSrlnbLYJlB7sjOywT0Mcu75jpiYCxKe5L8S52VuHJNez/3Kdo7Rx35/xAXG+aBvilLhINs+iVH9y9NybcQUJYCtvJvOfLeZo2cwFri0ERiWb9ccgxuI3DtZ/Yyw5F8TfxEjQIIG9oIdYFOeBY4P4ooJGYbX3WZ6H78cZxH0XX+Dr4OHhH6RJz7npxayLAAAAAElFTkSuQmCC'

def showLicense() -> None:
    # Create a new window for the license
    licenseWin = tk.Toplevel(root, takefocus=True)
    licenseWin.config(bg = '#1e1e2e')
    licenseWin.title(f'License - JSONly')
    licenseWin.focus()
    licenseWin.geometry(f'805x550+{root.winfo_x()}+{root.winfo_y()}')

    # Frame to hold the text widget and scrollbar
    textFrame = ttk.Frame(licenseWin)
    textFrame.pack(fill='both', expand=True, padx=10, pady=10)

    # Text widget to display the license
    licenseText = tk.Text(
        textFrame, wrap='word', bg='#1e1e2e',
        fg='white', font='Helvetica 12', state='normal'
    )
    licenseText.insert('1.0', LICENSE)  # Insert license text
    licenseText.config(state='disabled')  # Make it read-only
    licenseText.pack(side='left', fill='both', expand=True)

    # Scrollbar for the text widget
    textScrollbar = ttk.Scrollbar(textFrame, orient='vertical', command=licenseText.yview)
    licenseText.config(yscrollcommand=textScrollbar.set)
    textScrollbar.pack(side='right', fill='y')

    # Additional information section
    ttk.Label(
        licenseWin, text='Websites for more info on this topic:',
        font='Helvetica 15', background='#1e1e2e'
    ).pack(pady=(10, 5))

    # Frame to hold hyperlinks
    linkFrame = ttk.Frame(licenseWin)
    linkFrame.pack()

    # Hyperlinks
    Hyperlink(
        linkFrame, text='GNU GPL License V3',
        url='https://www.gnu.org/licenses/gpl-3.0.en.html', cursor='hand2',
        bg='#1e1e2e'
    ).pack()

def close() -> None:
    if not saved:
        ans = messagebox('Unsaved Work', 'Would you like to save your changes before loading a new file?', ('Save', 'Don\'t Save', 'Cancel'))
        if ans == 'Cancel':
            return
        elif ans == 'Save':
            if not save():
                return
    root.destroy()

def messagebox(title, message, buttons=("OK",), callback=None, geometry = '300x150'):
    # Create a new window
    window = tk.Toplevel()
    window.config(bg = '#1e1e2e')
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
        button = ttk.Button(button_frame, text=button_text, command=lambda bt=button_text: on_button_click(bt))
        button.pack(side=tk.LEFT, padx=5)

    # Center the window on the screen
    window.update_idletasks()
    window.geometry(f"+{(window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)}"
                    f"+{(window.winfo_screenheight() // 2) - (window.winfo_height() // 2)}")

    # Prevent interaction with the main window
    window.transient()
    window.grab_set()
    window.wait_window()
    return endVal

def load(event = None) -> None:
    global filename, file, saved
    if not saved:
        ans = messagebox('Unsaved Work', 'Would you like to save your changes before loading a new file?', ('Save', 'Don\'t Save', 'Cancel'))
        if ans == 'Cancel':
            return
        elif ans == 'Save':
            if not save():
                return
    filename = tkfilebrowser.askopenfilename(filetypes = [('JSON files', '*.json'), ('Any files', '*.*')])
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
        else:
            refresh_listbox(listbox, file)
            saved = True
    else:
        filename = None

def save(event = None, saveas: bool = False) -> bool:
    global filename, saved
    if filename is None or saveas:
        filename = tkfilebrowser.asksaveasfilename(filetypes = [('JSON files', '*.json'), ('Any files', '*.*')], initialfile = 'newfile.json')
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
        messagebox('I/O Error', f'There was an error while attempting to write to the file {filename}')
        filename = None
        return
    else:
        saved = True
        return True

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
    edit_window.config(bg = '#1e1e2e')
    edit_window.title("Edit Value")
    edit_window.focus()
    edit_window.grab_set()
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

    typeBox = ttk.Combobox(edit_window, textvariable=typeVar, 
                 state='readonly')
    typeBox.grid(row=current_row, column=1, padx=5, pady=5)
    typeBox['values'] = ('string', 'integer', 'floating point number', 'boolean', 'null')
    typeBox.current(num)
    current_row += 1

    ttk.Label(edit_window, text="Value:").grid(row=current_row, column=0, padx=5, pady=5)
    value_entry = ttk.Entry(edit_window, width = 100)
    value_entry.insert(0, str(val[key]).lower() if index is None else str(val[index]).lower())
    value_entry.selection_range(0, tk.END)
    value_entry.focus()
    value_entry.bind('<Return>', save_value)
    value_entry.grid(row=current_row, column=1, padx=5, pady=5)
    current_row += 1

    ttk.Button(edit_window, text="Save", command=save_value, cursor = 'hand2').grid(row=current_row, column=0, columnspan=2, pady=10)

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

def remove_item(parent, val, key=None, index=None) -> None:
    if key is not None:
        del val[key]
    elif index is not None:
        del val[index]
    parent.event_generate("<<ItemRemoved>>")

def config(event=None) -> None:
    setIndex(listbox)
    if listbox.curselection():
        key = listbox.get(listbox.curselection()[0])
        value = file[key]
        update_value_display(value, typeVar, valVar)
        
        if isinstance(value, (dict, list)):
            view.config(state='normal', command=lambda: display(value))
            edit.config(state='disabled')
            valueEntry.config(state='readonly')
        else:
            view.config(state='disabled')
            edit.config(state='normal', command=lambda: edit_value(root, file, typeVar, valVar, key=key))
            valueEntry.config(state='normal')
        
        remove_button.config(state='normal')
    else:
        remove_button.config(state='disabled')

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

def plainText() -> None:
    win = tk.Toplevel(root)
    win.config(bg = '#1e1e2e')
    win.title('JSONls (plain text)')
    win.focus()
    win.grab_set()
    text = tk.Text(win, width = 100, height = 20, bg = '#1e1e2e', insertbackground = 'white', fg = 'white')
    text.pack()
    text.insert(0.0, json.dumps(file, indent = 2))
    text.config(state = 'disabled')
    copy = ttk.Button(win, text = 'Copy', cursor = 'hand2', command = lambda: subprocess.run(["xsel", "-b"], input=json.dumps(file, indent = 2).encode('utf-8'), check=True))
    copy.pack()

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
    add_window.config(bg = '#1e1e2e')
    add_window.title("Add New Item")
    add_window.focus()
    add_window.grab_set()

    current_row = 0

    if isinstance(val, dict):
        ttk.Label(add_window, text="Key:").grid(row=current_row, column=0, padx=5, pady=5)
        key_entry = ttk.Entry(add_window, width = 100)
        key_entry.bind('<Return>', lambda e: value_entry.focus())
        key_entry.grid(row=current_row, column=1, padx=5, pady=5)
        key_entry.focus()
        current_row += 1

    ttk.Label(add_window, text="Type:").grid(row=current_row, column=0, padx=5, pady=5)
    type_var = tk.StringVar(value='string')
    ttk.Combobox(add_window, textvariable=type_var, 
                 values=['string', 'integer', 'floating point number', 'boolean', 'null', 'array', 'object'], 
                 state='readonly').grid(row=current_row, column=1, padx=5, pady=5)
    current_row += 1

    ttk.Label(add_window, text="Value:").grid(row=current_row, column=0, padx=5, pady=5)
    value_entry = ttk.Entry(add_window, width = 100)
    value_entry.bind('<Return>', save_item)
    value_entry.grid(row=current_row, column=1, padx=5, pady=5)
    current_row += 1

    ttk.Button(add_window, text="Save", command=save_item, cursor = 'hand2').grid(row=current_row, column=0, columnspan=2, pady=10)

def main_window() -> None:
    global root, listbox, typeVar, valVar, view, edit, add_button, remove_button, file, valueEntry

    root = tk.Tk()
    root.config(bg = '#1e1e2e')
    root.title('JSONly')
    if platform.system() == 'Windows':
        root.state('zoomed')
    else:
        root.attributes('-zoomed', True)
    root.focus()

    listbox = tk.Listbox(root, height=20, width=100, bg = '#1e1e2e', fg = 'white')
    listbox.pack()
    for i in file:
        listbox.insert(tk.END, i)
    listbox.bind('<<ListboxSelect>>', config)

    ttk.Label(root, text='Type').pack()
    typeVar = tk.StringVar()
    type_ = ttk.Entry(root, state='readonly', textvariable=typeVar, justify = 'center')
    type_.pack()

    ttk.Label(root, text='Value').pack()
    valVar = tk.StringVar()
    valueEntry = ttk.Entry(root, state='readonly', textvariable=valVar, width = 100, justify = 'center')
    valueEntry.pack()
    valueEntry.bind('<Return>', lambda e: directEdit(root, file, typeVar, valueEntry.get(), key=listbox.get(index)))
    valueEntry.bind('<FocusOut>', lambda e: directEdit(root, file, typeVar, valueEntry.get(), key=listbox.get(index)))

    view = ttk.Button(root, text='View complex value', cursor='hand2', state='disabled', width = 20)
    view.pack()
    Hovertip(view, 'look at complex values (arrays and objects)')

    edit = ttk.Button(root, text='Edit simple value', cursor='hand2', state='disabled', 
                      command=lambda: edit_value(root, file, key=listbox.get(listbox.curselection()[0])), width = 20)
    edit.pack()
    Hovertip(edit, 'edit the properties of simple values (strings, integers, etc.)')

    add_button = ttk.Button(root, text='Add new item', cursor='hand2', 
                            command=lambda: add_new_item(root, file), width = 20)
    add_button.pack()
    Hovertip(add_button, 'add a new item')

    remove_button = ttk.Button(root, text='Remove item', cursor='hand2', state='disabled',
                               command=lambda: remove_item(root, file, key=listbox.get(listbox.curselection()[0])), width = 20)
    remove_button.pack()
    Hovertip(remove_button, 'remove items')

    ttk.Label(root).pack()
    plain = ttk.Button(root, text = 'View plain text', cursor = 'hand2', command = plainText, width = 20)
    plain.pack()
    Hovertip(plain, 'view the JSON data as plain text')
    loadBtn = ttk.Button(root, text = 'Load file', cursor = 'hand2', command = load, width = 20)
    loadBtn.pack()
    Hovertip(loadBtn, 'load JSON data from a file (ctrl+o)')
    saveBtn = ttk.Button(root, text = 'Save', cursor = 'hand2', command = save, width = 20)
    saveBtn.pack()
    Hovertip(saveBtn, 'save the JSON data (ctrl+s)')
    saveas = ttk.Button(root, text = 'Save as', cursor = 'hand2', command = lambda: save(saveas = True), width = 20)
    saveas.pack()
    Hovertip(saveas, 'save the JSON data to a file of your choice (ctrl+shift+s)')

    # menu bar
    menubar = tk.Menu(root, bg = '#1e1e2e', fg = 'white')
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
    about.add_command(label = 'License', command = showLicense)
    menubar.add_cascade(label = 'About', menu = about)
    root.config(menu = menubar)

    root.bind("<<ValueEdited>>", lambda e: config())
    root.bind("<<ItemAdded>>", lambda e: refresh_listbox(listbox, file))
    root.bind("<<ItemRemoved>>", lambda e: refresh_listbox(listbox, file))
    root.bind('<Control-o>', load)
    root.bind('<Control-s>', save)
    root.bind('<Control-Shift-KeyPress-s>', lambda: save(saveas = True))
    root.protocol('WM_DELETE_WINDOW', close)
    root.bind('<Control-f>', lambda e: findWindow(listbox))
    listbox.bind('<Delete>', lambda e: remove_button.invoke())

    return root

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

def display(val) -> None:
    index = 0
    disp = tk.Toplevel(root)
    disp.config(bg = '#1e1e2e')
    disp.title('JSONly (complex value)')
    disp.grab_set()
    disp.focus()
    
    listbox = tk.Listbox(disp, height=20, width=100, fg = 'white', bg = '#1e1e2e')
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

    def config(event=None):
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
                view.config(state='normal', command=lambda: display(value))
                valueEntry.config(state = 'readonly')
                edit.config(state='disabled')
            else:
                view.config(state='disabled')
                valueEntry.config(state = 'normal')
                edit.config(state='normal', command=lambda: edit_value(disp, val, typeVar, valVar, key=key))
            
            remove_button.config(state='normal')
        else:
            remove_button.config(state='disabled')

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

    listbox.bind('<<ListboxSelect>>', config)
    ttk.Label(disp, text='Type').pack()
    typeVar = tk.StringVar()
    type_ = ttk.Entry(disp, state='readonly', textvariable=typeVar, justify = 'center')
    type_.pack()
    ttk.Label(disp, text='Value').pack()
    valVar = tk.StringVar()
    valueEntry = ttk.Entry(disp, state='readonly', textvariable=valVar, width = 100, justify = 'center')
    valueEntry.pack()
    if isinstance(val, dict):
        valueEntry.bind('<Return>', lambda e: directEdit(disp, file, typeVar, valueEntry.get(), key=listbox.get(index)))
        valueEntry.bind('<FocusOut>', lambda e: directEdit(disp, file, typeVar, valueEntry.get(), key=listbox.get(index)))
    else:
        valueEntry.bind('<Return>', lambda e: directEdit(disp, file, typeVar, valueEntry.get(), index=index))
        valueEntry.bind('<FocusOut>', lambda e: directEdit(disp, file, typeVar, valueEntry.get(), index=index))
    view = ttk.Button(disp, text='View complex value', cursor='hand2', state='disabled', width = 20)
    view.pack()
    Hovertip(view, 'look at complex values (arrays and objects)')
    edit = ttk.Button(disp, text='Edit simple value', cursor='hand2', state='disabled', width = 20)
    edit.pack()
    Hovertip(edit, 'edit the properties of simple values (strings, integers, etc.)')
    add_button = ttk.Button(disp, text='Add new item', cursor='hand2', 
                            command=lambda: add_new_item(disp, val), width = 20)
    add_button.pack()
    Hovertip(add_button, 'add a new item')

    remove_button = ttk.Button(disp, text='Remove item', cursor='hand2', state='disabled',
                               command=lambda: remove_item(disp, val, 
                                                           key=listbox.get(listbox.curselection()[0]) if isinstance(val, dict) else None,
                                                           index=listbox.curselection()[0] if isinstance(val, list) else None), width = 20)
    remove_button.pack()
    Hovertip(remove_button, 'remove items')

    disp.bind("<<ValueEdited>>", lambda e: config())
    disp.bind("<<ItemAdded>>", lambda e: refresh_listbox())
    disp.bind("<<ItemRemoved>>", lambda e: refresh_listbox())

def findWindow(listbox: tk.Listbox) -> None:
    def close() -> None:
        global findmode, findWord
        findWord = findEntry.get()
        findWin.destroy()
    findWin = tk.Toplevel(root)
    findWin.config(bg = '#1e1e2e')
    findWin.focus()
    findWin.grab_set()
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
    findEntry = ttk.Entry(findWin, width = 50)
    findEntry.pack(side = 'left')
    findEntry.focus()
    findEntry.insert(0, findWord)
    findEntry.select_range(0, tk.END)
    nextBtn = ttk.Button(findWin, text = '↓', command = lambda: findNext(findEntry.get(), listbox), width = 5, takefocus = False)
    nextBtn.pack(side = 'left')
    Hovertip(nextBtn, 'find next (enter, up)')
    prevBtn = ttk.Button(findWin, text = '↑', command = lambda: findPrev(findEntry.get(), listbox), width = 5, takefocus = False)
    prevBtn.pack(side = 'left')
    Hovertip(prevBtn, 'find previous (up)')
    closeBtn = ttk.Button(findWin, text = '×', command = close, width = 5, takefocus = False)
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

class Hyperlink(tk.Label):
    '''A simple hyperlink that opens a website when clicked.\n
    New parameters:\n
    • url - the website that is connected to the hyperlink\n
    • showHovertip - whether or not to show a tooltip for the website\n
    • changeColor - whether or not to change color when hovered over\n
    • same - if true and no text or textvariable is given, text is the same as url'''
    def __init__(self, master: tk.Misc | None = None, *, url: str, font: str | list | tuple = 'Helvetica 10 underline', highlightcolor: str = 'blue', showHovertip: bool = True, same: bool = True, changeColor: bool = True, **kwargs) -> None:
        if not (url.startswith('https://') or url.startswith('http://')):
            url = 'http://' + url
        if kwargs['text'] is None:
            if same:
                kwargs['text'] = url
            else:
                kwargs['text'] = ''
        self.changeColor = changeColor
        self.showHovertip = showHovertip
        self.same = same
        self.url = url
        super().__init__(master, activeforeground='#4FC3F7', disabledforeground='#4FC3F7', fg='#4FC3F7', font=font, foreground='#4FC3F7', highlightcolor=highlightcolor, **kwargs)
        if showHovertip:
            Hovertip(self, url)
    
    # handle url clicked
    def _onClick(self, event = None) -> None:
        webbrowser.open_new_tab(self.url)

    # handle mouse enters url
    def _onEnter(self, event = None) -> None:
        self.config(foreground = '#0077FF', activeforeground = '#0077FF')

    # handle mouse leave url
    def _onLeave(self, event = None) -> None:
        self.config(foreground = '#4FC3F7', activeforeground = '#4FC3F7')

    def _addBindings(self) -> None:
        self.bind('<Button-1>', self._onClick)
        if self.changeColor:
            self.bind('<Enter>', self._onEnter, '+')
            self.bind('<Leave>', self._onLeave, '+')

    def pack(self, **kwargs) -> None:
        super().pack(**kwargs)
        self._addBindings()
        super().pack_configure(**kwargs)

    def place(self, **kwargs) -> None:
        super().place(**kwargs)
        self._addBindings()
        super().place_configure(**kwargs)

    def grid(self, **kwargs) -> None:
        super().grid(kwargs)
        self._addBindings()
        super().grid_configure(kwargs)

    def configure(self, **kwargs) -> None:
        self.configure(**kwargs)
        if 'url' in kwargs:
            self.url = kwargs['url']
        if 'same' in kwargs:
            self.same = kwargs['same']
        if 'changeColor' in kwargs:
            self.changeColor = kwargs['changeColor']

root = main_window()
img = tk.PhotoImage(data = image)
root.iconphoto(True, img)
style = ttk.Style()
style.theme_use('alt')
style.configure('TButton', background = '#1e1e2e', foreground = 'white', focuscolor = 'gray')
style.map('TButton', background = [('disabled', '#383846'), ('active', '#2a2a3a')])
style.configure('TLabel', background = '#1e1e2e', foreground = 'white')
style.configure('TEntry', foreground = 'white', fieldbackground = '#1e1e2e', insertcolor = 'white')
style.map('TEntry', fieldbackground = [('readonly', '#2a2a3a')])
style.configure('TCombobox', foreground = 'white', fieldbackground = '#1e1e2e', background = '#1e1e2e', arrowcolor = 'white', insertcolor = 'white')
style.map('TCombobox', fieldbackground = [('readonly', '#2a2a3a')], background = [('active', '!focus', '#2a2a3a')])
style.configure('Vertical.TScrollbar', background = '#1e1e2e', troughcolor = '#1e1e2e', arrowcolor = 'white')
style.map('Vertical.TScrollbar', background = [('active', '!focus', '#2a2a3a')])
style.configure('TFrame', background = '#1e1e2e')
root.option_add('*TCombobox*Listbox.background', '#1e1e2e')
root.option_add('*TCombobox*Listbox.foreground', 'white')
del img, image
root.mainloop()
