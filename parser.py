from lexer import Lexer, Token, TokenType

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def error(self, message):
        raise Exception(f'Parser error: {message}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Expected token type {token_type}, but got {self.current_token.type}')

    def parse(self):
        self.current_token = self.lexer.get_next_token()
        return self.program()

    def program(self):
        nodes = []
        while self.current_token.type != TokenType.EOF:
            node = self.statement()
            if node is not None:
                nodes.append(node)
        return ProgramNode(nodes)

    def statement(self):
        if self.current_token.type == TokenType.VAR:
            return self.variable_declaration()
        elif self.current_token.type == TokenType.MUT:
            return self.mutable_declaration()
        elif self.current_token.type == TokenType.IF:
            return self.if_statement()
        elif self.current_token.type == TokenType.FOR:
            return self.for_loop()
        elif self.current_token.type == TokenType.WHILE:
            return self.while_loop()
        elif self.current_token.type == TokenType.FUNC:
            return self.function_declaration()
        elif self.current_token.type == TokenType.RETURN:
            return self.return_statement()
        else:
            return self.expression_statement()

    def variable_declaration(self):
        self.eat(TokenType.VAR)
        identifier = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        expr = self.expression()
        self.eat(TokenType.SEMICOLON)
        return VariableDeclarationNode(identifier, expr)

    def mutable_declaration(self):
        self.eat(TokenType.MUT)
        identifier = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        expr = self.expression()
        self.eat(TokenType.SEMICOLON)
        return MutableDeclarationNode(identifier, expr)

    def if_statement(self):
        self.eat(TokenType.IF)
        condition = self.expression()
        self.eat(TokenType.THEN)
        body = self.block()
        else_body = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            else_body = self.block()
        return IfStatementNode(condition, body, else_body)

    def for_loop(self):
        self.eat(TokenType.FOR)
        identifier = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.IN)
        iterable = self.expression()
        self.eat(TokenType.THEN)
        body = self.block()
        return ForLoopNode(identifier, iterable, body)

    def while_loop(self):
        self.eat(TokenType.WHILE)
        condition = self.expression()
        self.eat(TokenType.THEN)
        body = self.block()
        return WhileLoopNode(condition, body)

    def function_declaration(self):
        self.eat(TokenType.FUNC)
        identifier = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LEFT_PAREN)
        parameters = []
        if self.current_token.type != TokenType.RIGHT_PAREN:
            parameters.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                parameters.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.RIGHT_PAREN)
        body = self.block()
        return FunctionDeclarationNode(identifier, parameters, body)

    def return_statement(self):
        self.eat(TokenType.RETURN)
        expr = self.expression()
        self.eat(TokenType.SEMICOLON)
        return ReturnStatementNode(expr)

    def expression_statement(self):
        expr = self.expression()
        self.eat(TokenType.SEMICOLON)
        return ExpressionStatementNode(expr)

    def block(self):
        nodes = []
        self.eat(TokenType.LEFT_BRACE)
        while self.current_token.type != TokenType.RIGHT_BRACE:
            node = self.statement()
            if node is not None:
                nodes.append(node)
        self.eat(TokenType.RIGHT_BRACE)
        return BlockNode(nodes)

    def expression(self):
        node = self.equality()
        while self.current_token.type in (TokenType.AND, TokenType.OR):
            token = self.current_token
            if token.type == TokenType.AND:
                self.eat(TokenType.AND)
            elif token.type == TokenType.OR:
                self.eat(TokenType.OR)
            node = LogicalOperatorNode(node, token, self.equality())
        return node

    def equality(self):
        node = self.comparison()
        while self.current_token.type in (TokenType.EQUALS, TokenType.NOT_EQUALS):
            token = self.current_token
            if token.type == TokenType.EQUALS:
                self.eat(TokenType.EQUALS)
            elif token.type == TokenType.NOT_EQUALS:
                self.eat(TokenType.NOT_EQUALS)
            node = BinaryOperatorNode(node, token, self.comparison())
        return node

    def comparison(self):
        node = self.term()
        while self.current_token.type in (TokenType.LESS_THAN, TokenType.LESS_THAN_OR_EQUALS, TokenType.GREATER_THAN, TokenType.GREATER_THAN_OR_EQUALS):
            token = self.current_token
            if token.type == TokenType.LESS_THAN:
                self.eat(TokenType.LESS_THAN)
            elif token.type == TokenType.LESS_THAN_OR_EQUALS:
                self.eat(TokenType.LESS_THAN_OR_EQUALS)
            elif token.type == TokenType.GREATER_THAN:
                self.eat(TokenType.GREATER_THAN)
            elif token.type == TokenType.GREATER_THAN_OR_EQUALS:
                self.eat(TokenType.GREATER_THAN_OR_EQUALS)
            node = BinaryOperatorNode(node, token, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinaryOperatorNode(node, token, self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberNode(token)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return StringNode(token)
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            if self.current_token.type == TokenType.LEFT_PAREN:
                return self.function_call(token.value)
            else:
                return VariableNode(token)
        elif token.type == TokenType.LEFT_PAREN:
            self.eat(TokenType.LEFT_PAREN)
            node = self.expression()
            self.eat(TokenType.RIGHT_PAREN)
            return node
        elif token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            return UnaryOperatorNode(token, self.factor())
        else:
            self.error(f'Unexpected token {token.value} of type {token.type}')

    def function_call(self, identifier):
        self.eat(TokenType.LEFT_PAREN)
        arguments = []
        if self.current_token.type != TokenType.RIGHT_PAREN:
            arguments.append(self.expression())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                arguments.append(self.expression())
        self.eat(TokenType.RIGHT_PAREN)
        return FunctionCallNode(identifier, arguments)
