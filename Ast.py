import Parsing
import ScannerMain
from AstNode import *
from collections import deque
from graphviz import Graph
from TypeCheckingError import *

parseTree = Parsing.parsing()
i = 0
dot = Graph(comment='Abstract Syntax tree')


# Parsing.printParseTree(parseTree)
def ast(parsenode):
    global i
    parseTreechildrens = parsenode.getchildNodes()
    child = parseTreechildrens.pop(0)
    while child.getName() == 'E':
        if len(parseTreechildrens) > 0:
            child = parseTreechildrens.pop(0)
        else:
            return None
    if child.getisTerminal():
        parent = AstNode(child.getToken())
        parent.set_gv_name(str(i))
        i += 1
    else:
        parent = ast(child)
        while parent is None and len(parseTreechildrens) > 0:
            parent = ast(parseTreechildrens.pop(0))
    dot.node(parent.get_gv_name(), parent.getName())
    while len(parseTreechildrens) > 0:
        child = parseTreechildrens.pop(0)
        if child.getName() == 'E':
            continue
        elif child.getisTerminal():
            astNode = AstNode(child.getToken())
            astNode.set_gv_name(str(i))
            i += 1
        else:
            astNode = ast(child)
            while astNode is None and len(parseTreechildrens) > 0:
                astNode = ast(parseTreechildrens.pop(0))
        if astNode is not None:
            dot.node(astNode.get_gv_name(), astNode.getName())
            astNode.setparent(parent)
            parent.add_child_to_children_list(astNode)
            dot.edge(parent.get_gv_name(), astNode.get_gv_name())
    return parent

if parseTree is not None:
    reducedTree = ast(parseTree)
else:
    print('There exists Lexical Errors')
# dot.render('test-output/round-table.gv', view=True)


stable = {}


def symbolTable(reducedTree):
    global stable
    temp = reducedTree.getchildNodes()[0]
    while temp is not None:
        try:
            stable[temp.getchildNodes()[0].getName()] = temp.getchildNodes()[2].getName()
            temp = temp.getchildNodes()[4]
        except IndexError:
            break
    stable['readint'] = 'int'


# typechecking

def typeChecking(node):
    try:

        if node.getName() == 'program':
            typeChecking(node.getchildNodes()[2])
        elif node.gettype() == 'ident':
            assignmentCheck(node)
            children = node.getchildNodes()
            lastChild = children[len(children) - 1]
            if lastChild.getName() != ';':
                typeChecking(lastChild)
        elif node.getName() == 'while':
            childZero = node.getchildNodes()[0]
            assignmentCheck(childZero)
            children = node.getchildNodes()
            typeChecking(children[2])
            lastChild = children[len(children) - 1]
            if lastChild.getName() != ';':
                typeChecking(lastChild)
        elif node.getName() == 'if':
            childZero = node.getchildNodes()[0]
            assignmentCheck(childZero)
            children = node.getchildNodes()
            typeChecking(children[2])
            else_node = children[3]
            typeChecking(else_node.getchildNodes()[0])
            lastChild = children[len(children) - 1]
            if lastChild.getName() != ';':
                typeChecking(lastChild)
        elif node.getName() == 'writeint':
            childZero = node.getchildNodes()[0]
            if len(childZero.getchildNodes()) > 0:
                assignmentCheck(childZero)
            if childZero.getidenttype() is None:
                typeCheck = stable.get(childZero.getName())
            else:
                typeCheck = childZero.getidenttype()
            if typeCheck == 'bool':
                raise TypeCheckingError(childZero)
    except TypeCheckingError as tc:
        ast = tc.node
        print("Raising Exception:Type mismatch")
        while ast.getparent() is not None:
            dot.edge(ast.getparent().get_gv_name(), ast.get_gv_name(), color='red')
            ast = ast.getparent()
        pass


# end typechecking

def assignmentCheck(node):
    try:
        child1 = node.getchildNodes()[0]
        if child1.getName() == ':=':
            rhs = node.getchildNodes()[1]
        elif child1.gettype() == 'MULTIPLICATIVE' or child1.gettype() == 'ADDITIVE' or child1.gettype() == 'COMPARE':
            rhs = child1.getchildNodes()[0]
        else:
            return
        if len(rhs.getchildNodes()) > 0:
            temp = rhs
            while temp.getName() == '(':
                temp = temp.getchildNodes()[0]
            assignmentCheck(temp)
            if rhs.getName() == '(':
                rhs.setidenttype(temp.getidenttype())
        if rhs.gettype() == 'num':
            rType = 'int'
        elif rhs.getidenttype() is None:
            rType = stable[rhs.getName()]
        else:
            rType = rhs.getidenttype()
        if node.gettype() == 'num':
            lType = 'int'
        elif node.getidenttype() is None:
            lType = stable.get(node.getName())
        else:
            lType = node.getidenttype()
        if rType != lType:
            raise TypeCheckingError(rhs)
        node.setidenttype(rhs.getidenttype())

    except TypeCheckingError as tc:
        ast = tc.node
        print("Raising Exception:Type mismatch")
        while ast.getparent() is not None:
            dot.edge(ast.getparent().get_gv_name(), ast.get_gv_name(), color='red')
            ast = ast.getparent()
        pass

if parseTree is not None:
    outputFile = ScannerMain.sourceFile[:-3] + ".ast.dot"
    fileobject = open(outputFile, 'w')
    symbolTable(reducedTree)
    typeChecking(reducedTree)
    fileobject.write(dot.source)
    fileobject.close()
