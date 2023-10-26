""" Backend for RAG Chatbot """
import os
from collections.abc import Generator
from queue import Empty, Queue
from threading import Thread
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import RetrievalQA
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceTextGenInference
from langchain.prompts import PromptTemplate
from langchain.vectorstores.redis import Redis
from pydantic import BaseModel
from uvicorn import run

# Load local env vars if present
load_dotenv()

# App creation
app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)

# Data classes
class DestinationEntry(BaseModel):
    """ Additional destination entry """
    kind: str = ""
    coordinates: tuple[float,float] = None
    uuid: str = ""

    class Config:
        """ Example """
        json_schema_extra = {
            "example": {
                "kind": "wheat",
                "coordinates": (10.0,22.1),
                "uuid": "c303282d-f2e6-46ca-a04a-35d3d873712d"
            }
        }

# Status API
@app.get("/health")
async def root():
    """ Basic status """
    return {"message": "Status:OK"}

# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    run(app, host="0.0.0.0", port=port)
