from Ligma.Abstract.Node import TreeNode

class Differentiation:
    def differentiate(self, node, target):
        if node.left is None and node.right is None:
            if node.value.isalpha() and node.value==target:
                return TreeNode("1")
            else:
                return TreeNode("0")
            
        if node.value in ["-","+"]:
            node.left = self.differentiate(node.left, target)
            node.right = self.differentiate(node.right, target)
            return node
        
        if node.value == "*":
            temp = TreeNode("+")
            temp.right = TreeNode("*")
            temp.left = TreeNode("*")

            temp.right.left = self.differentiate(node.left, target)
            temp.right.right = node.right

            temp.left.left = node.left
            temp.left.right = self.differentiate(node.right, target)

            return temp 
        
        if node.value == "/":
            temp = TreeNode("/")
            temp.left = TreeNode("-")
            temp.right = TreeNode("^")

            temp.right.left = node.right
            temp.right.right = TreeNode("2")

            temp.left.left = TreeNode("*")
            temp.left.right = TreeNode("*")

            temp.left.left.left = node.right
            temp.left.left.right = self.differentiate(node.left, target)

            temp.left.right.left = node.left
            temp.left.right.right = self.differentiate(node.right, target)

            return temp 
        
        if node.value == "^":
            # cosnider taylor series expandsion for log so that only use basic operators
            temp = TreeNode("*")

            temp.left = TreeNode("^")
            temp.left.left = node.left 
            temp.left.right = node.right 

            temp.right = TreeNode("+")

            temp.right.left = TreeNode("*")
            temp.right.left.left = node.right 
            temp.right.left.right = TreeNode("/")
            temp.right.left.right.left = self.differentiate(node.left, target)
            temp.right.left.right.right = node.left 

            temp.right.right = TreeNode("*")
            temp.right.right.left = self.differentiate(node.right, target)
            temp.right.right.right = TreeNode("log")
            temp.right.right.right.left = node.left 
            temp.right.right.right.right = node.left 
            return temp

        if node.value == "log":
            temp = TreeNode("/")
            temp.left = TreeNode("1")
            temp.right = node.left
            return temp
        
    def getDiffTree(self, tree, target, n=1):
        tree.headNode = self.differentiate(tree.headNode,target)
        return tree