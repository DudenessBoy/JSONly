# Copyright (c) 2025 Luke Moyer
# Licensed under the MIT License. See LICENSE file for details.

import os
import sys
import platform
if platform.system() != 'Linux':  # can't use OS because of confilicts with DEB package
    import pyperclip
else:
    sys.path.append('/usr/share/JSONly/lib')
    import subprocess
import json
import subprocess
import webbrowser
import tkinter as tk
from tkinter import ttk
from plyer import filechooser
import customtkinter as ctk
from CTkListbox import CTkListbox # customtkinter doesn't have a native listbox
import darkdetect
import JSONly.License
import JSONly.lang
from JSONly.constants import *

# initialize some variables
file = {}  # JSON data to be viewed
filename = None  # filename to save to
saved = True  # whether or not the data has been saved
findWord = ''  # string in the find feature
buttons = []
isEnabled = True

# check for unsaved work before closing the main window
def close() -> None:
    if not isEnabled:
        print('closing blocked by popup')
        return
    if not saved:
        ans = messagebox(
            lang['popup.unsaved.title'],
            lang['popup.unsaved.body.close'],
            lang['popup.unsaved.buttons']
        )
        if ans == lang['popup.unsaved.buttons'][2]:
            return
        elif ans == lang['popup.unsaved.buttons'][0]:
            if not save():
                return
    root.destroy()

# load a file from the disk
def load(event = None, filePath = None) -> None:
    global filename, file, saved
    if not saved:
        ans = messagebox(
            lang['popup.unsaved.title'],
            lang['popup.unsaved.body.load'],
            lang['popup.unsaved.buttons'])
        if ans == lang['popup.unsaved.buttons'][2]:
            return
        elif ans == lang['popup.unsaved.buttons'][0]:
            if not save():
                return
    if filePath is None:
        filename = filechooser.open_file(
            filters=[(lang['filepicker.filter.json'], "*.json"), ('All files', '*.*')]
        )
    else:
        filename = [filePath]
    if filename:
        filename = filename[0]
        try:
            with open(filename, 'r', encoding = 'utf-8') as f:
                file = json.load(f)
        except FileNotFoundError:
            messagebox(
                lang['error.missingfile.title'],
                lang['error.missingfile.body'].format(filename)
            )
            filename = None
            return
        except json.JSONDecodeError:
            messagebox(
                lang['error.json.title'],
                lang['error.json.body'].format(filename)
            )
            filename = None
            return
        except EOFError:
            messagebox(
                lang['error.eof.title'],
                lang['error.eof.body'].format(filename)
            )
            filename = None
            return
        except PermissionError:
            messagebox(
                lang['error.permission.title'],
                lang['error.permission.read.body'].format(filename)
            )
            filename = None
            return
        except Exception as e:
            messagebox(
                lang['error.generic.title'],
                lang['error.generic.read.body'].format(filename, str(e))
            )
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
        filename = filechooser.save_file(filters=[(
            lang['filepicker.filter.json'],
            '*.json')]
        )
        if not filename:
            filename = None
            return False
        elif isinstance(filename, list):
            filename = filename[0]
    try:
        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(file, f, indent = 2)
    except PermissionError:
        messagebox(
            lang['error.permission.title'],
            lang['error.permission.write.body'].format(filename)
        )
        filename = None
        return
    except Exception as e:
        messagebox(
            lang['error.generic.title'],
            lang['error.generic.write.body'].format(filename, e)
        )
        return
    else:
        saved = True
        return True

