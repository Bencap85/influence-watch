export interface EventAnalyticsSource {
  type: "event_analytics";
  event_id: string;
  sentiment: Record<string, number>;
  keywords: Record<string, string[]>;
  link: string;
}