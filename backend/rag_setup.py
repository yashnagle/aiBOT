import os
import sys
import constants
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.embeddings import OllamaEmbeddings
from operator import itemgetter
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, MilvusClient
import pandas as pd
import pymupdf

# import langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
client = MilvusClient(uri="http://localhost:19530")

import PyPDF2

doc = pymupdf.open("uploads/test_doc1.pdf")
doc_meta = doc.metadata
pdf_txt = ""
for pages in doc:
    pdf_txt += pages.get_text()

# print(pdf_txt)



load_dotenv()

MODEL_KEY = os.getenv('MODEL_KEY')
MODEL = 'mistral'

# model = Ollama(model=MODEL)
embeddings = OllamaEmbeddings(model=MODEL)
parser = StrOutputParser()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=True,
    separators=['\n+']
)

docs = text_splitter.create_documents([pdf_txt], [doc_meta])
connections.connect(host="localhost",port="19530")

for doc in docs:
    meta = doc.metadata
    text = doc.page_content

    vector = embeddings.embed_query(text)
    res = client.insert(
        collection_name='aiBot_DB',
        data = [{
            "text":text,
            "embeddings":vector,
            "source":"uploads",
            "url": meta['author'],
            "source_title": meta['title']
        }]
    )
    print(res)



# template = """
# Answer the question based on the context below. If you cannot answer the question, reply "I don't know".

# Context: {context}

# Question: {question}
# """

# prompt = PromptTemplate.from_template(template)
# # print(prompt.format(context='Here is some context', question='Here is the question'))


# vectorstore = mil.from_documents(
#     pages, 
#     embedding=embeddings
# )

# retriever = vectorstore.as_retriever()

# chain = (

#     { "context": itemgetter("question") | retriever, "question": itemgetter("question") } 
#     | prompt
#     | model
#     | parser 
# )


# questions = [
#     'What are the cognitive benefits of reading?',
#     'How does reading help with creativity?'
# ]

# q = []
# a = []

# for question in questions:
#     print(f"Question: {question}")
#     q.append(question)
#     a.append(chain.invoke({'question':question}))

# pd.DataFrame(zip(q, a), columns=['Questions', 'Answers']).to_csv('uploads/test_rag.csv')
# print('Done!')



