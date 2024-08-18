import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.embeddings import OllamaEmbeddings
from operator import itemgetter
import pandas as pd
#Change vectorstore

load_dotenv()

MODEL_KEY = os.getenv('MODEL_KEY')
MODEL = 'mistral'

model = Ollama(model=MODEL)
embeddings = OllamaEmbeddings(model=MODEL)

parser = StrOutputParser()


loader = PyPDFLoader('uploads/test_doc1.pdf')
pages = loader.load_and_split()
# print(type(pages[0]))


template = """
Answer the question based on the context below. If you cannot answer the question, reply "I don't know".

Context: {context}

Question: {question}
"""

prompt = PromptTemplate.from_template(template)
# print(prompt.format(context='Here is some context', question='Here is the question'))


# print(chain.input_schema.schema()) #To check schema
# print(chain.invoke(
#     {
#         "context": "the name I was given is India",
#         "question": "Whats my name?"
#     }
# ))

vectorstore = DocArrayInMemorySearch.from_documents(
    pages, 
    embedding=embeddings
)

retriever = vectorstore.as_retriever()

chain = (

    { "context": itemgetter("question") | retriever, "question": itemgetter("question") } 
    | prompt
    | model
    | parser 
)


questions = [
    'What are the cognitive benefits of reading?',
    'How does reading help with creativity?'
]

q = []
a = []

for question in questions:
    print(f"Question: {question}")
    q.append(question)
    a.append(chain.invoke({'question':question}))

pd.DataFrame(zip(q, a), columns=['Questions', 'Answers']).to_csv('uploads/test_rag.csv')
print('Done!')



