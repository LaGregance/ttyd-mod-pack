import os
import tkinter as tk
from tkinter import ttk

from tools.dialog_editor.ttyd_txt_parser import TTYDTxtParser
from tools.shared.map.map_helpers import get_all_area_names
from tools.shared.ux.autocomplete_combobox import AutocompleteCombobox

msg_dir = 'raw_rom/files/msg/US'

def get_results(selected_area_id, search_query):

    result = []
    all_files = []
    with os.scandir(msg_dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.txt'):
                # Check area filter
                if not selected_area_id or entry.name.startswith(selected_area_id):
                    all_files.append(entry.name)

    for file in all_files:
        parser = TTYDTxtParser(msg_dir + '/' + file)
        parser.load()

        if not search_query:
            for key, value in parser.content.items():
                result.append(f"{file} {key}: {value}")
        else:
            for key, value in parser.search(search_query):
                result.append(f"{file} {key}: {value}")

        if len(result) > 100:
            break

    return result


def update_results(*args):
    selected_area_id = current_area_name.get().split(" ")[0]
    search_query = current_search.get()
    results = get_results(selected_area_id, search_query)

    # Clear current list
    result_list.delete(0, tk.END)

    # Insert new results
    for item in results:
        result_list.insert(tk.END, item)


def on_double_click(event):
    widget = event.widget
    index = widget.nearest(event.y)

    splitted_0 = widget.get(index).split(": ")
    splitted_1 = splitted_0[0].split(" ")
    text = splitted_0[1]
    file = splitted_1[0]
    text_id = splitted_1[1]

    dialog = tk.Toplevel(root)
    dialog.transient(root)
    dialog.title(f"{file} {text_id}")

    # Frame to contain text and button vertically
    container = tk.Frame(dialog)
    container.pack(fill='both', expand=True)

    input = tk.Text(container, font=("TkFixedFont", 12))
    input.insert(tk.END, text)
    input.pack(fill='both',padx=1, pady=1, expand=True)

    button = tk.Button(container, text="Valider", command=lambda: validate_edition(dialog, file, text_id, input.get(1.0, tk.END)))
    button.pack(fill='x',padx=1, pady=10, expand=True)

def validate_edition(dialog, file, text_id, text):
    dialog.destroy()

    parser = TTYDTxtParser(msg_dir + '/' + file)
    parser.load()

    parser.set(text_id, text)
    parser.save()


# Create main window
root = tk.Tk()
root.title("TTYD Dialog Editor")
root.geometry("1000x800")

# Map/Area select
area_label = tk.Label(root, text="Map/Area:", justify="left")
area_label.pack(anchor="w", padx=10, pady=(10, 0))

current_area_name = tk.StringVar()
area_menu = AutocompleteCombobox(root, textvariable=current_area_name, completevalues=["", *get_all_area_names()])
area_menu.pack(fill=tk.X, padx=10, pady=(0, 5))
area_menu.bind("<<ComboboxSelected>>", update_results)

# Search bar
search_label = tk.Label(root, text="Search:", justify="left")
search_label.pack(anchor="w", padx=10)

current_search = tk.StringVar()
search_entry = ttk.Entry(root, textvariable=current_search)
search_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
current_search.trace_add("write", update_results)

# Listbox to show results
result_list = tk.Listbox(root, height=200)
result_list.pack(pady=10, fill=tk.BOTH, expand=True, padx=15)
result_list.bind("<Double-Button-1>", on_double_click)

# Initial population
update_results()

# Run the application
root.mainloop()
