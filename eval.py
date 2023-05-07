from typing import Dict

class Interpreter:
    def __init__(self):
        self.environment = {}

    def evaluate(self, node):
        if isinstance(node, ProgramNode):
            return self.evaluate_program_node(node)
        elif isinstance(node, VariableDeclarationNode):
            return self.evaluate_variable_declaration_node(node)
        elif isinstance(node, MutableDeclarationNode):
            return self.evaluate_mutable_declaration_node(node)
        elif isinstance(node, AssignmentNode):
            return self.evaluate_assignment_node(node)
        elif isinstance(node, BinaryOperatorNode):
            return self.evaluate_binary_operator_node(node)
        elif isinstance(node, UnaryOperatorNode):
            return self.evaluate_unary_operator_node(node)
        elif isinstance(node, FunctionDeclarationNode):
            return self.evaluate_function_declaration_node(node)
        elif isinstance(node, FunctionCallNode):
            return self.evaluate_function_call_node(node)
        elif isinstance(node, IdentifierNode):
            return self.evaluate_identifier_node(node)
        elif isinstance(node, LiteralNode):
            return self.evaluate_literal_node(node)
        elif isinstance(node, IfStatementNode):
            return self.evaluate_if_statement_node(node)
        elif isinstance(node, ForLoopNode):
            return self.evaluate_for_loop_node(node)
        elif isinstance(node, WhileLoopNode):
            return self.evaluate_while_loop_node(node)
        elif isinstance(node, ReturnStatementNode):
            return self.evaluate_return_statement_node(node)
        elif isinstance(node, ExpressionStatementNode):
            return self.evaluate_expression_statement_node(node)
        elif isinstance(node, BlockNode):
            return self.evaluate_block_node(node)
        else:
            raise Exception(f"Invalid node type: {type(node)}")

    def evaluate_program_node(self, node):
        result = None
        for statement in node.statements:
            result = self.evaluate(statement)
        return result

    def evaluate_variable_declaration_node(self, node):
        value = self.evaluate(node.expression)
        self.environment[node.identifier] = value
        return value

    def evaluate_mutable_declaration_node(self, node):
        value = self.evaluate(node.expression)
        self.environment[node.identifier] = value
        return value

    def evaluate_assignment_node(self, node):
        value = self.evaluate(node.expression)
        self.environment[node.identifier] = value
        return value

    def evaluate_binary_operator_node(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        if node.operator.type == TokenType.PLUS:
            return left + right
        elif node.operator.type == TokenType.MINUS:
            return left - right
        elif node.operator.type == TokenType.MULTIPLY:
            return left * right
        elif node.operator.type == TokenType.DIVIDE:
            if right == 0:
                raise Exception("Division by zero")
            return left / right
        elif node.operator.type == TokenType.MODULO:
            return left % right
        elif node.operator.type == TokenType.EQUALS:
            return left == right
        elif node.operator.type == TokenType.NOT_EQUALS:
            return left != right
        elif node.operator.type == TokenType.LESS_THAN:
            return left < right
        elif node.operator.type == TokenType.LESS_THAN_OR_EQUALS:
            return left <= right
        elif node.operator.type == TokenType.GREATER_THAN:
            return left > right
        elif node.operator.type == TokenType.GREATER_THAN_OR_EQUALS:
            return left >= right
        elif node.operator.type == TokenType.AND:
            return left and right
        elif node.operator.type == TokenType.OR:
            return left or right
        else:
            raise Exception(f"Invalid operator: {node.operator.type}")

    def evaluate_unary_operator_node(self, node):
        operand = self.evaluate(node.operand)
        if node.operator.type == TokenType.MINUS:
            return -operand
        elif node.operator.type == TokenType.NOT:
            return not operand
        else:
            raise Exception(f"Invalid operator: {node.operator.type}")

    def evaluate_function_declaration_node(self, node):
        self.environment[node.identifier] = node
        return node

    def evaluate_function_call_node(self, node):
        function_node = self.evaluate(node.function)
        if not isinstance(function_node, FunctionDeclarationNode):
            raise Exception(f"Invalid function call: {node.function}")
        if len(function_node.parameters) != len(node.arguments):
            raise Exception(f"Invalid number of arguments for function call: {node.function}")
        local_environment = {}
        for parameter, argument in zip(function_node.parameters, node.arguments):
            local_environment[parameter] = self.evaluate(argument)
        previous_environment = self.environment
        self.environment = local_environment
        result = self.evaluate(function_node.body)
        self.environment = previous_environment
        return result

    def evaluate_identifier_node(self, node):
        if node.value not in self.environment:
            raise Exception(f"Undefined variable: {node.value}")
        return self.environment[node.value]

    def evaluate_literal_node(self, node):
        return node.value

    def evaluate_if_statement_node(self, node):
        condition = self.evaluate(node.condition)
        if condition:
            return self.evaluate(node.body)
        else:
            return self.evaluate(node.else_body)

    def evaluate_for_loop_node(self, node):
        iterable = self.evaluate(node.iterable)
        result = None
        for item in iterable:
            self.environment[node.identifier] = item
            result = self.evaluate(node.body)
        return result

    def evaluate_while_loop_node(self, node):
        result = None
        while self.evaluate(node.condition):
            result = self.evaluate(node.body)
        return result

    def evaluate_return_statement_node(self, node):
        return self.evaluate(node.expression)

    def evaluate_expression_statement_node(self, node):
        return self.evaluate(node.expression)

    def evaluate_block_node(self, node):
        result = None
        for statement in node.statements:
            result = self.evaluate(statement)
        return result
