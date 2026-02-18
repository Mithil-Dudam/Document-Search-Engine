class Node:
    def __init__(self, word):
        self.word = word 
        self.next = None 

class MyQueue:
    def __init__(self):
        self.head = None 
        self.tail = None 
    
    def enqueue(self, word):
        node = Node(word)
        if self.head is None:
            self.head = node 
            self.tail = node 
            return 
        self.tail.next = node 
        self.tail = node 
        return 

    def dequeue(self):
        if self.head is None:
            return None 
        temp = self.head 
        self.head = self.head.next 
        temp.next = None 
        if self.head is None:
            self.tail = None 
        return temp.word 