
import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
import threading
import subprocess

from shortcut_manager import ShortcutManager
from gui_windows import CreateShortcutWindow, ViewShortcutsWindow, EditShortcutWindow

class App(tk.Tk):
    """Main application window, jo saari sub-windows aur logic ko manage karti hai."""
    def __init__(self):
        super().__init__()
        self.title("Custom Shortcut App")
        self.geometry("600x400")
        self.pressed_keys = set()
        self.shortcut_manager = ShortcutManager()
        self.current_window = None

        self.start_global_listener()
        self.show_create_shortcut_window()

    # --- GUI Window Methods ---
    def show_create_shortcut_window(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = CreateShortcutWindow(self)

    def show_view_shortcuts_window(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = ViewShortcutsWindow(self)

    def show_edit_shortcut_window(self, shortcut, action):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = EditShortcutWindow(self, shortcut, action)

    # --- Keyboard Listener ---
    def start_global_listener(self):
        self.listener_thread = threading.Thread(target=self._run_listener, daemon=True)
        self.listener_thread.start()

    def _run_listener(self):
        with keyboard.Listener(on_press=self._on_press, on_release=self._on_release) as listener:
            listener.join()

    def _on_press(self, key):
        self.pressed_keys.add(key)
        key_sequence = self._format_key_sequence()
        if key_sequence:
            self._execute_shortcut(key_sequence)

    def _on_release(self, key):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)


    def _format_key_sequence(self):
       """Pressed keys ko normalized format me convert kare, consistent and reliable."""
       seq = []

    # Modifier keys ko normalize karo
       if any(k in self.pressed_keys for k in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]):
          seq.append("Control")
       if any(k in self.pressed_keys for k in [keyboard.Key.alt_l, keyboard.Key.alt_r]):
          seq.append("Alt")
       if any(k in self.pressed_keys for k in [keyboard.Key.shift_l, keyboard.Key.shift_r]):
          seq.append("Shift")

    # Main key
       main_key = None
       for key in self.pressed_keys:
        # Skip modifier keys
           if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
                   keyboard.Key.alt_l, keyboard.Key.alt_r,
                   keyboard.Key.shift_l, keyboard.Key.shift_r]:
               continue
           if hasattr(key, 'char') and key.char:
               main_key = key.char.lower()
           elif hasattr(key, 'name'):
               main_key = key.name.lower()

       if main_key:
          seq.append(main_key)

       if seq:
          formatted = f"<{'-'.join(seq)}>"
          print("DEBUG: Detected ->", formatted)  # debug print
          return formatted

       return None



    def _execute_shortcut(self, key_sequence):
        shortcuts = self.shortcut_manager.get_shortcuts()
        if key_sequence in shortcuts:
            action = shortcuts[key_sequence]
            try:
                if action.startswith("http://") or action.startswith("https://"):
                   import webbrowser
                   webbrowser.open(action)
                else:
                   subprocess.Popen(action, shell=True)
                   print(f"Executing: {action}")
            except Exception as e:
                print(f"Error executing command: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
