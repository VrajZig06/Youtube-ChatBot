from langchain_core.prompts import PromptTemplate
from schema.pydanticSchema import APIResponse
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser


pydanticParser = PydanticOutputParser(pydantic_object=APIResponse)
strParser = StrOutputParser()

prompt = PromptTemplate(
    template="""
        You are a helpful and intelligent Assistant.
        Answer the user's query based strictly on the provided context.
        For you I Provide Chat History also if you need then use That ChatHistory also.

        User Query:
        {query}

        Context:
        {context}

        Chat History:
        {chat_history}

        Instructions:
        - Base your response only on the context.
        - If the answer is not present in the context, politely state that.
        - Keep your response clear and informative.\n{format_instruction}
        """,
        input_variables=['query','context','chat_history'],
        partial_variables={"format_instruction" : pydanticParser.get_format_instructions()}
    )