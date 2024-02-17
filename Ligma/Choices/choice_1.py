from Ligma.Choices.base_choice import BChoice

class Choice(BChoice):

    def run(self,forestManager, settings):

        userInput = self.input.getInput('Enter the assignment statement you want to add/modify:\nFor example, a=(1+2)\n',
                                         validator=self.statementValidate.assignment_statement, 
                                         error='\nNo valid expression has been inputted, returning back to main menu',
                                         diff = settings["diff"])

        if not userInput: return  # skip if user input is invalid
        
        if settings.data["override_warning"] and forestManager.check_override(userInput):
            twoChoice = self.input.getInput(
                    "\nWarning: A statement already exists for this variable and will be overwritten. Continue (y/n) ? ",
                    error="Sorry. A valid choice was not received.",
                    validator=self.inpValidate.string,
                    accept=["y", "n"],
                    errorAction=self.run,
                )
            if twoChoice == "n":
                return
        forestManager.plant_tree(userInput,settings["diff"])
    
    def __str__(self):
        return 'Add/Modify assignment statement'