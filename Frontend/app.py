import streamlit as st
import requests
import pandas as pd

# Base URL of the FastAPI backend
BASE_URL = "http://127.0.0.1:8000"  # Replace with your backend URL

# App title and sidebar
st.title("AI-Powered Customer Service System")
st.sidebar.title("Menu")
menu = st.sidebar.radio("Pilih Menu:", ["Upload Knowledge Base", "Tanya AI", "Log Interaksi"])

# Upload documents to the knowledge base
if menu == "Upload Knowledge Base":
    st.header("Upload Knowledge Base")
    uploaded_file = st.file_uploader("Unggah file dokumen (PDF/TXT):", type=["pdf", "txt"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1]
        files = {"file": (uploaded_file.name, uploaded_file, f"application/{file_type}")}

        # Send file to backend
        with st.spinner("Mengunggah dan memproses file..."):
            response = requests.post(f"{BASE_URL}/upload-doc", files=files)
        
        if response.status_code == 200:
            st.success("File berhasil diunggah dan ditambahkan ke knowledge base!")
        else:
            st.error("Gagal mengunggah file. Pastikan formatnya benar.")

# Query AI assistant
elif menu == "Tanya AI":
    st.header("Tanya AI Customer Service")
    query = st.text_input("Masukkan pertanyaan Anda:")
    example_queries = [
        "Bagaimana cara mengaktifkan layanan roaming?",
        "Apa solusi untuk koneksi internet yang lambat?",
        "Berikan panduan troubleshooting untuk modem ini."
    ]

    st.markdown("**Contoh pertanyaan:**")
    for q in example_queries:
        st.markdown(f"- {q}")

    if st.button("Tanya AI") and query:
        with st.spinner("Mengambil jawaban dari AI..."):
            response = requests.post(f"{BASE_URL}/query", json={"query": query})

        if response.status_code == 200:
            result = response.json()
            st.success("Jawaban AI:")
            st.write(result.get("response", "Tidak ada jawaban yang ditemukan."))
            st.write(f"**Tingkat Urgensi:** {result.get('urgency_level', 'Tidak diketahui')}")
        else:
            st.error("Gagal mendapatkan jawaban dari AI.")

# View interaction logs
elif menu == "Log Interaksi":
    st.header("Log Interaksi")
    with st.spinner("Mengambil log interaksi..."):
        response = requests.get(f"{BASE_URL}/logs")

    if response.status_code == 200:
        logs = response.json().get("logs", [])

        if logs:
            st.dataframe(pd.DataFrame(logs))
        else:
            st.info("Belum ada interaksi yang dicatat.")
    else:
        st.error("Gagal mengambil log interaksi.")
