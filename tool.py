import subprocess
import sys
import json
import uuid
import tkinter as tk
from tkinter import ttk


def json_tree(tree, parent, dictionary):
    for key in dictionary:
        uid = uuid.uuid4()
        if isinstance(dictionary[key], dict):
            tree.insert(parent, 'end', uid, text=key)
            json_tree(tree, uid, dictionary[key])
        elif isinstance(dictionary[key], list):
            tree.insert(parent, 'end', uid, text=key + '[]')
            json_tree(tree,
                      uid,
                      dict([(i, x) for i, x in enumerate(dictionary[key])]))
        else:
            value = dictionary[key]
            if value is None:
                value = 'None'
            tree.insert(parent, 'end', uid, text=key, value=value)


def show_data(data):
    # Setup the root UI
    root = tk.Tk()
    root.title("JSON viewer")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Setup the Frames
    tree_frame = ttk.Frame(root, padding="3")
    tree_frame.grid(row=0, column=0, sticky=tk.NSEW)

    # Setup the Tree
    tree = ttk.Treeview(tree_frame, columns='Values')
    tree.column('Values', width=100, anchor='center')
    tree.heading('Values', text='Values')
    json_tree(tree, '', data)
    tree.pack(fill=tk.BOTH, expand=1)

    # Limit windows minimum dimensions
    root.update_idletasks()
    root.minsize(800, 800)
    root.mainloop()

def main():
	
	file = sys.argv[1]

# Compile 
#	print("-------------------Compile Result-------------------")	
#	compile = subprocess.run(['solc',file],encoding='utf-8')

#Ast parsing
	ast = subprocess.run(['sh','ex.sh',file],stdout=subprocess.PIPE,encoding='utf-8')
	ast_list = ast.stdout.splitlines()	
	
	json_list = [json.loads(i) for i in ast_list]
	print(json_list)
	#print(jsons)
# Version select is not adapted
#	version = jsons['body'][0]['start_version']['version']
#	compile = subprocess.run(['sh','ex2.sh',version,file],encoding='utf-8')

#	show_data(jsons)

main()

