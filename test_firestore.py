from app.infrastructure.firestore.client import FirestoreClient

db = FirestoreClient.get_client()

doc_ref = db.collection("documents").document("test")

doc_ref.set({
    "filename": "rag.pdf",
    "chunkCount": 35,
    "status": "INDEXED",
})

print("Document written successfully.")