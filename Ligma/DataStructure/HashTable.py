# hash table data structure
class HashTable():
    def __init__(self, size = 256) -> None:
        # if the size is an integer, then we want the hash table to have the said size but the keys and values are all none
        if isinstance(size, int):
            self.__size = size                  # size of the hash table, which includes the unassigned key value pair (with the None)
            self.__currentSize = 0              # size of the hash table, which only includes assigned key value pair (no None key value pair)
            self.__keys = [None] * self.__size
            self.__values = [None] * self.__size
        
        # or else, it must be a dictionary
        else:
            if not isinstance(size, dict):
                raise TypeError('Parameter size accepts either integer or dictionary')
            
            self.__keys = list(size.keys())
            self.__values = list(size.values())
            # the size of this hashtable is assumed to be the size of the dictonary given
            self.__size = self.__currentSize = len(self.__keys)
   

    
    # as I expect the key to be string, I will use the python built-in hash function to hash, and then add the rehash value, and then get the remainder
    def __hashing(self, key, rehash):
        return (hash(key) + rehash) % self.__size
    
    # method to double the size of the hashtable every time it fills up and then repopulate
    def __expandHashTable(self):
        tempKeys = self.__keys
        tempValues = self.__values
        
        # "reinitialise" the hashtable with a new size and then set all items again
        self.__size *= 2
        self.__keys = [None] * self.__size
        self.__values = [None] * self.__size

        for key, value in zip(tempKeys, tempValues):
            self.__setitem__(key, value)
    
    # setter
    def __setitem__(self, key, value):
        # first, check if the current size has match the size of the hash table, which means the hash table is full, then is time to double in size and repopulate
        if self.__currentSize == self.__size:
            self.__expandHashTable()
        
        # loop through the entire length of the hash table for rehashing (because in the real world, it is super rare to have a perfect hash table)
        # if the hash table is initially empty, the rehash value will always be 0. This way, lesser code will be needed compared to having a while loop
        for rehash_value in range(self.__size):
            idx = self.__hashing(key, rehash_value)
            # if the current index if empty, or the key matches, then set the values and break the for loop
            current_key = self.__keys[idx]
            if current_key == None or current_key == key:
                # if a new key has been added only, then append the current size
                if current_key == None: self.__currentSize += 1

                self.__keys[idx] = key
                self.__values[idx] = value
                break
        else:
            # if it managed to get here, it means the table is full as it managed to loop through the entire table, then expand and rehash every item, and try set again
            # the reason for doing it here is that there will be scenario when the hash table is full, but you only want to edit a value in a key that already exist
            # hence to avoid expanding the table unnecessarily, I just expand when it needs to
            self.__expandHashTable()
            self.__setitem__(key, value)

    
    # getter
    def __getitem__(self, key):
        # same as the setter, loop through the entire length but until the key is found
        for rehash_value in range(self.__size):
            idx = self.__hashing(key, rehash_value)
            if self.__keys[idx] == key:
                return self.__values[idx]
            
        # if the for loop managed to loop through the entire length and is still unable to find the key, raise an error
        raise KeyError('Error: hash table is unable to locate the key inputted!')
    
    # returns a key value pair, though will not return none keys, so just like a regular dictionary
    def items(self):
        return [(key, value) for key, value in zip(self.__keys, self.__values) if key != None]
    
    def keys(self):
        return sorted([i for i in self.__keys if i !=  None])

    # length of the hash table
    def __len__(self):
        return self.__currentSize
    
    # show the entire hash table
    def __str__(self) -> str:
        return '< ' + ', '.join([f'{key}:{value}' for key, value in zip(self.__keys, self.__values)]) + ' >'