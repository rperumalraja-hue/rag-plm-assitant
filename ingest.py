from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from config import DB_PATH, DOCS_PATH, EMBEDDING_MODEL

def ingest_documents():
    print(f"Loading documents from {DOCS_PATH}...")
    
    # Load PDFs and Text files
    pdf_loader = DirectoryLoader(DOCS_PATH, glob="./*.pdf", loader_cls=PyPDFLoader)
    txt_loader = DirectoryLoader(DOCS_PATH, glob="./*.txt", loader_cls=TextLoader)
    
    docs = []
    docs.extend(pdf_loader.load())
    docs.extend(txt_loader.load())
    
    if not docs:
        print("No documents found.")
        return

    # Split text into chunks (Change Management usually needs larger chunks to keep context)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    # Create Vector Database
    print("Creating Vector Database (this may take a while)...")
    embedding_function = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    # Persist to disk
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding_function,
        persist_directory=DB_PATH
    )
    print("Ingestion Complete. Database saved locally.")

if __name__ == "__main__":
    ingest_documents()