from __future__ import annotations

import html
import os

import requests
import streamlit as st
from dotenv import load_dotenv

from services.document_formatter import format_docx, format_pdf

load_dotenv()

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.markdown(
    """
    <style>
    .hero {
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #111827, #1f2937);
        color: white;
        margin-bottom: 1rem;
    }
    .preview {
        background: #0b1220;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1.2rem;
        max-height: 620px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: Georgia, serif;
        line-height: 1.55;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>⚖️ LegalEase</h1>
      <p>AI-powered legal document drafting, editing and export.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Document details")
    document_type = st.text_input(
        "Document type",
        value="Freelance Work Contract",
        help="Example: NDA, Lease Agreement, Employment Contract.",
    )
    parties = st.text_area(
        "Parties involved",
        value="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=120,
    )
    terms = st.text_area(
        "Terms & conditions",
        value=(
            "Payment to be made within 30 days of invoice; "
            "The provider agrees to deliver work by the agreed deadline; "
            "Confidentiality must be maintained at all times; "
            "Either party may terminate with 15 days notice"
        ),
        height=180,
        help="Separate individual terms with semicolons.",
    )
    dates = st.text_input("Effective date", value="April 15, 2026")

    generate = st.button(
        "Generate Document",
        type="primary",
        use_container_width=True,
    )

if generate:
    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": dates,
    }

    try:
        with st.spinner("Generating legal draft..."):
            response = requests.post(
                f"{BACKEND_URL}/generate",
                json=payload,
                timeout=120,
            )
        if response.ok:
            data = response.json()
            st.session_state["document"] = data["content"]
            st.session_state["doc_type"] = data["document_type"]
            st.session_state["model"] = data["model"]
            st.session_state["demo_mode"] = data.get("demo_mode", False)
            st.success("Document generated.")
        else:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            st.error(f"Backend error: {detail}")
    except requests.RequestException as exc:
        st.error(
            "Could not connect to FastAPI. Start the backend first. "
            f"Details: {exc}"
        )

if "document" not in st.session_state:
    st.info("Enter the document details in the sidebar and click Generate Document.")
else:
    if st.session_state.get("demo_mode"):
        st.warning(
            "Demo mode is active because GEMINI_API_KEY is not configured. "
            "The backend is running, but the generated content is a local placeholder."
        )

    st.caption(
        f"Model: {st.session_state.get('model', 'unknown')} "
        " | Edit the draft below before exporting."
    )

    edited = st.text_area(
        "Editable document",
        value=st.session_state["document"],
        height=520,
        key="editable_document",
    )
    st.session_state["document"] = edited

    st.subheader("Preview")
    safe = html.escape(edited)
    st.markdown(f'<div class="preview">{safe}</div>', unsafe_allow_html=True)

    st.subheader("Download")
    col1, col2, col3 = st.columns(3)

    filename_base = (
        st.session_state.get("doc_type", "legal_document")
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
    )

    with col1:
        st.download_button(
            "Download TXT",
            data=edited.encode("utf-8"),
            file_name=f"{filename_base}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:
        docx_bytes = format_docx(edited, st.session_state.get("doc_type", "Legal Document"))
        st.download_button(
            "Download DOCX",
            data=docx_bytes,
            file_name=f"{filename_base}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

    with col3:
        pdf_bytes = format_pdf(edited, st.session_state.get("doc_type", "Legal Document"))
        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name=f"{filename_base}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.divider()
st.caption(
    "LegalEase creates AI-assisted drafts. Review the document and obtain "
    "professional legal advice where appropriate."
)
