import os
import pdfplumber
import streamlit as st
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
VECTOR_DB_DIR = "knowledge_base"
PDF_STORAGE_DIR = "source_documents"

os.makedirs(VECTOR_DB_DIR, exist_ok=True)
os.makedirs(PDF_STORAGE_DIR, exist_ok=True)

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def stop_on_start_if_debugging():
    if os.getenv("STREAMLIT_BREAK_ON_START") == "1":
        breakpoint()


stop_on_start_if_debugging()

# ---------------------------------------------------
# PDF Content Processing
# ---------------------------------------------------
def read_pdf_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"

    return text


# ---------------------------------------------------
# Text Processing and Chunk Creation
# ---------------------------------------------------
def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    return splitter.split_text(text)


# ---------------------------------------------------
# Generate Vector Index
# ---------------------------------------------------
def create_vector(chunks):

    embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")

    docs = [Document(page_content=chunk) for chunk in chunks]

    vector_store = FAISS.from_documents(docs, embedding)

    vector_store.save_local(VECTOR_DB_DIR)

    return len(chunks)


# ---------------------------------------------------
# Initialize Vector Database
# ---------------------------------------------------
def load_vector_index():

    embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")

    return FAISS.load_local(
        VECTOR_DB_DIR, embedding, allow_dangerous_deserialization=True
    )


# ---------------------------------------------------
# AI-Powered Question Answering
# ---------------------------------------------------
def generate_answer(question):

    vector_store = load_vector_index()

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.2)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a helpful assistant.

Answer ONLY from the provided context.

If the answer is not available in the context, reply exactly:

I can't find this information in the PDF

Do not use external knowledge.
Do not make assumptions.
""",
            ),
            ("human", "Context:\n{context}\n\nQuestion:\n{question}"),
        ]
    )

    chain = (
        RunnableParallel(
            {
                "context": lambda x: "\n\n".join(
                    [doc.page_content for doc in retriever.invoke(x["question"])]
                ),
                "question": lambda x: x["question"],
            }
        )
        | prompt
        | llm
    )

    result = chain.invoke({"question": question})

    return result.content


# ---------------------------------------------------
# Streamlit UI
# ---------------------------------------------------
st.set_page_config(page_title="PDF RAG Assistant", page_icon="📚", layout="wide")

# ---------------------------------------------------
# Application Status
# ---------------------------------------------------
with st.sidebar:

    st.header("Application Status")

    st.write("Knowledge Base:", f"`{os.path.abspath(VECTOR_DB_DIR)}`")
    st.write("Document Storage:", f"`{os.path.abspath(PDF_STORAGE_DIR)}`")

    if OPENAI_API_KEY:
        st.success("OpenAI API Key Connected")
    else:
        st.error("OpenAI API Key Missing")


# ---------------------------------------------------
# Tabs
# ---------------------------------------------------
tab1, tab2 = st.tabs(["📚 Upload Documents", "🤖 AI Document Assistant"])

# ---------------------------------------------------
# Document Processing - Tab1
# ---------------------------------------------------
with tab1:

    st.title("Document Upload & Knowledge Base Creation")

    uploaded_document = st.file_uploader("Upload a PDF Document", type=["pdf"])

    if uploaded_document:

        document_path = os.path.join(PDF_STORAGE_DIR, uploaded_document.name)

        with open(document_path, "wb") as file:
            file.write(uploaded_document.getbuffer())

        st.info("📄 Extracting document content...")

        document_text = read_pdf_text(document_path)

        st.info("✂️ Creating document chunks...")

        text_chunks = split_text(document_text)

        st.write(f"Generated Chunks: {len(text_chunks)}")

        st.info("🧠 Building semantic knowledge base...")

        total_chunks = create_vector(text_chunks)

        st.success(f"Vector base created successfully! ({total_chunks} chunks indexed)")

        st.balloons()
# ---------------------------------------------------
# AI Document Assistant
# ---------------------------------------------------
with tab2:

    st.title("Ask Your Documents")

    user_query = st.text_input("Enter your question")

    if st.button("Get Answer"):

        if not user_query.strip():

            st.warning("Please enter a valid question.")

        else:

            with st.spinner("Analyzing documents and generating response..."):

                try:

                    response = generate_answer(user_query)

                    st.success("Response Generated")

                    st.write(response)

                except Exception as error:

                    st.error(f"Unexpected Error: {str(error)}")