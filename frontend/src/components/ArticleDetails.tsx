import { useNavigate, useParams } from "react-router-dom";
import { fetchEventById } from "../api/events";
import type { Event } from "../types/event";
import { useQuery } from "@tanstack/react-query";
import type { Article } from "../types/article";
import 'flag-icons/css/flag-icons.min.css';
import { countryCodeToFlagCode } from "../constants/countryCodeToFlag";
import CountryList from "./CountryList";
import ArticlesTable from "./ArticlesTable";
import NarrativesTable from "./NarrativesTable";
import { ReportingTimeline } from "./ReportingTimeline";
import { DivergenceScoreCard } from "../ui/DivergenceScoreCard";
import { fetchArticleById, fetchArticlesByEvent } from "../api/article";
import BackButton from "../ui/BackButton";


export default function ArticleDetailsPage({ }) {
    const navigate = useNavigate();

    const { id } = useParams();
    const articleId = id;

    const {
        data: article,
        isLoading: articleLoading,
        error: articleError
    } = useQuery<Article>({
        queryKey: ["article", articleId],
        queryFn: () => fetchArticleById(articleId),
        enabled: !!articleId
    });

    if (articleLoading) return <div>Loading article…</div>;
    if (articleError) return <div>Error loading article</div>;
    if (!article) return <div>No article found</div>

    return (
        <div className="space-y-2 text-gray-200">
            <div className="flex items-center justify-between">
                <h2 className="">
                    {article.title}
                </h2>
                <BackButton />
            </div>

            <div className="bg-tech-panel border border-tech-border rounded-lg p-6 
              shadow-[0_0_20px_rgba(0,255,255,0.05)] space-y-4">

                <div className="flex justify-between">
                    <span className="text-gray-400">Title</span>
                    <span className="font-mono">{article.title}</span>
                </div>

                <div className="flex justify-between">
                    <span className="text-gray-400">Article ID</span>
                    <span className="font-mono">{article.article_id}</span>
                </div>

                <div className="flex justify-between items-start">
                    <span className="text-gray-400">Country</span>
                    <CountryList countries={[article.country]} />
                </div>

                <div className="flex justify-between">
                    <span className="text-gray-400">Source</span>
                    <span className="font-mono">{article.source_name || "-"}</span>
                </div>

                <div className="flex justify-between">
                    <span className="text-gray-400">State Affiliated</span>
                    <span className="font-mono">{article.is_state_affiliated ? "True" : "False"}</span>
                </div>

                <div className="flex justify-between">
                    <span className="text-gray-400">Published At</span>
                    <span className="font-mono">{new Date(article.published_at).toDateString()}</span>
                </div>

            </div>

            <div className="flex gap-6">

                <div className="flex-1">
                    <div className="bg-tech-panel border border-tech-border rounded-lg px-6 py-6
                    shadow-[0_0_20px_rgba(0,255,255,0.05)] space-y-4">
                        
                        <h3>Description</h3>
                        <div className="flex justify-between">
                            <span className="font-mono text-sm" style={{ textIndent: "2rem" }}>{article.clean_description_text || "-"}</span>
                        </div>
                    </div>
                </div>

                <div className="flex-1">
                    <div className="bg-tech-panel border border-tech-border rounded-lg p-6 
                    shadow-[0_0_20px_rgba(0,255,255,0.05)] space-y-4">
                        <h3>Body</h3>
                        <div className="flex justify-between">
                            <span className="font-mono text-sm" style={{ textIndent: "2rem" }}>{article.clean_body_text || "-"}</span>
                        </div>
                    </div>
                </div>

            </div>

        </div>


    );
}