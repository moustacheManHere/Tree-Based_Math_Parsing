# this assignment statement validator is used to validate whether the math statement is valid
class StatementValidator():
    def assignment_statement(self, s: str, diff=False):

        OPERATORS = '+-*/^'

        # use the common check to check the basic stuff 
        LHS, RHS = self.common_check(s)
        if LHS == None and RHS == None: return None

        # make sure the LHS must only contain alphabets
        if not LHS.strip().isalpha():
            print('\nError: The left hand side of the expression must be a valid variable name!')
            return None
        # that's it for the left hand side
        
        # now we want to add some padding to the string so we can split into array for easy checking
        # and also change the exponent symbol to ^ so that the multipler symbol won't change the exponent symbol
        if '^' in RHS: 
            print('\nError: Invalid right hand side input')
            return None      # but if there are already existing '^' symbols, then treat it as invalid

        # "tokenise" the expression
        arr =  self.formatter(RHS, diff)

        # make sure that the first and last element are the parenthesis, and they must be the right parenthesis
        if diff:
            if (arr[0] != '(' and arr[0]!="diff_") or arr[-1] != ')':
                print('\nError: Please add parenthesis around the right hand side of the expression!')
                return None
            if arr[0]=="diff_" and arr[1] == "(":
                print("Please specify a valid variable to differentiate!")
                return None 
            if arr[0]=="diff_" and  self.isNum(arr[1]):
                print("Error! The variable referenced is not valid!")
                return None
            if arr[0] == "diff_":
                arr = arr[2:]
        else:
            if arr[0] != '(' or arr[-1] != ')':
                print('\nError: Please add parenthesis around the right hand side of the expression!')
                return None

        # now go through the RHS and check if the statement is valid
        parenthesisOpening = 0
        for i, element in enumerate(arr):
            if element in OPERATORS:
                # if element is an operator, make sure the previous and the next element must be a number or algebra or the correct parenthesis
                try:
                    prev = arr[i - 1]
                    next_ = arr[i + 1]
                except: 
                    print('\nError: Invalid placement of operators!')
                    return None     # if there is error, it will be index out of range, then it means the operator is at the start or end of RHS
                
                # check that the previous character is either an alphabet, a number, or the closing parenthesis
                # and check that the next character is either an alphabet, a number, or the opening parenthesis
                if not prev.isalpha() and not self.isNum(prev) and prev != ')' or not next_.isalpha() and not self.isNum(next_) and next_ != '(':
                    print('\nError: Invalid placement of operators!')
                    return None
            
            elif element.isalpha() or self.isNum(element):
                # if element is an algebra or number, then check that the previous value must only be open parenthesis or operator
                # then the next value must be only close parenthesis or operator
                try:
                    prev = arr[i - 1]
                    next_ = arr[i + 1]
                except: 
                    print('\nError: Invalid placement of variables!')
                    return None

                if prev not in OPERATORS and prev != '(' or next_ not in OPERATORS and next_ != ')':
                    print('\nError: Invalid placement of variables!')
                    return None
            
            elif element in '()':
                # if is parenthesis, then add or minus the parenthesisOpening, to check if the parenthesis are fully close
                parenthesisOpening = parenthesisOpening + 1 if element == '(' else parenthesisOpening - 1
            
            else: 
                print('\nError: Invalid character(s) inside the right hand side of the expression')
                return None   # if the element is not an operator, a proper algebra, a number, or parenthesis, then is invalid element
        
        # check if the parenthesis is closed
        if parenthesisOpening != 0:
            print('\nError: You did not close your parenthesis properly!')
            return None
        
        return s
    

    # method to validate equation input
    # example valid input: 5*a + b + 2*c = 11
    def equation(self, s: str):
        # the first few checks will be the same as the assignment statement

        OPERATORS = '+-*/^'
        LHS, RHS = self.common_check(s)
        if LHS == None and RHS == None: return None

        # make sure the RHS must contain a number
        if not self.isNum(RHS.strip()):
            print('\nError: The right hand side of the expression must be a valid number!')
            return None
        
        if '^' in LHS: 
            print('\nError: Invalid right hand side input')
            return None      # but if there are already existing '^' symbols, then treat it as invalid

        arr = self.formatter(LHS)

        # if parenthesis is found, then is invalid
        if '(' in arr or ')' in arr:
            print('\nError: No parenthesis are allowed!')
            return None

        # now go through the LHS and check if the statement is valid
        for i, element in enumerate(arr):
            if element in OPERATORS:
                # if element is an operator, make sure the previous and the next element must be a number or algebra or the correct parenthesis
                try:
                    prev = arr[i - 1]
                    next_ = arr[i + 1]
                except: 
                    print('\nError: Invalid placement of operators!')
                    return None     # if there is error, it will be index out of range, then it means the operator is at the start or end of RHS
                
                # check that the previous character is either an alphabet or a number
                # and check that the next character is either an alphabet or a number
                if not prev.isalpha() and not self.isNum(prev) or not next_.isalpha() and not self.isNum(next_):
                    print('\nError: Invalid placement of operators!')
                    return None
                
                # lastly, check if the power symbol is associated with a variable, if so, then is invalid because no power or exponential variables are allowed
                # if a power symbol is used for constant, then is fine
                if element == '^':
                    if arr[i - 1].isalpha() or arr[i + 1].isalpha():
                        print('\nError: Power symbol can only be used for constants in equation, not variable!')
                        return None
                    '''
                    if self.check_algebra(arr, i, -1) or self.check_algebra(arr, i, 1):
                        print('\nError: Power symbol can only be used for constants in equation, not variable!')
                        return None
                    '''
            
            elif element.isalpha() or self.isNum(element):
                # if element is an algebra or number, then check that the previous value must be an operator or nothing (starting value)
                # then the next value must be only operator or nothing (last value)
                if i != 0 and i != len(arr) - 1:
                    if arr[i - 1] not in OPERATORS or arr[i + 1] not in OPERATORS:
                        print('\nError: Invalid placement of variables or values!')
                        return None
                    
                    if element.isalpha():
                        # for algebra, make sure that the any multiplier or divider beside it is also not another algebra
                        if arr[i - 1] in '*/' and arr[i - 2].isalpha() or arr[i + 1] in '*/' and arr[i + 2].isalpha():
                            print('\nError: Two variables must not be multiplied or divied together!')
                            return None
            
            else: 
                print('\nError: Invalid character(s) inside the right hand side of the expression')
                return None   # if the element is not an operator, a proper algebra, a number, or parenthesis, then is invalid element
        
        return s
    

    '''
    # method to check if the previous or next item is an algebra or not. To be used as a recursive function
    # this is to check whether the power symbol "links" to an algebra
    def check_algebra(self, arr, i, direction):
        # if i is already out of range, simply return false
        if i < 0 or i == len(arr):
            return False
        
        # if item is a number or a multiplier, divider, or another power symbol, keep moving
        if self.isNum(arr[i]) or arr[i] in '*/^':
            return self.check_algebra(arr, i + direction, direction)
        
        # if item is a plus or minus, then return false, as plus or minus will act as separator for equation
        if arr[i] in '+-':
            return False
        
        # otherwise, it will only be an algebra, which means is invalid as it doesn't support power or exponential variable
        return True
    '''


    # method to validate basic infix mathematical input
    def common_check(self, s):
        # first check if there's equal sign (should stop empty string or string with no equal sign)
        if '=' not in s: 
            print(f'\nError: Invalid input!')
            return (None, None)

        # next, split the equal sign, make sure there must be two values, the left hand side, and right hand side
        try: LHS, RHS = s.split('=')
        except: 
            print('\nError: Please only use one equal sign!')
            return (None, None)

        # check that both the LHS and RHS are not empty
        if not LHS or not RHS: 
            print('\nError: Both the left and right hand sign of the expression must not be empty!')
            return (None, None)
        
        return LHS, RHS
    
    
    # method to check if the value is a number, floating point or integer
    def isNum(self, value):
        try: float(value)
        except: return False
        return True
    
    
    # method to simply format the string to "tokenise"
    def formatter(self, s: str,diff=False):
        
        s = (
            s.replace("(", " ( ")
            .replace(")", " ) ")
            .replace('**', ' ^ ')
            .replace("+", " + ")
            .replace("-", " - ")
            .replace("/", " / ")
            .replace("*", " * ")
        )
        if diff:
            s = s.replace("diff_", " diff_ ")
        return s.split()
