from nltk.stem import PorterStemmer
from math import log
from trie import Trie
from heap import MaxHeap
from stack import Stack
from my_queue import MyQueue
from lru import DoublyLinkedList
from graph import Graph

class SearchEngine:
    def __init__(self):
        self.documents = dict()
        self.inverted_index = dict()
        self.stop_words = {
            "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at",
            "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could",
            "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for",
            "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's",
            "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
            "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't",
            "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
            "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't",
            "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
            "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
            "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't",
            "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
            "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
            "yourselves"
            }
        self.ps = PorterStemmer()
        self.trie = Trie()
        self.lru_cache = DoublyLinkedList(10)
        self.graph = Graph()

    def add_document(self, document_name, content):
        original_document_name = document_name
        document_name = document_name.strip(".,():';\"!? ").lower()
        if document_name not in self.documents:
            content = content.split()
            words = []
            for word in content:
                word = word.strip(".,():';\"!? ").lower()
                if word in self.stop_words:
                    continue 
                words.append(self.ps.stem(word))
            self.documents[document_name] = words
            self.graph.add_node(document_name, words)
            for i, word in enumerate(words):
                if word not in self.inverted_index:
                    self.inverted_index[word] = dict()
                    self.trie.insert(word)
                if document_name not in self.inverted_index[word]:
                    self.inverted_index[word][document_name] = {"count": 0, "positions": []}
                self.inverted_index[word][document_name]["count"] += 1
                self.inverted_index[word][document_name]["positions"].append(i)
            return f"{original_document_name} added"
        return f"{original_document_name} already exists"

    def delete_document(self, document_name):
        original_document_name = document_name
        document_name = document_name.strip(".,():';\"!? ").lower()
        if document_name not in self.documents:
            return f"{original_document_name} does not exist"
        for word in self.documents[document_name]:
            del self.inverted_index[word][document_name]
            if not self.inverted_index[word]:
                del self.inverted_index[word]
                self.trie.delete(word)
        self.graph.delete_node(document_name)
        del self.documents[document_name]
        return f"{original_document_name} deleted"

    def search(self, query):
        query = query.split()
        docs_scores = dict()
        docs_containing_all_query_words = set()
        words = []
        for word in query:
            word = word.strip(".,():';\"!? ").lower()
            if word in self.stop_words:
                continue
            word = self.ps.stem(word)
            if word not in self.inverted_index:
                return None
            words.append(word)
        ans = self.lru_cache.get(words)
        if ans is not None:
            return ans
        docs_containing_all_query_words = set(self.inverted_index[words[0]].keys())
        if len(words) > 1:
            for i in range(1, len(words)):
                words_docs = set(self.inverted_index[words[i]].keys())
                docs_containing_all_query_words = docs_containing_all_query_words & words_docs
        docs_containing_query_phrase = docs_containing_all_query_words.copy()
        for doc in docs_containing_all_query_words:
            for index in self.inverted_index[words[0]][doc]["positions"]:
                i = 1
                while i < len(words):
                    if (index + i) in self.inverted_index[words[i]][doc]["positions"]:
                        i += 1
                    else:
                        docs_containing_query_phrase.remove(doc)
                        break
        docs_scores = dict()
        for word in words:
            for doc in docs_containing_query_phrase:
                term_frequency_tf = self.inverted_index[word][doc]["count"] / len(self.documents[doc])
                inverse_document_frequency_idf = log((1 + len(self.documents)) / (1 + len(self.inverted_index[word].keys())))
                score = term_frequency_tf * inverse_document_frequency_idf
                score = score + 0.2 * (len(self.graph.nodes[doc].adj_list))
                docs_scores[doc] = docs_scores.get(doc, 0) + score
        docs_to_rank = [(document_name, tf_idf_score) for document_name, tf_idf_score in docs_scores.items()]
        heap = MaxHeap()
        heapified_docs = heap.heapify(docs_to_rank)
        len_heapified_docs = len(heapified_docs)
        query_result = []
        for _ in range(min(len_heapified_docs, 10)):
            query_result.append(heap.extract(heapified_docs))
        ans = [doc for doc, _ in query_result]
        self.lru_cache.set(words, query_result)
        top_doc = ans[0]
        related_docs = self.graph.bfs(top_doc)
        return ans, related_docs

    def autocomplete_suggestions(self, prefix):
        prefix = prefix.strip(".,():';\"!? ").lower()
        if prefix in self.stop_words:
            return None 
        prefix = self.ps.stem(prefix)
        words = self.trie.prefix(prefix)
        if words is None:
            return None 
        docs_containing_all_prefix = set(self.inverted_index[words[0]].keys())
        for i in range(1, len(words)):
            word_docs = set(self.inverted_index[words[i]].keys())
            docs_containing_all_prefix = docs_containing_all_prefix | word_docs
        
        # We can slice the words list to speed up the next step 
        docs_scores = dict()
        for word in words:
            for doc in docs_containing_all_prefix:
                term_frequency_tf = self.inverted_index[word][doc]["count"] / len(self.documents[doc])
                inverse_document_frequency_idf = log((1 + len(self.documents)) / (1 + len(self.inverted_index[word].keys())))
                score = term_frequency_tf * inverse_document_frequency_idf
                score = score + 0.2 * (len(self.graph.nodes[doc].adj_list))
                docs_scores[doc] = docs_scores.get(doc, 0) + score
        docs_to_rank = [(document_name, tf_idf_score) for document_name, tf_idf_score in docs_scores.items()]
        heap = MaxHeap()
        heapified_docs = heap.heapify(docs_to_rank)
        len_heapified_docs = len(heapified_docs)
        query_result = []
        for _ in range(min(len_heapified_docs, 10)):
            query_result.append(heap.extract(heapified_docs))
        return [doc for doc, _ in query_result]

    def boolean_search(self, query):
        query = query.split()
        words = []
        for word in query:
            word = word.strip(".,:';\"!? ").lower()
            if word in ["not", "and", "or", "(", ")"]:
                words.append(word)
                continue
            if word in self.stop_words:
                continue
            word = self.ps.stem(word)
            if word not in self.inverted_index:
                return None
            words.append(word)
        ans = self.lru_cache.get(words)
        if ans is not None:
            return ans
        stack = Stack()
        queue = MyQueue()
        self.infix_to_postfix(words, stack, queue)  
        query_result = self.evaluate_postfix(stack, queue)
        self.lru_cache.set(words, query_result)
        return query_result

    def infix_to_postfix(self, words, stack, queue):
        for word in words:
            if word == ")":
                top = stack.peek()
                while top != "(":
                    queue.enqueue(stack.pop())
                    top = stack.peek()
                stack.pop()
            elif word in ["not", "("]:
                stack.push(word)
            elif word == "or":
                top = stack.peek()
                while True:
                    if top in ["not", "and"]:
                        queue.enqueue(stack.pop())
                        top = stack.peek()
                    else:
                        break
                stack.push(word)
            elif word == "and":
                top = stack.peek() 
                while True:
                    if top == "not":
                        queue.enqueue(stack.pop())
                        top = stack.peek()
                    else:
                        break
                stack.push(word)
            else:
                queue.enqueue(set(self.inverted_index[word].keys()))
        while stack.head is not None:
            queue.enqueue(stack.pop())
        return
    
    def evaluate_postfix(self, stack, queue):
        stack.head = None 
        while queue.head is not None:
            word = queue.dequeue()
            if word == "not":
                word_docs = stack.pop()
                if not word_docs:
                    return None
                all_docs = set(self.documents.keys())
                result = all_docs - word_docs
                stack.push(result)
            elif word == "and":
                word2_docs = stack.pop()
                word1_docs = stack.pop()
                if not word1_docs or not word2_docs:
                    return None
                stack.push(word1_docs & word2_docs)
            elif word == "or":
                word2_docs = stack.pop()
                word1_docs = stack.pop()
                if not word1_docs or not word2_docs:
                    return None
                stack.push(word1_docs | word2_docs)
            else:
                stack.push(word)
        return stack.pop()