# rule_ast.py

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # 'operator' or 'operand'
        self.left = left            # Left child node (for operators)
        self.right = right          # Right child node (for operators)
        self.value = value          # The value of the operand or operator

    def __repr__(self):
        return f'Node(type={self.node_type}, value={self.value})'
