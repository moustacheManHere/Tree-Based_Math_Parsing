from Ligma.IO.File import FileHandler
import os


class FileValidator:
    def __init__(self):
        self.fileHandle = FileHandler()
        self.reserved = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]

    # validating the file name that will be used to read or write a file
    # NOTE: the mode parameter should only accept 'r' as reading file or 'w' as writing file
    def filename(self, user_input, mode, extensions=[".txt"]):
        if mode not in ['r', 'w']: raise ValueError('Error: file validator filename only accepts "r" or "w" for mode parameter.')

        user_input = user_input.strip()
        validExt = any(user_input.lower().endswith(ext) for ext in extensions)

        # first check if is valid file extension
        if not validExt:
            print("\nError: This file extension is not yet supported.")
            return None
        
        # then check if there are any slashes "/" or "\" which implies going out of the directory
        if '/' in user_input or '\\' in user_input:
            print('\nError: Do not use any slashes')
            return None
        
        # at this stage, it should be the right extension and right directory, then check if the file exists for file reading
        if not self.fileHandle.ifFileExists(user_input) and mode == 'r':
            print("\nError: File does not exist!")
            return None
        elif self.fileHandle.ifFileExists(user_input) and mode == 'w':      # however, if file exists and is write mode, then need to prompt the user whether to overwrite
            toOverwrite = input('\nWarning: The file you want to write to already exists. Do you want to overwrite? (y/n) ').strip().lower()
            if toOverwrite != 'y':
                return 0     # if user doesn't want to overwrite, then return 0, which will skip the rest of the process
        
        # then, check if the file name is a reserved file name
        base_name = os.path.splitext(user_input)[0].upper()
        if base_name in self.reserved:
            print("\nDo not use reserved names you idiot!")
            return None
        
        # lastly, the content of the file shouldn't be empty for reading file
        if mode == 'r':
            content = self.fileHandle.readFile(user_input).strip()
            if not content:
                print('\nError: The file content is empty, there is nothing to read!')
                return None
        
        return user_input   # if all the validations pass, then return the user input

    def foldername(self, user_input, extensions=[".txt"], mustexist=True):

        user_input = user_input.strip()
        if not mustexist:
            try:
                os.makedirs(user_input)
                print(f"Directory '{user_input}' created successfully.")
            except OSError as e:
                print(f"Error creating directory '{user_input}': {e}")
            return user_input
        if not self.fileHandle.ifFolderExists(user_input):
            print("Folder not found!")
            return None
        accept = self.fileHandle.extractFilesWithExt(user_input, extensions)
        accept = [i for i in accept if os.path.basename(i)[0] not in self.reserved]
        if accept == None:
            print("Error: Folder does not contain files of desired types.")
            return None
        return accept

    def __str__(self):
        return "<File Validation Object>"