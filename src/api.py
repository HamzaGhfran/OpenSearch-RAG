from fastapi import APIRouter, File, UploadFile
from injection import injest_pdf
from retrieval import rag_answer


router = APIRouter(
    prefix = "/user",
    tags = "User"
)

@router.post("/upload_file")
@app.post("/upload-pdf")
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
    

@router.post("/retrive")
def retriver(query:str):
    pass