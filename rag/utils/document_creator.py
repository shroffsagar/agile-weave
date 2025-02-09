from enum import Enum
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.docstore.document import Document
from typing import List

class TextSplitterType(Enum):
    """Enum for supported text splitter types."""
    RECURSIVE = "recursive"
    CHARACTER = "character"

class DocumentCreator:
    """
    Helper class for creating document objects by splitting text into required chunk size.
    In RAG the size of chunks helps in better performance, so while integrating this class
    one needs to play around on what chunk size fits best for their purpose of textual data.
    
    Args:
        chunk_size (int): The size of each text chunk. Defaults to 500.
        chunk_overlap (int): The overlap size between consecutive chunks. Defaults to 50.
        splitter_type (TextSplitterType): The type of text splitter to use. Defaults to RECURSIVE.
    """

    def __init__(self, 
                 chunk_size: int = 500, 
                 chunk_overlap: int = 50,
                 splitter_type: TextSplitterType = TextSplitterType.RECURSIVE):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter_type = splitter_type
        self.text_splitter = self._initialize_text_splitter()

    def _initialize_text_splitter(self):
        if self.splitter_type == TextSplitterType.RECURSIVE:
            return RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
        elif self.splitter_type == TextSplitterType.CHARACTER:
            return CharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
        else:
            raise ValueError("Unsupported text splitter type")

    def create_documents(self, full_text: str) -> List[Document]:
        """
        Split the input text into chunks and create Document objects.
        
        Args:
            full_text (str): The input text to be split into chunks.
            
        Returns:
            List[Document]: A list of Document objects, each containing a chunk of the input text.
        """
        chunks = self.text_splitter.split_text(full_text)
        return [Document(page_content=chunk) for chunk in chunks]
