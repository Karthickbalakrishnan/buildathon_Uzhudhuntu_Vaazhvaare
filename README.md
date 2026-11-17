# 🌾 உழுதுண்டு வாழ்வாரே (Uzhudhuntu Vaazhvaare)
> **Tamil Nadu Agricultural Subsidies, Drip Irrigation, Solar Pumps & NABARD Unit Cost AI Assistant**

An intelligent, bilingual (Tamil & English) RAG-powered assistant designed for Tamil Nadu farmers and agricultural officers to instantly query government schemes, NABARD unit costs, dairy/livestock loans, and subsidies via text and voice.

---

## 🚀 Key Features
* **Bilingual RAG Engine**: Powered by official Tamil Nadu government booklets, citizen charters, and NABARD unit cost reports.
* **Voice-Enabled Assistant**: Whisper-powered speech-to-text with gTTS audio responses in Tamil and English.
* **Officer Mode**: Built-in document manager allowing officers to upload and index new scheme PDFs on the fly.
* **Instant WhatsApp Sharing**: One-click sharing of verified scheme benefit summaries directly to farmers' WhatsApp chats.
* **Cultural Grounding**: Embedded daily Thirukkural agricultural wisdom ticker.

---

## 🛠️ Tech Stack
* **Frontend**: Streamlit (Custom responsive UI)
* **Backend**: FastAPI, Uvicorn
* **AI / RAG**: LangChain, OpenAI GPT-4o-mini, OpenAI Whisper, FAISS Vector Store, gTTS
* **Data Processing**: PyPDF

---

## ⚙️ Local Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/Uzhudhuntu_Vaazhvaare.git](https://github.com/your-username/Uzhudhuntu_Vaazhvaare.git)
cd Uzhudhuntu_Vaazhvaare
