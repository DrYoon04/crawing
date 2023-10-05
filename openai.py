import os
import platform
import openai
import chromadb
import langchain
import tiktoken

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import DirectoryLoader

# OpenAI API 키를 설정합니다.
os.environ["OPENAI_API_KEY"] = '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'

# OpenAI 모델을 생성합니다.
model = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

# 텍스트 토큰화 클래스를 생성합니다.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

# 벡터 데이터베이스 클래스를 생성합니다.
vector_store = Chroma()

# 벡터 데이터베이스에 텍스트 데이터를 로드합니다.
document_loader = DirectoryLoader("/Users/dryoon/Documents/GitHub/schoolproject/vector store(3주차)/lyrics")
docs = document_loader.load()
docs = text_splitter.split_documents(docs)
vector_store.from_documents(docs, embedding=OpenAIEmbeddings(), persist_directory="music_index_hf")
vector_store.persist()

# 대화 검색 체인을 생성합니다.
chain = ConversationalRetrievalChain.from_llm(model, vector_store, return_source_documents=True)

# 대화 검색 체인에 질문을 입력합니다.
query = "경서예지"

# 대화 검색 체인에서 검색 결과를 가져옵니다.
results = chain.generate(query)

# 검색 결과를 출력합니다.
for result in results:
    print(result.text)
    print(result.source_document)
