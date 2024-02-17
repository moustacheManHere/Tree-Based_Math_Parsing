from Ligma.Choices.base_choice import BChoice
from Ligma.Abstract.Diff import Differentiation

# NOTE: DONE BY JEYAKUMAR SRIRAM   
class Choice(BChoice):
    def __init__(self):
        super().__init__()
        self.diff = Differentiation()
    def run(self,forestManager,settings):
        
        choices = settings.print_choices()
        print(f"\t\t{len(choices)+1}. Exit.")
        choice = self.input.getInput("\n\tEnter your choice: ", 
                                     validator=self.inpValidate.integer, 
                                     max_tries = 3,
                                     num_range=range(1,len(choices)+2))
        if not choice: return
        if not choice or choice == len(choices)+1: return
        choice = choice -1 
        if choices[choice] in ["override_warning","save_history","default_graph"]:
            stringToPrint = settings.getDesc(choices[choice])
            print(stringToPrint)

            twoChoice = self.input.getInput(
                    "\n\tToggle True or False? (t,f) ",
                    error="Sorry. A valid choice was not received.",
                    validator=self.inpValidate.string,
                    accept=["T", "F", "t", "f"],
                )
            if not twoChoice: self.run(forestManager,settings)

            if twoChoice in ["T","t"]:
                settings[choices[choice]] = True
            else:
                settings[choices[choice]] = False
           
        elif choices[choice] == "round_sf":
            stringToPrint = settings.getDesc(choices[choice])
            print(stringToPrint)

            twoChoice = self.input.getInput(
                    "\n\tEnable or Disable? (e,d) ",
                    error="Sorry. A valid choice was not received.",
                    validator=self.inpValidate.string,
                    accept=["E", "e", "D", "d"],
                )
            if not twoChoice: self.run(forestManager,settings) 

            if twoChoice in ["e","E"]:
                rounding = self.input.getInput("\n\tEnter your preferred rounding (1-10): ", 
                                     validator=self.inpValidate.integer, 
                                     max_tries = 3,
                                     num_range=range(1,11))
                settings[choices[choice]] = rounding
            else:
                settings[choices[choice]] = False

        self.run(forestManager,settings)
    
    def __str__(self):
        return 'Preferences'