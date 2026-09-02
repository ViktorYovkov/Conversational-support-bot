import os
import chromadb

FAQ_FILE_PATH = os.path.join("data", "FAQ.txt")
CHROMA_DB_DIR = "chroma_db"

def init_vector_db():
    print("Инициализираме базата данни...")

    client = chromadb.PersistentClient(path = CHROMA_DB_DIR)

    try:
        client.delete_collection(name = "faq_collection")
    except Exception:
        pass

    collection = client.create_collection(name = "faq_collection")

    if not os.path.exists(FAQ_FILE_PATH):
        print(f"Файлът {FAQ_FILE_PATH} не съществува, създавй го в папка 'data'.")
        return
    
    with open(FAQ_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]

    if not chunks:
        print(f"Файлът {FAQ_FILE_PATH} е празен. Моля, добавете съдържание.")
        return
    
    documents = chunks
    ids = [f"FAQ_doc_{i}" for i in range(len(chunks))]
    metadatas = [{"source": "FAQ.txt"} for _ in range(len(chunks))]

    collection.add(
        documents = documents,
        ids = ids, 
        metadatas = metadatas
    )
    print(f"Базата е създадена успешно с {len(chunks)} документа от {FAQ_FILE_PATH}.")


def search_faq(query: str, n_results: int = 2):
    client = chromadb.PersistentClient(path = CHROMA_DB_DIR)
    try:
        collection = client.get_collection(name = "faq_collection")
    except Exception:
        return ""
    
    # Търсим най-близките резултати:
    results = collection.query(
        query_texts = [query],
        n_results = n_results
    )
    
    # Merge-ва резултатите в цял текст:
    if results and results['documents'] and results['documents'][0]:
        found_documents = results['documents'][0]
        return "\n\n".join(found_documents)
    return ""
    
if __name__ == "__main__":
    init_vector_db()