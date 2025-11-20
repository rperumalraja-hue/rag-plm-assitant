# RAG PLM Assistant (DefenseBot)

A Retrieval-Augmented Generation (RAG) chatbot that allows you to chat with your own PDF documents. It uses OpenAI and ChromaDB to search through your files and answer questions based on their content.

## 🚀 Features
- **Ingest PDFs:** Automatically reads and indexes PDF files.
- **Vector Search:** Uses ChromaDB to find the most relevant text chunks.
- **AI Chat:** Uses OpenAI to generate accurate answers based *only* on your documents.

## 🛠️ Prerequisites
**Before you start, make sure you have:**
1.  **Python 3.10 or 3.11** installed.
2.  **OpenAI API Key** (active with credits).
3.  **Microsoft C++ Build Tools** (⚠️ Required for Windows users):
    * If `pip install` fails with a "Visual C++ 14.0" error, you must download [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
    * Install the **"Desktop development with C++"** workload.

## 📥 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/rperumalraja-hue/rag-plm-assitant.git](https://github.com/rperumalraja-hue/rag-plm-assitant.git)
    cd rag-plm-assitant
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

### 1. Setup API Keys
* Open the `config.py` file.
* Replace the placeholder text with your actual OpenAI API Key:
    ```python
    OPENAI_API_KEY = "sk-..."
    ```

### 2. Setup Data Folders
* Go to the `data_source` folder.
* **Important:** If the folders are missing, create them manually so the structure looks like this:
    ```
    data_source/
    ├── documents/          <-- Put your PDF files here
    └── structured_data/    <-- (Optional) Additional data
    ```
* Add your PDF files into `data_source/documents`.

## 🏃‍♂️ How to Run

**Step 1: Build the Database (Run this first!)**
You must run this script to process your PDFs and save them into the vector database.
```bash
python ingest.py

Step 2: Start the Chatbot Once the database is built, run this command to launch the application:
```bash
python app.py
