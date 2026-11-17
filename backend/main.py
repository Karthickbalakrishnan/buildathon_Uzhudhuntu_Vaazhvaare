import base64
import io
import os
import shutil
import tempfile
from collections import Counter
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

DATA_DIR = "data"
FAISS_INDEX_PATH = "faiss_index"
os.makedirs(DATA_DIR, exist_ok=True)

app = FastAPI(title="Uzhudhuntu Vaazhvaare - RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_client = OpenAI()
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)


class QueryRequest(BaseModel):
    query: str
    language: str = "Tamil"


class StructuredSchemeResponse(BaseModel):
    scheme_title: str
    benefit_summary: str
    eligibility_points: List[str]
    contact_action: str
    spoken_summary: str


def get_splitter():
    return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


def load_vectorstore() -> Optional[FAISS]:
    if os.path.exists(FAISS_INDEX_PATH):
        try:
            return FAISS.load_local(
                FAISS_INDEX_PATH,
                embeddings,
                allow_dangerous_deserialization=True,
            )
        except Exception as e:
            print(f"FAISS load warning: {e}")
    return None


def index_all_data_pdfs(force_rebuild: bool = False) -> dict:
    if force_rebuild and os.path.exists(FAISS_INDEX_PATH):
        shutil.rmtree(FAISS_INDEX_PATH)

    vectorstore = None if force_rebuild else load_vectorstore()
    existing_files = set()

    if vectorstore is not None:
        for doc in vectorstore.docstore._dict.values():
            src = doc.metadata.get("source") or doc.metadata.get("file_name")
            if src:
                existing_files.add(os.path.basename(src))

    splitter = get_splitter()
    newly_indexed = []
    skipped = []

    for filename in sorted(os.listdir(DATA_DIR)):
        if not filename.lower().endswith(".pdf") or filename in existing_files:
            continue

        file_path = os.path.join(DATA_DIR, filename)
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            for d in docs:
                d.metadata["source"] = filename

            chunks = splitter.split_documents(docs)
            if not chunks:
                skipped.append(f"{filename} (no extractable text)")
                continue

            if vectorstore is not None:
                try:
                    vectorstore.add_documents(chunks)
                except AssertionError:
                    return index_all_data_pdfs(force_rebuild=True)
            else:
                vectorstore = FAISS.from_documents(chunks, embeddings)

            newly_indexed.append(f"{filename} ({len(chunks)} chunks)")
        except Exception as e:
            skipped.append(f"{filename} ({str(e)})")

    if vectorstore is not None and newly_indexed:
        vectorstore.save_local(FAISS_INDEX_PATH)

    return {"newly_indexed": newly_indexed, "skipped": skipped}


@app.on_event("startup")
async def on_startup():
    index_all_data_pdfs(force_rebuild=False)


