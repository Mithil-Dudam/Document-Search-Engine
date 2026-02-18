from search_engine import SearchEngine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


se = SearchEngine()


@app.post("/add_document")
def add_document(document_name: str, content: str):
    return se.add_document(document_name, content)

@app.delete("/delete_document/{document_name}")
def delete_document(document_name: str):
    return se.delete_document(document_name)

@app.get("/search")
def search(query: str):
    return se.search(query)

@app.get("/prefix")
def prefix(prefix: str):
    return se.trie.prefix(prefix)

@app.get("/documents")
def documents():
    return list(se.documents.keys())

@app.get("/boolean_search")
def boolean_search(query: str): 
    return se.boolean_search(query)

@app.get("/content/{doc_name}")
def get_content(doc_name: str):
    doc_name = doc_name.strip(",.?!() '\" ").lower()
    if doc_name not in se.documents:
        return None 
    return se.documents[doc_name]

@app.get("/similar_documents/{doc_name}")
def get_similar_documents(doc_name: str):
    doc_name = doc_name.strip(",.?!() '\" ").lower()
    if doc_name not in se.documents:
        return None 
    return se.graph.bfs(doc_name)

@app.get("/connected_components")
def get_connected_components():
    return se.graph.dfs()