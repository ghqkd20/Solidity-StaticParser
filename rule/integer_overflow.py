import sys, os
import linecache

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def binary(answer,func):

    for es in func:
        if es['type'] == 'ExpressionStatement' and es['expression_type']=='BinaryOperation':
            answer[0] = True
            answer[1].add(es['line'][0])

    
def apply(file,src):
    print("Integer Overflow")
    answer = [False,set(),[]]

        # Contract Traverse
    for ix,tp in enumerate(src):
        # Library = pass
        if tp["kind"] == 'library':
            continue
        # Contract + Binary Operation => Warning
        # In Contract expression
        if 'expression' in tp:
            binary(answer,tp['expression'])

        for func in tp['functions']:
            if 'expression' in func:
                binary(answer,func['expression'])
    print(answer[1])
    
                
    if answer[0] == True:
        result =["Warning : Binary Operation is used, so Integer Overflow can occur"]
        result.append(sorted(answer[1]))
        result.append([])
        with open(file) as f:
            for i,line in enumerate(f):
                if i+1 in result[1]:
                    result[2].append(line)

        return result

