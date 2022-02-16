from rule import delegate
from rule import integer_overflow
from rule import unchecked_call
from rule import dos_costly_patterns

class Rule_Build:
    result = dict()
    json_list = []
    file = ""
    
    def __init__(self,file,json_list):
        self.json_list = json_list
        self.file = file
        self.apply()


    def rule_list(self):
        rules = ["delegate","integer_overflow","unchecked_call","dos_costly_patterns"]
        return rules


    def apply(self):
        rules = self.rule_list()
        func = ".apply(self.file,self.json_list)"

        for rule in rules:
            self.result[rule] = eval(rule+func)


    def get_result(self):
        return self.result
