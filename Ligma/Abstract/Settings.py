from Ligma.DataStructure.HashTable import HashTable
from Ligma.IO.File import FileHandler

class Settings:
    def __init__(self):
        self.data = HashTable()
        self.file = FileHandler()
        self.load_settings()
        pass

    def load_settings(self):
        loaded_data = self.file.readFile("./settings.json", True)
        if loaded_data is None:
            self.data["override_warning"] = False
            self.data["round_sf"] = False
            self.data["default_graph"] = True
            self.data["save_history"] = False
            self.data["diff"] = False
            return

        # Validate and set override_warning
        self.data["override_warning"] = loaded_data.get("override_warning", False)
        if not isinstance(self.data["override_warning"], bool):
            self.data["override_warning"] = False

        # Validate and set round_sf
        self.data["round_sf"] = loaded_data.get("round_sf", False)
        if not isinstance(self.data["round_sf"], int):
            self.data["round_sf"] = False

        # Validate and set default_graph
        self.data["default_graph"] = loaded_data.get("default_graph", False)
        if not isinstance(self.data["default_graph"],bool):
            self.data["default_graph"] = False

        # Validate and set save_history
        self.data["save_history"] = loaded_data.get("save_history", False)
        if not isinstance(self.data["save_history"], bool):
            self.data["save_history"] = False
        
        self.data["diff"] = loaded_data.get("diff", False)
        if not isinstance(self.data["diff"], bool):
            self.data["diff"] = False

    def save_settings(self):
        dic = {key: value for key, value in self.data.items() if key is not None}
        self.file.saveFile(dic, "./settings.json", True)
    
    def print_choices(self):
        print("\n\tPlease select the setting you would like to modify:")
        keys = self.data.keys()
        keys = [i for i in keys if i != "diff"]
        sub = {"default_graph": "Change Default Graph View",
                "override_warning": "Warn me when new statement override old ones",
                "round_sf":"Round off values shown to me",
                "save_history":"Make my assignments persistent across sessions"}
        for index, key in enumerate(keys, start=1):
            print(f"\t\t{index}. {sub[key]}")
        return keys
    
    def getDesc(self, key):

        if key == "override_warning":
            return """
            Description: If set to True, it overrides warnings.
            
                When assigning to the same variable twice, the previous assignment 
                get overriden. To have a warning if this happens, please toggle this.
            """
        
        elif key == "round_sf":
            return """
            Description: Set the number of decimal figures for rounding. False if not needed.
            
            Possible values (1-10)"""
        
        elif key == "default_graph":
            return """
        Description: If set to True, the a new graph is enabled.
            
            Old Graph:
                        .2
                        +
                        .1

            New Graph: 
                        └── +
                            └── 1
                            ├── 2
            """
        
        elif key == "save_history":
            return """
            Description: If set to True, the your assignments and values are saved for the next time you will come.
        
            Note: Remeber to open the app in the same directory"""
        
        else:
            return "Invalid key. No description available for this setting."
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save_settings()