def generate_tts_base64(text: str, language: str) -> Optional[str]:
    try:
        clean_text = text.replace("*", "").replace("#", "").strip()
        if not clean_text:
            return None
        lang_code = "ta" if language == "Tamil" else "en"
        tts = gTTS(text=clean_text[:900], lang=lang_code, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")
    except Exception as e:
        print(f"TTS warning: {e}")
        return None


def execute_rtcfr_rag(user_query: str, language: str) -> dict:
    vectorstore = load_vectorstore()
    if vectorstore is None:
        index_all_data_pdfs(force_rebuild=False)
        vectorstore = load_vectorstore()

    if vectorstore is None:
        empty_msg = (
            "தற்போது திட்ட ஆவணங்கள் எதுவும் இணைக்கப்படவில்லை. அதிகாரி பக்கத்தில் PDF கோப்பைச் சேர்க்கவும்."
            if language == "Tamil"
            else "No scheme documents are loaded yet. Please add a PDF in Officer Mode."
        )
        return {
            "scheme_title": "ஆவணம் தேவை / Document Needed",
            "benefit_summary": empty_msg,
            "eligibility_points": [],
            "contact_action": "உதவி வேளாண்மை அலுவலர் (Assistant Agricultural Officer)",
            "sources": [],
            "audio_base64": generate_tts_base64(empty_msg, language),
        }

    try:
        docs = vectorstore.as_retriever(search_kwargs={"k": 4}).invoke(user_query)
    except AssertionError:
        index_all_data_pdfs(force_rebuild=True)
        vectorstore = load_vectorstore()
        docs = vectorstore.as_retriever(search_kwargs={"k": 4}).invoke(user_query)

    context_blocks = []
    sources = []
    for doc in docs:
        src_name = os.path.basename(doc.metadata.get("source", "Scheme Policy"))
        page_num = doc.metadata.get("page", 0) + 1
        label = f"{src_name} (Page {page_num})"
        if label not in sources:
            sources.append(label)
        context_blocks.append(f"[{label}]\n{doc.page_content}")

    context_text = "\n\n---\n\n".join(context_blocks)

    lang_directive = (
        "Write ALL fields strictly in simple, warm, spoken-style Tamil (தமிழ்) easy for a rural farmer to understand."
        if language == "Tamil"
        else "Write ALL fields in clear, jargon-free English."
    )

    system_prompt = f"""You are 'Uzhudhuntu Vaazhvaare', a trusted Tamil Nadu agricultural advisor.
Extract accurate facts ONLY from the provided NABARD Unit Cost and TN Agriculture Citizen Charter context.
{lang_directive}

Return a valid JSON object matching this exact schema:
{{
  "scheme_title": "Short clear title of the scheme or loan item",
  "benefit_summary": "1-2 sentences stating exact subsidy percentage, unit cost, or loan amount in bold numbers",
  "eligibility_points": ["Short rule 1", "Short rule 2", "Short rule 3 (max 3 bullets)"],
  "contact_action": "Exact officer designation to meet and portal/app name (e.g., Uzhavar App / tnagrisnet.tn.gov.in)",
  "spoken_summary": "A natural 2-3 sentence summary meant to be read aloud to the farmer"
}}

If the exact detail is not in the context, state that clearly in benefit_summary and recommend contacting the local Assistant Agricultural Officer."""

    structured_llm = llm.with_structured_output(StructuredSchemeResponse)
    parsed: StructuredSchemeResponse = structured_llm.invoke(
        [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nFarmer's Question: {user_query}",
            },
        ]
    )

    audio_b64 = generate_tts_base64(parsed.spoken_summary, language)

    return {
        "scheme_title": parsed.scheme_title,
        "benefit_summary": parsed.benefit_summary,
        "eligibility_points": parsed.eligibility_points,
        "contact_action": parsed.contact_action,
        "sources": sources,
        "audio_base64": audio_b64,
    }


@app.get("/indexed-pdfs")
async def get_indexed_pdfs():
    vectorstore = load_vectorstore()
    if vectorstore is None:
        return {"total_files": 0, "files": []}

    counts = Counter()
    for doc in vectorstore.docstore._dict.values():
        src = doc.metadata.get("source") or doc.metadata.get("file_name")
        if src:
            counts[os.path.basename(src)] += 1

    return {
        "total_files": len(counts),
        "files": [{"filename": k, "chunks": v} for k, v in sorted(counts.items())],
    }


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    dest_path = os.path.join(DATA_DIR, file.filename)
    try:
        with open(dest_path, "wb") as buf:
            shutil.copyfileobj(file.file, buf)

        res = index_all_data_pdfs(force_rebuild=False)
        if not res["newly_indexed"] and res["skipped"]:
            raise HTTPException(status_code=400, detail=", ".join(res["skipped"]))

        return {"status": "success", "message": f"Added {file.filename} successfully."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sync-data-folder")
async def sync_data_folder(rebuild: bool = False):
    try:
        res = index_all_data_pdfs(force_rebuild=rebuild)
        return {
            "status": "success",
            "message": f"Synced {len(res['newly_indexed'])} new document(s).",
            "details": res,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def text_query(req: QueryRequest):
    try:
        return execute_rtcfr_rag(req.query, req.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/voice-query")
async def voice_query(
    audio: UploadFile = File(...),
    language: str = Form("Tamil"),
):
    temp_path = None
    try:
        suffix = os.path.splitext(audio.filename or "voice.wav")[1] or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(audio.file, tmp)
            temp_path = tmp.name

        with open(temp_path, "rb") as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                prompt="Tamil Nadu agriculture, NABARD loan, subsidy, solar pump, drip irrigation, tractor, crop insurance, மானியம், கடன், விவசாயம்",
            )

        spoken_text = transcript.text.strip()
        if not spoken_text or len(spoken_text) < 2:
            retry_msg = (
                "குரல் தெளிவாகக் கேட்கவில்லை. மைக்கை அழுத்தி மீண்டும் பேசவும்."
                if language == "Tamil"
                else "Could not hear clearly. Please tap the microphone and speak again."
            )
            return {
                "transcribed_text": "...",
                "scheme_title": "மீண்டும் முயற்சிக்கவும் / Try Again",
                "benefit_summary": retry_msg,
                "eligibility_points": [],
                "contact_action": "",
                "sources": [],
                "audio_base64": generate_tts_base64(retry_msg, language),
            }

        rag_result = execute_rtcfr_rag(spoken_text, language)
        rag_result["transcribed_text"] = spoken_text
        return rag_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice processing error: {str(e)}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
