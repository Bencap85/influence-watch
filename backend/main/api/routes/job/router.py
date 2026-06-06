import threading
import main.ingestion.main
import main.processing.main
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/job", tags=["job"])

@router.get("/ingestion")
def run_ingestion():
    try:
        thread = threading.Thread(target=main.ingestion.main.main, daemon=True)
        thread.start()

        return { "status": "accepted" }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/process")
def run_ingestion():
    try:
        thread = threading.Thread(target=main.processing.main.main, daemon=True)
        thread.start()

        return { "status": "accepted" }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))