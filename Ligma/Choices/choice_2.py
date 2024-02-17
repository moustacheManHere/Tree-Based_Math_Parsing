from Ligma.Choices.base_choice import BChoice

class Choice(BChoice):
    def run(self,forestManager,settings):
        forestManager.harvest_tree()

        # print the results 
        if not settings.data["round_sf"]:
            self.output.show_trees(forestManager)
        else:
            rounding = settings.data["round_sf"]
            self.output.show_trees(forestManager, rounding)
    
    def __str__(self):
        return 'Display current assignment statements'