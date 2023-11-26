import os

import openai
from llama_index import StorageContext, load_index_from_storage

file_path = '/Users/dryoon04/Documents/GitHub/university-project/discord_chatbot/api key.txt'
# 파일 열기 (읽기 모드로 열기)
with open(file_path, 'r', encoding='utf-8') as file:
    # 파일 내용 읽어오기
    file_content = file.read()
os.environ["OPENAI_API_KEY"] = file_content
openai.api_key = os.getenv("OPENAI_API_KEY")

# loader = SimpleDirectoryReader('../data', recursive=True, exclude_hidden=True)
# documents = loader.load_data()
# llm = OpenAI(model="gpt-3.5-turbo", temperature=0)
#
# service_context = ServiceContext.from_defaults(llm=llm)
# vector_index = VectorStoreIndex.from_documents(documents, service_context=service_context)
# print("공지사항 인덱싱 완료")
#
# vector_index.storage_context.persist("notice_index")
storage_context = StorageContext.from_defaults(persist_dir="./notice_index")
new_index = load_index_from_storage(storage_context)
new_query_engine = new_index.as_query_engine()
def shool_notice(quary):
    response = new_query_engine.query(quary,"제목과 링크로 알려줄것")
    return response