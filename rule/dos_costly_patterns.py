import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))



def apply(file,src):
    print("Dos Costly patterns")

    result_list = []
    for ix,tp in enumerate(src):
        if "functions" in tp:
            for func in tp["functions"]:
                variables = []
                if "parameters" in func:
                    variables = func["parameters"]
                else:
                    continue
                
                if "ForStatement" in func:
                    for k in func["ForStatement"]:
                        if k["init_expression"] in variables:
                            result_list.append(k["line"])
                        if k["condition"] in variables:
                            result_list.append(k["line"])

    
    if result_list:
        result_list = list(set(result_list))
        result =["Warning : Dos Costly patterns, Check your parmeter in For statement"]
        with open(file) as f:
            for i,line in enumerate(f):
                if i+1 in result_list:
                    result.append(line)

        return result
    

                    
        



