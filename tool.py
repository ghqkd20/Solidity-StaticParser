import subprocess
import sys
import json
import uuid
import tkinter as tk
from rule import rule_build
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

def preprocess(json_list):

    compact_json = []
    ix = -1
    fx = -1

    for i in json_list:
        if i["type"] == "ContractDefinition":
            new_contract = dict()
            new_contract["type"] = i["type"]
            new_contract["name"] = i["name"]
            new_contract["kind"] = i["kind"]
            compact_json.append(new_contract)
            ix +=1
            fx = -1

        elif i["type"] =="VariableDeclaration":
            if i["typeName"]["type"] != "ElementaryTypeName":
                continue
            # type, typename
            new_variable = dict()
            new_variable["type"] = i["type"]
            new_variable["typename"] = i["typeName"]["name"]
            # line number ?

           #Contract in
            if fx == -1:
                try:
                    compact_json[ix]["variables"].append(new_variable)
                except:
                    compact_json[ix]["variables"] = [new_variable]
           #Function in
            else:
                try:
                    compact_json[ix]["functions"][fx]["variables"].append(new_variable)
                except:
                    compact_json[ix]["functions"][fx]["variables"] = [new_variable]
                    
            
        elif i["type"] =="FunctionDefinition":
            # function name, parameter(=type,name)
            new_func = dict()
            new_func["type"] = i["type"]
            new_func["name"] = i["name"]
            new_func["parameters"] = [k["name"] for k in i["parameters"]]

            #Contract First Function
            try:
                compact_json[ix]["functions"].append(new_func)
            except:
                compact_json[ix]["functions"] = [new_func]
                
            fx +=1

        elif i["type"] =="FunctionCall":
            # 1 expression -> type == memberAccess
            # 2 expression -> type == Identifier
            # memberName, loc 
            new_funccall = dict()
            new_funccall["type"] = i["type"]
            new_funccall["expression_type"] = i["expression"]["type"]
            if i["expression"]["type"] == "Identifier" and i["expression"]["name"] =="require" : # catch require 
                new_funccall["membername"] = i["expression"]["name"]
                if i["arguments"][0]["type"] == "Identifier":
                    new_funccall["args"] = i["arguments"][0]["name"]
                elif i["arguments"][0]["type"] == "BinaryOperation":
                    new_funccall["args"] = i["arguments"][0]["left_id"]
                new_funccall["line"] = [i["loc"]["start"]["line"],i["loc"]["end"]["line"]]
            elif i["expression"]["type"] =="MemberAccess":                                      # catch call
                try:
                    new_funccall["membername"] = i["expression"]["expression"]["memberName"]
                    new_funccall["line"] = [i["loc"]["start"]["line"],i["loc"]["end"]["line"]]
                except:
                    new_funccall["membername"] = i["expression"]["memberName"]
                    new_funccall["line"] = [i["loc"]["start"]["line"],i["loc"]["end"]["line"]]
            #Contract in 
            if fx == -1:
                try:
                    compact_json[ix]["function_call"].append(new_funccall)
                except:
                    compact_json[ix]["function_call"] = [new_funccall]
            #Function in
            else:
                try:
                    compact_json[ix]["functions"][fx]["function_call"].append(new_funccall)
                except:
                    compact_json[ix]["functions"][fx]["function_call"] = [new_funccall]

        elif i["type"] =="ExpressionStatement":
            # type, operator
            new_expression = dict()
            new_expression["type"] = i["type"]
            new_expression["expression_type"] = i["expression"]["type"]
            if i["expression"]["type"] != "BinaryOperation":
                continue
            new_expression["operator"] = i["expression"]["operator"]
            new_expression["line"] = [i["loc"]["start"]["line"],i["loc"]["end"]["line"]]

            #Contract in 
            if fx == -1:
                try:
                    compact_json[ix]["expression"].append(new_expression)
                except:
                    compact_json[ix]["expression"] = [new_expression]
           #Function in
            else:
                try:
                    compact_json[ix]["functions"][fx]["expression"].append(new_expression)
                except:
                    compact_json[ix]["functions"][fx]["expression"] = [new_expression]

            

        elif i["type"] =="ForStatement":
            # type, initExpression->initvalue->name, conditionExpression->right->expression_name
            new_for = dict()
            new_for["type"] = i["type"]
            new_for["init_expression"] = i["initExpression"]["initialValue"]["name"]
            new_for["condition"] = i["conditionExpression"]["right"]["expression_name"]

            try:
                compact_json[ix]["functions"][fx]["ForStatement"].append(new_for)
            except:
                compact_json[ix]["functions"][fx]["ForStatement"] = [new_for]


        elif i["type"] =="IfStatement":
            # type,
            new_if = dict()
            new_if["type"] = i["type"]

            if i["condition"]["type"] == "Identifier":
                new_if["args"] = i["condition"]["name"]
            elif i["condition"]["type"] == "BinaryOperation":
                new_if["args"] = i["condition"]["left_id"]

            try:
                compact_json[ix]["functions"][fx]["IfStatement"].append(new_if)
            except:
                compact_json[ix]["functions"][fx]["IfStatement"] = [new_if]

            new_if["line"] = [i["loc"]["start"]["line"],i["loc"]["end"]["line"]]

    return compact_json


def main():
	
	file = sys.argv[1]

# Compile 
#	print("-------------------Compile Result-------------------")	
#	compile = subprocess.run(['solc',file],encoding='utf-8')

#Ast parsing
	ast = subprocess.run(['sh','ex.sh',file],stdout=subprocess.PIPE,encoding='utf-8')
	ast_list = ast.stdout.splitlines()	
	
	json_list = [json.loads(i) for i in ast_list]
	#print(json_list)

	compact_json = preprocess(json_list)
	print(file,compact_json)

	rule = rule_build.Rule_Build(file,compact_json)
	print(rule.get_result())
	#print(jsons)

# Version select is not adapted
#	version = jsons['body'][0]['start_version']['version']
#	compile = subprocess.run(['sh','ex2.sh',version,file],encoding='utf-8')

#	show_data(jsons)

main()

