class AstNode:
    def __init__(self, token):
        self.parent = None
        self.childNodes = []
        self.name = token[1]
        self.type = token[0]
        self.gv_name = None
        self.identType = None

    def get_gv_name(self):
        return self.gv_name

    def set_gv_name(self, gv_name):
        self.gv_name = gv_name

    def getparent(self):
        return self.parent

    def setparent(self, parent):
        self.parent = parent

    def getchildNodes(self):
        return self.childNodes

    def add_child_to_children_list(self, child_node):
        self.childNodes.append(child_node)

    def getName(self):
        return self.name

    def setName(self, tokenName):
        self.name = tokenName

    def gettype(self):
        return self.type

    def settype(self, tokenType):
        self.type = tokenType

    def getidenttype(self):
        return self.identType

    def setidenttype(self, identType):
        self.type = identType
