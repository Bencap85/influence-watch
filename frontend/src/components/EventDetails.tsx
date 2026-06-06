import { useParams } from "react-router-dom";
import { fetchEventById } from "../api/events";
import { useQuery } from "@tanstack/react-query";
import 'flag-icons/css/flag-icons.min.css';
import CountryList from "./CountryList";
import ArticlesTable from "./ArticlesTable";
import { ReportingTimeline } from "./ReportingTimeline";
import { DivergenceScoreCard } from "../ui/DivergenceScoreCard";
import { fetchArticlesByEvent } from "../api/article";
import BackButton from "../ui/BackButton";


export default function EventDetails({ }) {

    const { id } = useParams();
    const eventId = id;

    const {
        data: event,
        isLoading: eventLoading,
        error: eventError
    } = useQuery({
        queryKey: ["event", eventId],
        queryFn: () => fetchEventById(eventId),
        enabled: !!eventId
    });

    const {
        data: articles,
        isLoading: articlesLoading,
        error: articlesError
    } = useQuery({
        queryKey: ["eventArticles", eventId],
        queryFn: () => fetchArticlesByEvent(eventId),
        enabled: !!eventId
    });

    if (eventLoading || articlesLoading) return <div>Loading event…</div>;
    if (eventError || articlesError) return <div>Error loading event</div>;
    if (!event) return <div>No event found</div>

    return (
        <div className="space-y-2 text-gray-200">
            <div className="flex items-center justify-between">
                <h2 className="">
                    {event.title}
                </h2>
                <BackButton />
            </div>

            <div className="bg-tech-panel border border-tech-border rounded-lg p-6 
              shadow-[0_0_20px_rgba(0,255,255,0.05)] space-y-4">

                <div className="flex justify-between items-start">
                    <span className="text-gray-400">Countries</span>
                    <CountryList countries={event.countries} />

                </div>

                <div className="flex justify-between">
                    <span className="text-gray-400">Articles</span>
                    <span className="font-mono">{event.num_articles}</span>
                </div>

                <div className="flex justify-between">
                    <span className="text-gray-400">First Seen</span>
                    <span className="font-mono">{new Date(event.first_seen_at).toDateString()}</span>
                </div>

                <div className="flex justify-between">
                    <span className="text-gray-400">Last Seen</span>
                    <span className="font-mono">{new Date(event.last_seen_at).toDateString()}</span>
                </div>

            </div>

            <div>
                {/* <h2 className="text-stone-600 text-lg mb-2">Reporting Timeline</h2> */}
                
                <ReportingTimeline articles={articles} />
            </div>

            <div>
                <h2 className="text-stone-600 text-lg mb-2">Articles</h2>
                <ArticlesTable articles={articles} />
            </div>

        </div>

    );
}