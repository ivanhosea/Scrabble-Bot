class TrieNode:
    # Initiate TrieNode: contains subword (for compression), child nodes (A-Z), and value
    def __init__(self, subword='', value=-1):
        self.subword = subword
        self.value = value
        self.suffix = None
        self.nodes = [None for i in range(26)]
    
    # To indicate that this node isn't a leaf
    def isLeaf(self):
        return False