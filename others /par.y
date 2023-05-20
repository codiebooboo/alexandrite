%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lex.yy.h"
%}

// Define the tokens used by the grammar
%token <str> IDENTIFIER
%token INTEGER FLOAT BOOL STRING
%token IF ELSE WHILE FOR IN
%token RETURN
%token PLUS MINUS MULTIPLY DIVIDE MODULO
%token LESS LESS_EQUAL GREATER GREATER_EQUAL EQUAL NOT_EQUAL
%token AND OR NOT
%token ASSIGNMENT COLON SEMICOLON COMMA DOT
%token LPAREN RPAREN LBRACE RBRACE LBRACKET RBRACKET
%token IMPORT MODULE

// Define the precedence and associativity of operators
%left AND OR
%left LESS LESS_EQUAL GREATER GREATER_EQUAL EQUAL NOT_EQUAL
%left PLUS MINUS
%left MULTIPLY DIVIDE MODULO
%left UNARY_MINUS NOT

// Define the union type used by the grammar
%union {
    int integer;
    float float_val;
    char* str;
}

// Define the grammar rules
%%
program:
    module_list
    ;

module_list:
    module_declaration
    | module_list module_declaration
    ;

module_declaration:
    IMPORT IDENTIFIER SEMICOLON
| MODULE IDENTIFIER LBRACE declaration_list RBRACE SEMICOLON
    ;

declaration_list:
    declaration
    | declaration_list declaration
    ;

declaration:
    variable_declaration SEMICOLON
    | function_declaration
    ;

variable_declaration:
    IDENTIFIER COLON type_annotation ASSIGNMENT expression
    | IDENTIFIER COLON type_annotation
    | IDENTIFIER ASSIGNMENT expression
    | IDENTIFIER
    ;

type_annotation:
    INTEGER
    | FLOAT
    | BOOL
    | STRING
    | IDENTIFIER
    ;

function_declaration:
    IDENTIFIER LPAREN parameter_list RPAREN COLON type_annotation LBRACE statement_list RBRACE
    | IDENTIFIER LPAREN parameter_list RPAREN LBRACE statement_list RBRACE
    | IDENTIFIER LPAREN RPAREN COLON type_annotation LBRACE statement_list RBRACE
    | IDENTIFIER LPAREN RPAREN LBRACE statement_list RBRACE
    ;

parameter_list:
    parameter
    | parameter_list COMMA parameter
    ;

parameter:
    IDENTIFIER COLON type_annotation
    ;

statement_list:
    statement
    | statement_list statement
    ;

statement:
    variable_declaration SEMICOLON
    | assignment_statement SEMICOLON
    | expression_statement
