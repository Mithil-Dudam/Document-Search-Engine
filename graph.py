from stack import Stack
from my_queue import MyQueue


class Node:
        def __init__(self, doc_name, content):
            self.doc_name = doc_name
            self.content = content 
            self.adj_list = set()


class Graph:
    def __init__(self):
        self.nodes = dict()

    def add_node(self, doc_name, content):
        node = Node(doc_name, content)
        self.nodes[node.doc_name] = node
        for n in self.nodes:
            if n == node.doc_name:
                continue
            n_words = set(self.nodes[n].content)
            node_words = set(node.content)
            intersection_of_words = n_words & node_words
            union_of_words = n_words | node_words
            similarity = len(intersection_of_words) / len(union_of_words)
            if similarity > 0.3:
                self.nodes[n].adj_list.add((node.doc_name, similarity))
                self.nodes[node.doc_name].adj_list.add((n, similarity))
        return f"{doc_name} added"

    def delete_node(self, doc_name):
        for doc, score in list(self.nodes[doc_name].adj_list):
            self.nodes[doc].adj_list.remove((doc_name, score))
        del self.nodes[doc_name]
        return f"{doc_name} deleted"

    def bfs(self, doc_name):
        queue = MyQueue()
        queue.enqueue(self.nodes[doc_name])
        seen = set()
        seen.add(doc_name)
        ans = [doc_name]
        while queue.head is not None:
            node = queue.dequeue()
            for n in node.adj_list:
                n = n[0]
                if n not in seen:
                    queue.enqueue(self.nodes[n])
                    seen.add(self.nodes[n].doc_name)
                    ans.append(self.nodes[n].doc_name)
        return ans 

    def dfs(self):
        all_nodes = list(self.nodes.keys())
        seen = set()
        components = []
        while all_nodes:
            stack = Stack()
            stack.push(self.nodes[all_nodes[0]])
            seen.add(self.nodes[all_nodes[0]].doc_name)
            part = [self.nodes[all_nodes[0]].doc_name]
            all_nodes.remove(self.nodes[all_nodes[0]].doc_name)
            while stack.head is not None:
                node = stack.pop()
                for n in node.adj_list:
                    n = n[0]
                    if n not in seen:
                        stack.push(self.nodes[n])
                        seen.add(self.nodes[n].doc_name)
                        part.append(self.nodes[n].doc_name)
                        all_nodes.remove(self.nodes[n].doc_name)
            components.append(part)
        return components