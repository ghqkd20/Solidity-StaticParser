import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def apply(file,src):
    result_list = []
	# Contract Traverse

    for ix,tp in enumerate(src):
        # Library + delegate Call => pass
        if tp["kind"] == 'library':
            continue
        # Contract + delegate Call => Warning
	# Function Traverse
        for func in tp["functions"]:
            if 'function_call' in func:
                #FunctionCall Traverse
                for fc in func["function_call"]:
                    try:
                        if fc["membername"] == "delegatecall":
                            result_list.append(fc["line"][0])
                    except:
                        pass
    if result_list:
        result =["Warning : Delegate Call is used, But Contract is not library"]
        with open(file) as f:
            for i,line in enumerate(f):
                if i+1 in result_list:
                    result.append("line : "+str(i+1)+line)
                        
        return result

