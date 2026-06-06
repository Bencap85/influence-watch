from typing import List
import uuid

from fastapi import APIRouter, HTTPException
from shared.db.session import SessionLocal
from shared.repository import DetectionRepo
from .schemas import DetectionResponse

router = APIRouter(prefix="/detections", tags=["detections"])
detection_repo =  DetectionRepo()

@router.get("/{detection_id}", response_model=DetectionResponse)
def get_detection(detection_id: str):
    with SessionLocal() as db:
        row = detection_repo.get_detection_for_ui(db, uuid.UUID(detection_id))

        if not row:
            raise HTTPException(status_code=404, detail="detection not found")

        detection, event_name = row

        detection_response = DetectionResponse(
            id=detection.id,
            event_id=detection.event_id,
            event_name=event_name,
            country_code=detection.country_code,
            detection_type=detection.detection_type,
            timestamp_detected=detection.timestamp_detected,
            evidence=detection.evidence,
        )

        return detection_response
    
@router.get("/", response_model=List[DetectionResponse])
def get_all_detections():
    with SessionLocal() as db:
        rows = detection_repo.get_detections_for_ui(db)

        detections = []
        for detection, event_name in rows:
            detections.append(
                DetectionResponse(
                    id=detection.id,
                    event_id=detection.event_id,
                    event_name=event_name,
                    country_code=detection.country_code,
                    detection_type=detection.detection_type,
                    timestamp_detected=detection.timestamp_detected,
                    evidence=detection.evidence,
                )
            )

        return detections
