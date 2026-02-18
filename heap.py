class MaxHeap:
    def heapify(self, docs):
        parent = (len(docs) - 2) // 2
        for i in range(parent, -1, -1):
            index = i 
            while index < len(docs):
                left = 2 * index + 1
                right = 2 * index + 2
                largest = index 
                if left < len(docs) and docs[left][1] > docs[largest][1]:
                    largest = left 
                if right < len(docs) and docs[right][1] > docs[largest][1]:
                    largest = right 
                if index == largest:
                    break 
                docs[largest], docs[index] = docs[index], docs[largest]
                index = largest  
        return docs 

    def extract(self, docs):
        if not docs:
            return None
        if len(docs) == 1:
            return docs.pop()
        top_doc = docs[0]
        docs[0], docs[-1] = docs[-1], docs[0]
        docs.pop()
        index = 0 
        while index < len(docs):
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index 
            if left < len(docs) and docs[left][1] > docs[largest][1]:
                largest = left 
            if right < len(docs) and docs[right][1] > docs[largest][1]:
                largest = right 
            if largest == index:
                break 
            docs[index], docs[largest] = docs[largest], docs[index]
            index = largest 
        return top_doc