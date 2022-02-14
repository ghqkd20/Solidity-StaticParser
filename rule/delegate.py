import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def apply(file,src):
    print("Delegate")
    answer = [False,[],[]]

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
                            answer[0]=True
                            answer[1].append(fc["line"][0])
                    except:
                        pass
    if answer[0] == True:
        result =["Warning : Delegate Call is used, But Contract is not library"]
        result.append(answer[1])
        result.append([])
        with open(file) as f:
            print("Here",result)
            for i,line in enumerate(f):
                if i+1 in result[1]:
                    print('yes',i,line)
                    result[2].append(line)
                        
        return result

