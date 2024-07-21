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

def ingest(file_extension):
    file_path = glob.glob('uploads/*.'+file_extension)
    indexing_pipeline.run({"converter": {"sources": [Path(i) for i in file_path]}})

    return document_store.count_documents()