# edit the value, using a dedicated window
def editValue(
    parent,
    val,
    typeVar: tk.StringVar,
    valVar: tk.StringVar,
    key=None,
    index=None
    ) -> None:
    def saveValue(event = None):
        newValue = valueEntry.get()
        if typeVar.get() == lang['window.types'][1]:
            try:
                newValue = int(float(newValue))
            except ValueError:
                newValue = 1
        elif typeVar.get() == lang['window.types'][2]:
            try:
                newValue = float(newValue)
            except ValueError:
                newValue = 1.0
        elif typeVar.get() == lang['window.types'][3]:
            if newValue.lower() != 'true' and newValue.lower() != 'false':
                if newValue == '0' or newValue == '':
                    newValue = 'false'
                else:
                    newValue = 'true'
            newValue = newValue.lower() == 'true'
        elif typeVar.get() == lang['window.types'][4]:
            newValue = None

        if key is not None:
            val[key] = newValue
        elif index is not None:
            val[index] = newValue
        
        editWindow.destroy()
        parent.event_generate("<<ValueEdited>>")

    editWindow = tk.Toplevel(parent)
    editWindow.wait_visibility()
    editWindow.transient(root)
    editWindow.grab_set()
    editWindow.group(root)
    editWindow.attributes("-type", "dialog")
    editWindow.configure(bg = color)
    editWindow.title(lang['popup.edit.title'])
    editWindow.focus()
    currentRow = 0

    ttk.Label(
        editWindow,
        text="Type:"
    ).grid(row=currentRow, column=0, padx=5, pady=5)
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

    typeBox = ctk.CTkOptionMenu(
        editWindow,
        variable=typeVar,
        values=lang['window.types'],
        fg_color='#646cff',
        button_color='#646cff',
        button_hover_color='#4b50d8'
    )
    typeBox.grid(row=currentRow, column=1, padx=5, pady=5)
    typeBox.set(typeBox._values[num])
    currentRow += 1

    ttk.Label(
        editWindow,
        text="Value:"
    ).grid(row=currentRow, column=0, padx=5, pady=5)
    valueEntry = ctk.CTkEntry(
        editWindow,
        width=800,
        fg_color=color,
        border_color='#646cff',
        bg_color=color,
        text_color = fore
    )
    valueEntry._entry.config(insertbackground=fore)
    valueEntry.insert(
        0,
        str(val[key]).lower() if index is None \
        else str(val[index]).lower()
    )
    valueEntry.select_range(0, tk.END)
    valueEntry.focus()
    valueEntry.bind('<Return>', saveValue)
    valueEntry.grid(row=currentRow, column=1, padx=5, pady=5)
    currentRow += 1

    StyledButton(
        editWindow,
        text=lang['popup.button.save'],
        command=saveValue,
        cursor = 'hand2',
        height=30,
        width = 150
    )

# edit the value directly from the entry widget
def directEdit(parent, val, typeVar: tk.StringVar, value, key=None, index=None) -> None:
    newValue = value
    if typeVar.get() == lang['window.types'][1]:
        try:
            newValue = int(float(newValue))
        except ValueError:
            newValue = 1
    elif typeVar.get() == lang['window.types'][2]:
        try:
            newValue = float(newValue)
        except ValueError:
            newValue = 1.0
    elif typeVar.get() == lang['window.types'][3]:
        if newValue.lower() != 'true' and newValue.lower() != 'false':
            if newValue == '0' or newValue == '':
                newValue = 'false'
            else:
                newValue = 'true'
        newValue = newValue.lower() == 'true'
    elif typeVar.get() == lang['window.types'][4]:
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
    if listbox.curselection() is not None:
        key = listbox.get(listbox.curselection())
        value = file[key]
        updateValueDisplay(value, typeVar, valVar)
        
        if isinstance(value, (dict, list)):
            view.configure(state='normal', command=lambda: display(value))
            edit.configure(state='disabled')
            valueEntry.configure(state='readonly')
        else:
            view.configure(state='disabled')
            edit.configure(
                state='normal',
                command=lambda: editValue(
                    root,
                    file,
                    typeVar,
                    valVar,
                    key=key
                )
            )
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
        typeVar.set(lang['window.types'][5])
        valVar.set('(complex value)')
    elif isinstance(value, dict):
        typeVar.set(lang['window.types'][6])
        valVar.set('(complex value)')
    else:
        valVar.set(str(value))
        if isinstance(value, str):
            typeVar.set(lang['window.types'][0])
        elif isinstance(value, bool):
            typeVar.set(lang['window.types'][3])
            valVar.set(valVar.get().lower())
        elif isinstance(value, int):
            typeVar.set(lang['window.types'][1])
        elif isinstance(value, float):
            typeVar.set(lang['window.types'][2])

