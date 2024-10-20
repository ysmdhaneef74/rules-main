# rules.py

import json
from rule_ast import Node

def create_rule(rule_string):
    # A simplified rule parser that creates an AST from a rule string
    # In practice, you'd want a more robust parser here
    if 'AND' in rule_string:
        parts = rule_string.split(' AND ')
        left = create_rule(parts[0].strip())
        right = create_rule(' AND '.join(parts[1:]).strip())
        return Node(node_type='operator', left=left, right=right, value='AND')
    elif 'OR' in rule_string:
        parts = rule_string.split(' OR ')
        left = create_rule(parts[0].strip())
        right = create_rule(' OR '.join(parts[1:]).strip())
        return Node(node_type='operator', left=left, right=right, value='OR')
    else:
        # Parsing a simple operand condition
        operand = rule_string.strip()
        return Node(node_type='operand', value=operand)

def evaluate_rule(ast, user_data):
    if ast.node_type == 'operator':
        left_result = evaluate_rule(ast.left, user_data)
        right_result = evaluate_rule(ast.right, user_data)
        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result
    elif ast.node_type == 'operand':
        # Evaluate the operand condition against user_data
        # Example: "age > 30"
        try:
            left, operator, right = ast.value.split()
        except ValueError:
            raise ValueError(f"Invalid rule format: {ast.value}. Expected format is 'field operator value'.")

        left_value = user_data.get(left)
        if left_value is None:
            raise ValueError(f"User data does not contain the field '{left}'.")

        # Convert the right side to an integer if it's a digit, otherwise keep it as a string
        right_value = int(right) if right.isdigit() else right

        if operator == '>':
            return left_value > right_value
        elif operator == '<':
            return left_value < right_value
        elif operator == '=':
            return left_value == right_value
        elif operator == '>=':
            return left_value >= right_value
        elif operator == '<=':
            return left_value <= right_value
        elif operator == '!=':
            return left_value != right_value
        else:
            raise ValueError(f"Invalid operator: {operator}")
    return False

