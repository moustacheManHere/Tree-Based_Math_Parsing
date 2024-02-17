from Ligma.Choices.base_choice import BChoice

class Choice(BChoice):
    def run(self,forestManager,settings):
        # if there are no assignment statement in the forest manager, then there's no reason to proceed 
        if not len(forestManager):
            print('\nWarning: There is no assignment statements in memory, please add a new assignment statement first.')
            return

        userInput = self.input.getInput('Please enter the variable you want to evaluate:\n', 
                                        validator=self.inpValidate.checkItem, 
                                        error='\nNo correct variable inputted, returning back to main menu',
                                        error_msg = '\nError: variable name not found!',
                                        item_list = forestManager.get_vars())
        
        # if the user input is not none, then is a valid input, then show tree
        if userInput != None:
            self.output.display_tree(forestManager,userInput,settings.data["default_graph"])

    def __str__(self):
        return 'Evaluate a single variable'