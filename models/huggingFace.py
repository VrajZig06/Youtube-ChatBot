from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace,HuggingFaceEmbeddings

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-Coder-480B-A35B-Instruct",
    task="text-generation",
    max_new_tokens=100)

# LLM Model
model = ChatHuggingFace(llm=llm)


# Embedding Model to Generate vectors 
embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
