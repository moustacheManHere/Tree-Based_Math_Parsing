class Stack():
    def __init__(self) -> None:
        self.__list = []
        self.__len = 0
    
    def push(self, value):
        self.__list.append(value)
        self.__len += 1
    
    def pop(self):
        if not self.__len: return None
        value = self.__list.pop()
        self.__len -= 1
        return value
    
    # reset method will clear all values in the stack
    def reset(self):
        self.__list = []
        self.__len = 0

    # method to check whether there are cyclical pattern. For example, [1, 2, 3, 1, 2, 3]
    def checkCyclical(self):
         # if the stack length is odd number, or it has zero length, there will never be a cyclical pattern
        if self.__len % 2 == 1 or self.__len == 0: return False

        # divide by the length by half, we will have two "pointers"
        # first "pointer" will check from index 0 to self.__len / 2 - 1
        # while the second "pointer" will check from index self.__len / 2 to self.__len - 1
        # if all element matches, then there is cyclical pattern, else, no
        # checkup cost function: O(n) = n/2 
        halfLen = int(self.__len / 2)
        for i in range(halfLen):
            if self.__list[i] != self.__list[i + (halfLen)]: return False
        
        return True
    
    def __len__(self):
        return self.__len

    def __contains__(self, value):
        return value in self.__list
    
    def __str__(self) -> str:
        return '<' + ', '.join(self.__list) + '>'
    
    def listit(self):
        return self.__list