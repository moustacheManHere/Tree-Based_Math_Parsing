from Ligma.IO.Input import InputHandler
from Ligma.Validate.Input import InputValidator
from Ligma.Validate.Statement import StatementValidator
from Ligma.IO.File import FileHandler
from Ligma.Validate.File import FileValidator
from Ligma.IO.Output import OutputHandler

class BChoice:
    def __init__(self):
        self.inpValidate = InputValidator()
        self.statementValidate = StatementValidator()
        self.input = InputHandler()
        self.file = FileHandler()
        self.fileValidate = FileValidator()
        self.output = OutputHandler()