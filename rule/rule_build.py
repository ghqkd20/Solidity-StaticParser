from rule import delegate

class Rule_Build:
    result = dict()
    json_list = []
    
    def __init__(self,json_list):
        self.json_list = json_list
        self.apply()


    def rule_list(self):
        rules = ["delegate"]
        return rules


    def apply(self):
        rules = self.rule_list()
        func = ".apply(self.json_list)"

        for rule in rules:
            self.result[rule] = exec(rule+func)


    def get_result(self):
        return self.result
