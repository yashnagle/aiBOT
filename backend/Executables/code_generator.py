import os
import sys
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

MODEL = 'codestral'

model = Ollama(model=MODEL)


template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

chain = prompt | model

chain.invoke({'question':'Write code to read a csv file and return all the column names'})