# display the file as JSON plain text
def plainText() -> None:
    win = tk.Toplevel(root)
    win.configure(bg = color)
    win.title(lang['popup.plaintext.title'])
    win.focus()
    win.wait_visibility()
    win.transient(root)
    win.grab_set()
    win.group(root)
    win.attributes("-type", "dialog")
    text = tk.Text(
        win,
        width=100,
        height=20,
        bg=color,
        insertbackground=fore,
        fg=fore
    )
    text.pack()
    text.insert(0.0, json.dumps(file, indent = 2))
    text.configure(state='disabled')
    if OS == 'Linux':
        copy = StyledButton(
            win,
            text=lang['popup.plaintext.button.copy'],
            cursor='hand2',
            command=lambda: subprocess.run(
                ["xsel", "-b"],
                input=json.dumps(file, indent = 2).encode('utf-8'),
                check=True
            )
        )
    else:
        copy = StyledButton(
            win,
            text=lang['popup.plaintext.button.copy'],
            cursor='hand2',
            command=lambda: pyperclip.copy(json.dumps(file, indent=2))
        )
    copy.pack()

# add a new item to the listbox
def addNewItem(parent, val) -> None:
    def saveItem(event = None):
        newValue = valueEntry.get()
        if type_var.get() == lang['window.types'][1]:
            try:
                newValue = int(float(newValue))
            except ValueError:
                newValue = 1
        elif type_var.get() == lang['window.types'][2]:
            try:
                newValue = float(newValue)
            except ValueError:
                newValue = 1.0
        elif type_var.get() == lang['window.types'][3]:
            if newValue.lower() != 'true' and newValue.lower() != 'false':
                if newValue == '0' or newValue == '':
                    newValue = 'false'
                else:
                    newValue = 'true'
            newValue = newValue.lower() == 'true'
        elif type_var.get() == 'null':
            newValue = None
        elif type_var.get() == lang['window.types'][5]:
            newValue = []
        elif type_var.get() == lang['window.types'][6]:
            newValue = {}

        if isinstance(val, dict):
            new_key = key_entry.get().strip()
            if not new_key:
                messagebox(
                    lang['error.generic.title'],
                    lang['error.generic.emptykey']
                )
                return
            if new_key in val:
                messagebox(
                    lang['error.generic.title'],
                    lang['error.generic.dupekey']
                )
                return
            val[new_key] = newValue
        elif isinstance(val, list):
            val.append(newValue)
        
        addWindow.destroy()
        parent.event_generate("<<ItemAdded>>")

    addWindow = tk.Toplevel(parent)
    addWindow.wait_visibility()
    addWindow.transient(root)
    addWindow.grab_set()
    addWindow.group(root)
    addWindow.attributes("-type", "dialog")
    addWindow.geometry('900x150')
    addWindow.configure(bg = color)
    addWindow.title(lang['popup.add.title'])
    addWindow.focus()

    currentRow = 0

    if isinstance(val, dict):
        ttk.Label(
            addWindow,
            text="Key:"
        ).grid(row=currentRow, column=0, padx=5, pady=5)
        key_entry = ctk.CTkEntry(
            addWindow,
            width=200,
            fg_color=color,
            border_color='#646cff',
            bg_color=color,
            text_color=fore
        )
        key_entry._entry.config(insertbackground=fore)
        key_entry.bind('<Return>', lambda e: valueEntry.focus())
        key_entry.grid(row=currentRow, column=1, padx=5, pady=5)
        key_entry.focus()
        currentRow += 1

    ttk.Label(addWindow, text="Type:").grid(row=currentRow, column=0, padx=5, pady=5)
    type_var = tk.StringVar(value=lang['window.types'][0])
    ctk.CTkOptionMenu(
        addWindow,
        variable=type_var,
        values=lang['window.types'],
        fg_color='#646cff',
        button_color='#646cff',
        button_hover_color='#4b50d8'
    ).grid(row=currentRow, column=1, padx=5, pady=5)
    currentRow += 1

    ttk.Label(addWindow, text="Value:").grid(row=currentRow, column=0, padx=5, pady=5)
    valueEntry = ctk.CTkEntry(
        addWindow,
        width=800,
        fg_color=color,
        border_color='#646cff',
        bg_color=color,
        text_color=fore
    )
    valueEntry._entry.config(insertbackground=fore)
    valueEntry.bind('<Return>', saveItem)
    valueEntry.grid(row=currentRow, column=1, padx=5, pady=5)
    currentRow += 1

    StyledButton(
        addWindow,
        text=lang['popup.button.save'],
        command=saveItem,
        cursor='hand2',
        height=30,
        width=150
    ).grid(row=currentRow, column=0, columnspan=2, pady=10)

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
        if langSel.get().startswith('lang/'):
            data['preferences']['lang'] = os.path.basename(
                JSONly.lang.langFiles[langSel.get()]
            )
        else:
            data['preferences']['lang'] = JSONly.lang.langFiles[langSel.get()]
        saveData(data)
        win.destroy()
    win = tk.Toplevel(root)
    win.wait_visibility()
    win.transient(root)
    win.grab_set()
    win.group(root)
    win.attributes("-type", "dialog")
    win.title(lang['settings.title'])
    win.config(bg = color)
    win.protocol('WM_DELETE_WINDOW', close)
    ttk.Label(win, text = lang['settings.label.indent'], font = 1).pack()
    number = ttk.Label(win, text = data['preferences']['indent'])
    number.pack()
    indent = ctk.CTkSlider(
        win,
        to=10,
        from_=0,
        number_of_steps=10,
        command=configNumLabel,
        button_color='#646cff',
        button_hover_color='#4b50d8'
    )
    indent.set(2)
    indent.pack()
    ttk.Label(win, text=lang['settings.label.extension'], font = 1).pack()
    ext = ctk.CTkEntry(
        win,
        width=200,
        fg_color=color,
        border_color='#646cff',
        bg_color=color,
        text_color=fore
    )
    ext._entry.config(insertbackground=fore)
    ext.pack()
    ext.insert(0, data['preferences']['extension'])

    ttk.Label(win, text=lang['settings.label.lang'], font = 1).pack()
    langSel = ctk.CTkOptionMenu(
        win,
        values=list(JSONly.lang.langFiles.keys()),
        fg_color='#646cff',
        button_color='#646cff',
        button_hover_color='#4b50d8'
    )
    langSel.pack()

