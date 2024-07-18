from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
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


class SummerizationRequest(BaseModel):
    text: str


@app.post("/summarize")
async def summarize_text(request: SummerizationRequest):
    response = llm([HumanMessage(content=f"다음 텍스트를 요약해주세요: {request.text}")])
    return {"summary": response.content}
