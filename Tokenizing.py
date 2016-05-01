import re

tokens = []
parserTokens = []


# this function is used to identify identifiers

def identifyingNumbers(tok):
    matchObj = re.match(r'^[1-9]*[1-9]+$|^[0]$', tok, re.M)
    if (matchObj):
        tokens.append(['num(', tok + ")"])
        parserTokens.append(['num', tok])
    else:
        tokens.append(['Lexical Error', 'Lexical Error'])
        parserTokens.append(['Lexical Error', 'Lexical Error'])
        return 'invalid'
    return tok;


# end of builtinfunction

# this function is used to identify identifiers
def identifyingIdentifiers(tok):
    matchObj = re.match(r'^-?[A-Z][A-Z0-9]*$', tok, re.M)
    if (matchObj):
        tokens.append(['ident(', tok + ")"])
        parserTokens.append(['ident', tok])
    else:
        tok = identifyingNumbers(tok)
    return tok;


# end of builtinfunction

# this function will be used to identify
def identifyingOperators(tok):
    compareOperators = ['>', '<', '>=', '<=', '=', '!=']
    additiveOperators = ['+', '-']
    multiplicativeOperators = ['*', 'div', 'mod']
    if (tok in compareOperators):
        tokens.append(["COMPARE(", tok + ")"])
        parserTokens.append(['COMPARE', tok])
    elif (tok in additiveOperators):
        tokens.append(["ADDITIVE(", tok + ")"])
        parserTokens.append(['ADDITIVE', tok])
    elif (tok in multiplicativeOperators):
        tokens.append(["MULTIPLICATIVE(", tok + ")"])
        parserTokens.append(['MULTIPLICATIVE', tok])
    elif (tok is ";"):
        tokens.append(["SC(", tok + ")"])
        parserTokens.append(['SC', tok])
    elif (tok == ":="):
        tokens.append(["ASGN(", tok + ")"])
        parserTokens.append(['ASGN', tok])
    elif (tok is "("):
        tokens.append(["LP(", tok + ")"])
        parserTokens.append(['LP', tok])
    elif (tok is ")"):
        tokens.append(["RP(", tok + ")"])
        parserTokens.append(['RP', tok])
    else:
        tok = identifyingIdentifiers(tok)
    return tok;


# end of operators function

# this function will be used to identify
def identifyingComments(tok):
    if (tok == "%"):
        return "%"
    else:
        tok = identifyingOperators(tok)
    return tok;


# end of comments function

# this function will be used to identify keywords
def identifyingBoollit(tok):
    bool_literals = ['true', 'false'];
    if tok in bool_literals:
        tokens.append(["boollit(", tok + ")"])
        parserTokens.append(['boollit', tok])
    else:
        tok = identifyingComments(tok)
    return tok;
    # end of keywords function


# this function will be used to identify keywords
def identifyingKeyWords(tok):
    keywords_list = ['if', 'then', 'else', 'begin', 'end', 'while', 'do', 'program', 'var', 'as', 'writeint', 'readint',
                     'int', 'bool'];
    if tok in keywords_list:
        tokens.append([str(tok).upper(), ''])
        parserTokens.append(['KEYWORD', tok])
    else:
        tok = identifyingBoollit(tok)
    return tok;
    # end of keywords function
