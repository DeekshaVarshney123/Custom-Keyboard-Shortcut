import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
import threading
import subprocess

from shortcut_manager import ShortcutManager
from gui_windows import CreateShortcutWindow, ViewShortcutsWindow, EditShortcutWindow

# App Class: Poore application ka control center
class App(tk.Tk):
    """Main application window, jo saari sub-windows aur logic ko manage karti hai."""
    def __init__(self):
        super().__init__()
        self.title("Custom Shortcut App")
        self.geometry("600x400")
        
        # ShortcutManager ka object banate hain, jisse hum data ko access kar payenge.
        self.shortcut_manager = ShortcutManager()
        self.current_window = None

        # Application shuru hote hi background keyboard listener ko shuru karo.
        self.start_global_listener()
        
        # Application shuru hote hi 'Create Shortcut' window dikhao.
        self.show_create_shortcut_window()

    def show_create_shortcut_window(self):
        """'Create Shortcut' window dikhata hai."""
        if self.current_window:
            self.current_window.destroy()
        self.current_window = CreateShortcutWindow(self)

    def show_view_shortcuts_window(self):
        """'View Shortcuts' window dikhata hai."""
        if self.current_window:
            self.current_window.destroy()
        self.current_window = ViewShortcutsWindow(self)

    def show_edit_shortcut_window(self, shortcut, action):
        """'Edit Shortcut' window dikhata hai."""
        if self.current_window:
            self.current_window.destroy()
        self.current_window = EditShortcutWindow(self, shortcut, action)

    def start_global_listener(self):
        """Global keyboard listener ko background thread mein shuru karta hai."""
        # threading.Thread se hum listener ko ek alag thread mein chalate hain,
        # taaki GUI freeze na ho.
        self.listener_thread = threading.Thread(target=self._run_listener, daemon=True)
        self.listener_thread.start()

    def _run_listener(self):
        """pynput listener ka function."""
        with keyboard.Listener(on_press=self._on_press) as listener:
            listener.join()

    def _on_press(self, key):
        """Keyboard press events par call hone wala function."""
        try:
            # key object se key ka naam nikalte hain.
            key_name = key.name.lower() if hasattr(key, 'name') else key.char
            
            # Modifier keys (Alt, Control) ke saath shortcut check karte hain.
            if key_name and keyboard.Controller().alt_pressed:
                key_sequence = f"<Alt-{key_name}>"
                self._execute_shortcut(key_sequence)
            elif key_name and keyboard.Controller().ctrl_pressed:
                key_sequence = f"<Control-{key_name}>"
                self._execute_shortcut(key_sequence)
            elif key_name:
                key_sequence = f"<{key_name}>"
                self._execute_shortcut(key_sequence)
        except AttributeError:
            pass

    def _execute_shortcut(self, key_sequence):
        """Shortcut se jude action ko run karta hai."""
        shortcuts = self.shortcut_manager.get_shortcuts()
        if key_sequence in shortcuts:
            action = shortcuts[key_sequence]
            try:
                # subprocess.Popen se command run karte hain.
                subprocess.Popen(action, shell=True)
                print(f"Executing: {action}")
            except Exception as e:
                print(f"Command run karne mein error: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
