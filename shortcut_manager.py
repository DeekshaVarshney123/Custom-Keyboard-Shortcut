import json
import os

class ShortcutManager:
    """Manages all shortcut data, including file I/O and validation."""
    
    def __init__(self, filename="shortcuts.json"):
        self.filename = filename
        self.shortcuts = {}
        self.load_shortcuts()

    def load_shortcuts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.shortcuts = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.shortcuts = {}

    def save_shortcuts(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.shortcuts, f, indent=4, ensure_ascii=False)

    def add_shortcut(self, key_sequence, action):
        if self.is_shortcut_or_action_exist(key_sequence, action):
            return False, "Shortcut ya action pehle se maujood hai."
        self.shortcuts[key_sequence] = action
        self.save_shortcuts()
        return True, "Shortcut successfully create ho gaya."

    def delete_shortcut(self, key_sequence):
        if key_sequence in self.shortcuts:
            del self.shortcuts[key_sequence]
            self.save_shortcuts()
            return True
        return False

    def update_shortcut(self, old_key, new_key, new_action):
        if self.is_shortcut_or_action_exist(new_key, new_action, old_key):
            return False, "Shortcut ya action pehle se maujood hai."
        
        if self.delete_shortcut(old_key):
            self.shortcuts[new_key] = new_action
            self.save_shortcuts()
            return True, "Shortcut update ho gaya."
        return False, "Shortcut update nahi ho paya."

    def is_shortcut_or_action_exist(self, key_sequence, action, ignore_key=None):
        if key_sequence in self.shortcuts and key_sequence != ignore_key:
            return True
        for key, value in self.shortcuts.items():
            if value == action and key != ignore_key:
                return True
        return False

    def get_shortcuts(self):
        return self.shortcuts
