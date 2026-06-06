

export interface Article {
    article_id: string;                     // UUID → string
    title: string;
    clean_body_text: string | null;
    clean_description_text: string | null;
    summary: string | null;
    source_name: string;

    sentiment_score: number | null;
    keyword_list: string[] | null;
    entity_list: Record<string, any>[] | null; // RootModel[List[str]] → array of dicts or arrays

    country: string | null;

    published_at: string;                   // ISO datetime string
    processed_at: string | null;            // ISO datetime string

    is_state_affiliated: boolean;
}
