export interface Detection {
  id: string;                     // UUID → string
  event_id: string;               // UUID → string

  country_code: string;
  detection_type: string;

  timestamp_detected: string;     // ISO datetime string

  evidence: Record<string, any>;  // Python Dict → TS object

  event_name: string | null;
}
