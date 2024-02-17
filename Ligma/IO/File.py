import os
import json
import hashlib

class FileHandler:
    def getChoices(self):
        temp = sorted([i.split(".")[0] for i in os.listdir("Ligma/Choices") if i.startswith("choice_") and i.endswith(".py")])
        OPTIONS = []
        for i in temp:
            try:
                temp = __import__(f"Ligma.Choices.{i}", fromlist=['Choice'])
                choice = temp.Choice()
                OPTIONS.append(choice)
            except:
                pass
        return OPTIONS
    def readFile(self, filename, jsonFile = False):
        try:
            with open(filename, "r") as file:
                if jsonFile:
                    text = json.load(file)
                else:
                    text = file.read()
        except:
            text = None
            if not jsonFile:
                print("Warning: File wasn't read. An default string will be used instead.")
                text = "Lol how did you get here"
        return text
    
    def readChecksumFile(self, filename):
        try:
            with open(filename, "r") as file:
                json_data = json.loads(file.readline().strip())
                stored_checksum = file.readline().strip()
            recalculated_checksum = self.calculate_checksum(json_data)
            if not recalculated_checksum == stored_checksum:
                return None
            return json_data
        except:
            return None
    
    def saveChecksumFile(self,json_data,filename):
        checksum = self.calculate_checksum(json_data)
        with open(filename, 'w') as file:
            file.write(json.dumps(json_data) + '\n')
            file.write(checksum)

    def calculate_checksum(self,data):

        data_bytes = json.dumps(data).encode()  # Convert JSON string to bytes
        hash_object = hashlib.md5(data_bytes)
        return hash_object.hexdigest()

    def ifFileExists(self, filename):
        return os.path.isfile(filename)

    def ifFolderExists(self, folder):
        if not os.path.isdir(folder):
            print("Error: Folder not found!")
            return False
        elif not os.access(folder, os.W_OK):
            print(f"Error: No write permission for {folder}.")
            return False
        return True

    def isWritable(self, filename):
        try:
            _ = open(filename, "w")
            return True
        except:
            return False

    def extractFilesWithExt(self, folder, extensions):
        files = os.listdir(folder)
        if not any(file.lower().endswith(tuple(extensions)) for file in files):
            return None
        accepted_files = [
            os.path.join(folder, file)
            for file in files
            if file.lower().endswith(tuple(extensions))
        ]
        return accepted_files

    def saveFile(self, text, filename, jsonFile = False):
        try:
            with open(filename, "w") as file:
                if jsonFile:
                    json.dump(text, file)
                else:
                    file.write(text)
            return True
        except:
            print("Warning: File couldn't be written.")
            return False
    def getCWD(self):
        return os.getcwd()
    def __str__(self):
        return "<File Handler Object>"