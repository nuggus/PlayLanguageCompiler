from ScannerMain import *
from ParseError import *
from TreeNode import *
from collections import deque

i = 0
tokensList = []
tokenList = scannerMethod()
nextToken = tokenList[i]
identifierList = []
compare = ['>', '<', '>=', '<=', '=', '!=']
declarationFlag = False


# begin of term()
def term(param):
    termNode = TreeNode()
    global nextToken, i
    if param in nextToken:
        if i < (len(tokenList) - 1):
            termNode = TreeNode(param, True, nextToken)
            i += 1
            nextToken = tokenList[i]
        else:
            termNode = TreeNode(param, True, nextToken)
    else:
        raise ParseError('term did not match')

    return termNode


# end of term()

# begin of expression1() no:13 completed
def expression1():
    exp1ParentNode = TreeNode('<expression1>')  # parent node and is child of assignment1
    exp1ChildList = []
    if nextToken[1] in [';', 'then', 'do', ')']:
        exp1ChildList.append(epsilon())
    elif nextToken[0] == 'COMPARE':
        exp1ChildList.append(termType('COMPARE'))
        exp1ChildList.append(expression())
    else:
        raise ParseError('Raise ParseError:in expression1()')

    exp1ParentNode.setchildNodes(exp1ChildList)
    return exp1ParentNode


# end of expression1()

# begin of simplexpression1() no:15 completed
def simplexpression1():
    simexp1ParentNode = TreeNode('<simpleexpression1>')  # parent node and is child of simpleexpression
    simexp1ChildList = []
    if nextToken[1] in [';', 'then', 'do', ')']:
        simexp1ChildList.append(epsilon())
    elif nextToken[0] == 'COMPARE':
        simexp1ChildList.append(epsilon())
    elif nextToken[0] == 'ADDITIVE':
        simexp1ChildList.append(termType('ADDITIVE'))
        simexp1ChildList.append(simplexpression())
    else:
        raise ParseError('Raise ParseError:in simpleexpression1()')

    simexp1ParentNode.setchildNodes(simexp1ChildList)
    return simexp1ParentNode


# end of simplexpression()
# start of termType()
def termType(type):
    termNode = TreeNode()
    global nextToken, i
    if nextToken[0] == type:
        if i < (len(tokenList) - 1):
            termNode = TreeNode(nextToken[1], True, nextToken)
            i += 1
            nextToken = tokenList[i]
        else:
            termNode.setName(nextToken[1])
            termNode.setisTerminal('True')
    else:
        raise ParseError('term did not match')

    return termNode


# end of termType()
# begin of termgrammar1() no:17 completed
def termgrammar1():
    termgrammar1ParentNode = TreeNode('<term1>')  # parent node and is child of term
    termgrammar1ChildList = []

    if nextToken[0] == 'COMPARE' or nextToken[0] == 'ADDITIVE' or nextToken[1] in [';', ')', 'do', 'then']:
        termgrammar1ChildList.append(epsilon())
    elif nextToken[0] == 'MULTIPLICATIVE':
        termgrammar1ChildList.append(term(nextToken[1]))
        termgrammar1ChildList.append(termgrammar())
    else:
        raise ParseError('Raise ParseError:in termgrammar1()')

    termgrammar1ParentNode.setchildNodes(termgrammar1ChildList)
    return termgrammar1ParentNode


# end of termgrammar1()

# begin of factor() no:18 completed
def factor():
    factorParentNode = TreeNode('<factor>')  # parent node and is child of termgrammar
    factorChildList = []
    if nextToken[0] == 'num':
        factorChildList.append(termType('num'))
    elif nextToken[0] == 'ident':
        factorChildList.append(termType('ident'))
    elif nextToken[0] == 'boollit':
        factorChildList.append(termType('boollit'))
    elif nextToken[1] == '(':
        factorChildList.append(term('('))
        factorChildList.append(expression())
        factorChildList.append(term(')'))
    else:
        raise ParseError('Raise ParseError:in factor()')

    factorParentNode.setchildNodes(factorChildList)
    return factorParentNode


# end of factor()

# begin of termgrammar() no:16 completed
def termgrammar():
    termgrammarParentNode = TreeNode('<term>')  # parent node and is child of simpleexpression
    termgrammarChildList = []

    if nextToken[0] == 'ident' or nextToken[0] == 'num' or nextToken[0] == 'boollit' or nextToken[1] == '(':
        termgrammarChildList.append(factor())
        termgrammarChildList.append(termgrammar1())
    else:
        raise ParseError('Raise ParseError:in termgrammar()')

    termgrammarParentNode.setchildNodes(termgrammarChildList)
    return termgrammarParentNode


# end of termgrammar()

