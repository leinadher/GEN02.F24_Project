## Loading unstructured data from PDFs

import os
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader
import openai
openai.api_key = "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"

# for more readers, go to https://llamahub.ai/l/readers/llama-index-readers-file?from=readers

# Function for getting the vector store index using llama_index
# Load the pdf reader, pass the data, create an index and show the progress, then store the index in a folder
# All of this code is taken from the llama_index documentation
def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(StorageContext.from_defaults(persist_dir=index_name))
    return index

pdf_path = os.path.join("data", "Module Descriptions HS22.pdf")
module_descriptions_pdf = PDFReader().load_data(file=pdf_path)
module_descriptions_index = get_index(module_descriptions_pdf, "module_descriptions")

# Create a query engine from the index
module_descriptions_engine = module_descriptions_index.as_query_engine()