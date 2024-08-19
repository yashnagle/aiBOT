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

load_dotenv()

MODEL_KEY = os.getenv('MODEL_KEY')
MODEL = 'mistral'

embeddings = OllamaEmbeddings(model=MODEL)
parser = StrOutputParser()

template = """
    Answer the question based on the context below. If you cannot answer the question, reply "I don't know".

    Context: {context}

    Question: {question}
    """
prompt = PromptTemplate.from_template(template)

# vector_db = MilvusClient(
#     embedding_function = embeddings,
#     collection_name='aiBot_DB',
#     connection_args={"host":'127.0.0.1', "port":'19530'}
#     )


connections.connect("default", host="127.0.0.1", port="19530")
collection = Collection(name='aiBot_DB')
collection.load()

# embed_query = embeddings.embed_query(['what are the benefits of reading?'])
# print(type(embed_query))

# result = collection.query('What are the beneifts of reading?')
# print(result)


