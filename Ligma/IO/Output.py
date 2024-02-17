
from Ligma.Abstract.Sort import MergeSort
import os

class OutputHandler:
    def __init__(self):
        self.sorter = MergeSort()
    # method to allow the program to print a menu based on the given options
    def print_options(self, OPTIONS):
        optionIndex = [i + 1 for i in range(len(OPTIONS)+1)]
        optionIndexStr = map(lambda i: f"'{i}'", optionIndex)
        print(f'\nPlease select your choice ({",".join([s for s in optionIndexStr])}):')
        for option in optionIndex:
            if option == len(optionIndex):
                print(f'\t{option}. Exit')
                return
            print(f'\t{option}. {OPTIONS[option - 1]}')
    
    def print_end(self):
        print("")
        print("Bye, thanks for using ST1507 DSAA: Assignment Statement Evaluator & Sorter")

    def print_start(self):
        os.system("cls" if os.name == "nt" else "clear")
        # the welcome screen will dynamically adjust the width based on the max length of any of the strings below
        TITLE = 'ST1507 DSAA: Evaluating & Sorting Assignment Statements'
        NAMES = ' - Done by: Shawn Lim (2239745) & Jeyakumar Sriram (2214618)'
        CLASSNAME = ' - Class DAAA/2B/01'

        # get max length to determine the width of the table
        maxLen = max([len(TITLE), len(NAMES), len(CLASSNAME)])

        # function to do space padding based on its length
        lineFormatter = lambda text: '* ' + text.ljust(maxLen, ' ') + ' *'

        # print the table
        print()
        print('*' * (maxLen + 4))
        print(lineFormatter(TITLE))
        print('*' + '-' * (maxLen + 2) + '*')
        print('*' + ' ' * (maxLen + 2) + '*')
        print(lineFormatter(NAMES))
        print(lineFormatter(CLASSNAME))
        print('*' + ' ' * (maxLen + 2) + '*')
        print('*' * (maxLen + 4))  
    
    def display_tree(self, forest, var, nicer=False):
        print('\nExpression tree:')
        varTree = forest.getOneTree(var)
        if not nicer:
            self.print_tree(varTree) # TODO: downgrade the print tree to look like the one in the brief
        else:
            print("")
            self.nicer_print_tree(varTree)
            print("")
        # evaluate and get result for the var
        forest.harvest_tree(var)
        result = forest.getOneResult(var)
        print(f'Value for variable "{var}" is {result}')
    
    def show_trees(self,forest,rounding=False):
        # TODO: implement sorting
        print('\nCURRENT ASSIGNMENTS:')
        print('********************')
        variables = forest.get_vars()
        variables = self.sorter.sort(variables)
        for var in variables:
            if not rounding:
                print(f'{var}={forest.getOneStatement(var)}=> {forest.getOneResult(var)}')
            else:
                value = forest.getOneResult(var)
                if isinstance(value, float):
                    value = round(value, rounding)
                print(f'{var}={forest.getOneStatement(var)}=> {value}')

    def show_trees_file(self,forest):
        string = ""
        results = forest.get_results()
        temp = list(results.items())
        trees = self.sorter.sort(temp,True)
        trees = trees[::-1] #reversing it

        if len(trees)<1:
            return "No statements have been written yet dumb dumb"

        string += f"*** Statements with value=> {trees[0][1]}\n"
        string += f"{trees[0][0]}={forest.getOneStatement(trees[0][0])}\n"

        prev = trees[0][1]
        for i in range(1,len(trees)):
            if trees[i][1] == prev:
                string += f"{trees[i][0]}={forest.getOneStatement(trees[i][0])}\n"
            else:
                string += f"\n*** Statements with value=> {trees[i][1]}\n"
                string += f"{trees[i][0]}={forest.getOneStatement(trees[i][0])}\n"
                prev = trees[i][0]

        return string
    
    def print_tree(self,forest):

        def printer(node,level=0):
          if node is not None:
            if node.right is not None:
              printer(node.right,level+1)
            print("."*level + ('**' if node.value == '^' else node.value))
            if node.left is not None:
              printer(node.left,level+1)
              
        printer(forest.headNode)
    
    def nicer_print_tree(self,forest):
        if not forest or not forest.headNode:
            print("Empty tree")
            return

        stack = [(forest.headNode, "", True)] 

        while stack:
            node, prefix, is_last = stack.pop()

            print(prefix + ("└── " if is_last else "├── ") + ("**" if node.value == '^' else str(node.value)))

            if node.right or node.left:
                new_prefix = prefix + ("    " if is_last else "│   ")
                if node.right:
                    stack.append((node.right, new_prefix, not node.left))
                if node.left:
                    stack.append((node.left, new_prefix, True))