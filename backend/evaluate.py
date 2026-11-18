import time
from backend.main import load_vectorstore, index_all_data_pdfs

TEST_DATASET = [
    {
        "query": "What are the NABARD unit costs and subsidies for 5 HP solar pumps?",
        "expected_keywords": ["solar", "5 hp", "subsidy", "unit cost"]
    },
    {
        "query": "What is the loan amount for dairy farming?",
        "expected_keywords": ["dairy", "cow", "loan", "nabard"]
    },
    {
        "query": "What is the subsidy percentage for drip irrigation?",
        "expected_keywords": ["drip", "irrigation", "subsidy", "percent"]
    },
    {
        "query": "How to apply for crop insurance under PMFBY?",
        "expected_keywords": ["crop insurance", "pmfby", "apply"]
    },
    {
        "query": "What are the conditions for goat rearing loans?",
        "expected_keywords": ["goat", "rearing", "loan", "unit"]
    },
    {
        "query": "What financial assistance is available for farm machinery?",
        "expected_keywords": ["machinery", "tractor", "subsidy"]
    },
    {
        "query": "Who is the contact officer for agricultural subsidies?",
        "expected_keywords": ["assistant agricultural officer", "officer"]
    },
    {
        "query": "Are there special subsidies for sprinkler irrigation?",
        "expected_keywords": ["sprinkler", "irrigation"]
    },
    {
        "query": "What is the total project cost for a poultry farm unit?",
        "expected_keywords": ["poultry", "unit cost", "farm"]
    },
    {
        "query": "Where can farmers check scheme status online?",
        "expected_keywords": ["portal", "tnagrisnet", "app"]
    }
]

def run_evaluation():
    print("Initializing RAG Evaluation...")
    vectorstore = load_vectorstore()
    if vectorstore is None:
        index_all_data_pdfs(force_rebuild=False)
        vectorstore = load_vectorstore()
        
    if vectorstore is None:
        print("Error: No PDFs indexed in FAISS. Please index documents first.")
        return

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    total_queries = len(TEST_DATASET)
    hits = 0
    total_recall_score = 0.0
    latencies = []

    for idx, item in enumerate(TEST_DATASET, 1):
        query = item["query"]
        keywords = item["expected_keywords"]

        start_time = time.time()
        docs = retriever.invoke(query)
        elapsed_ms = (time.time() - start_time) * 1000
        latencies.append(elapsed_ms)

        retrieved_text = " ".join([d.page_content.lower() for d in docs])

        matched_keywords = [kw for kw in keywords if kw.lower() in retrieved_text]
        keyword_recall = len(matched_keywords) / len(keywords)
        total_recall_score += keyword_recall

        is_hit = 1 if len(matched_keywords) > 0 else 0
        hits += is_hit

        print(f"[{idx}/{total_queries}] Query: {query}")
        print(f"   -> Latency: {elapsed_ms:.2f} ms | Recall: {keyword_recall:.2f} | Hit: {is_hit}")

    hit_rate = (hits / total_queries) * 100
    avg_recall = total_recall_score / total_queries
    avg_latency = sum(latencies) / total_queries

    print("\n" + "="*40)
    print("📊 RAG EVALUATION RESULTS")
    print("="*40)
    print(f"• Total Questions Tested : {total_queries}")
    print(f"• Retrieval Hit Rate     : {hit_rate:.1f}% ({hits}/{total_queries})")
    print(f"• Average Keyword Recall : {avg_recall:.2f}")
    print(f"• Average Latency        : {avg_latency:.2f} ms")
    print("="*40)

if __name__ == "__main__":
    run_evaluation()
