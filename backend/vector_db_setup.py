import sys
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, MilvusClient

client = MilvusClient(uri="http://localhost:19530")

connections.connect(host="localhost",port="19530")

# primary id key
item_id = FieldSchema(
    name="id",
    dtype=DataType.INT64,
    is_primary=True
)

# text field to hold text content of embeddings
text = FieldSchema(
    name="text",
    dtype=DataType.VARCHAR,
    max_length=50000
)
# vector field to hold embeddings
embeddings = FieldSchema(
    name="embeddings",
    dtype=DataType.FLOAT_VECTOR,
    dim=4096 # for the "Ollama Embedding model" embedding model
)

# source of the embedding (id)
source = FieldSchema(
    name="source",
    dtype=DataType.VARCHAR,
    max_length=20
)

# a URL pointing to the source of the data, if any
url = FieldSchema(
    name="url",
    dtype=DataType.VARCHAR,
    max_length=250
)

# a title, if any, of the wordpress article, for example
title = FieldSchema(
    name="source_title",
    dtype=DataType.VARCHAR,
    max_length=250
)

# define collection schema 
schema = CollectionSchema(
    fields=[item_id, text, embeddings, source, url, title],
    description="aiBot_DB",
    enable_dynamic_field=False,
    auto_id=True
)

# define the collection
collection = Collection(
    name="aiBot_DB",
    schema=schema,
    using='default'
)
# create an index to speed up queries
collection.create_index(
    field_name="embeddings",
    index_params={"metric_type":"IP","index_type":"IVF_FLAT","params":{"nlist":4096}}
)