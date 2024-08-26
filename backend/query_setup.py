import os
import sys
import json
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
from langchain_community.vectorstores import milvus
from langchain_milvus.retrievers import MilvusCollectionHybridSearchRetriever
from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    WeightedRanker,
    connections,
)

load_dotenv()

MODEL_KEY = os.getenv('MODEL_KEY')
MODEL = 'mistral'

embeddings = OllamaEmbeddings(model=MODEL)
parser = StrOutputParser()

milvus = milvus.Milvus(
    embedding_function = embeddings,
    collection_name = 'aiBot_DB',
    primary_field = 'id',
    auto_id=True,
    vector_field = 'embeddings',
    text_field='text',
    connection_args={
        'address':'localhost:19530'
    }

)
print(milvus)

MODEL = 'mistral'

model = Ollama(model=MODEL)


# template = """
#     Answer the question based on the context below. If you cannot answer the question, reply "I don't know".

#     Context: {context}

#     Question: {question}
#     """
# prompt = PromptTemplate.from_template(template)

# vector_db = MilvusClient(
#     embedding_function = embeddings,
#     collection_name='aiBot_DB',
#     connection_args={"host":'127.0.0.1', "port":'19530'}
#     )

connections.connect("default", host="127.0.0.1", port="19530")
collection_db = Collection(name='aiBot_DB')
collection_db.load()
client = MilvusClient(uri='http://localhost:19530')


param = {
    # use `IP` as the metric to calculate the distance
    "metric_type": "IP",
    "params": {
        # search for vectors with a distance greater than 0.8
        "radius": 0.8,
        # filter out most similar vectors with a distance greater than or equal to 1.0
        "range_filter" : 1.0
    }
}

# def query(question):
#     res = collection_db.search(
#         data= [embeddings.embed_query(question)],
#         anns_field='embeddings',
#         param=param,
#         limit=5
#     )

#     result = []
#     for i in res:
#         for j in i:
#             val = client.get(collection_name='aiBot_DB',
#             ids = [j.id])
#             result.append(val)

#     return result



# print(query('What are the benefits of reading?'))

retriever = milvus.as_retriever()

print(retriever)

template = """
Answer the question based on the context below. If you cannot answer the question, reply "I don't know".

Context: {context}

Question: {question}
"""

prompt = PromptTemplate.from_template(template)

chain = (

    { "context": itemgetter("question") | retriever, "question": itemgetter("question") } 
    | prompt
    | model
    | parser 
)

print(chain.invoke({'question':'Write a 500 word essay on the benefits of reading?'}))

# result = json.dumps(res, indent=4)
# print(result)

# #Hybrid search
# retriever = MilvusCollectionHybridSearchRetriever(
#     collection=collection_db,
#     rerank=WeightedRanker(0.5, 0.5),
#     anns_fields=['embeddings', 'embeddings'],
#     field_embeddings=[embeddings, embeddings],
#     field_search_params=[{"metric_type": "IP"}, {"metric_type": "IP"}],
#     top_k=3,
#     text_field='text',
# )
# print(retriever.invoke("What are the benefits of reading?"))




# query = 'What are the benefits of reading?'
# query_vector = embeddings.embed_query(query)

# result = search_and_query(collection, [query_vector], 'embeddings', {"metric_type": "IP", "params": {"nlist": 4096}})

# print(result)


# embed_query = embeddings.embed_query(['what are the benefits of reading?'])
# print(type(embed_query))

# result = collection.query('What are the beneifts of reading?')
# print(result)


