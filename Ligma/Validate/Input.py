from Ligma.IO.File import FileHandler

class InputValidator:
    def __init__(self):
        self.fileHandle = FileHandler()
        
    def integer(self,user_input,num_range=None,isInteger=True):
        user_input = user_input.strip()
        try:
            if isInteger:
                user_input = int(user_input)
            else:
                user_input = float(user_input)
        except:
            print("\nError: Unable to convert user input to number.")
            return None
        if num_range is not None and user_input not in num_range:
            print(f"\nError: Number not within acceptable range. ({min(list(num_range))},{max(list(num_range))})")
            return None
        return user_input
    
    def string(self,user_input,accept=None,acceptEmpty=False):
        user_input = user_input.strip()
        try:
            cleaned_string = ''.join(char for char in user_input if char.isalpha() or char.isdigit())
        except:
            print("\nError: Unable to parse given string.")
            return None
        if not acceptEmpty and cleaned_string=="":
            print("\nError: Empty strings or invalid characters are not accepted")
            return None
        if accept is not None and cleaned_string not in accept:
            print("\nError: String not in acceptable values.")
            return None
        return cleaned_string
    
    # checks if an item is inside a list
    # reverse_bool determines whether to check if item is not in list
    def checkItem(self, user_input, item_list: list, reverse_bool = False, error_msg = '\nError: item is not in the list'):
        isItInside = user_input in item_list

        if not isItInside and not reverse_bool or isItInside and reverse_bool:
            print(error_msg)
            return None
        
        return user_input
    
    def is_comma_separated_numbers(self, user_input, item_list):
        numbers = user_input.strip().split(',')
        
        try:
            numbers = [float(num.strip()) for num in numbers]
        except ValueError:
            print("\nError: Unable to convert all parts of the input to numbers.")
            return None
        
        for i in numbers:
            if i not in item_list:
                print("\nError: Invalid Number Found!")
                return None

        return numbers