import re

# Define the set of tokens
tokens = [
    ('COMMENT', r'//.*'),
    ('COMMENT', r'/\*[\s\S]*?\*/'),
    ('VAR', r'var'),
    ('MUT', r'mut'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('COLON', r':'),
    ('EQUALS', r'='),
    ('TYPE', r'Int|Float|Bool|String|List|Dictionary'),
    ('OPERATOR', r'[+\-*/]'),
    ('COMPARISON', r'[=!<>]=|[<>]'),
    ('LOGICAL', r'&&|\|\|'),
    ('IF', r'if'),
    ('ELSE', r'else'),
    ('FOR', r'for'),
    ('IN', r'in'),
    ('RANGE', r'\.\.'),
    ('WHILE', r'while'),
    ('FUNC', r'func'),
    ('CLASS', r'class'),
    ('INIT', r'init'),
    ('OVERRIDE', r'override'),
    ('MODULE', r'module'),
    ('IMPORT', r'import'),
    ('THROW', r'throw'),
    ('TRY', r'try'),
    ('CATCH', r'catch'),
    ('ERROR', r'[a-zA-Z_][a-zA-Z0-9_]*Error'),
    ('LEFT_PAREN', r'\('),
    ('RIGHT_PAREN', r'\)'),
    ('LEFT_BRACE', r'{'),
    ('RIGHT_BRACE', r'}'),
    ('LEFT_BRACKET', r'\['),
    ('RIGHT_BRACKET', r'\]'),
    ('COMMA', r','),
    ('DOT', r'\.'),
    ('NEWLINE', r'\n'),
]

# Read input text
text = """
// This is a comment
var name: String = "Alice"
var age = 30
mut counter: Int = 0
var sum = 3 + 5
if x < 10 {
    print("x is less than 10")
} else if x >= 10 && x <= 20 {
    print("x is between 10 and 20")
} else {
    print("x is greater than 20")
}
for i in 0..10 {
    print(i)
}
while counter < 5 {
    print(counter)
    counter += 1
}
func greet(name: String) {
    print("Hello, \(name)!")
}
class Animal {
    var name: String
    init(name: String) {
        self.name = name
    }
    func speak() {
        print("\(name) makes a sound")
    }
}
"""

# Initialize variables
pos = 0
tokens_list = []

# Match tokens
while pos < len(text):
    match = None
    for token in tokens:
        pattern = token[1]
        regex = re.compile(pattern)
        match = regex.match(text, pos)
        if match:
            if token[0] == 'NEWLINE':
                tokens_list.append(('NEWLINE', '\n'))
            else:
                tokens_list.append((token[0], match.group(0)))
            pos = match.end(0)
            break
    if not match:
        print('Invalid input at position:', pos)
        break

# Output tokens
print(tokens_list)
