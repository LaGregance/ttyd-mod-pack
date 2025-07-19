import tkinter as tk

from tools.dialog_editor.ttyd_txt_parser import TTYDTxtParser
from tools.shared.constants import RAW_ROM_MESSAGE_FOLDER


class EditTextDialog(tk.Toplevel):
    def __init__(self, root, file, text_id, text):
        super().__init__(root)
        self.on_validate = None
        self.transient(root)
        self.grab_set()

        self.is_new = text_id is None
        self.file = file
        self.text_id = text_id

        if self.is_new:
            self.title(f"Add text to {file}")
        else:
            self.title(f"{file} {text_id}")

        # Frame to contain text and button vertically
        container = tk.Frame(self)
        container.pack(fill='both', expand=True, padx=10, pady=10)

        if self.is_new:
            tk.Label(container, text=f"Map: {file}", justify="left", anchor='w').pack(expand=True, fill='x')

            key_frame = tk.Frame(container)
            key_frame.pack(fill='x', pady=1)

            tk.Label(key_frame, text="Key: ", justify="left").pack(side="left")

            key_input = tk.Entry(key_frame, font=("TkFixedFont", 12))
            key_input.pack(fill='x', expand=True, side="left")
            key_input.focus()

        input = tk.Text(container, font=("TkFixedFont", 12))
        input.insert(tk.END, text)
        input.pack(fill='both',padx=1, pady=1, expand=True)

        if not self.is_new:
            input.focus()

        button = tk.Button(container, text="Valider", command=lambda: self.__validate_edition(input.get(1.0, tk.END).strip(), key_input.get().strip() if self.is_new else None))
        button.pack(fill='x',padx=1, pady=10, expand=True)

    def set_on_validate_listener(self, callback):
        self.on_validate = callback

    def __validate_edition(self, text, new_key):
        if self.is_new and not new_key:
            return

        self.destroy()

        parser = TTYDTxtParser(RAW_ROM_MESSAGE_FOLDER + '/' + self.file)
        parser.load()

        parser.set(new_key if self.is_new else self.text_id, text)
        parser.save()

        if self.on_validate:
            self.on_validate()
