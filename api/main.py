from fastapi import FastAPI, Request, HTTPException
from src.utility import get_requested_files, post_processing
from src.processor import process_pdfs, flatten_didi_data

app = FastAPI()

@app.post("/upload-pdf")
async def upload_pdf(request: Request):
    success, message, files = await get_requested_files(request)
    if not success:
        return {"message": message, "status": "failed", "status_code": 400, "data": None}
    try:
        structured_data = process_pdfs(files)
        
        # structured_data = post_processing(structured_data)

        #return {"message": "File uploaded and processed successfully", "status": "success", "status_code": 200, "data": structured_data}

        # Example usage
        csv_file_path = "/Users/ashwin.2k3/Downloads/Uber_summary.csv"
        flatten_didi_data(structured_data, csv_file_path)

        return structured_data
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": str(e), "status": "failed", "status_code": 500, "data": None})
