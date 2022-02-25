import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


# parameter = call -> args return
# [line1,line2] => [True,"args", ], True = not parameter
def check_line(file,call_list):
    tmp = []
    with open(file) as f:
        for i,line in enumerate(f):
            if i+1 in call_list:
                if "=" in line:
                    tmp.append([line.split("=")[0],i+1])
                else:
                    tmp.append(True)

    return tmp    

    

# check = [True, ["args",line number],["args",line number] .. ]
# exclude list = [["args",line],["args",line]... ]

def check_result(check,exclude_list):

    result_list = []
    
    for i in exclude_list:
        for ix,k in enumerate(check):
            if k == True:
                continue
            elif i in k[0]:
                print("exclude",k[0])
                check[ix] = True
        
    
    for li in check:
        if li != True:
            result_list.append(li[1])

    return result_list

    

def apply(file,src):

    result_list = []
    
    # Contract Traverse
    for ix,tp in enumerate(src):
        # Library = pass
        if tp["kind"] == 'library':
            continue
        # Find Function_definition
        for func in tp["functions"]:
            call_list = []
            exclude_list = []
            if "function_call" in func:
                for fc in func["function_call"]:
                    if "membername" in fc and fc["membername"] == 'call':
                        call_list.append(fc["line"][0])
                    elif "membername" in fc and fc["membername"] == 'require':
                        exclude_list.append(fc["args"])
            if "IfStatement" in func:
                for fc in func["IfStatement"]:
                    if "args" in fc:
                        exclude_list.append(fc["args"])
            if call_list:
                check = check_line(file,call_list)
                result_list =check_result(check,exclude_list)
    if result_list:
        result =["Warning : Unchecked Call is used, Please check your return value"]
        with open(file) as f:
            for i,line in enumerate(f):
                if i+1 in result_list:
                    result.append("line : " +str(i+1)+line)

        return result
