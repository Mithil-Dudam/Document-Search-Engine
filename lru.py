class Node:
    def __init__(self, query, query_result):
        self.query = query
        self.query_result = query_result
        self.next = None 
        self.prev = None 

class DoublyLinkedList:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queries = dict()
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail 
        self.tail.prev = self.head

    def get(self, query):
        if " ".join(query) in self.queries:
            node = self.queries[" ".join(query)]
            query_result = node.query_result
            node.next.prev = node.prev 
            node.prev.next = node.next
            node.next = self.head.next 
            self.head.next.prev = node 
            node.prev = self.head 
            self.head.next = node 
            return query_result
        return None 

    def set(self, query, query_result):
        self.queries[" ".join(query)] = Node(" ".join(query), query_result)
        
        def add(query):
            node = self.queries[" ".join(query)]
            node.next = self.head.next 
            self.head.next.prev = node 
            node.prev = self.head 
            self.head.next = node 
            return 
        
        if len(self.queries) < self.capacity:
            add(query)
            return
        temp = self.tail.prev
        self.tail.prev = temp.prev 
        temp.prev.next = self.tail 
        temp.next = None 
        temp.prev = None 
        del self.queries[temp.query]
        add(query)
        return