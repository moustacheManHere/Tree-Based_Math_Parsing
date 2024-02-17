from Ligma.Tree.Parse import ParseTree
from Ligma.DataStructure.Stack import Stack
from Ligma.DataStructure.HashTable import HashTable
from Ligma.Abstract.Diff import Differentiation
import math 

OPERATORS = ['+', '-', '*', '/', '^']
ADD = lambda x, y: x + y
SUBTRACT = lambda x, y: x - y
MUL = lambda x, y: x * y
DIVIDE = lambda x, y: x / y
POWER = lambda x, y: x ** y
MAPPING = {
    '+' : ADD,
    '-' : SUBTRACT,
    '*' : MUL,
    '/' : DIVIDE,
    '^' : POWER
}

# class to store and handle all the assignment statements from user input and file input
class ForestManager():
    def __init__(self) -> None:
        self.__trees = HashTable(64)     # stores all the assignments where the variable is the key and its assignment (which will be the tree) is the value
        self.__statements = HashTable(64)    # same but stores the original assignment statement
        self.__results = HashTable(64)   # stores the evaluated result
        self.__vars = []  # stores all the __vars so I don't need to keep doing .keys() every time
        self.__var_stack = Stack()  # stores all the variables that are currently in evaluation. Used to check for cyclical recursion to prevent falling into it
        self.__functions = HashTable(64) #store all the functions
        self.operators = ['+', '-', '*', '/', '^',"log"]
        self.diff_mode = False
        self.differentiation = Differentiation()
        self.initBaseFuncs()
    
    def initBaseFuncs(self):
        self.__functions['+'] = lambda x, y: x + y
        self.__functions['-'] = lambda x, y: x - y
        self.__functions['*'] = lambda x, y: x * y
        self.__functions['/'] = lambda x, y: x / y
        self.__functions['^'] = lambda x, y: x ** y
        self.__functions["log"] = lambda x,y: math.log(x)
    
    # method to add or modify assignment statement. This is assumed that the statement has already been validated
    def plant_tree(self, statement, diff_mode = False):
        
        statement = statement.replace(' ', '')      # remove all whitespaces
        var, assignment = statement.split('=')      # separate by equal sign, so left hand side is variable name, right hand side will be the tree
        if diff_mode and assignment[0] != "(":
            variable = assignment[5:assignment.find('(')]
            assignment_temp = assignment[assignment.find('('):]
            tree = ParseTree(assignment_temp)   
            tree = self.differentiation.getDiffTree(tree,variable)
            # insert differentiation
        else:
            tree = ParseTree(assignment)                # create a tree

        # store all the necessary values
        self.__trees[var] = tree
        self.__statements[var] = assignment
        self.__results[var] = None
        if var not in self.__vars: self.__vars.append(var)

    # method to determine which variable(s) to evaluate
    def harvest_tree(self, var = None):
        
        # set all the variables result to none as a way to "refresh" the result every time the evaluation has to be done
        for var_i in self.__vars:
            self.__results[var_i] = None

        # if var is none, then evaluate all, else, evaluate the said var
        var_list = self.__vars if var == None else [var]

        # now iterate through the list of variables to be evaluated
        for var_i in var_list:
            # reset the variable stack for each assignment statement
            self.__var_stack.reset()
            
            # before evaluating the current variable, check the result to see if there already has a value
            # if there is a value, it means the current variable has been evaluated earlier as a dependent variable on a previous variable, so just skip
            if self.__results[var_i] is not None: continue

            # put the evaluation under the try block so that if any issue arises such as a cyclical recursion, then it will not crash the program
            try:
                val = self.evaluate(self.__trees[var_i].get_tree())     # gets the tree head of the current variable and evaluate it
                _ = float(val).imag                                     # if the final value is an infinity or complex value, then warn the user and leave the value as it is
            except Exception as e:
                # if the error is due to divide by zero, warn the user
                if 'division by zero' in e.__str__():
                    print(f'\nWarning: Division by zero occurred in variable {var_i}! Returning None value for this variable')
                # if the error is due to complex number, warn the user
                if 'complex' in e.__str__():
                    print(f'\nWarning: Complex number found in variable {var_i}! Returning None value for this variable!')
                continue                                                # if there are errors, then leave the variable as none as it's an invalid statement so continue

            # check if the value is an integer or float. If is an integer, change to integer so it removes the decimal point, or else leave it as it is
            if val is not None and int(float(val)) == float(val):
                val = int(val)
            self.__results[var_i] = val
    
    def getOneTree(self,var):
        return self.__trees[var]
    
    def getOneResult(self,var):
        return self.__results[var]
    
    def getOneStatement(self,var):
        return self.__statements[var]
    
    def get_vars(self):
        return self.__vars
    
    def get_results(self):
        return self.__results
    
    # to check the node and return a value. To reduce code duplication, this part of the code will be in its own method, rather than part of the .evaluate() method
    def __checkNode(self, node):
        # if the value is an operator, then there's more branches, then go recursive
        if node.value in self.operators:
            value = self.evaluate(node)

        # # if the value is an alphabet or a word, then...
        elif node.value.isalpha():
            algebra = node.value

            self.__var_stack.push(algebra)
            #print(self.__results,algebra)
            if self.__results[algebra] != None:
                    return self.__results[algebra]
            #print(self.__results[algebra])
            # first check if the variable stack has a cyclical list pattern (for example, [1, 2, 3, 1, 2, 3]), which means it is a cyclical recursion
            if self.__var_stack.checkCyclical():
               raise ValueError('Cyclical recursion warning')  # then just raise the error
            

            # if the variable is not in self.__results keys, it means the variable wasn't even defined at all, so the statement will result in None
            if algebra not in self.__vars:
                return None
            
            # if the variable has a None result, it means the variable has not been evaluated yet, hence, go recursive
            if self.__results[algebra] == None:
                value = self.evaluate(self.__trees[algebra].get_tree())
                self.__results[algebra] = value  # add the result from the evaluated variable into result, so no need to re-evaluate

            else:
                value = self.__results[algebra]  # or else, then just use the result, hence this self.__results can act as caching, reducing the need to re-evaluate
        
        # if the value is not an operator or word/alphabet, it should be a number, then just use that number as the value
        else:
            value = node.value

        return value
    
    # the method to do the actual evaluation
    def evaluate(self, node):

        # if both the left and right side are none, then it can only occur when there are only one value/variable in the expression
        if node.left is None and node.right is None:
            if node.value.isalpha():

                alpha = node.value

                self.__var_stack.push(alpha)
                if self.__results[alpha] != None:
                    return self.__results[alpha]
                # check if there's an infinite recursion happening within the statements
                if self.__var_stack.checkCyclical():
                    raise ValueError('Cyclical recursion warning')

                value = self.evaluate(self.__trees[alpha].get_tree())
                return value
            else:
                return node.value

        # first check the node for the left side
        left_value = self.__checkNode(node.left)
        # and then right side
        right_value = self.__checkNode(node.right)
        # if the left or right value gets a none, it means one of them had a variable that was never defined at all
        if left_value is None or right_value is None: return None
        # map the operator to the appropriate function, and call that function and input the values
        return self.__functions[node.value](float(left_value), float(right_value))

    def check_override(self, statement):
        variable = statement.replace(' ', '').split("=")[0]
        if variable in self.__vars:
            return True 
        else:
            return False
    
    def saveTrees(self):
        jsonOut = {"statements":{},"var":self.__vars,"trees":{},"results":{}}
        self.harvest_tree()
        for i in self.__vars:
            jsonOut["statements"][i]=self.__statements[i]
            jsonOut["results"][i]=self.__results[i]
            jsonOut["trees"][i] = self.__trees[i].serialize()
        return jsonOut
    def loadTrees(self, load):
        self.__vars = load["var"]
        for i in self.__vars:
            tree = ParseTree(load["statements"][i])
            tree.headNode = tree.deserialize(load["trees"][i])
            self.__trees[i] = tree
            self.__statements[i] = load["statements"][i]
            self.__results[i] = load["results"][i]
        self.harvest_tree()
        

    
    # adds the ability to get the length of forest manager, which should return the number of __statements in the forest
    def __len__(self):
        return len(self.__vars)