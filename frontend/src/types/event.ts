
export interface Event {
    id: string;                     // UUID → string
    title: string | null;
    event_summary: string | null;

    global_keywords: string[] | null;
    global_entities: Record<string, any>[] | null; // EntityItem root model
    global_sentiment: number | null;

    countries: string[] | null;
    num_articles: number;

    first_seen_at: string;          // ISO datetime string
    last_seen_at: string;           // ISO datetime string
}
