import tkinter as tk
from tkinter import ttk, messagebox

# --- GUI Window Classes ---

class CreateShortcutWindow(ttk.Frame):
    """Naye shortcuts banane ke liye window."""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill="both", expand=True, padx=10, pady=10)

        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 20))
        
        heading = ttk.Label(header_frame, text="CREATE YOUR SHORTCUT", font=("Helvetica", 16, "bold"))
        heading.pack(side="left")

        view_button = ttk.Button(header_frame, text="VIEW", command=self.parent.show_view_shortcuts_window)
        view_button.pack(side="right")
        
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Shortcut Key (e.g., <Control-c>, <Alt-b>):").grid(row=0, column=0, sticky="w", pady=5)
        self.key_entry = ttk.Entry(form_frame, width=40)
        self.key_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Action to Perform (e.g., notepad.exe):").grid(row=1, column=0, sticky="w", pady=5)
        self.action_entry = ttk.Entry(form_frame, width=40)
        self.action_entry.grid(row=1, column=1, pady=5)

        create_button = ttk.Button(self, text="CREATE", command=self.create_shortcut)
        create_button.pack(pady=20)

    def create_shortcut(self):
        key_sequence = self.key_entry.get().strip()
        action = self.action_entry.get().strip()
        if not key_sequence or not action:
            messagebox.showerror("Error", "Shortcut aur action dono zaroori hain.")
            return

        success, message = self.parent.shortcut_manager.add_shortcut(key_sequence, action)
        if success:
            messagebox.showinfo("Success", message)
            self.key_entry.delete(0, tk.END)
            self.action_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", message)

class ViewShortcutsWindow(ttk.Frame):
    """Shortcuts dekhne, edit karne, aur delete karne ke liye window."""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill="both", expand=True, padx=10, pady=10)

        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 20))
        
        back_button = ttk.Button(header_frame, text="< Back", command=self.parent.show_create_shortcut_window)
        back_button.pack(side="left")

        heading = ttk.Label(header_frame, text="YOUR SHORTCUTS", font=("Helvetica", 16, "bold"))
        heading.pack(side="left", padx=(100, 0))

        columns = ("Shortcut", "Action", "Edit", "Delete")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center")

        self.tree.bind("<ButtonRelease-1>", self.on_item_click)
        
        self.load_shortcuts()

    def load_shortcuts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        shortcuts = self.parent.shortcut_manager.get_shortcuts()
        for key, value in shortcuts.items():
            self.tree.insert("", tk.END, values=(key, value, "Edit", "Delete"))

    def on_item_click(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return

        col = self.tree.identify_column(event.x)
        values = self.tree.item(item, 'values')
        
        if values and col == "#3":
            self.parent.show_edit_shortcut_window(values[0], values[1])
        elif values and col == "#4":
            if messagebox.askyesno("Confirm Delete", f"Kya aap shortcut '{values[0]}' delete karna chahte hain?"):
                if self.parent.shortcut_manager.delete_shortcut(values[0]):
                    messagebox.showinfo("Success", "Shortcut delete ho gaya.")
                    self.load_shortcuts()

class EditShortcutWindow(ttk.Frame):
    """Shortcut edit karne ke liye window."""
    def __init__(self, parent, old_key, old_action):
        super().__init__(parent)
        self.parent = parent
        self.old_key = old_key
        self.old_action = old_action
        self.pack(fill="both", expand=True, padx=10, pady=10)

        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 20))

        back_button = ttk.Button(header_frame, text="< Back", command=self.parent.show_view_shortcuts_window)
        back_button.pack(side="left")

        heading = ttk.Label(header_frame, text="EDIT SHORTCUT", font=("Helvetica", 16, "bold"))
        heading.pack(side="left", padx=(100, 0))

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Shortcut Key:").grid(row=0, column=0, sticky="w", pady=5)
        self.key_entry = ttk.Entry(form_frame, width=40)
        self.key_entry.grid(row=0, column=1, pady=5)
        self.key_entry.insert(0, self.old_key)

        ttk.Label(form_frame, text="Action to Perform:").grid(row=1, column=0, sticky="w", pady=5)
        self.action_entry = ttk.Entry(form_frame, width=40)
        self.action_entry.grid(row=1, column=1, pady=5)
        self.action_entry.insert(0, self.old_action)
        
        save_button = ttk.Button(self, text="SAVE", command=self.save_edit)
        save_button.pack(pady=20)
        
    def save_edit(self):
        new_key = self.key_entry.get().strip()
        new_action = self.action_entry.get().strip()

        if not new_key or not new_action:
            messagebox.showerror("Error", "Shortcut aur action dono zaroori hain.")
            return

        success, message = self.parent.shortcut_manager.update_shortcut(self.old_key, new_key, new_action)
        if success:
            messagebox.showinfo("Success", message)
            self.parent.show_view_shortcuts_window()
        else:
            messagebox.showerror("Error", message)
