import streamlit as st
import pandas as pd
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# --- IMPORTS ---
from langchain_core.prompts import ChatPromptTemplate
try:
    from langchain.chains import create_retrieval_chain, create_stuff_documents_chain
except Exception:
    from langchain_classic.chains.retrieval import create_retrieval_chain
    from langchain_classic.chains.combine_documents.stuff import create_stuff_documents_chain

from config import DB_PATH, MODEL_NAME, EMBEDDING_MODEL

# --- PAGE CONFIG ---
st.set_page_config(page_title="Defense Design Assistant", layout="wide")
st.title("PLM Assistant")

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []
if "trigger_query" not in st.session_state:
    st.session_state.trigger_query = None

# --- INITIALIZE LLM ---
llm = ChatOllama(model=MODEL_NAME, temperature=0.3)

# --- MODE MAPPING ---
MODE_MAP = {
    "Design Q&A": "Design Q&A (Unstructured)",
    "Manager Report": "Manager Reports (Structured)",
    "Admin": "Admin: Database Viewer"
}

# ==========================================
# 1. SIDEBAR: FIXED CONTROLS (Top)
# ==========================================
st.sidebar.header("Controls")

# A. Mode Selection
mode = st.sidebar.radio(
    "Select Mode", 
    ["Design Q&A (Unstructured)", "Manager Reports (Structured)", "Admin: Database Viewer"],
    key="app_mode"
)

# B. Context-Specific Controls
use_general_knowledge = False 

if mode == "Design Q&A (Unstructured)":
    st.sidebar.markdown("---")
    use_general_knowledge = st.sidebar.toggle("Enable General AI Knowledge", value=False)
    
    if use_general_knowledge:
        st.sidebar.success("Mode: Hybrid (Docs + Internet Knowledge)")
    else:
        st.sidebar.warning("Mode: Strict (Documents Only)")

# ==========================================
# 2. SIDEBAR: SEARCH HISTORY (Scrollable)
# ==========================================
st.sidebar.markdown("---")
st.sidebar.subheader("🕒 Search History") # <--- RENAMED

# Clear Button
if st.sidebar.button("Clear History", use_container_width=True):
    st.session_state.history = []
    st.rerun()

# --- SCROLLABLE CONTAINER ---
# height=300px is roughly enough to show 5 collapsed entries.
# If the list is longer, a scrollbar will automatically appear inside this box.
with st.sidebar.container(height=300, border=False):
    
    history_items = list(enumerate(st.session_state.history))
    
    if not history_items:
        st.caption("No search history yet.")
    
    # Loop (Newest First)
    for i, item in reversed(history_items):
        short_q = item['question'][:30] + "..." if len(item['question']) > 30 else item['question']
        
        with st.expander(f"Q: {short_q}"):
            st.caption(f"Mode: {item['mode']}")
            st.write(item['answer'][:80] + "...")
            
            if st.button("🔄 Re-Run", key=f"btn_rerun_{i}"):
                st.session_state.trigger_query = item['question']
                
                saved_mode = item['mode']
                target_mode = MODE_MAP.get(saved_mode, mode)
                if target_mode != st.session_state.app_mode:
                    st.session_state.app_mode = target_mode
                st.rerun()

# ==========================================
# 3. MAIN APPLICATION LOGIC
# ==========================================

# --- MODE 1: RAG (Design Docs) ---
if mode == "Design Q&A (Unstructured)":
    st.subheader("Query Design Standards & Requirements")
    
    # Load Vector DB
    embedding_function = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    
    # Define Prompts
    strict_template = """
    Answer the user's question based STRICTLY on the context provided below.
    If the answer is not in the context, say "I cannot find this in the provided documents."
    Do not use outside knowledge.
    <context>{context}</context>
    Question: {input}
    """

    hybrid_template = """
    You are an intelligent Defense Engineering Assistant.
    Instructions:
    1. First, look for the answer in the <context> provided below.
    2. If the answer is in the context, cite the specific document.
    3. If the answer is NOT in the context, use your own internal knowledge to answer, 
       but clearly state: "Note: This information is based on general engineering principles, not the uploaded documents."
    <context>{context}</context>
    Question: {input}
    """

    selected_template = hybrid_template if use_general_knowledge else strict_template
    prompt = ChatPromptTemplate.from_template(selected_template)

    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    # Input Logic
    chat_input = st.chat_input("Ask about assembly details or standards...")
    
    query = None
    if st.session_state.trigger_query:
        query = st.session_state.trigger_query
        st.session_state.trigger_query = None
        st.info(f"🔄 Re-running: **{query}**")
    elif chat_input:
        query = chat_input

    if query:
        with st.spinner("Searching secure archives..."):
            response = retrieval_chain.invoke({"input": query})
            answer_text = response['answer']
            
            st.session_state.history.append({
                "mode": "Design Q&A",
                "question": query,
                "answer": answer_text
            })
            
            st.write(answer_text)
            
            with st.expander("Source Documents"):
                if "context" in response and response['context']:
                    for doc in response['context']:
                        st.info(f"Source: {doc.metadata.get('source', 'Unknown')}")
                else:
                    st.write("No local documents used for this answer.")

# --- MODE 2: Data Analysis ---
elif mode == "Manager Reports (Structured)":
    st.subheader("Generate PLM Reports")
    st.info("Data Source: Local Exports from Teamcenter (Excel/CSV)")
    
    uploaded_file = st.file_uploader("Upload Teamcenter Export (Excel/CSV)", type=['xlsx', 'csv'])
    
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.dataframe(df.head(3))
        
        agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)
        
        default_val = ""
        auto_run = False
        if st.session_state.trigger_query:
            default_val = st.session_state.trigger_query
            auto_run = True
            st.session_state.trigger_query = None

        query = st.text_input("Ask for a report...", value=default_val)
        
        if st.button("Generate Report") or auto_run:
            with st.spinner("Analyzing data..."):
                try:
                    response = agent.invoke(query)
                    answer_text = response['output']
                    st.session_state.history.append({
                        "mode": "Manager Report",
                        "question": query,
                        "answer": answer_text
                    })
                    st.success(answer_text)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

# --- MODE 3: ADMIN ---
elif mode == "Admin: Database Viewer":
    st.subheader("💾 Vector Database Inspector")
    embedding_function = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    data = vectorstore.get()
    
    if len(data['ids']) == 0:
        st.error("Database is empty. Please run ingest.py.")
    else:
        st.metric("Total Documents Chunks", len(data['ids']))
        df_view = pd.DataFrame({
            'ID': data['ids'],
            'Source': [m.get('source') for m in data['metadatas']],
            'Content Preview': data['documents']
        })
        st.dataframe(df_view, use_container_width=True)