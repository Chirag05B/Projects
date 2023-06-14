# -*- coding: utf-8 -*-
"""LangChain_PDF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16Y0S_DZhtJt1clqXXOmJFZn5OEwuKllP

# Talk to a pdf using LangChain and ChatGPT
## Steps
1. Loading the document
2. Creating embeddings and Vectorization
3. Querying the PDF

1. Loading the document
"""

# Download a paper using the curl command line tool directly from jupyter notebook
!curl -o paper.pdf https://arxiv.org/pdf/2303.13519.pdf

# Install the necessary dependencies of the project and import the modules we'll use for the project
!pip install openai
!pip install langchain
!pip install pypdf
!pip install chromadb
!pip install tiktoken
from langchain.document_loaders import PyPDFLoader # For loading the pdf
from langchain.embeddings import OpenAIEmbeddings # for creating embeddings
from langchain.vectorstores import Chroma # for vectorization part
from langchain.chains import ChatVectorDBChain # for chatting with the pdf
from langchain.llms import OpenAI # the LLM model we'll use (ChatGPT)

OPENAI_API_KEY = "" ## YOUR OPENAI API KEY ##

"""## Load our pdf"""

# The code uses the PyPDFLoader class from the langchain.document_loaders module
# to load and split the PDF document into seperate pages or sections
pdf_path = "./paper.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()
print(pages[0].page_content)

"""2. Creating embeddings and Vectorization"""

# The code creates embeddings using the OpenAIEbeddings class from the langchain.embeddings.openai
# These embeddings are then passed to the Chroma class from the langchain.vectorstores module, which
# generates a vector database for the given PDF document.
embeddings = OpenAIEmbeddings(openai_api_key=[OPENAI_API_KEY])
vectordb = Chroma.from_documents(pages, embedding=embeddings, persist_directory = ".")
vectordb.persist()

"""3. Querying"""

# The code sets up the ChatVectorDBChain class from langchain.chains to interact with ChatGPT using the previous generated vector database.
# The query, provided as a command line argument is passed to the ChatVectorDBChain instance,
# which returns an answer generated by ChatGPT

pdf_qa = ChatVectorDBChain.from_llm(OpenAI(temperature=0.9, model_name='gpt-3.5-turbo',openai_api_key=[OPENAI_API_KEY]), vectordb, return_source_documents=True)

query = 'What is the VideoTaskformer?'
result = pdf_qa({'question': query, 'chat_history':''})
print('Answer:')
print(result['answer'])

"""## Answer:
VideoTaskformer is a pre-trained video model that focuses on representing the semantics and structure of instructional videos. It uses a simple and effective objective of predicting weakly supervised textual labels for steps that are randomly masked out from an instructional video (masked step modeling) to learn task-aware step representations from a large corpus of instructional videos. It can verify if an unseen video correctly executes a given task, as well as forecast which steps are likely to be taken after a given step. VideoTaskformer outperforms previous baselines on various benchmarks and achieves new state-of-the-art performance.

# Summary and Final Thoughts
The ability to ask questions and receive concise, relevant answers from a PDF document, can enable efficient engagement with the material, improving retention, understanding, and overall the entire learning experience.

This example is just a glimpse of the immense possibilities that AI tools powered by LLMs can bring to the table.
"""

