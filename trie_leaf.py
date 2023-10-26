class TrieLeaf:
    # Initiate a leaf: contains its subword (for compression) and value
    def __init__(self, subword, value=-1):
        self.value = value
        self.subword = subword
        self.suffix = None
    
    # To check if this object is a leaf
    def isLeaf(self):
        return True