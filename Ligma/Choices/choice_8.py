from Ligma.Choices.base_choice import BChoice
from Ligma.Abstract.Diff import Differentiation

# NOTE: DONE BY JEYAKUMAR SRIRAM   
class Choice(BChoice):
    def __init__(self):
        super().__init__()
        self.diff = Differentiation()
    def run(self,forestManager,settings):
        
        print("Enable Differentiations?")
        # show all custom functions

        # ask if editting, removing existing function or adding ["e", "r", "a"]
        choice = self.input.getInput("Enter your choice (E for enable, D for diable): ", 
                                     validator=self.inpValidate.string, 
                                     max_tries = 3,
                                     accept=["e","E","d","D"])
        if not choice: return

        if choice in ["e","E"]:
            settings["diff"] = True
            
        if choice in ["d","D"]:
            settings["diff"] = False
        

    
    def __str__(self):
        return 'Enable Differentiation'