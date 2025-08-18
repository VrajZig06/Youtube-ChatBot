from fastapi import FastAPI
from schema.pydanticSchema import APIInput
from utils.fetchYouTubeTranscript import getYoutubeTranscript
from utils.textSplitters import split_text
from utils.vectorStore import vector_store,getContext
from langchain_chroma import Chroma
from models.huggingFace import embeddings,model
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import ContextualCompressionRetriever
from prompts.prompts import prompt,strParser
from langchain_core.messages import AIMessage,HumanMessage
import json

app = FastAPI()

chat_history = []

@app.get("/")
def hello():
    return {
        "msg" : chat_history
    }

@app.post("/predict")
async def getAIResponse(data:APIInput):
    try:
        query = data.model_dump()['query']
        url = data.model_dump()['url']

        transcript,videoId =  getYoutubeTranscript(url)

        chunk_list = split_text(transcript)

        vector_store = Chroma(
                embedding_function=embeddings,
                persist_directory="YT_Vector_DB",
                collection_name= f"Transcript-{videoId}"
            )
        
        vector_store.add_texts(chunk_list)

        # Creating Contextual Compressor Retriever 
        base_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        compressor = LLMChainExtractor.from_llm(llm=model)
        compression_retriever =  ContextualCompressionRetriever(
                base_retriever=base_retriever,
                base_compressor=compressor
            )
        relativeVectors = compression_retriever.invoke(query)
        all_relative_documents = [doc.page_content for doc in relativeVectors]
        context = "\n\n".join(all_relative_documents)

        chain = prompt | model | strParser

        response = chain.invoke({
            'query' : query,
            'context' : context,
            'chat_history' : chat_history
        })

        response = json.loads(response).get("result")
        print(response)

        chat_history.append(HumanMessage(content=query))
        chat_history.append(AIMessage(content=response))

        return {
            "url" : url,
            "query" : query,
            "result" : response,
            "chatHistory" : chat_history
        }
    except Exception as e:
        print(f"Error : {e}")
