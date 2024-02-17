from Ligma.IO.Output import OutputHandler
from Ligma.IO.Input import InputHandler
from Ligma.Validate.Input import InputValidator
from Ligma.Validate.Statement import StatementValidator
from Ligma.IO.File import FileHandler
from Ligma.Tree.Forest import ForestManager
from Ligma.Abstract.Settings import Settings
class Ballz():
    def __init__(self):
        self.output = OutputHandler()
        self.input = InputHandler()
        self.inpValidate = InputValidator()
        self.file = FileHandler()
        self.forestManager = ForestManager()
        self.OPTIONS = self.file.getChoices()
        self.statementValidate = StatementValidator()
        self.settings = Settings()
        
        self.settings.load_settings()
        history = self.file.readChecksumFile("history.lol")
        if history is not None:
            self.forestManager.loadTrees(history)

    def run(self):

        choice = None
        
        while True:

            self.input.getInput("\nPress enter to continue....  ")
            self.output.print_options(self.OPTIONS)
            choice = self.input.getInput("Enter choice: ", validator=self.inpValidate.integer, num_range=range(1,len(self.OPTIONS)+2), max_tries = 0)
            if not choice: continue
            if choice == len(self.OPTIONS) + 1:
                self.file.saveChecksumFile(self.forestManager.saveTrees(),"history.lol")
                self.settings.save_settings()
                break

            script = self.OPTIONS[choice-1]
            script.run(self.forestManager, self.settings)