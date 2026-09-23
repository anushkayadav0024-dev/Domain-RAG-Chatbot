import streamlit as st
import tempfile
import os

from document_loader import load_and_split_pdf
from vector_store import VectorStore
from rag_pipeline import generate_answer


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Domain RAG Chatbot",
    page_icon="📚",
    layout="centered"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "uploaded_names" not in st.session_state:
    st.session_state.uploaded_names = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Controls")

    if st.session_state.vector_store is not None:

        st.success(
            f"📚 {len(st.session_state.uploaded_names)} "
            f"PDF(s) loaded"
        )

        st.markdown("### 📄 Documents")

        for name in st.session_state.uploaded_names:
            st.write(f"• {name}")

        st.divider()

        # Clear only conversation
        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        ):

            st.session_state.messages = []

            st.rerun()

        # Completely remove current PDFs
        if st.button(
            "📄 New PDF",
            use_container_width=True
        ):

            st.session_state.vector_store = None
            st.session_state.uploaded_names = []
            st.session_state.messages = []

            # Create a fresh uploader
            st.session_state.uploader_key += 1

            st.rerun()


# --------------------------------------------------
# Main UI
# --------------------------------------------------

st.title("📚 Domain-Specific RAG Chatbot")

st.write(
    "Upload one or more PDFs and ask questions "
    "based only on their content."
)


# --------------------------------------------------
# PDF Upload
# --------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True,
    key=f"pdf_uploader_{st.session_state.uploader_key}"
)


# --------------------------------------------------
# Process PDFs
# --------------------------------------------------

if uploaded_files:

    uploaded_names = sorted(
        file.name for file in uploaded_files
    )

    current_names = sorted(
        st.session_state.uploaded_names
    )

    # Process only if PDFs have changed
    if uploaded_names != current_names:

        with st.spinner(
            "📖 Processing your PDF documents..."
        ):

            all_chunks = []

            for uploaded_file in uploaded_files:

                # Create temporary PDF
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getvalue()
                    )

                    pdf_path = temp_file.name

                # Extract and chunk
                chunks = load_and_split_pdf(
                    pdf_path
                )

                # Replace temporary filename
                # with actual uploaded filename
                for chunk in chunks:

                    chunk.metadata["source"] = (
                        uploaded_file.name
                    )

                all_chunks.extend(chunks)

                os.remove(pdf_path)

            # Create ONE vector store
            # containing all uploaded PDFs
            st.session_state.vector_store = (
                VectorStore(all_chunks)
            )

            st.session_state.uploaded_names = (
                uploaded_names
            )

            # New documents = new conversation
            st.session_state.messages = []

        st.success(
            f"✅ {len(uploaded_files)} PDF(s) "
            f"processed successfully."
        )


# --------------------------------------------------
# Chat
# --------------------------------------------------

if st.session_state.vector_store is not None:

    st.subheader("💬 Chat with your documents")

    # ----------------------------------------------
    # Display COMPLETE conversation
    # ----------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

            if (
                message["role"] == "assistant"
                and message.get("sources")
            ):

                st.markdown("**📚 Sources:**")

                for source in message["sources"]:

                    st.write(
                        f"📄 {source['file']} "
                        f"— Page {source['page']}"
                    )


    # ----------------------------------------------
    # Question Input
    # ----------------------------------------------

    question = st.chat_input(
        "Ask another question..."
    )


    if question:

        # Save user question FIRST
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Display question immediately
        with st.chat_message("user"):

            st.write(question)


        # ------------------------------------------
        # Retrieval
        # ------------------------------------------

        with st.spinner(
            "🔎 Searching your documents..."
        ):

            retrieved_chunks = (
                st.session_state.vector_store.search(
                    question,
                    k=3
                )
            )


        # ------------------------------------------
        # Gemini Answer
        # ------------------------------------------

        with st.spinner(
            "🤖 Generating answer..."
        ):

            answer = generate_answer(
                question,
                retrieved_chunks
            )


        # ------------------------------------------
        # Sources
        # ------------------------------------------

        sources = []
        shown_sources = set()

        for chunk in retrieved_chunks:

            file_name = os.path.basename(
                chunk.metadata["source"]
            )

            page = chunk.metadata["page"]

            source_key = (
                file_name,
                page
            )

            if source_key not in shown_sources:

                sources.append(
                    {
                        "file": file_name,
                        "page": page
                    }
                )

                shown_sources.add(
                    source_key
                )


        # ------------------------------------------
        # Save Answer
        # ------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources
            }
        )


        # ------------------------------------------
        # Display Answer
        # ------------------------------------------

        with st.chat_message("assistant"):

            st.write(answer)

            if sources:

                st.markdown("**📚 Sources:**")

                for source in sources:

                    st.write(
                        f"📄 {source['file']} "
                        f"— Page {source['page']}"
                    )