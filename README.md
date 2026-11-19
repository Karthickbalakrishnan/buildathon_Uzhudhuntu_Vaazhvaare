# 🌾 உழுதுண்டு வாழ்வாரே (Uzhudhuntu Vaazhvaare)

### Bilingual Agricultural Information Assistant for Tamil Nadu

> **A Tamil and English RAG assistant for Tamil Nadu agricultural subsidies, drip irrigation, solar pumps, NABARD unit costs, and farmer-oriented scheme guidance.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) [![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/) [![License](https://img.shields.io/badge/License-Not%20Specified-lightgrey)](#license)

---

## 📌 Project Overview

**உழுதுண்டு வாழ்வாரே** is a bilingual, retrieval-augmented generation (RAG) application designed to help farmers and agricultural officers access verified information about Tamil Nadu government schemes and agricultural investments.

The system converts official PDFs into searchable vector data, retrieves relevant information for a user's question, and generates a concise Tamil or English response grounded in the selected documents. It is also designed around practical field use, including voice interaction, WhatsApp sharing, officer document management, and culturally relevant agricultural guidance.

> **Important:** This project provides decision-support information. It does not replace official departmental verification, eligibility rules, or the latest government notifications.

---

## ✨ Key Features

- **Bilingual RAG Engine** — Answers queries in Tamil or English using indexed government and NABARD documents.
- **Voice Input** — Uses OpenAI Whisper for speech-to-text transcription.
- **Voice Output** — Uses gTTS for Tamil and English audio playback.
- **Officer Document Management** — Uploads and indexes official PDFs into the FAISS knowledge base.
- **Source-Grounded Responses** — Retrieves relevant content before generating an answer.
- **WhatsApp Sharing** — Sends a concise, readable scheme response to a farmer's chat.
- **Agricultural Context** — Supports scheme, subsidy, crop, dairy, livestock, drip irrigation, solar pump, and unit-cost questions.
- **Thirukkural Integration** — Provides culturally relevant Tamil agricultural wisdom.
- **Evaluation Module** — Includes `backend/evaluate.py` for buildathon and response-quality evaluation workflows.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | Bilingual user interface and officer controls |
| Backend | FastAPI, Uvicorn | API and application orchestration |
| LLM | OpenAI GPT-4o-mini | Response generation |
| Retrieval | LangChain, FAISS | Document chunking, embeddings, and semantic retrieval |
| Speech-to-Text | OpenAI Whisper | Voice query transcription |
| Text-to-Speech | gTTS | Tamil and English audio playback |
| Document Processing | PyPDF | PDF text extraction |
| Document Format | PDF | Government schemes and NABARD unit-cost sources |

---

## 🏗️ System Architecture

```text
┌────────────────────┐
│  Farmer / Officer  │
└─────────┬──────────┘
          │ Tamil or English text / voice
          ▼
┌────────────────────┐
│ Streamlit Frontend │
└─────────┬──────────┘
          │ HTTP API request
          ▼
┌────────────────────┐
│  FastAPI Backend   │
├────────────────────┤
│ Query processing   │
│ Document retrieval │
│ RAG generation     │
│ Voice processing   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ FAISS Vector Store │
└─────────┬──────────┘
          │
          ▼
┌──────────────────────────────────┐
│ Official PDFs, circulars, reports│
└──────────────────────────────────┘
```

### RAG Workflow

1. A document is uploaded or loaded into the application.
2. PyPDF extracts its text.
3. LangChain chunks the content into searchable passages.
4. Passages are converted into embeddings and stored in FAISS.
5. The user's query retrieves the most relevant passages.
6. GPT-4o-mini generates a contextual response from retrieved evidence.
7. Streamlit presents the answer, with optional voice and WhatsApp actions.

---

## 📁 Repository Structure

```text
buildathon_Uzhudhuntu_Vaazhvaare/
├── backend/
│   ├── main.py       # FastAPI application and RAG endpoints
│   └── evaluate.py   # Evaluation utilities
├── frontend/
│   └── app.py        # Streamlit interface
├── data/
│   ├── 1.banner_en.png
│   └── 2.banner_ta.png
├── 0. Tamil Nadu Unit cost Booklet 2026-27 FINAL.pdf.pdf
├── agri_e_cc_2025_26.pdf
├── agri_e_cc_2026_27.pdf.pdf
├── agri_e_pn_2026_27.pdf
├── Binder1.pdf
├── Agricultural_Schemes_RAG_RTCFR_Prompt.pdf
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- OpenAI API key
- Internet access for model and text-to-speech services
- Microphone support for browser voice input

### 1. Clone the repository

```bash
git clone https://github.com/Karthickbalakrishnan/buildathon_Uzhudhuntu_Vaazhvaare.git
cd buildathon_Uzhudhuntu_Vaazhvaare
```

### 2. Create and activate a virtual environment

**Linux or macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Add the required API key:

```dotenv
OPENAI_API_KEY=your_openai_api_key
```

Never commit your real API key or expose it in screenshots or logs.

### 5. Start the backend

In Terminal 1:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

FastAPI API documentation should be available at:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the frontend

In Terminal 2:

```bash
streamlit run frontend/app.py
```

Open:

```text
http://localhost:8501
```

---

## 👨‍🌾 Officer Mode

Officer Mode enables authorized users or officers to refresh the knowledge base during demonstrations or operational use.

1. Open the Streamlit sidebar.
2. Enable **Officer Mode**.
3. Upload an official Tamil Nadu or NABARD PDF.
4. Select **Index PDF**.
5. Wait for the document-processing operation to complete.
6. Ask a question through the normal chat interface.

Use only accurate, current, and officially published documents. Remove or replace outdated files and rebuild the index when source information changes.

---

## 💬 Example Queries

### Tamil

- Tamil Nadu-வில் drip irrigation subsidy எப்படி பெறுவது?
- Solar pumpக்கு NABARD unit cost என்ன?
- Woman farmer eligibility for agricultural subsidy என்ன?
- Dairy cow scheme benefits என்ன?

### English

- What is the subsidy for drip irrigation in Tamil Nadu?
- What is the NABARD unit cost for a solar pump?
- What documents are required to apply for a dairy loan?
- Compare available assistance for micro-irrigation and livestock.

---

## 🧪 Evaluation

The repository includes `backend/evaluate.py` for buildathon-oriented evaluation. Evaluations should measure:

- **Retrieval relevance** — Is the correct source passage returned?
- **Answer correctness** — Does the response match the official document?
- **Grounding** — Can each key claim be traced to retrieved evidence?
- **Bilingual quality** — Is the answer understandable in both Tamil and English?
- **Completeness** — Are eligibility, benefits, documents, and next steps handled when available?
- **Safety** — Does the system avoid unsupported promises or fabricated policy details?
- **User experience** — Does voice input, text-to-speech, and sharing work reliably?

A strong demonstration should include at least one successful answer, one Tamil query, one voice interaction, and one officer-mode document indexing example.

---

## 🔒 Responsible AI and Safety

- The application uses RAG, but retrieved context can still be incomplete or misinterpreted.
- Answers should not be presented as a final approval or guarantee of benefits.
- Farmers should confirm eligibility, deadlines, subsidy rates, and documents with the relevant department or official portal.
- Uploaded documents should be authorized and current.
- API keys and personal data must not be stored in source files or shared in public demonstrations.

---

## ⚠️ Known Limitations

- PDF extraction quality may vary for scanned or image-heavy documents.
- Retrieval results depend on document indexing quality and chunk selection.
- Scheme rules and unit costs may change over time.
- OpenAI and speech services require network access and valid credentials.
- Application performance depends on API availability and the quality of source PDFs.

---

## 🗺️ Future Enhancements

- District and block-level scheme filtering
- Source citations in every response
- Document freshness indicators
- Offline or cached scheme search
- SMS and IVRS support
- Improved scanned-PDF OCR
- Structured eligibility assessment
- User feedback-based response evaluation
- Multi-document and scheme comparison views

---

## 🤝 Contributing

Contributions should improve accuracy, usability, accessibility, or retrieval quality.

1. Create a new branch.
2. Make focused changes.
3. Test backend and frontend behavior locally.
4. Update the README if setup or features change.
5. Submit a pull request with a clear description and test evidence.

---

## 📄 License

A license is not currently specified in this repository. Until a license is added, no permission is granted for reuse or distribution beyond the source owner's rights.

---

## 📚 Official Reference Use

The knowledge base may include Tamil Nadu government circulars, citizen charters, agricultural schemes, and NABARD or other official unit-cost documents. Always verify the latest document, notification, and eligibility rules through the responsible government department or authorized portal before submission or financial commitment.

---

## 📬 Repository

**GitHub:** [Karthickbalakrishnan/buildathon_Uzhudhuntu_Vaazhvaare](https://github.com/Karthickbalakrishnan/buildathon_Uzhudhuntu_Vaazhvaare)
