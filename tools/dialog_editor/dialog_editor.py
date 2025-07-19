import os
import tkinter as tk
from tkinter import ttk

from tools.dialog_editor.ttyd_txt_parser import TTYDTxtParser
from tools.shared.map.map_helpers import get_all_area_names
from tools.shared.ux.autocomplete_combobox import AutocompleteCombobox

def get_results(selected_area_id, search_query):
    msg_dir = 'raw_rom/files/msg/US'

    result = []
    all_files = []
    with os.scandir(msg_dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.txt'):
                # Check area filter
                if not selected_area_id or entry.name.startswith(selected_area_id):
                    all_files.append(msg_dir + '/' + entry.name)

    for file in all_files:
        parser = TTYDTxtParser(file)
        parser.load()

        if not search_query:
            for key, value in parser.content.items():
                result.append(f"{key}:\n {value}")
        else:
            for key, value in parser.search(search_query):
                result.append(f"{key}:\n {value}")

        if len(result) > 100:
            break

    print("selected_option =", selected_area_id)
    print("search_query =", search_query)

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


# Create main window
root = tk.Tk()
root.title("TTYD Dialog Editor")
root.geometry("1000x800")

# Map/Area select
current_area_name = tk.StringVar()
area_menu = AutocompleteCombobox(root, textvariable=current_area_name, completevalues=["", *get_all_area_names()])
area_menu.pack(pady=10, fill=tk.X, padx=10)
area_menu.bind("<<ComboboxSelected>>", update_results)

# Search bar
current_search = tk.StringVar()
search_entry = ttk.Entry(root, textvariable=current_search)
search_entry.pack(pady=10, fill=tk.X, padx=10)
current_search.trace_add("write", update_results)

# Listbox to show results
result_list = tk.Listbox(root, height=200)
result_list.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

# Initial population
update_results()

# Run the application
root.mainloop()
