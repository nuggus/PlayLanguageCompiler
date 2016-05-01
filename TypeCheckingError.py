class TypeCheckingError(Exception):
    def __init__(self, node):
        self.node = node

    def getnode(self):
        return self.node

    def setparent(self, node):
        self.node = node
