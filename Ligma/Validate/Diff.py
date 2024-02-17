class DifferentiationValidator:
    # this assignment statement validator is used to validate whether the math statement is valid

    def __init__(self) -> None:
        pass

    def diff_assignment_statement(self, s: str):

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
        arr =  self.diffformatter(RHS)

        # make sure that the first and last element are the parenthesis, and they must be the right parenthesis
        if arr[0] not in ['(',"diff"] or arr[-1] != ')':
            print('\nError: Please add parenthesis around the right hand side of the expression!')
            return None

        print(arr)
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
                if not prev.isalpha() and not self.isNum(prev) and prev != ')' or not next_.isalpha() and not self.isNum(next_) and next_ != '(' and not next_ != 'diff':
                    print('\nError: Invalid placement of operators!')
                    return None
            
            elif (element.isalpha() or self.isNum(element)) and element != "diff":
                # if element is an algebra or number, then check that the previous value must only be open parenthesis or operator
                # then the next value must be only close parenthesis or operator
                try:
                    prev = arr[i - 1]
                    next_ = arr[i + 1]
                except: 
                    print('\nError: Invalid placement of variables')
                    return None
                if prev not in OPERATORS and prev != '(' or next_ not in OPERATORS and next_ != ')':
                    print('\nError: Invalid placement of variables!')
                    return None
            
            elif element in '()':
                # if is parenthesis, then add or minus the parenthesisOpening, to check if the parenthesis are fully close
                parenthesisOpening = parenthesisOpening + 1 if element == '(' else parenthesisOpening - 1
            
            elif element == "diff":
                next_ = arr[i + 1]
                if next_ != "(":
                    print("invalid diff")
                    return None

            else: 
                print('\nError: Invalid character(s) inside the right hand side of the expression')
                return None   # if the element is not an operator, a proper algebra, a number, or parenthesis, then is invalid element
        
        # check if the parenthesis is closed
        if parenthesisOpening != 0:
            print('\nError: You did not close your parenthesis properly!')
            return None
        
        return s


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
    def diffformatter(self, s: str):
        s = (
            s.replace("(", " ( ")
            .replace("diff", " diff ")
            .replace(")", " ) ")
            .replace('**', ' ^ ')
            .replace("+", " + ")
            .replace("-", " - ")
            .replace("/", " / ")
            .replace("*", " * ")
        )
        return s.split()