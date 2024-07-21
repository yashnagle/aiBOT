import os
import glob

#Indexing pipeline
from haystack import Pipeline
from haystack.components.converters import PyPDFToDocument
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter
from milvus_haystack import MilvusDocumentStore
from milvus_haystack.milvus_embedding_retriever import MilvusEmbeddingRetriever
from pathlib import Path

#connecting to the database
document_store = MilvusDocumentStore(
    connection_args={
        "host": "localhost",
        "port": "19530",
        "user": "root",
        "password": "Milvus",
        "secure": False,
    },
    drop_old=True,
)

indexing_pipeline = Pipeline()

indexing_pipeline.add_component("converter", PyPDFToDocument())
indexing_pipeline.add_component("splitter", DocumentSplitter(split_by="sentence", split_length=2))
indexing_pipeline.add_component("embedder", SentenceTransformersDocumentEmbedder())
indexing_pipeline.add_component("writer", DocumentWriter(document_store))
indexing_pipeline.connect("converter", "splitter")
indexing_pipeline.connect("splitter", "embedder")
indexing_pipeline.connect("embedder", "writer")

file_path = glob.glob('uploads/*.pdf')
# indexing_pipeline.run({"converter": {"sources": [Path(i) for i in file_path]}})
indexing_pipeline.run({"converter": {"sources": [Path('uploads/test_doc1.pdf')]}})

question = 'Motivations?'
retrieval_pipeline = Pipeline()
retrieval_pipeline.add_component("embedder", SentenceTransformersTextEmbedder())
retrieval_pipeline.add_component("retriever", MilvusEmbeddingRetriever(document_store=document_store, top_k=3))
retrieval_pipeline.connect("embedder", "retriever")


retrieval_results = retrieval_pipeline.run({"embedder": {"text": question}})
print(retrieval_results)
# for doc in retrieval_results["retriever"]["documents"]:
#     print(doc.content)
#     print("-" * 10)


# def ingest(file_extension):
#     file_path = glob.glob('uploads/*.'+file_extension)
#     indexing_pipeline.run({"converter": {"sources": [Path(i) for i in file_path]}})

#     return document_store.count_documents()