def writeFile(path: str, data: str) -> bool:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)
        return True
    except PermissionError:
        messagebox(
            lang['error.permission.title'],
            lang['error.permission.write.body'].format(path)
        )
        return False
    except Exception as e:
        messagebox(
            lang['error.generic.title'],
            lang['error.generic.write.body'].format(path, e)
        )
        return False

def loadData(path: str, default: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            ret = f.read()
            return ret
    except FileNotFoundError:
        writeFile(path, default)
        return default
    except PermissionError:
        messagebox(
            lang['error.permission.title'],
            lang['error.permission.read.body'].format(path)
        )
        return default
    except json.JSONDecodeError:
        messagebox(
            lang['error.json.title'],
            lang['error.json.body'].format(path) + \
                ' ' + \
                lang['error.json.submessage.overwrite']
            )
        writeFile(path, default)
        return default
    except Exception as e:
        messagebox(
            lang['error.generic.title'],
            lang['error.generic.read.body'] + \
            ' ' + \
            lang['error.json.submessage.attempt']
        )
        writeFile(path, default)
        return default

# theme settings
def theme() -> None:
    def close() -> None:
        data['theme']['global'] = globalTheme.get()
        saveData(data)
        win.destroy()
    win = tk.Toplevel()
    win.wait_visibility()
    win.transient(root)
    win.grab_set()
    win.group(root)
    win.attributes("-type", "dialog")
    win.title(lang['theme.title'])
    win.config(bg=color)
    ttk.Label(win, text=lang['theme.label.global'], font=1).pack()
    globalTheme=tk.IntVar(value=data['theme']['global'])
    auto = ctk.CTkRadioButton(
        win,
        variable=globalTheme,
        value=0,
        text=lang['theme.option.auto']
    )
    auto.pack()
    dark = ctk.CTkRadioButton(
        win,
        variable=globalTheme,
        value=1,
        text=lang['theme.option.dark']
    )
    dark.pack()
    light = ctk.CTkRadioButton(
        win,
        variable=globalTheme,
        value=2,
        text=lang['theme.option.light']
    )
    light.pack()
    ttk.Label(win, text=lang['theme.warn.restart']).pack()
    win.protocol('WM_DELETE_WINDOW', close)

# construct the main window with all of it's widgets
def mainWindow() -> None:
    global root
    global listbox
    global typeVar
    global valVar
    global view
    global edit
    global addButton
    global removeButton
    global file
    global valueEntry

    root = tk.Tk()
    root.configure(bg = color)
    root.title(lang['window.title'])
    root.geometry('1000x800')
    if OS == 'Windows':
        root.state('zoomed')
    elif OS != 'Darwin':
        root.attributes('-zoomed', True)
    
    root.focus()

    listbox = ResizableListbox(
        root,
        width=800,
        fg_color=color,
        hover_color='#646cff',
        highlight_color='#4b50d8',
        text_color=fore
    )
    listbox.pack()
    for i in file:
        listbox.insert(tk.END, i)
    listbox.bind('<<ListboxSelect>>', configure)

    ttk.Label(root, text='Type').pack()
    typeVar = tk.StringVar()
    type_ = ctk.CTkEntry(
        root,
        state='readonly',
        textvariable=typeVar,
        justify='center',
        width=200,
        fg_color=color,
        border_color='#646cff',
        bg_color=color,
        text_color=fore
    )
    type_.pack()

    ttk.Label(root, text='Value').pack()
    valVar = tk.StringVar()
    valueEntry = ctk.CTkEntry(
        root,
        state='readonly',
        textvariable=valVar,
        width=800,
        justify='center',
        fg_color=color,
        border_color='#646cff',
        bg_color=color,
        text_color=fore
    )
    valueEntry.pack()
    valueEntry.bind(
        '<Return>',
        lambda e: directEdit(
            root,
            file,
            typeVar,
            valueEntry.get(),
            key=listbox.get(listbox.curselection())
        )
    )
    valueEntry.bind(
        '<FocusOut>',
        lambda e: directEdit(root, file, typeVar, valueEntry.get(),
        key=listbox.get(listbox.curselection()))
    )

    view = StyledButton(
        root,
        text=lang['window.button.complex'],
        cursor='hand2',
        state='disabled'
    )
    view.pack()

    edit = StyledButton(
        root,
        text=lang['window.button.edit'],
        cursor='hand2',
        state='disabled', 
        command=lambda: editValue(root, file, key=listbox.get(listbox.curselection()))
    )
    edit.pack()

    addButton = StyledButton(
        root,
        text=lang['window.button.add'],
        cursor='hand2', 
        command=lambda: addNewItem(root, file)
    )
    addButton.pack()

    removeButton = StyledButton(
        root,
        text=lang['window.button.remove'],
        cursor='hand2',
        state='disabled',
        command=lambda: removeItem(root, file, key=listbox.get(listbox.curselection()))
    )
    removeButton.pack()

    # menu bar
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff = 0)
    filemenu.add_command(label=lang['menubar.file.open'], command=load)
    filemenu.add_command(label=lang['menubar.file.save'], command=save)
    filemenu.add_command(
        label=lang['menubar.file.saveas'],
        command=lambda: save(saveas=True)
    )
    filemenu.add_separator()
    filemenu.add_command(label=lang['menubar.file.exit'], command=close)
    menubar.add_cascade(label=lang['menubar.file'], menu=filemenu)
    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(label=lang['menubar.edit.add'], command=addButton.invoke)
    editmenu.add_command(label=lang['menubar.edit.plaintext'], command=plainText)
    menubar.add_cascade(label=lang['menubar.edit'], menu=editmenu)
    about = tk.Menu(menubar, tearoff = 0)
    about.add_command(
        label=lang['menubar.about.website'],
        command=lambda: webbrowser.open(LINKS['website'])
    )
    about.add_command(
        label=lang['menubar.about.repo'],
        command=lambda: webbrowser.open(LINKS['repo'])
    )
    about.add_command(
        label=lang['menubar.about.license'],
        command=JSONly.License.showLicense
    )
    menubar.add_cascade(label=lang['menubar.about'], menu=about)
    settingmenu = tk.Menu(menubar, tearoff=0)
    settingmenu.add_command(label=lang['menubar.settings.theme'], command=theme)
    settingmenu.add_command(label=lang['menubar.settings.preferences'], command=settings)
    menubar.add_cascade(label=lang['menubar.settings'], menu=settingmenu)
    if OS != 'Windows':
        for menu in (menubar, filemenu, editmenu, about, settingmenu):
            menu.configure(
                bg=color,
                fg=fore,
                activebackground='#646cff',
                activeforeground='#cccccc'
            )
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

