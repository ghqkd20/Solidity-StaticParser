import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def bool_variable(variable,ls):
    for v in ls:
        if v["typename"] =="bool":
            variable.append(v["name"])

 
def apply(file,src):
    result_list = [] # reenter line list 
    for ix,tp in enumerate(src):
        variable = []
        if "variables" in tp:
            bool_variable(variable,tp["variables"])
        if "functions" in tp:
            for f in tp["functions"]:
                mutex = True # check if and require
                reenter = False # Check call and update expression -> reenter
                call = False  # to break for statement because not call function 
                call_list = [] # append line
                check_list = [] # append if,require => args,line
                if "function_call" in f:
                    for k in f["function_call"]:
                        # if call is exists, append line number
                        if k["expression_type"] == 'MemberAccess' and k["membername"] == 'call':
                            call = True
                            call_list.append(k["line"][0])
                        # Require check
                        try:
                            if k["expression_type"] == 'Identifier' and k["membername"] == "require":
                                check_list.append([k["line"][0],k["args"]])
                        except:
                            pass
                            
                # if call is not found, continue( next functions)                               
                if call == False:
                    continue

                # Reenter Check 
                if "expression" in f:
                    # if update is executed after call
                    for e in f["expression"]:
                        if max(call_list)<e["line"][0]:
                            reenter = True
                    
                if "IfStatement" in f:
                    for i in f["IfStatement"]:
                        check_list.append([i["line"][0],i["args"]])

                
                # mutex check and get result
                for line,arg in check_list:
                    if line < call_list[0] and arg in variable:
                        mutex = False
                            
                                    
                # if mutex & reenter append result_list
                if mutex and reenter:
                    result_list.append(call_list[0])
                
    # get result line from result_list and source code
   # print(result_list)
                
    # get result line from result_list and source code
    if result_list:
        result =["Warning : Reenterency : Call and update is occur, Please Check your code"]
        with open(file) as f:
            for i,line in enumerate(f):
                if i+1 in result_list:
                    result.append("line : "+str(i+1)+line)                
        return result
    


    
                
        

