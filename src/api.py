from fastapi import APIRouter, File, UploadFile
from injection import injest_pdf
from retrieval import rag_answer


router = APIRouter(
    prefix = "/user",
    tags = "User"
)

@router.post("/upload_file")
async def upload_pdf(file: UploadFile = File(...)):
    
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload_file(file_path)

    return {
        "message": "File uploaded and processed successfully",
        "filename": file.filename
    }
    

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    answer = rag_answer(request.question)

    return {
        "question": request.question,
        "answer": answer
    }