# display complex value
def display(val) -> None:
    index = 0
    disp = tk.Toplevel(root)
    disp.configure(bg = color)
    disp.geometry('1000x800')
    disp.title('JSONly (complex value)')
    disp.wait_visibility()
    disp.transient(root)
    disp.group(root)
    disp.attributes("-type", "dialog")
    disp.focus()
    
    listbox = ResizableListbox(
        disp,width=800,
        fg_color=color,
        hover_color='#646cff',
        highlight_color='#4b50d8',
        text_color=fore
    )
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
        if listbox.curselection() is not None:
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
                edit.configure(
                    state='normal',
                    command=lambda: editValue(disp, val, typeVar, valVar, key=key)
                )
            
            removeButton.configure(state='normal')
        else:
            removeButton.configure(state='disabled')
            view.configure(state='disabled')
            edit.configure(state='disabled')
            valueEntry.configure(state='readonly')

    def directEdit(
        parent,
        otherVal,
        typeVar: tk.StringVar,
        value,
        key=None,
        index=None
    ) -> None:
        newValue = value
        if typeVar.get() == lang['window.types'][1]:
            try:
                newValue = int(float(newValue))
            except ValueError:
                newValue = 1
        elif typeVar.get() == lang['window.types'][2]:
            try:
                newValue = float(newValue)
            except ValueError:
                newValue = 1.0
        elif typeVar.get() == lang['window.types'][3]:
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
    type_ = ctk.CTkEntry(
        disp,
        state='readonly',
        textvariable=typeVar,
        justify='center',
        width=200,
        fg_color=color, 
        border_color='#646cff',
        bg_color=color,
        text_color=fore
    )
    type_.pack()
    ttk.Label(disp, text='Value').pack()
    valVar = tk.StringVar()
    valueEntry = ctk.CTkEntry(
        disp,
        state='readonly',
        textvariable=valVar,
        justify = 'center',
        width = 800,
        fg_color=color,
        border_color='#646cff',
        bg_color=color,
        text_color=fore
    )
    valueEntry._entry.config(insertbackground=fore)
    valueEntry.pack()
    if isinstance(val, dict):
        valueEntry.bind(
            '<Return>',
            lambda e: directEdit(
                disp,
                file,
                typeVar,
                valueEntry.get(),
                key=listbox.get(listbox.curselection())
            )
        )
        valueEntry.bind(
            '<FocusOut>',
            lambda e: directEdit(
                disp,
                file,
                typeVar,
                valueEntry.get(),
                key=listbox.get(listbox.curselection())
            )
        )
    else:
        valueEntry.bind(
            '<Return>',
            lambda e: directEdit(
                disp,
                file,
                typeVar,
                valueEntry.get(),
                index=listbox.curselection()
            )
        )
        valueEntry.bind(
            '<FocusOut>',
            lambda e: directEdit(
                disp,
                file,
                typeVar,
                valueEntry.get(),
                index=listbox.curselection()
            )
        )
    view = StyledButton(
        disp,
        text=lang['window.button.complex'],
        cursor='hand2',
        state='disabled'
    )
    view.pack()
    edit = StyledButton(
        disp,
        text=lang['window.button.edit'],
        cursor='hand2',
        state='disabled'
    )
    edit.pack()
    addButton = StyledButton(
        disp,
        text=lang['window.button.add'],
        cursor='hand2', 
        command=lambda: addNewItem(disp, val)
    )
    addButton.pack()

    removeButton = StyledButton(
        disp,
        text=lang['window.button.remove'],
        cursor='hand2',
        state='disabled',
        command=lambda: removeItem(disp, val, 
        key=listbox.get(listbox.curselection()) if isinstance(val, dict) else None,
        index=listbox.curselection() if isinstance(val, list) else None)
    )
    removeButton.pack()

    disp.bind("<<ValueEdited>>", lambda e: configure())
    disp.bind("<<ItemAdded>>", lambda e: refreshListbox())
    disp.bind("<<ItemRemoved>>", lambda e: refreshListbox())

