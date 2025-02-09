from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

class RAGContext:
    """Encapsulates retrieval-augmented generation logic."""
    
    def __init__(self, OPENAI_API_KEY, documents):
        """Initializes Vector DB"""
        self.embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        self.vector_store = FAISS.from_documents(documents, self.embeddings)

    def retrieve_context(self, query: str, k: int = 3) -> str:
        """
        Retrieves the context from initialized vector db for given query
        Returns the combines context string.
        """
        results = self.vector_store.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in results])
        return context