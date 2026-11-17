# 🌾 உழுதுண்டு வாழ்வாரே (Uzhudhuntu Vaazhvaare)
> **Tamil Nadu Agricultural Subsidies, Drip Irrigation, Solar Pumps & NABARD Unit Cost AI Assistant**

An intelligent, bilingual (Tamil & English) RAG-powered assistant designed for Tamil Nadu farmers and agricultural officers to instantly query government schemes, NABARD unit costs, dairy/livestock loans, and subsidies via text and voice.

---

## 🚀 Key Features
* **Bilingual RAG Engine**: Grounded directly in official Tamil Nadu government booklets, citizen charters, and NABARD unit cost reports.
* **Voice-Enabled Assistant**: Whisper-powered speech-to-text input with gTTS natural audio playback in Tamil and English.
* **Officer Management Mode**: Built-in document management drawer allowing officers to upload and index new scheme PDFs on the fly.
* **Instant WhatsApp Sharing**: One-click sharing of verified scheme benefit summaries directly to farmers' WhatsApp chats.
* **Cultural Grounding**: Embedded daily Thirukkural agricultural wisdom ticker (`சுழன்றும்ஏர்ப் பின்னது உலகம்...`).

---

## 🛠️ Tech Stack
* **Frontend**: Streamlit (Responsive, custom agricultural UI)
* **Backend**: FastAPI, Uvicorn
* **AI / RAG Pipeline**: LangChain, OpenAI GPT-4o-mini, OpenAI Whisper, FAISS Vector Store, gTTS (Google Text-to-Speech)
* **Document Processing**: PyPDF

---

## 📁 Repository Structure
```text
Uzhudhuntu_Vaazhvaare/
├── backend/
│   ├── __init__.py
│   └── main.py
├── frontend/
│   └── app.py
├── data/
│   ├── 1.banner_en.png
│   ├── 2.banner_ta.png
│   └── [Official Scheme PDFs & Booklets]
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

⚙️ Local Installation & Setup Guide
1. Clone the Repository
Bash
git clone [https://github.com/your-username/Uzhudhuntu_Vaazhvaare.git](https://github.com/your-username/Uzhudhuntu_Vaazhvaare.git)
cd Uzhudhuntu_Vaazhvaare
2. Set Up Virtual Environment & Dependencies
Bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the root directory:

Bash
touch .env
Open .env and add your OpenAI API key:

Code snippet
OPENAI_API_KEY=your_actual_openai_api_key_here
4. Run the Application (Two Terminal Tabs)
Open two separate terminal windows in the project root directory:

Terminal 1: Start Backend (FastAPI)

Bash
source venv/bin/activate
python -m uvicorn backend.main:app --reload --port 8000
Terminal 2: Start Frontend (Streamlit)

Bash
source venv/bin/activate
streamlit run frontend/app.py
Access the application locally in your browser at http://localhost:8501.

👨‍🌾 Officer Mode Instructions
Expand the Officer Management sidebar on the left.

Toggle Enable Officer Mode.

Upload any official Tamil Nadu agricultural PDF or NABARD circular.

Click Index PDF to instantly update the FAISS vector database.