# next three functions are for finding objects
def findWindow(listbox: tk.Listbox) -> None:
    def close() -> None:
        global findmode, findWord
        findWord = findEntry.get()
        findWin.destroy()
    findWin = tk.Toplevel(root)
    findWin.wait_visibility()
    findWin.transient(root)
    findWin.grab_set()
    findWin.group(root)
    findWin.attributes("-type", "dialog")
    findWin.configure(bg=color)
    findWin.focus()
    findWin.overrideredirect(True)
    # Calculate the center coordinates of the main window
    root.update_idletasks()
    rootWidth = root.winfo_width()
    rootHeight = root.winfo_height()
    x_center = root.winfo_rootx() + rootWidth // 2
    y_center = root.winfo_rooty() + rootHeight // 2
    
    # Calculate the offset to position the Toplevel window in the center of the main window
    findWin_width = findWin.winfo_width()
    findWin_height = findWin.winfo_height()
    x_offset = (x_center - findWin_width // 2 ) - 100
    y_offset = (y_center - findWin_height // 2) + 20
    
    findWin.geometry(f"+{x_offset}+{y_offset}")
    findEntry = ctk.CTkEntry(
        findWin,
        width = 200,
        fg_color=color,
        border_color='#646cff',
        bg_color=color,
        text_color=fore
    )
    findEntry._entry.config(insertbackground=fore)
    findEntry.pack(side = 'left')
    findEntry.focus()
    findEntry.insert(0, findWord)
    findEntry.select_range(0, tk.END)
    nextBtn = StyledButton(
        findWin,
        text = '↓',
        command = lambda:
        findNext(findEntry.get(), listbox),
        width = 5
    )
    nextBtn.pack(side = 'left')
    prevBtn = StyledButton(findWin, text = '↑', command = lambda: findPrev(findEntry.get(), listbox), width = 5)
    prevBtn.pack(side = 'left')
    closeBtn = StyledButton(findWin, text = '×', command = close, width = 5)
    closeBtn.pack(side = 'left')
    findWin.bind('<Return>', lambda event: findNext(findEntry.get(), listbox))
    findWin.bind('<Down>', lambda event: findNext(findEntry.get(), listbox))
    findWin.bind('<Up>', lambda event: findPrev(findEntry.get(), listbox))

def findNext(searchKey: str, listbox: tk.Listbox):
    if searchKey:
        items = listbox.get(0, 'end')
        currentSelection = listbox.curselection()
        if currentSelection:
            currentIndex = currentSelection[0]
        else:
            currentIndex = -1  # Set a default index when nothing is selected
        
        found = False
        for i in range(currentIndex + 1, len(items)):
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
        currentSelection = listbox.curselection()
        if currentSelection:
            currentIndex = currentSelection[0]
        else:
            currentIndex = len(items)  # Set a default index when nothing is selected
        
        found = False
        for i in range(currentIndex - 1, -1, -1):
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
    try:
        with open(dataFile, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except PermissionError:
        messagebox(lang['error.permission.title'], lang['error.permission.write.body'].format(dataFile))
    except Exception as e:
        messagebox(lang['error.generic.title'], lang['error.generic.write.body'].format(dataFile, e))

# context menu
def context(event: tk.Event) -> None:
    contextMenu = tk.Menu(root, tearoff=0)
    contextMenu.add_command(label=lang['contextmenu.save'], command=save)
    contextMenu.add_command(label=lang['contextmenu.saveas'], command=lambda: save(saveas=True))
    contextMenu.add_command(label=lang['contextmenu.open'], command=load)
    contextMenu.add_separator()
    contextMenu.add_command(label=lang['contextmenu.add'], command=addButton.invoke)
    contextMenu.add_command(label=lang['contextmenu.remove'], command=removeButton.invoke)
    contextMenu.add_separator()
    contextMenu.add_command(label=lang['contextmenu.plaintext'], command=plainText)
    contextMenu.tk_popup(event.x_root, event.y_root)
    if OS != 'Windows':
        contextMenu.configure(
            bg=color,
            fg=fore,
            activebackground='#646cff',
            activeforeground='#cccccc'
        )

# a custom button class, useless outside of this program, pre-sets a lot of things that were causing repitition
class StyledButton(ctk.CTkButton):
    def __init__(
            self,
            master,
            width=200,
            height=40,
            text='',
            cursor='arrow',
            state='normal',
            command=None
        ) -> None:
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
        super().__init__(
            master, 
            width,
            height,
            fg_color='#646cff',
            hover_color='#4b50d8',
            border_color=border_color,
            border_width=2,
            bg_color=bg_color,
            text=text,
            cursor=cursor,
            state=state,
            command=command
        )
    
    def changeTheme(self) -> None:
        match data['theme']['global']:
            case 0:
                self.border_color = color
                self.bg_color = color
            case 1:
                self.border_color = fore
                self.bg_color = fore
        super().configure(bg_color=self.bg_color, border_color=self.border_color)

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
            padding = 300  # padding for buttons
            available = max(self._master.winfo_height() - padding, 1)  # Prevent negative or zero height
            super().configure(height=available)

# load save data
dataFile = os.path.join(CONFIGDIR, 'settings.json')
os.makedirs(CONFIGDIR, exist_ok=True)
os.makedirs(DATADIR, exist_ok=True)
try:
    data = json.loads(loadData(dataFile, r'{}'))
except json.JSONDecodeError:
    messagebox(lang['error.json.title'], lang['error.json.body'].format(dataFile) + ' ' + lang['error.json.submessage.overwrite'])
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
if 'lang' not in data['preferences'].keys():
    data['preferences']['lang'] = 'en_US.json'
    saveData(data)

themeData = data['theme']['global']
if themeData == 0:
    if darkdetect.isLight():
        color = 'white'
        fore = 'black'
    else:
        color = '#1e1e2e'
        fore = 'white'
elif themeData == 1:
    color = '#1e1e2e'
    fore = 'white'
else:
    color = 'white'
    fore = 'black'

if os.path.dirname(data['preferences']['lang']) == '':
    langPath = os.path.join(
        RESOURCEDIR,
        'lang',
        data['preferences']['lang']
    )
else:
    langPath = data['preferences']['lang']
lang = JSONly.lang.loadData(langPath)

# display messages in a pop-up, below others because it needs the 'lang' variable to be set
def messagebox(title, message, buttons=(lang['popup.button.ok'],), callback=None, geometry='400x150'):
    # Create a new window
    window = tk.Toplevel()
    window.configure(bg=color)
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
    def onButtonClick(btnText):
        nonlocal endVal
        if callback:
            callback(btnText)
        endVal = btnText
        window.destroy()
    
    endVal = 'closed'

    # Add buttons
    for buttonText in buttons:
        button = StyledButton(
            buttonFrame,
            text=buttonText,
            command=lambda bt=buttonText: onButtonClick(bt),
            height=30,
            width = 100
        )
        button.pack(side=tk.LEFT, padx=5)

    # Center the window on the screen
    window.update_idletasks()

    window.attributes('-topmost', True)
    window.wait_visibility()
    window.transient(root)
    window.grab_set()
    window.group(root)
    window.attributes("-type", "dialog")
    window.protocol('WM_DELETE_WINDOW', lambda: onButtonClick(buttons[-1]))
    window.wait_window()
    return endVal

root = mainWindow()
img = tk.PhotoImage(file=os.path.join(RESOURCEDIR, 'icon.png'))
root.iconphoto(True, img)
# styling ttk widgets
style = ttk.Style()
style.theme_use('alt')
style.configure('TLabel', background=color, foreground=fore)
style.configure('TFrame', background=color)

if len(sys.argv) > 1:
    print('opened:', sys.argv[1])
    load(filePath=sys.argv[1])

root.mainloop()
