from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure OpenAI 설정
llm = AzureChatOpenAI(
    api_key=os.getenv("API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system",
     """
        You are an advanced AI system providing meeting minutes transcription services. Your primary task is to create organized meeting minutes based on provided text. The meeting text is converted using STT (Speech-to-Text) technology, which may have inaccuracies. Thus, it is crucial to understand the context accurately and write the minutes flexibly.

        - Comprehend the context of the meeting text to produce coherent and clear documents.
        - Include key points, decisions made, assigned tasks, and items for future discussion.
        - Correct any recognition errors or grammatical issues as necessary, ensuring a natural flow of content.
        - Maintain the format and structure of the minutes while emphasizing key information.
        - Write the summary in the specified language.
    """.strip()
     ),
    ("human", "Meeting text: {input}\nLanguage for summary: {language}")
])

summarize_chain = prompt_template | llm | StrOutputParser()


class SummerizationRequest(BaseModel):
    text: str
    language: str = Field(default="korean")


@app.post("/summarize")
async def summarize_text(request: SummerizationRequest):
    response = summarize_chain.invoke(
        {"input": request.text, "language": request.language})
    return {"summary": response}
