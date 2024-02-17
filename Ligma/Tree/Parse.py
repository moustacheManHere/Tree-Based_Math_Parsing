from Ligma.Abstract.Node import TreeNode

class ParseTree:
    def __init__(self,expression):
        self.expression = expression

        exp_format = self.formatter(expression)

        # if the splitted expression has only 3 items, it means there were originally only one value in the expression
        # then simply create a lonely tree node with no connection
        if len(exp_format) == 3:
            self.headNode = TreeNode(exp_format[1])
        
        else:
            exp_array, _ = self.depth_spliter(exp_format)
            self.headNode = self.tree_build(exp_array)

    def formatter(self,exp):
        exp = (
            exp.replace("(", " ( ")
            .replace(")", " ) ")
            .replace("**", " ^ ")
            .replace("+", " + ")
            .replace("-", " - ")
            .replace("/", " / ")
            .replace("*", " * ")
        )

        return exp.split()

    def depth_spliter(self, arr, index=0):
        current_list = []

        while index < len(arr):
            item = arr[index]
            if item == "(":
                sub_list, index = self.depth_spliter(arr, index + 1)
                current_list.append(sub_list)
            elif item == ")":
                return current_list, index 
            else:
                current_list.append(item)

            index += 1

        return current_list, index

    def tree_build(self,arr):
        PODMAS_rev = ["+","-","*","/",'^']
        if len(arr) < 1 or arr is None:
            return None
            
        if len(arr) == 1 and isinstance(arr[0],str):
            return TreeNode(arr[0])

        if len(arr) == 1 and isinstance(arr[0],list):
            return self.tree_build(arr[0])

        for i in PODMAS_rev:
            if i in arr:
                op_index = arr.index(i)
                left_arr = arr[0:op_index]
                right_arr = arr[op_index+1:]
                node = TreeNode(i,self.tree_build(right_arr),self.tree_build(left_arr))
                return node
    
    def serialize(self):
        serial_arr = []
        def serial(node):
            val = node.value 
            if node.left is None and node.right is None:
                temp = (val,None,None)
                serial_arr.append(temp)
                return len(serial_arr) - 1
            else:
                left = serial(node.left)
                right = serial(node.right)
                temp = (val, left, right)
                serial_arr.append(temp)
                return len(serial_arr) - 1
        head_index = serial(self.headNode)
        return serial_arr
    
    def deserialize(self, serialized_data):
        def deserial(index):
            val = serialized_data[index][0]
            right = serialized_data[index][2]
            left = serialized_data[index][1]
            if left is not None and right is not None:
                left = deserial(left)
                right = deserial(right)
            else:
                left = None 
                right= None
            node = TreeNode(val,right,left)
            return node
        root = deserial(len(serialized_data)-1)
        return root

    def get_tree(self):
        return self.headNode
    
    def __str__(self) -> str:
        return self.expression