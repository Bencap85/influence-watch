import uuid
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from shared.db.entity import Detection, Event
from typing import List

class DetectionRepo:

    def get_detection(self, db: Session, detection_id: uuid.UUID) -> Detection | None:
        return db.query(Detection).filter(Detection.id == detection_id).first()
    
    def get_detection_for_ui(self, db: Session, detection_id: uuid.UUID):
        return (
            db.query(
                Detection,
                Event.title.label("event_name")
            )
            .filter(Detection.id == detection_id)
            .join(Event, Event.id == Detection.event_id)
            .one()
        )
    
    def get_detections_for_ui(self, db: Session):
        return (
            db.query(
                Detection,
                Event.title.label("event_name")
            )
            .join(Event, Event.id == Detection.event_id)
            .order_by(desc(Detection.timestamp_detected))
            .all()
        )
    
    from sqlalchemy.dialects.postgresql import insert

    def upsert_detections(self, db: Session, detections: List[Detection]) -> List[Detection]:
        results = []

        table = Detection.__table__

        for d in detections:
            stmt = (
                insert(Detection)
                .values(
                    event_id=d.event_id,
                    detection_type=d.detection_type,
                    country_code=d.country_code,
                    evidence=d.evidence,
                    timestamp_detected=d.timestamp_detected,
                )
                .on_conflict_do_update(
                    index_elements=["event_id", "detection_type", "country_code"],
                    set_={
                        "evidence": d.evidence,
                        "timestamp_detected": d.timestamp_detected,
                    }
                )
                .returning(table)
            )

            row = db.execute(stmt).fetchone()
            results.append(row)

        db.commit()
        return results

            

    