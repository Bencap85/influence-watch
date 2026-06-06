import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchArticles } from "../api/article";
import type { Article } from "../types/article";
import { Table } from "../ui/Table";
import CountryList from "./CountryList";
import { useSearch } from "../context/SearchContext";

interface ArticleTableProps {
   articles: Article[] | null
}

export default function ArticleTable({ articles }: ArticleTableProps) {

    const navigate = useNavigate();
    const { query, setQuery } = useSearch();

    function handleRowClick(article: Article) {
        navigate(`/article/${article.article_id}`);
    }

    if (!articles) {
      const { data, isLoading, error } = useQuery<Article[]>({
          queryKey: ["articles"],
          queryFn: fetchArticles
      });
      if (isLoading) return <div className="text-stone-500">Loading articles…</div>;
      if (error) return <div className="text-red-500">Error loading articles</div>;
      if (!data) return <div>No articles found</div>;

      articles = data;

    }

    
    const filtered = articles.filter((a) =>
        a.title.toLowerCase().includes(query.toLowerCase())
        || (a.clean_description_text?? "").toLowerCase().includes(query.toLowerCase())
    );

    return (
        <Table<Article>
            data={filtered}
            rowKey={(a) => a.article_id}
            columns={[
                {
                    key: "title",
                    label: "Title",
                    render: (a) => (
                      a.title
                    )
                },
                {
                    key: "country",
                    label: "Country",
                    render: (a) => (
                        <div className="flex">
                          <CountryList countries={[a.country]} />
                        </div>
                    )
                },
                {
                    key: "published_at",
                    label: "Published",
                    render: (a) =>
                        new Date(a.published_at).toLocaleString()
                },
                {
                    key: "sentiment_score",
                    label: "Sentiment",
                    render: (a) =>
                        a.sentiment_score !== null
                            ? `${(a.sentiment_score * 100).toFixed(0)}%`
                            : "—"
                },
                {
                    key: "keyword_list",
                    label: "Keywords",
                    render: (a) =>
                        a.keyword_list?.slice(0, 3).join(", ") ?? "—"
                },
            ]}
            onRowClick={(a) => handleRowClick(a)}
        />
    );
}
