import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def binary(answer,func):

    for es in func:
        if es['type'] == 'ExpressionStatement' and es['expression_type']=='BinaryOperation':
            answer.append(es['line'][0])


def apply(file,src):
    result_list = []

        # Contract Traverse
    for ix,tp in enumerate(src):
        # Library = pass
        if tp["kind"] == 'library':
            continue
        # Contract + Binary Operation => Warning
        # In Contract expression
        if 'expression' in tp:
            binary(result_list,tp['expression'])

        for func in tp['functions']:
            if 'expression' in func:
                binary(result_list,func['expression'])

    
    if result_list:
        result =["Warning : Binary Operation is used, so Integer Overflow can occur"]
        result_list.sort()
        with open(file) as f:
            for i,line in enumerate(f):
                if i+1 in result_list:
                    result.append("line : "+str(i+1)+line)

        return result

