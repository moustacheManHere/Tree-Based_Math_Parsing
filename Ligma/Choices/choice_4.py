from Ligma.Choices.base_choice import BChoice

class Choice(BChoice):
    def run(self,forestManager,settings):
        file = self.input.getInput('\nPlease enter input file: ', 
                                           error='No valid file name provided, returning back to main menu',
                                           validator=self.fileValidate.filename, 
                                           mode='r')
        # if file variable can be "false", it must have been none, which means validation fail, then return back to main menu
        if not file: return   

        content = self.file.readFile(file)

        # marker to check whether content is valid
        isValid = True
        # look through the entire content and validate each line
        for i, line in enumerate(content.split('\n')):
            # if a line is empty, simply skip the whole loop. If the file is empty, it would have been flagged as invalid earlier in the validator
            if not line.strip(): continue

            validated = self.statementValidate.assignment_statement(line,settings["diff"])               # if an input is invalid, it will show why is occur
            if validated == None:
                print(f'The error shown above occurs at line {i + 1} in inputted text file')      # an addition message to show where the error occurred
                isValid = False
                break    # if is already invalid, don't bother continuing
        
        # if the file contents are all valid, proceed to add all the statements into the forest manager
        if isValid:
            for line in content.split('\n'):
                if not line.strip(): continue   # skip empty lines
                forestManager.plant_tree(line)
            forestManager.harvest_tree()
            self.output.show_trees(forestManager)
    
    def __str__(self):
        return 'Read assignment statements from file'