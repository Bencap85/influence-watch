from shared.db.connect import SessionLocal
from shared.db.entity import Detection

def get_detection(detection_id: str) -> dict:
    with SessionLocal() as db:
        det = db.query(Detection).filter(Detection.id == detection_id).first()

        if not det:
            return {"error": "not_found"}

        return {
            "detection_id": det.id,
            "event_id": det.event_id,
            "country_code": det.country_code,
            "detection_type": det.detection_type,
            "timestamp_detected": det.timestamp_detected.isoformat(),
            "evidence": det.evidence,
        }
