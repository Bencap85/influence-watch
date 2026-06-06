export interface DetectionSource {
  type: "detection";
  detection_id: string;
  event_id: string;
  detection_type: string;
  severity: string;
  confidence: number;
  timestamp_detected: string;
  evidence: object;
}