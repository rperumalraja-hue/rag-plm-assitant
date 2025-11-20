# RAG PLM Assistant (DefenseBot)
A Retrieval-Augmented Generation (RAG) chatbot that allows you to chat with your own PDF documents. It uses ChromaDB to search through your files and answer questions based on their content.

## 🚀 Features
- **Ingest PDFs:** Automatically reads and indexes PDF files.
- **Vector Search:** Uses ChromaDB to find the most relevant text chunks.
- **AI Chat:** Generates answers based on your documents.

## 🛠️ Prerequisites
**Before you start, make sure you have:**
1.  **Python 3.10 or 3.11** installed.
2.  **Microsoft C++ Build Tools** (⚠️ Required for Windows users):
    * If `pip install` fails with a "Visual C++ 14.0" error, download [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
    * Install the **"Desktop development with C++"** workload.

## 📥 Installation
1.  **Install Project:**
Download ZIP (No Git required)
1.  Click the green **<> Code** button at the top of this page.
2.  Select **Download ZIP**.
3.  Extract (Unzip) the folder to your computer.
4.  Open your terminal (Command Prompt) and navigate into the extracted folder:
    ```bash
    cd rag-plm-assitant-main
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

### 1. Setup Data Folders
* Go to the `data_source` folder.
* **Important:** If the folders are missing, create them manually so the structure looks like this:
    ```
    data_source/
    ├── documents/          <-- Put your PDF files here
    └── structured_data/    <-- (Optional) Additional data
    ```
* Add your PDF files into `data_source/documents`.


## How to Ingest
You must run this script to process your PDFs and save them into the vector database.
```bash
python ingest.py
```

## How to Run
Start the Chatbot Once the database is built, run this command to launch the application:
```bash
python app.py
```

