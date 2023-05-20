%{
#include <stdio.h>
#include <stdlib.h>
%}

%option noyywrap

DIGIT [0-9]
LETTER [a-zA-Z]
IDENTIFIER ({LETTER}|_)(({DIGIT}|{LETTER}|_)*)
FLOAT ({DIGIT}+\.{DIGIT}+)
STRING \"([^\\\n]|(\\.))*\"

%%

{IDENTIFIER} {
    printf("IDENTIFIER %s\n", yytext);
}

{FLOAT} {
    printf("FLOAT %s\n", yytext);
}

{STRING} {
    printf("STRING %s\n", yytext);
}

"+" {
    printf("PLUS\n");
}

"-" {
    printf("MINUS\n");
}

"*" {
    printf("MULTIPLY\n");
}

"/" {
    printf("DIVIDE\n");
}

"=" {
    printf("ASSIGN\n");
}

">" {
    printf("GREATER_THAN\n");
}

"<" {
    printf("LESS_THAN\n");
}

">=" {
    printf("GREATER_THAN_OR_EQUAL\n");
}

"<=" {
    printf("LESS_THAN_OR_EQUAL\n");

"==" {
    printf("EQUAL\n");
}

"!=" {
    printf("NOT_EQUAL\n");
}

"&&" {
    printf("LOGICAL_AND\n");
}

"||" {
    printf("LOGICAL_OR\n");
}

"!" {
    printf("LOGICAL_NOT\n");
}

"if" {
    printf("IF\n");
}

"else" {
    printf("ELSE\n");
}

"for" {
    printf("FOR\n");
}

"while" {
    printf("WHILE\n");
}

"func" {
    printf("FUNCTION\n");
}

"class" {
    printf("CLASS\n");
}

"var" {
    printf("VAR\n");
}

"mut" {
    printf("MUT\n");
}

"import" {
    printf("IMPORT\n");
}

"module" {
    printf("MODULE\n");
}

"return" {
    printf("RETURN\n");
}

"true" {
    printf("TRUE\n");
}

"false" {
    printf("FALSE\n");
}

"//"(.*) {
    // Ignore single-line comments
}

"/\*"([^*]|\*[^/])*\*/" {
    // Ignore multi-line comments
}

\n {
    // Ignore newline characters
}

[ \t]+ {
    // Ignore whitespace characters
}

. {
    printf("INVALID_CHARACTER %c\n", yytext[0]);
}

%%

int main() {
    yylex();
    return 0;
}