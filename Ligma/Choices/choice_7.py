from Ligma.Choices.base_choice import BChoice
from Ligma.Abstract.Node import TreeNode
from Ligma.Tree.Forest import ForestManager
import turtle

OPERATORS = ['+', '-', '*', '/', '^']
ADD = lambda x, y: x + y
SUBTRACT = lambda x, y: x - y
MUL = lambda x, y: x * y
DIVIDE = lambda x, y: x / y
POWER = lambda x, y: x ** y
MAPPING = {
    '+' : ADD,
    '-' : SUBTRACT,
    '*' : MUL,
    '/' : DIVIDE,
    '^' : POWER
}

# NOTE: DONE BY SHAWN LIM
class Choice(BChoice):

    def __init__(self):
        super().__init__()
        # parameters for adjusting the turtle drawing
        self.VALUE_HEIGHT = 20      # sets the height of the value written, to give some empty spaces between each branch line for the text
        self.CHANGE_OF_ANGLE = 0.8  # sets the rate of change of the spread for every level, to prevent the branches from overlapping itself
        self.INITIAL_ANGLE = 150    # sets the initial angle between the branchs
        self.FONT = ('Arial', 12, 'normal')     # configure and standarise the font for the text
    
    # formula for getting the length of branch
    def __get_branch_length(self, x):
        return 1000 / (x + 5)
            
    # the method to do the actual evaluation
    def evaluate(self, node: TreeNode, t: turtle.Turtle, angle: float, length_step: int, forestManager: ForestManager):

        # set the angle for left and right branches
        l_angle = 270 - (angle / 2)
        r_angle = 270 + (angle / 2)
        next_level_angle = angle * self.CHANGE_OF_ANGLE     # also set angle for the next recursive layer
        # get the branch length, it is a decay curve because the top part of the branch must be long enough so bottom part will not overlap easily
        branch_len = self.__get_branch_length(length_step)

        # if both the left and right side are none, then it can only occur when there are only one value/variable in the expression
        if node.left is None and node.right is None:
            if node.value.isalpha():

                alpha = node.value

                # try to find the variable and go further, it there's error, it means it doesn't exists
                try:
                    value = self.evaluate(forestManager.getOneTree(alpha).get_tree(), t, next_level_angle, length_step + 1, forestManager)
                    value = round(float(value), 2)
                except Exception as e:
                    value = None

                t.penup(); t.setheading(90); t.forward(self.VALUE_HEIGHT * 2); t.pendown() # move down a bit without writing
                t.write(f'{alpha} = {value}', font=self.FONT)
                t.penup(); t.backward(self.VALUE_HEIGHT * 2); t.pendown();    # go back
            else:
                value = node.value

                t.penup(); t.setheading(270); t.forward(self.VALUE_HEIGHT); t.pendown() # move down a bit without writing
                t.write(value, font=self.FONT)
                t.penup(); t.backward(self.VALUE_HEIGHT); t.pendown();    # go back

            return value
        
        # check and see what's the current node value
        current_val = node.value
        # if is an operator, then evaluate further, and also write the symbol
        if current_val in OPERATORS:
            t.write(current_val, font=self.FONT)

            t.setheading(l_angle); t.forward(branch_len)    # set direction and move
            left_value = self.evaluate(node.left, t, next_level_angle, length_step + 1, forestManager)
            t.setheading(l_angle); t.penup(); t.backward(branch_len); t.pendown()

            t.setheading(r_angle); t.forward(branch_len)    # set direction and move
            right_value = self.evaluate(node.right, t, next_level_angle, length_step + 1, forestManager)
            t.setheading(r_angle); t.penup(); t.backward(branch_len); t.pendown()
        

        # if the left or right value gets a none, it means one of them had a variable that was never defined at all
        if left_value is None or right_value is None: 
            t.penup(); t.setheading(90); t.forward(self.VALUE_HEIGHT); t.pendown() # move down a bit without writing
            t.write('None', font=self.FONT)
            t.penup(); t.backward(self.VALUE_HEIGHT); t.pendown();    # go back
            return None
        
        t.penup(); t.setheading(90); t.forward(self.VALUE_HEIGHT); t.pendown() # move up a bit without writing to write the output value

        # map the operator to the appropriate function, and call that function and input the values
        try:
            output = MAPPING[node.value](float(left_value), float(right_value))
        except Exception as e:
            # if there's error, means got none value, or something invalid, then go here and write none and return none
            t.write('None', font=self.FONT)
            t.penup(); t.backward(self.VALUE_HEIGHT); t.pendown();    # go back
            return None
        
        t.write(round(output, 2), font=self.FONT)
        t.penup(); t.backward(self.VALUE_HEIGHT); t.pendown();    # go back
        return output
    

    def run(self,forestManager, _):
        # this option will be similar to option 3, except that this option will actually visualise the evaluation with a GUI
        # if there are no assignment statement in the forest manager, then don't proceed
        if not len(forestManager):
            print('\nWarning: There is no assignment statements in memory, please add a new assignment statement first.')
            return
        
        userInput = self.input.getInput('Please enter the variable you want to visualise the evaluation:\n', 
                                        validator=self.inpValidate.checkItem, 
                                        error='\nNo correct variable inputted, returning back to main menu',
                                        error_msg = '\nError: variable name not found!',
                                        item_list = forestManager.get_vars())
        
        # if the user input is none, then is an invalid input, then don't proceed to visualise the evaluation
        if userInput == None: return

        # set the turtle to running so that every time it was closed, it can be run again
        turtle.TurtleScreen._RUNNING=True

        tur = turtle.Turtle()
        tur.speed(1)

        # make the turtle go up a bit to make space for the drawing
        tur.penup()
        tur.setheading(90)
        tur.forward(256)
        tur.pendown()

        turtle.title('Assignment statement visualisation')
    
        self.evaluate(forestManager.getOneTree(userInput).get_tree(), tur, self.INITIAL_ANGLE, 1, forestManager)
        turtle.exitonclick()
        
    def __str__(self):
        return 'Visualising variable evaluation'
