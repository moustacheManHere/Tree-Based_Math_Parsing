from Ligma.Choices.base_choice import BChoice

class Choice(BChoice):
    def run(self,forestManager,settings):
        file = self.input.getInput('\nPlease enter output file: ', validator=self.fileValidate.filename, mode='w')

        # same thing for option 5, but it can be 0 if user doesn't want to overwrite, then go back to main menu
        if not file: return
        forestManager.harvest_tree()
        # sorting should occur over here
        outputString = self.output.show_trees_file(forestManager)

        # try writing
        self.file.saveFile(outputString, file)
        
    def __str__(self):
        return 'Sort assignment statements'