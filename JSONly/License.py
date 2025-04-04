# Copyright (c) 2025 Luke Moyer
# Licensed under the MIT License. See LICENSE file for details.

# file that displays JSONly's license (MIT)
import tkinter as tk
from tkinter import ttk
import webbrowser
from JSONly.constants import *

with open(os.path.join(RESOURCEDIR, 'LICENSE'), 'r') as f:
    LICENSE = f.read()

class Hyperlink(tk.Label):
    '''A simple hyperlink that opens a website when clicked.\n
    New parameters:\n
    • url - the website that is connected to the hyperlink\n
    • changeColor - whether or not to change color when hovered over\n
    • same - if true and no text or textvariable is given, text is the same as url'''
    def __init__(self, master: tk.Misc | None = None, *, url: str, font: str | list | tuple = 'Helvetica 10 underline', highlightcolor: str = 'blue', same: bool = True, changeColor: bool = True, **kwargs) -> None:
        if not (url.startswith('https://') or url.startswith('http://')):
            url = 'http://' + url
        if kwargs['text'] is None:
            if same:
                kwargs['text'] = url
            else:
                kwargs['text'] = ''
        self.changeColor = changeColor
        self.same = same
        self.url = url
        super().__init__(master, activeforeground='#4FC3F7', disabledforeground='#4FC3F7', fg='#4FC3F7', font=font, foreground='#4FC3F7', highlightcolor=highlightcolor, **kwargs)
    
    # handle url clicked
    def _onClick(self, event = None) -> None:
        webbrowser.open_new_tab(self.url)

    # handle mouse enters url
    def _onEnter(self, event = None) -> None:
        self.configure(foreground = '#0077FF', activeforeground = '#0077FF')

    # handle mouse leave url
    def _onLeave(self, event = None) -> None:
        self.configure(foreground = '#4FC3F7', activeforeground = '#4FC3F7')

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

def showLicense() -> None:
    # Create a new window for the license
    licenseWin = tk.Toplevel()
    licenseWin.configure(bg = '#1e1e2e')
    licenseWin.title(f'License - JSONly')
    licenseWin.focus()
    # licenseWin.geometry(f'805x550+{root.winfo_x()}+{root.winfo_y()}')

    # Frame to hold the text widget and scrollbar
    textFrame = ttk.Frame(licenseWin)
    textFrame.pack(fill='both', expand=True, padx=10, pady=10)

    # Text widget to display the license
    licenseText = tk.Text(
        textFrame, wrap='word', bg='#1e1e2e',
        fg='white', font='Helvetica 12', state='normal'
    )
    licenseText.insert('1.0', LICENSE)  # Insert license text
    licenseText.configure(state='disabled')  # Make it read-only
    licenseText.pack(side='left', fill='both', expand=True)

    # Scrollbar for the text widget
    textScrollbar = ttk.Scrollbar(textFrame, orient='vertical', command=licenseText.yview)
    licenseText.configure(yscrollcommand=textScrollbar.set)
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
        linkFrame, text='MIT License',
        url='https://opensource.org/license/mit', cursor='hand2',
        bg='#1e1e2e'
    ).pack()