# begin of simpleexpression() no:14 completed
def simplexpression():
    simexpParentNode = TreeNode('<simpleexpression>')  # parent node and is child of assignment1
    simexpChildList = []
    if nextToken[0] == 'ident' or nextToken[0] == 'num' or nextToken[0] == 'boollit' or nextToken[1] == '(':
        simexpChildList.append(termgrammar())
        simexpChildList.append(simplexpression1())
    else:
        raise ParseError('Raise ParseError:in simplexpression()')

    simexpParentNode.setchildNodes(simexpChildList)
    return simexpParentNode


# end of simpleexpression()
# begin of expression() no:12 completed
def expression():
    expParentNode = TreeNode('<expression>')  # parent node and is child of assignment1
    expChildList = []
    if nextToken[0] == 'ident' or nextToken[0] == 'num' or nextToken[0] == 'boollit' or nextToken[1] == '(':
        expChildList.append(simplexpression())
        expChildList.append(expression1())
    else:
        raise ParseError('Raise ParseError:in expression()')

    expParentNode.setchildNodes(expChildList)
    return expParentNode


# end of expression()

# begin of elseclause() no:09 completed
def elseclause():
    elseParentNode = TreeNode('<else clause>')  # parent node and is child of ifstatement
    elseChildList = []
    if nextToken[1] == 'else':
        elseChildList.append(term('else'))
        elseChildList.append(statementsequence())
    elif nextToken[1] == 'end':
        elseChildList.append(epsilon())
    else:
        raise ParseError('Raise ParseError: elseclause()')

    elseParentNode.setchildNodes(elseChildList)
    return elseParentNode


# end of elseclause()

# begin of ifstatement() no:08 completed
def ifstatement():
    ifParentNode = TreeNode('<ifstatement>')  # parent node and is child of statement
    ifChildList = []

    if nextToken[1] == 'if':
        ifChildList.append(term('if'))
        ifChildList.append(expression())
        ifChildList.append(term('then'))
        ifChildList.append(statementsequence())
        ifChildList.append(elseclause())
        ifChildList.append(term('end'))
    else:
        raise ParseError('Raise ParseError:inifstatement()')

    ifParentNode.setchildNodes(ifChildList)
    return ifParentNode


# end of ifstatement()

# begin of whilestatement() no:10 completed

def whilestatement():
    whileParentNode = TreeNode('<whilestatement>')  # parent node and is child of statement
    whileChildList = []
    if nextToken[1] == 'while':
        whileChildList.append(term('while'))
        whileChildList.append(expression())
        whileChildList.append(term('do'))
        whileChildList.append(statementsequence())
        whileChildList.append(term('end'))
    else:
        raise ParseError('Raise ParseError:inwhilestatement()')

    whileParentNode.setchildNodes(whileChildList)
    return whileParentNode


# end of whilestatement()

# begin of writeint() no:11 completed
def writeint():
    writeintParentNode = TreeNode('<writeint>')  # parent node and is child of statement
    writeintChildList = []
    if nextToken[1] == 'writeint':
        writeintChildList.append(term('writeint'))
        writeintChildList.append(expression())
    else:
        raise ParseError('Raise ParseError:in writeint()')

    writeintParentNode.setchildNodes(writeintChildList)
    return writeintParentNode


# end of writeint()

# begin of assignment1() no:07 completed
def assignment1():
    asgn1ParentNode = TreeNode('<assignment1>')  # parent node and is child of assignment
    asgn1ChildList = []
    if nextToken[1] == 'readint':
        asgn1ChildList.append(term('readint'))
    elif nextToken[0] == 'ident' or nextToken[0] == 'num' or nextToken[0] == 'boollit' or nextToken[1] == '(':
        asgn1ChildList.append(expression())
    else:
        raise ParseError('Raise ParseError:in assignment1()')

    asgn1ParentNode.setchildNodes(asgn1ChildList)
    return asgn1ParentNode


# end of assignment1()

# begin of ident()
def ident():
    termNode = TreeNode()
    global nextToken, i, declarationFlag

    if nextToken[0] == 'ident':
        if nextToken[1] in identifierList:
            if i < (len(tokenList) - 1):
                termNode = TreeNode(nextToken[1], True, nextToken)
                i += 1
                nextToken = tokenList[i]
            else:
                termNode.setName(nextToken[1])
                termNode.setisTerminal('True')
        else:
            raise ParseError('Trying to use undeclared variable')
    else:
        raise ParseError('term did not match')

    return termNode


# end of ident()

# begin of assignment() no:06 completed
def assignment():
    asgnParentNode = TreeNode('<assignment>')  # parent node and is child of statement
    asgnChildList = []
    if nextToken[0] == 'ident':
        asgnChildList.append(ident())
        asgnChildList.append(term(':='))
        asgnChildList.append(assignment1())
    else:
        raise ParseError('Raise ParseError:in assignment()')

    asgnParentNode.setchildNodes(asgnChildList)
    return asgnParentNode


