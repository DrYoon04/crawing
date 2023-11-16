import openai
import os
import langchain
from langchain.document_loaders import UnstructuredExcelLoader

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key_path = 'discord_chatbot/gptkey.txt'

