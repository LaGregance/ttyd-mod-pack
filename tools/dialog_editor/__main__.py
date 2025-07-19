import os
import tkinter as tk
from tkinter import ttk

from tools.dialog_editor.edit_text_dialog import EditTextDialog
from tools.dialog_editor.ttyd_txt_parser import TTYDTxtParser
from tools.shared.constants import RAW_ROM_MESSAGE_FOLDER
from tools.shared.map.map_helpers import get_all_area_names
from tools.shared.ux.autocomplete_combobox import AutocompleteCombobox

def get_results(selected_area_id, search_query):
    result = []
    all_files = []
    with os.scandir(RAW_ROM_MESSAGE_FOLDER) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.txt'):
                # Check area filter
                if not selected_area_id or entry.name.startswith(selected_area_id):
                    all_files.append(entry.name)

    for file in all_files:
        parser = TTYDTxtParser(RAW_ROM_MESSAGE_FOLDER + '/' + file)
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

    add_button["state"] = "normal" if len(selected_area_id) > 3 else "disabled"

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

    dialog = EditTextDialog(root, file, text_id, text)
    dialog.set_on_validate_listener(lambda: update_results())

def on_click_add():
    selected_area_id = current_area_name.get().split(" ")[0]
    dialog = EditTextDialog(root, selected_area_id + '.txt', None, "")
    dialog.set_on_validate_listener(lambda: update_results())

# Create main window
root = tk.Tk()
root.title("TTYD Dialog Editor")
root.geometry("1000x800")

# Map/Area select
area_label = tk.Label(root, text="Map/Area:", justify="left")
area_label.pack(anchor="w", padx=10, pady=(10, 0))

area_frame = tk.Frame(root)
area_frame.pack(padx=10, expand=True, fill=tk.X, pady=(0, 5))

current_area_name = tk.StringVar()
area_menu = AutocompleteCombobox(area_frame, textvariable=current_area_name, completevalues=["", *get_all_area_names()])
area_menu.pack(fill=tk.X, side="left", expand=True)
area_menu.bind("<<ComboboxSelected>>", update_results)

add_button = ttk.Button(area_frame, text="Add", command=on_click_add)
add_button["state"] = "disabled"
add_button.pack(side="left")

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
