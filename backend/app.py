""" Backend for RAG Chatbot """
import logging
import os
from collections.abc import Generator
from queue import Empty, Queue
from threading import Thread
from typing import Optional

import redis_utils
from app_config import LOG_LEVELS, LOGGING_CONFIG
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import RetrievalQA
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceTextGenInference
from langchain.prompts import PromptTemplate
from langchain.vectorstores.redis import Redis
from uvicorn import run
from dotenv import dotenv_values
import data_classes

# Load local env vars if present
load_dotenv()

# Initialize logger
logger = logging.getLogger("app")

# Get config
config = {
    **dotenv_values(".env"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}
logger.info(f'Config: INFERENCE_SERVER_URL={config["INFERENCE_SERVER_URL"]}')

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

# Status API
@app.get("/health")
async def health():
    """ Basic status """
    return {"message": "Status:OK"}

@app.get("/ping_redis")
async def ping_redis():
    """
    Checks Redis connection. Returns 'true' if the connection is OK, 'false' otherwise
    """
    return redis_utils.ping_redis(config)

# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    run(app, host="0.0.0.0", port=port)
