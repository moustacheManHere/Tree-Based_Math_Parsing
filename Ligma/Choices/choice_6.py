from Ligma.Choices.base_choice import BChoice
from Ligma.DataStructure.HashTable import HashTable
from Ligma.Tree.Forest import ForestManager
from Ligma.Tree.Parse import ParseTree
from Ligma.Abstract.Sort import MergeSort
import re

MUL = lambda x, y: x * y
DIVIDE = lambda x, y: x / y
POWER = lambda x, y: x ** y
MAPPING = {
    '*' : MUL,
    '/' : DIVIDE,
    '^' : POWER
}

# NOTE: DONE BY SHAWN LIM
class Choice(BChoice):

    # a quick and simple method to parse and evaluate an expression without variables
    def eval(self, exp : str, fm : ForestManager):
        exp = f'({exp})'    # add brackets because the parse tree was designed to take into account it
        pt = ParseTree(exp).get_tree()
        result = fm.evaluate(pt)
        return result
    
    # prints the matrix. Takes in the matrix itself and the right hand side values
    def print_matrix(self, matrix, RHS):
        # first get the keys
        keys = matrix[0].keys()

        s = ''
        # iterate each row and print
        for i, row in enumerate(matrix):
            if i == 0:
                s += '┌ '
            elif i == len(keys) - 1:
                s += '└ '
            else:
                s += '│ '

            s += ' '.join([str(row[key]) for key in keys]) + f' │ {RHS[i]}'

            if i == 0:
                s += ' ┐\n'
            elif i == len(keys) - 1:
                s += ' ┘\n'
            else:
                s += ' │\n'
        
        print(s)

    def run(self, forestManager, _):
        # first, we need to know how many equations we are solving
        NUM_VARS = self.input.getInput('\nEnter the number of equations to solve\nNote: Only accept 2 to 10 equations\n>> ', 
                                       validator=self.inpValidate.integer, 
                                       error='No valid integer inputted, returning back to main menu',
                                       num_range = range(2, 11))
        if not NUM_VARS: return

        # then, we prompt for each equation. The input will be in equation form rather than the assignment statement in option 1
        eqns = []
        isValid = True
        for i in range(1, NUM_VARS + 1):
            eqn = self.input.getInput(f'\nEnter equation no. {i}\nNote: No parenthesis allowed, each equation won\'t be evaluated individually. No power or exponential variable allowed.\nFor example, 5*a + b + 2*c = 11\n>> ',
                                      validator=self.statementValidate.equation,
                                      error='No valid equation entered, returning back to main menu')
            # if the input is invalid, then set isValid to false to return back to main menu and break the for loop
            if not eqn:
                isValid = False
                break
            eqns.append(eqn)
        
        if not isValid: return

        # first identify all the unique variable names, this will determine all the variables in the linear system
        unique_vars = []
        formatter = lambda s: s.replace('**', ' ^ ').replace("+", " + ").replace("-", " - ").replace("/", " / ").replace("*", " * ").replace('=', ' = ').split()

        RHS_values = []     # stores all the RHS values

        # iterate each equation and get all the algebra, and then use set class to only get unique variables
        # not only that, extract all the values from all the RHS of the equations
        for eqn in eqns:
            eqn_s = formatter(eqn)
            RHS_values.append(float(eqn_s[-1]))    # the right hand side value will always be the last value in the splitted list
            unique_vars += [element for element in eqn_s if element.isalpha()]
        
        # sort the variable names
        sorter = MergeSort()
        unique_vars = list(set(unique_vars))

        # if the number of variables do not match the number of equations, tell the user it does not match and return back
        if len(unique_vars) != NUM_VARS:
            print(f'\nError: The number of variables do not match the number of equations. {NUM_VARS} equations chosen but only detected {len(unique_vars)} unique variables!')
            return
        
        unique_vars = sorter.sort(unique_vars)
        # by know all the unique variables, I can then instantiate a list of hash tables with predefined size as our matrix
        # each hash table in the list will be one row, and each key value pair in the hash table will be the variable and its value
        # initially, we'll assume each variable in every row is 0, because if a variable is never mentioned in an equation, it is assumed to be 0
        matrix = [HashTable({var : 0 for var in unique_vars}) for _ in range(len(eqns))]

        # and now for each equation, separate the value/variables by the least priority operator (+ and -) 
        # we now only care about the LHS, hence remove all spaces, then split the equation by equal sign and only extract the LHS, and then further separate out the operands by + and -
        separate_low_operand = lambda s: s.replace(' ', '').split('=')[0].replace('-', '+0-1*').split('+')   # we need the negative, so change it into +0-1* so we can split
        extract_var_sym = re.compile(r'([*/+-]?)([a-zA-Z]+)([*/+-]?)')  # regular expression to extract the variable and symbols
        for i, eqn in enumerate(eqns):
            operands = separate_low_operand(eqn)
            # now loop through each operand group
            for operand in operands:
                # if the operand group is purely a number, then subtract the respective RHS value by the operand
                if self.statementValidate.isNum(operand):
                    RHS_values[i] -= float(operand)

                # if not, then check if there is alphabets in it, if so, it's a variable, such as 3*x
                elif bool(re.search('[a-zA-Z]', operand)):
                    # extract the variable and symbol
                    var_syms = re.findall(extract_var_sym, operand)[0]
                    var = var_syms[1]   # get the variable

                    # get the coefficient
                    coef = 1

                    # if the left side of the variable got something, then send to evaluate
                    if var_syms[0] != '':
                        left_value = self.eval(operand.split(var)[0][:-1], forestManager)    # split by variable, extract the left side, and pass in without the symbol on the very right
                        coef = MAPPING[var_syms[0]](coef, float(left_value))           # then extract the symbol, get the right operator function and perform
                    
                    # repeat the same thing but for the right side
                    if var_syms[2] != '':
                        right_value = self.eval(operand.split(var)[1][1:], forestManager)    # split by variable, extract the left side, and pass in without the symbol on the very right
                        coef = MAPPING[var_syms[2]](coef, float(right_value))           # then extract the symbol, get the right operator function and perform

                    # finally set coefficient into the matrix
                    matrix[i][var] = coef
                
                # lastly, if is not purely number or variables, then is just a simple expression, then just pass to eval and minus from the RHS value
                else:
                    RHS_values[i] -= self.eval(operand, forestManager)

        self.print_matrix(matrix, RHS_values)
        # now is the solving part. Gauss jordan elimination has a simple algorithm to implement programmatically
        # rearrange the rows such that the row with the most 0s in front will be the first to be evaluated
        numOf0s_list = []
        for row in matrix:
            numOf0s = 0
            for element in row.items():
                if element[1] == 0:
                    numOf0s += 1
                else:
                    break
            numOf0s_list.append(numOf0s)
        
        # a simple bubble sort to sort the rows based on the number of zeros
        n = len(numOf0s_list)
        for i in range(n):
            # Last i elements are already sorted, so we don't need to check them
            for j in range(0, n-i-1):
                # Swap if the element found is greater than the next element
                if numOf0s_list[j] > numOf0s_list[j+1]:
                    numOf0s_list[j], numOf0s_list[j+1] = numOf0s_list[j+1], numOf0s_list[j]
                    matrix[j], matrix[j+1] = matrix[j+1], matrix[j]
                    RHS_values[j], RHS_values[j+1] = RHS_values[j+1], RHS_values[j]

        # now start from bottom pivot and work my way up
        matrix.reverse()
        RHS_values.reverse()
        for i, row in enumerate(matrix):
            var_i = 0; pivot_i = len(unique_vars) - i
            # now iterating from left to right
            while var_i < pivot_i:
                value = row[unique_vars[var_i]]     # get the value

                # if the var i + 1 is the same as the pivot i, then there will be 3 outcomes
                if var_i + 1 == pivot_i:
                    # first outcome, it is a 1, then is already reduced, so then set all the other rows above in this column zero, and change the RHS accordingly
                    if value == 1:
                        for j in range(i + 1, n):
                            value_change = matrix[j][unique_vars[var_i]] * -1
                            matrix[j][unique_vars[var_i]] = 0
                            RHS_values[j] = RHS_values[j] + value_change * RHS_values[i]
                    
                    # second outcome, it is not 1, nor 0, then simply multiply itself to be 1 for that row
                    elif value != 1 and value != 0:
                        value_change = (1 / value) if value > 0 else (-1 / value)
                        matrix[i][unique_vars[var_i]] = 1
                        RHS_values[i] *= value_change
                    
                    # third outcome, it is 0, then check if the RHS is zero as well, if is not, then this problem is unsolvable
                    elif value == 0 and RHS_values[i] != 0:
                        print('\nWarning, this system of equation is unsolvable! It has no solutions!')
                        return  # if is unsolvable, then don't proceed further
                    
                    
                # or else if var i is lesser, then try to deduct itself from other rows if is not 0
                elif value != 0:
                    # look through the other row, see if got zero
                    for j in range(i + 1, n):
                        value_other = matrix[j][unique_vars[var_i]]
                        if value_other != 0:    # if is not zero, attempt to deduct from them
                            multiplier = value_other / value
                            matrix[i][unique_vars[var_i]] = 0
                            for var_j in range(var_i + 1, len(unique_vars)):
                                matrix[i][unique_vars[var_j]] = matrix[j][unique_vars[var_j]] - matrix[i][unique_vars[var_j]] * multiplier
                            RHS_values[i] = RHS_values[j] - RHS_values[i] * multiplier
                            break   # break it because already found a potential one to deduct from

                    else:
                    # if all are 0, then deduct itself by that value
                        matrix[i][unique_vars[var_i]] = 0
                        for var_j in range(var_i + 1, len(unique_vars)):
                            matrix[i][unique_vars[var_j]] -= value
                        RHS_values[i] -= value

                var_i += 1
        
        matrix.reverse()
        RHS_values.reverse()
        self.print_matrix(matrix, RHS_values)

        print('\nSolutions:')
        for i, var in enumerate(unique_vars):
            print(f'{var} = {RHS_values[i]}')

    def __str__(self) -> str:
        return 'Simultaneous equations solver with Gauss-Jordan Elimination'