# end of assignment()

# begin statement()  no:05 completed: ifstatement, whilestatement, writeint, assignment

def statement():
    # <assignment> | <ifstatement> | <whilestatement> | <writeInt>
    stmtParentNode = TreeNode('<statement>')  # parent node and is child of statementsequence
    stmtChildList = []

    if nextToken[1] == 'if':
        stmtChildList.append(ifstatement())
    elif nextToken[1] == 'while':
        stmtChildList.append(whilestatement())
    elif nextToken[1] == 'writeint':
        stmtChildList.append(writeint())
    elif nextToken[0] == "ident":
        stmtChildList.append(assignment())
    else:
        raise ParseError('ParseError raised:in statement()')

    stmtParentNode.setchildNodes(stmtChildList)
    return stmtParentNode


# end statement()

# begin of statementSequence() no:04 completed
def statementsequence():
    stseqParentNode = TreeNode('<statementsequence>')  # parent node and is child of program
    stseqChildList = []

    if nextToken[1] == 'end' or nextToken[1] == 'else':
        stseqChildList.append(epsilon())
    elif nextToken[0] == 'ident' or nextToken[1] == 'if' or nextToken[1] == 'while' or nextToken[1] == 'writeint':
        stseqChildList.append(statement())
        stseqChildList.append(term(';'))
        stseqChildList.append(statementsequence())
    else:
        raise ParseError('Raise ParserError: in statementsequence()')

    stseqParentNode.setchildNodes(stseqChildList)
    return stseqParentNode


# end of statementSequence()


# begin of epsilon()
def epsilon():
    eNode = TreeNode('E', True)
    return eNode


# end of epsilon()

# typeMethod() begin no:03 completed
def typemethod():
    typeParentNode = TreeNode('<type>')  # parent node and is child of declarations
    typeChildList = []

    if nextToken[1] == 'int' or nextToken[1] == 'bool':
        typeChildList.append(term(nextToken[1]))
    else:
        raise ParseError('Raising ParseError in checking type')

    typeParentNode.setchildNodes(typeChildList)
    return typeParentNode


# typeMethod() end no:03 completed
# begin of identifier()


def identifier():
    global i, nextToken
    identifierNode = None
    if nextToken[0] == "ident":
        if not declarationFlag:
            if nextToken[1] in identifierList:
                # print(identifierList)
                # print("Identifier is already declared!")
                if i < (len(tokenList) - 1):
                    i += 1
                    nextToken = tokenList[i]
                raise ParseError('Raising ParseError:Identifier is already declared')
            else:
                identifierNode = TreeNode(nextToken[1], True, nextToken)
                identifierList.append(nextToken[1])
                if i < (len(tokenList) - 1):
                    i += 1
                    nextToken = tokenList[i]
        else:
            if nextToken[1] not in identifierList:
                raise ParseError('Raising ParseError:Trying to use undeclared variable')
    else:
        raise ParseError('Raised ParserError: in identifier()')

    return identifierNode


# end of identifier()

# begin of declaration() no:02 completed
def declarations():
    decParentNode = TreeNode('<declaration>')  # parent node and is child of program
    decChildList = []
    global declarationFlag

    if nextToken[1] == 'begin':
        decChildList.append(epsilon())
        declarationFlag = True
    elif nextToken[1] == 'var':
        decChildList.append(term('var'))
        decChildList.append(identifier())
        decChildList.append(term('as'))
        decChildList.append(typemethod())
        decChildList.append(term(';'))
        decChildList.append(declarations())
    else:
        raise ParseError('Raising ParseError while declarations')

    decParentNode.setchildNodes(decChildList)
    return decParentNode


# end of declarations()

# begin of program() no:01 completed
def program():
    programNode = None
    childList = []
    try:
        if nextToken[1] == 'program':
            programNode = TreeNode('<program>')  # root node
            childList.append(term('program'))
            childList.append(declarations())
            childList.append(term('begin'))
            childList.append(statementsequence())
            childList.append(term('end'))
            programNode.setchildNodes(childList)
        else:
            raise ParseError('Program did not start with keyword:program')
    except ParseError as e:
        print(e)
    return programNode


# end of program()

queue = deque()


# start tree traversal
def printParseTree(parsetree):
    if parsetree is not None:
        level = 0
        queue.append(parsetree)
        while len(queue) > 0:
            node = queue.popleft()
            print(node.getName())

            if not node.getisTerminal():
                try:
                    for n in node.getchildNodes():
                        queue.append(n)
                except Exception as e:
                    print(e)


# end tree traversal

def parsing():
    if 'Lexical Error' not in tokenList[-1][0]:
        parsetree = program()
        return parsetree
    else:
        print('Lexical Errors Exist, so can not parse')
    return None


#printParseTree(parsing())
