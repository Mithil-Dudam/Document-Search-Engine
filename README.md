# Document Search Engine

A Python-based search engine with phrase search, autocomplete, boolean search, LRU caching, and document similarity graph, exposed via a FastAPI web API.

## Features

- **Add/Delete Documents**: Store and manage documents with automatic preprocessing (stemming, stopword removal).
- **Phrase Search**: Efficient phrase and keyword search using an inverted index and TF-IDF ranking.
- **Autocomplete**: Fast prefix-based word suggestions using a Trie.
- **Boolean Search**: Support for AND, OR, NOT queries.
- **LRU Cache**: Caches recent search results for performance.
- **Document Similarity Graph**: Graph structure connects similar documents (Jaccard similarity > 0.3), supports BFS/DFS for recommendations and clustering.
- **REST API**: FastAPI endpoints for all major operations.

## Project Structure

```
main.py              # FastAPI app exposing the search engine
search_engine.py     # Core search engine logic
trie.py              # Trie data structure for autocomplete
stack.py             # Stack for boolean search and DFS
lru.py               # Doubly linked list for LRU cache
heap.py              # MaxHeap for ranking search results
my_queue.py          # Queue for BFS and boolean search
graph.py             # Document similarity graph
requirements.txt     # Python dependencies for the project
```

## API Endpoints

- `POST /add_document` — Add a document (name, content)
- `DELETE /delete_document/{document_name}` — Delete a document
- `GET /search?query=...` — Phrase search
- `GET /prefix?prefix=...` — Autocomplete suggestions
- `GET /documents` — List all document names
- `GET /boolean_search?query=...` — Boolean search
- `GET /content/{doc_name}` — Get document content
- `GET /similar_documents/{doc_name}` — Get similar documents (BFS)
- `GET /connected_components` — Get connected components (DFS)

## How It Works

- **Inverted Index**: Maps stemmed words to document positions for fast search and phrase matching.
- **Trie**: Stores all unique words for prefix-based autocomplete.
- **LRU Cache**: Stores recent search/boolean results for quick retrieval.
- **Graph**: Each document is a node; edges connect documents with Jaccard similarity > 0.3.
- **TF-IDF**: Used for ranking search results.

## Example Usage

```python
# Add a document
POST /add_document {"document_name": "doc1", "content": "Hello world!"}

# Search for a phrase
GET /search?query=hello world

# Autocomplete
GET /prefix?prefix=hel

# Boolean search
GET /boolean_search?query=hello AND world

# Get similar documents
GET /similar_documents/doc1
```

## Requirements

- Python 3.8+
- fastapi
- nltk
- uvicorn

All dependencies are listed in `requirements.txt`.

## Running the Project

1. Install dependencies:
   ```sh
   pip install fastapi uvicorn nltk
   ```
2. Start the server:
   ```sh
   uvicorn main:app --reload
   ```
3. Access the API at `http://localhost:8000`

## License

MIT
