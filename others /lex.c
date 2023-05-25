#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Define token types
typedef enum {
    TOK_EOF,
    TOK_IDENTIFIER,
    TOK_INTEGER,
    TOK_STRING,
    TOK_PLUS,
    TOK_MINUS,
    TOK_STAR,
    TOK_SLASH,
    TOK_LPAREN,
    TOK_RPAREN,
} TokenType;

// Define token structure
typedef struct {
    TokenType type;
    char* lexeme;
} Token;

// Define lexer function
Token* lex(char* input) {
    // Allocate memory for token list
    Token* tokens = (Token*) malloc(sizeof(Token) * 100);
    int tokenCount = 0;
    
    // Iterate through input string
    int i = 0;
    while (input[i] != '\0') {
        // Ignore whitespace
        if (isspace(input[i])) {
            i++;
            continue;
        }
        
        // Identify tokens
        if (isdigit(input[i])) {
            // Integer token
            char* start = &input[i];
            while (isdigit(input[i])) {
                i++;
            }
            char* end = &input[i];
            int length = end - start;
            char* lexeme = (char*) malloc(sizeof(char) * (length+1));
            strncpy(lexeme, start, length);
            lexeme[length] = '\0';
            Token token = { TOK_INTEGER, lexeme };
            tokens[tokenCount++] = token;
        } else if (isalpha(input[i])) {
            // Identifier or keyword token
            char* start = &input[i];
            while (isalnum(input[i]) || input[i] == '_') {
                i++;
            }
            char* end = &input[i];
            int length = end - start;
            char* lexeme = (char*) malloc(sizeof(char) * (length+1));
            strncpy(lexeme, start, length);
            lexeme[length] = '\0';
            Token token;
            if (strcmp(lexeme, "var") == 0) {
                token.type = TOK_VAR;
            } else if (strcmp(lexeme, "if") == 0) {
                token.type = TOK_IF;
            } else if (strcmp(lexeme, "else") == 0) {
                token.type = TOK_ELSE;
            } else if (strcmp(lexeme, "while") == 0) {
                token.type = TOK_WHILE;
            } else {
                token.type = TOK_IDENTIFIER;
            }
            token.lexeme = lexeme;
            tokens[tokenCount++] = token;
        } else {
            // Operator or punctuation token
            Token token;
            switch (input[i]) {
                case '+': token.type = TOK_PLUS; break;
                case '-': token.type = TOK_MINUS; break;
                case '*': token.type = TOK_STAR; break;
                case '/': token.type = TOK_SLASH; break;
                case '(': token.type = TOK_LPAREN; break;
                case ')': token.type = TOK_RPAREN; break;
                default:
                    printf("Error: invalid character '%c'\n", input[i]);
                    exit(1);
            }
            char* lexeme = (char*) malloc(sizeof(char) * 2);
            lexeme[0] = input[i];
            lexeme[1] = '\0';
            token.lexeme = lexeme;
            tokens[tokenCount++] = token;
            i++;
        }
    }
    
    // Add EOF token
    Token eofToken = { TOK_EOF, "" };
    tokens[tokenCount++] = eofToken;
    
    // Trim token list
    tokens = (Token*) realloc(tokens, sizeof(Token) * tokenCount);
    
    return tokens;
}

int main() {
    // Test lexer
    char* input = "var x = 123 + y";
    Token* tokens = lex(input);
    for (int i = 0; tokens[i].type != TOK_EOF; i++) {
        printf("%d: %s\n", tokens[i].type, tokens[i].lexeme);
    }
    return 0;
}
