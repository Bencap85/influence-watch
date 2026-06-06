import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchEvents } from "../api/events";
import type { Event } from "../types/event";
import CountryList from "./CountryList";
import { Table } from "../ui/Table";
import { DivergenceScoreCard } from "../ui/DivergenceScoreCard";
import { useSearch } from "../context/SearchContext";

export default function EventTable() {

    const navigate = useNavigate();
    const { query, setQuery } = useSearch();

    function handleRowClick(eventData: Event) {
        navigate(`/event/${eventData.id}`)
    }

    const { data, isLoading, error } = useQuery<Event[]>({
        queryKey: ["events"],
        queryFn: fetchEvents
    });

    if (isLoading) return <div className="text-stone-500">Loading events…</div>;
    if (error) return <div className="text-red-500">Error loading events</div>;
    if (!data) return <div>No events found</div>;

    const filtered = data.filter((event: Event) =>
        // event.title.toLowerCase().includes(query.toLowerCase()) ||
        // event.countries.includes(query.toUpperCase())
        true
    );

    return (
        <Table<Event>
            data={filtered}
            rowKey={(e) => e.id}
            columns={[
                {
                    key: "title",
                    label: "Event",
                    render: (e) => (
                        e.title
                    )
                },
                {
                    key: "countries",
                    label: "Countries Reporting",
                    render: (e) => (
                        <div className="flex">
                            <CountryList countries={e.countries} />
                        </div>
                    )
                },
                {
                    key: "num_articles",
                    label: "Articles",
                    render: (e) => e.num_articles ?? "—"
                },
                {
                    key: "last_seen_at",
                    label: "Last Seen",
                    render: (e) =>
                        e.last_seen_at
                            ? new Date(e.last_seen_at).toDateString()
                            : "—"
                }
            ]
            }
            onRowClick={(e) => handleRowClick(e)}
        />
    );
}
