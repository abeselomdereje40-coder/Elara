import ast
import operator

operators={
    ast.Add:operator.add,
    ast.Sub:operator.sub,
    ast.Mult:operator.mul,
    ast.Div:operator.truediv,
    ast.FloorDiv:operator.floordiv,
    ast.Mod:operator.mod,
    ast.Pow:operator.pow
}

unary_operators={
    ast.UAdd:operator.pos,
    ast.USub:operator.neg
}

def calculate_node(node):
    if isinstance(node,ast.Constant):
        if isinstance(node.value,(int,float)):
            return node.value
        raise ValueError("Only numbers are allowed")

    if isinstance(node,ast.BinOp):
        operator_type=type(node.op)
        if operator_type not in operators:
            raise ValueError("Operator is not supported")

        left=calculate_node(node.left)
        right=calculate_node(node.right)
        return operators[operator_type](left,right)

    if isinstance(node,ast.UnaryOp):
        operator_type=type(node.op)
        if operator_type not in operators:
            raise ValueError("Operator is not supported")

        value=calculate_node(node.operand)

        return unary_operators[operator_type](value)
    raise ValueError("Invalid mathimatical expression")

def calculator_tool(expression):
    try:
        expression=expression.strip()
        tree=ast.parse(
            expression,
            mode="eval"
        )
        result=calculate_node(tree.body)
        return result
    except ZeroDivisionError:
        return f"Can not divide by zero"

    except Exception as e:
        return f"Calculator error:{str(e)}"
