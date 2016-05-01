class TreeNode:
    def __init__(self, name=None, isterminal=False, token=None):
        self.name = name
        self.isterminal = isterminal
        self.token = token
        self.childNodes = None

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getisTerminal(self):
        return self.isterminal

    def setisTerminal(self, isterminal):
        self.isterminal = isterminal

    def getToken(self):
        return self.token

    def setToken(self, token):
        self.token = token

    def getchildNodes(self):
        return self.childNodes

    def setchildNodes(self, childNodes):
        self.childNodes = childNodes