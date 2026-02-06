from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

import os

from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

model=ChatGroq(model="llama-3.1-8b-instant",groq_api_key=groq_api_key)

# Create prompt template

system_template = "Transalate the following into {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", "{text}")
    ]
)

# create parser

parser = StrOutputParser()

# Create chain

chain = prompt_template|model|parser


# App definition

app=FastAPI(
    title="Langchain server",
    version="1.0",
    description="A simple API server creating by using langchain runnable interface"
)

## Addinf chain routes
add_routes(
    app,
    chain,
    path="/chain"
    
)

if __name__ == "__main__":
    import uvicorn
    print("Starting Langchain server (uvicorn) on 127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)