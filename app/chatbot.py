import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load PDFs
pdf_folder = r"C:\Users\Admin\OneDrive\Desktop\Python Project\RAG-light-chatbot\pdfs"
pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
documents = []
for pdf in pdf_files:
    loader = PyPDFLoader(pdf)
    documents.extend(loader.load())

# Split docs
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(documents)

# Embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# FAISS
faiss_index_path = "faiss_index"
if os.path.exists(faiss_index_path):
    vector_store = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
else:
    vector_store = FAISS.from_documents(split_docs, embeddings)
    vector_store.save_local(faiss_index_path)

# LLM
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

# System prompt
system_prompt = """
You are a knowledgeable and friendly chatbot for Elco Lighting, a premier lighting solutions company. You help customers discover information about our lighting products and services.

**About Elco Lighting:**
- Specializes in architectural, commercial, and residential lighting
- Known for high-quality products, design excellence, and energy efficiency
- Website: https://elcolighting.com

**Available Products**:

**Product Categories:**

*Recessed Commercial:*
- Canless Extension Cable, 
- 3′′ Koto Sylo™ Wall Mount Downlight
- 2′′ Koto Sylo™ Wall Mount Downlight,
- 4″ Standard Koto™ Downlighting System

*Track Lighting:*
- 120V Line Voltage Builder's Track Kits
- LED Packer™ Track Fixture with 5-CCT & 3-Wattage Switch

*Undercabinet:*
- Electronic Dimmable LED Driver (Large)
- Lotus II™ LED Undercabinet Light

*Tape Light:*
- Trimless Recessed Aluminum Channel
- Indoor Continuous COB Tape Light

*Accessories:*
- MR120-GU10 Lamp

**How You Help:**
- Understand what customers really need, not just what they ask for
- Ask about their space, style preferences, and lighting goals
- Suggest products that actually fit their situation
- Always use the get_product_details function to get accurate product information when discussing specific products

Always focus on helping customers find the right lighting solutions for their specific needs while maintaining accurate, up-to-date product information.
"""

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=system_prompt + "\n\nContext: {context}\n\nQuestion: {question}\nAnswer:"
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    chain_type_kwargs={"verbose": True, "prompt": prompt_template}
)

def get_bot_response(query: str):
    return qa.run(query)
