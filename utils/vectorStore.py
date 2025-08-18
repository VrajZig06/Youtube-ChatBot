from langchain_chroma import Chroma
from models.huggingFace import embeddings,model
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import ContextualCompressionRetriever


vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory="YT_Vector_DB",
            collection_name= f"Transcript"
        )

# Creating Contextual Compressor Retriever 
base_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
compressor = LLMChainExtractor.from_llm(llm=model)
compression_retriever = ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=compressor
    )

from utils.vectorStore import compression_retriever

def getContext(query):

    """
    return Context by making semantic search on Vector Store
    """
    relativeVectors = compression_retriever.invoke(query)
    all_relative_documents = [doc.page_content for doc in relativeVectors]
    context = "\n\n".join(all_relative_documents)

    return context
