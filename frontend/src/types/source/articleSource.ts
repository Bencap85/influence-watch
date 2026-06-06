export interface ArticleSource {
  type: "article";
  article_id: string;
  title: string;
  summary: string | null;
  clean_description_text: string;
  clean_body_text: string;
  sentiment: number;
  country: string;
  keywords: string[];
  link: string;
}