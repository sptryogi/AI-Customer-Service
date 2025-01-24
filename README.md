# AI-Powered Customer Service System

Sistem ini adalah aplikasi layanan pelanggan berbasis AI yang menggunakan teknik Retrieval-Augmented Generation (RAG) untuk memberikan jawaban otomatis kepada pelanggan berdasarkan dokumen yang diunggah. Aplikasi ini memiliki backend berbasis **FastAPI** dan frontend berbasis **Streamlit**.

---

## Fitur Utama

1. **Unggah Knowledge Base**
   - Mendukung file PDF dan TXT untuk dimasukkan ke dalam basis pengetahuan.
   - Dokumen dipecah menjadi potongan kecil dan diindeks menggunakan FAISS.

2. **Tanya AI**
   - Menjawab pertanyaan pelanggan berdasarkan dokumen yang tersedia di knowledge base.
   - Menampilkan tingkat urgensi dari setiap pertanyaan yang diajukan.

3. **Log Interaksi**
   - Menyimpan riwayat interaksi pelanggan, termasuk pertanyaan, jawaban, dan tingkat urgensi.

---

## Struktur Proyek

```plaintext
.
├── backend
│   ├── customer_service.py   # Backend FastAPI
│   ├── data
│   │   ├── knowledge_base    # Folder untuk dokumen yang diunggah
│   │   ├── faiss_index       # Indeks FAISS
│   │   └── interactions.db   # Database SQLite untuk log interaksi
├── frontend
│   ├── app.py                # Frontend Streamlit
└── README.md                 # Dokumentasi proyek
```

---

## Persyaratan Sistem

- **Python** >= 3.8
- Library Python:
  - FastAPI
  - Streamlit
  - LangChain
  - FAISS
  - Transformers
  - SQLite3
  - PyPDF2
  - Requests

---

## Langkah-Langkah Instalasi dan Penggunaan

1. **Kloning Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Buat Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # Untuk Linux/MacOS
   env\Scripts\activate    # Untuk Windows
   ```

3. **Instal Dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Backend (FastAPI)**
   ```bash
   cd backend
   uvicorn customer_service:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Jalankan Frontend (Streamlit)**
   Buka terminal baru dan jalankan:
   ```bash
   cd frontend
   streamlit run app.py
   ```

6. **Akses Aplikasi**
   - **Backend API**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - **Frontend**: [http://localhost:8501](http://localhost:8501)

---

## Alur Penggunaan

1. **Unggah Dokumen**: Masukkan file knowledge base dalam format PDF atau TXT melalui menu "Upload Knowledge Base".
2. **Tanya AI**: Ajukan pertanyaan di menu "Tanya AI". Jawaban AI akan diberikan berdasarkan dokumen yang telah diunggah.
3. **Cek Log Interaksi**: Riwayat pertanyaan dan jawaban dapat dilihat di menu "Log Interaksi".

---

## Catatan Tambahan

1. Pastikan model lokal (T5-Base) telah diunduh saat pertama kali digunakan.
2. File knowledge base disimpan di folder `data/knowledge_base` secara otomatis.
3. Jika ada masalah dengan integrasi atau error pada sistem, periksa log backend di terminal.

---

## Lisensi
Proyek ini dilisensikan di bawah lisensi [MIT](LICENSE).
