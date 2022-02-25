from rule import delegate
from rule import integer_overflow
from rule import unchecked_call
from rule import dos_costly_patterns
from rule import reenterency

class Rule_Build:
    result = dict()
    json_list = []
    file = ""
    
    def __init__(self,file,json_list):
        self.json_list = json_list
        self.file = file
        self.apply()


    def rule_list(self):
        rules = ["delegate","integer_overflow","unchecked_call","dos_costly_patterns","reenterency"]
        return rules


    def apply(self):
        rules = self.rule_list()
        func = ".apply(self.file,self.json_list)"

        for rule in rules:
            self.result[rule] = eval(rule+func)


    def get_result(self):
        self.display()
        #return self.result

    def display(self):
        print()
        print()
        print("\033[3m" +"\033[41m"+"                 Tool analysis Result                   "+"\033[0m")
        for name in self.result:
            if self.result[name] ==None:
                print(name + ": " +"\033[0m"+"\033[1m"+ " not detected"+"\033[0m")
            else:
                print("\033[1m"+ name + ": " +"\033[0m"+ "\033[32m"+self.result[name][0])
                for k in self.result[name][1:]:
                    print("\033[32m"+k+"\033[0m")
            print()
