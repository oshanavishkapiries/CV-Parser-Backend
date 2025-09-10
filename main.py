from fastapi import FastAPI, UploadFile, File
import pdfplumber
from io import BytesIO

app = FastAPI()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Not a PDF file"}

    contents = await file.read()
    pdf_file = BytesIO(contents)  # ✅ wrap bytes in BytesIO
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return {"text": text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
