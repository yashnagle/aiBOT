import os
from dotenv import load_dotenv, dotenv_values
from jinja2 import Template
load_dotenv()
from pymilvus import (
        connections,
        utility,
        FieldSchema,
        CollectionSchema,
        DataType,
        Collection,
    )


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

generator = HuggingFaceAPIGenerator(api_type='serverless_inference_api',
                                    api_params={'model':'mistralai/Mistral-Nemo-Instruct-2407'},
                                    token=Secret.from_token(os.getenv('MODEL_KEY')))

sentence_transformer = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2",token=Secret.from_token(os.getenv('MODEL_KEY')))

model = InferenceClient("mistralai/Mistral-Nemo-Instruct-2407", token=Secret.from_token(os.getenv('MODEL_KEY')))
documents = []

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
conversation_history = []

template = Template(prompt_template)

def update_conversation(conv):
    #conv 
    conversation_history.append(conv)
    return conversation_history

def get_query_pipeline():
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
    connections.connect("default", host="localhost", port="19530")

    print('DOC LENGTH:', document_store.count_documents())

    sentence_window_retriever = SentenceWindowRetrieval(document_store, window_size=3)

    conversation_history.append('User:What are the motivations of studying abroad?')
    rag_pipeline = Pipeline()
    rag_pipeline.add_component("text_embedder", sentence_transformer)
    # rag_pipeline.add_component("text_embedder", SentenceTransformersTextEmbedder(model))
    rag_pipeline.add_component("retriever", MilvusEmbeddingRetriever(document_store=document_store))
    rag_pipeline.add_component("sentence_window_retriever", sentence_window_retriever)
    rag_pipeline.add_component("prompt_builder", PromptBuilder(template=prompt_template))
    rag_pipeline.add_component("generator", generator)

    rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
    # rag_pipeline.connect("retriever", "prompt_builder.documents")
    rag_pipeline.connect("retriever", "sentence_window_retriever")
    rag_pipeline.connect("sentence_window_retriever", "prompt_builder.documents")
    rag_pipeline.connect("prompt_builder", "generator")

    return rag_pipeline

    # results = rag_pipeline.run(
    #     {
    #         "text_embedder": {"text": question},
    #         "prompt_builder": {"query": question},
    #     }
    # )

    # print('RAG answer:', results["generator"]["replies"][0])
    # print('RAG answer:', results['generator']['replies'][0])
    # conversation_history.append('Bot:'+ results['generator']['replies'][0])
    # print(conversation_history)