import os
import glob
from haystack.utils import Secret
from jinja2 import Template
from milvus_haystack import MilvusDocumentStore
from milvus_haystack.milvus_embedding_retriever import MilvusEmbeddingRetriever
from pathlib import Path

from haystack.components.writers import DocumentWriter
from haystack.components.converters import MarkdownToDocument, PyPDFToDocument, TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder

from haystack import Pipeline
from haystack.utils import Secret
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.embedders import HuggingFaceAPIDocumentEmbedder
from haystack.components.builders import PromptBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
from huggingface_hub import InferenceClient
from milvus_haystack import MilvusDocumentStore
from milvus_haystack.milvus_embedding_retriever import MilvusEmbeddingRetriever
from haystack.components.retrievers import SentenceWindowRetrieval

from haystack import Pipeline
#Imports a PyMilvus package:
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

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

generator = HuggingFaceAPIGenerator(api_type='serverless_inference_api',
                                    api_params={'model':'mistralai/Mistral-Nemo-Instruct-2407'},
                                    token=Secret.from_token(os.getenv('MODEL_KEY')))

sentence_transformer = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2",token=Secret.from_token(os.getenv('MODEL_KEY')))

model = InferenceClient("mistralai/Mistral-Nemo-Instruct-2407", token=Secret.from_token(os.getenv('MODEL_KEY')))

documents = []
conversation_history = []
prompt_template = """Answer the following query based on the context. If the context do
                        not include an answer, reply with 'I don't know'.\n
                        Previous Conversation:\n
                        {% for turn in conversation_history %}
                            {{ turn }}
                        {% endfor %}
                        Current Query: {{query}}
                        Documents:
                        {% for doc in documents %}
                            {{ doc.content }}
                        {% endfor %}
                        Answer: 
                    """
template = Template(prompt_template)

def get_ingesting_pipeline():
    connections.connect("default", host="localhost", port="19530")


    #File routers and converters
    file_type_router = FileTypeRouter(mime_types=["text/plain", "application/pdf", "text/markdown"])
    text_file_converter = TextFileToDocument()
    markdown_converter = MarkdownToDocument()
    pdf_converter = PyPDFToDocument()
    document_joiner = DocumentJoiner()

    document_cleaner = DocumentCleaner()
    # document_splitter = DocumentSplitter(split_by="word", split_length=150, split_overlap=50)
    document_splitter = DocumentSplitter(split_by='sentence', split_threshold = 10)
    # document_splitter = DocumentSplitter()


    document_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2",token=Secret.from_token(os.getenv('MODEL_KEY')))
    document_writer = DocumentWriter(document_store)

    preprocessing_pipeline = Pipeline()
    preprocessing_pipeline.add_component(instance=file_type_router, name="file_type_router")
    preprocessing_pipeline.add_component(instance=text_file_converter, name="text_file_converter")
    preprocessing_pipeline.add_component(instance=markdown_converter, name="markdown_converter")
    preprocessing_pipeline.add_component(instance=pdf_converter, name="pypdf_converter")
    preprocessing_pipeline.add_component(instance=document_joiner, name="document_joiner")
    preprocessing_pipeline.add_component(instance=document_cleaner, name="document_cleaner")
    preprocessing_pipeline.add_component(instance=document_splitter, name="document_splitter")
    preprocessing_pipeline.add_component(instance=document_embedder, name="document_embedder")
    preprocessing_pipeline.add_component(instance=document_writer, name="document_writer")

    preprocessing_pipeline.connect("file_type_router.text/plain", "text_file_converter.sources")
    preprocessing_pipeline.connect("file_type_router.application/pdf", "pypdf_converter.sources")
    preprocessing_pipeline.connect("file_type_router.text/markdown", "markdown_converter.sources")
    preprocessing_pipeline.connect("text_file_converter", "document_joiner")
    preprocessing_pipeline.connect("pypdf_converter", "document_joiner")
    preprocessing_pipeline.connect("markdown_converter", "document_joiner")
    preprocessing_pipeline.connect("document_joiner", "document_cleaner")
    preprocessing_pipeline.connect("document_cleaner", "document_splitter")
    preprocessing_pipeline.connect("document_splitter", "document_embedder")
    preprocessing_pipeline.connect("document_embedder", "document_writer")

    file_dir = 'uploads'
    return preprocessing_pipeline

def get_query_pipeline():
    sentence_window_retriever = SentenceWindowRetrieval(document_store, window_size=3)

    # conversation_history.append('User:What is unforgettable energy?')
    rag_pipeline = Pipeline()
    # rag_pipeline.add_component("text_embedder", sentence_transformer)
    rag_pipeline.add_component("text_embedder", SentenceTransformersTextEmbedder(model))
    rag_pipeline.add_component("retriever", MilvusEmbeddingRetriever(document_store=document_store, top_k=3))
    rag_pipeline.add_component("prompt_builder", PromptBuilder(template=prompt_template))
    rag_pipeline.add_component("generator", generator)

    rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
    rag_pipeline.connect("retriever.documents", "prompt_builder.documents")
    rag_pipeline.connect("prompt_builder", "generator")

    return rag_pipeline