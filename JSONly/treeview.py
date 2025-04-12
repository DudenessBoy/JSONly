import customtkinter
from CTkListbox import CTkListbox
import tkinter as tk


class TreeView(CTkListbox):
    def __init__(self, master, height=100, width=150, values=None, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.values = values or {}
        self._config_values(self.values)

    def _config_values(self, values, level=0, parent=None):
        """
        Recursively configure the tree structure with expandable/collapsible nodes.
        """
        for key, value in values.items():
            # Indent child items
            indent = " " * (level * 4)
            is_expandable = isinstance(value, (dict, list))

            # Create the button for the current item
            display_text = f"{indent}{key}"
            btn = self.insert(tk.END, display_text, update=False)

            # Initialize attributes for expandable items
            btn.children_visible = False  # Tracks if children are visible
            btn.child_buttons = []  # Holds references to child buttons

            if is_expandable:
                # Add arrow button for expandable items
                arrow = customtkinter.CTkButton(
                    self,
                    text="▶",  # Initially collapsed arrow
                    width=20,
                    command=lambda b=btn, v=value: self.toggle_children(b, v, level + 1),
                )
                arrow.grid(row=btn.grid_info()["row"], column=0, sticky="w")
                btn.arrow_button = arrow  # Store reference to the arrow button

    def toggle_children(self, button, children, level):
        """
        Toggles the visibility of child items.
        """
        if not hasattr(button, "children_visible"):
            # Ensure the button has the necessary attributes
            button.children_visible = False
            button.child_buttons = []

        if button.children_visible:
            # Hide children
            for child in button.child_buttons:
                child.grid_remove()
            button.children_visible = False
            # Change arrow to collapsed state
            button.arrow_button.configure(text="▶")
        else:
            # Show children
            if not button.child_buttons:  # If children haven't been created yet
                self._add_children(button, children, level)
            for child in button.child_buttons:
                child.grid()
            button.children_visible = True
            # Change arrow to expanded state
            button.arrow_button.configure(text="▼")

    def _add_children(self, parent, children, level):
        """
        Adds child buttons for a given parent.
        """
        if isinstance(children, dict):
            items = children.items()
        elif isinstance(children, list):
            items = enumerate(children)  # Convert list to index-value pairs

        # Track the current row
        current_row = parent.grid_info()["row"] + 1  # Start directly under the parent

        for key, value in items:
            is_expandable = isinstance(value, (dict, list))

            # Create the child button with indentation for alignment
            child_text = str(key)  # Display key as text
            child_button = customtkinter.CTkButton(
                self,
                text=child_text,
                width=150 - (level * 20),  # Reduce width for indentation
                anchor="w",  # Align text to the left
            )
            child_button.grid(row=current_row, column=1, padx=(level * 20, 0), sticky="w")  # Indent child buttons
            child_button.children_visible = False  # Initialize visibility
            child_button.child_buttons = []  # Initialize child buttons list

            parent.child_buttons.append(child_button)

            if is_expandable:
                # Add arrow button for expandable children
                arrow = customtkinter.CTkButton(
                    self,
                    text="▶",
                    width=20,
                    command=lambda b=child_button, v=value: self.toggle_children(b, v, level + 1),
                )
                arrow.grid(row=current_row, column=0, sticky="w")  # Place arrow in same row as child
                child_button.arrow_button = arrow  # Store reference to the arrow button

            # Increment the row for the next child
            current_row += 1


if __name__ == '__main__':
    root = tk.Tk()
    treeview = TreeView(
        root,
        values={
            'test1': 1,
            'test2': [1, 2, {'list1': 1, 'list2': 2}],
            'test3': {'one': 1, 'two': ['obj1', 'obj2']}
        },
        button_color='black',
        height=200,
        width=200
    )
    treeview.pack()
    root.mainloop()