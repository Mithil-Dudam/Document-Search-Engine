class Node:
    def __init__(self, word):
        self.word = word 
        self.next = None

class Stack: 
    def __init__(self):
        self.head = None 
    
    def push(self, word):
        node = Node(word)
        node.next = self.head 
        self.head = node 
        return 

    def pop(self):
        if self.head is None:
            return None 
        temp = self.head 
        self.head = self.head.next 
        temp.next = None 
        return temp.word 

    def peek(self):
        if self.head is None:
            return None 
        return self.head.word 