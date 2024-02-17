# class to handle all the input related functionalities
class InputHandler:
    # method to get user input, can be customised to determine whether to validate, set the max number of tries, etc.
    def getInput(self,prompt,error="Unknown Error!",validator=None,max_tries=3,errorAction=None,**kwargs):

        user_input = input(prompt)
        if validator is None: return user_input
        validated = validator(user_input,**kwargs)

        if max_tries == 0: return validated 

        tries = 1
        while tries < max_tries and validated is None:
            tries += 1
            user_input = input(prompt)
            validated = validator(user_input,**kwargs)
        if tries == max_tries and validated is None:
            print(error)
            if errorAction is None:
                return None
            else:
                errorAction()
                return
        return validated
    def __str__(self):
        return "<Input Handler Object>"