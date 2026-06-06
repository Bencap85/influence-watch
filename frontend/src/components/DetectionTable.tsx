import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchDetections } from "../api/detection";
import type { Detection } from "../types/detection";
import { Table } from "../ui/Table";
import CountryList from "./CountryList";
import { useSearch } from "../context/SearchContext";


export default function DetectionTable() {

    const navigate = useNavigate();
    const { query, setQuery } = useSearch();

    function handleRowClick(det: Detection) {
        navigate(`/detection/${det.id}`);
    }

    const { data, isLoading, error } = useQuery<Detection[]>({
        queryKey: ["detections"],
        queryFn: fetchDetections
    });

    if (isLoading) return <div className="text-stone-500">Loading detections…</div>;
    if (error) return <div className="text-red-500">Error loading detections</div>;
    if (!data) return <div>No detections found</div>;

    const filtered = data.filter((d) =>
        d.detection_type.toLowerCase().includes(query.toLowerCase())
        || d.country_code.toLowerCase().includes(query.toLowerCase())
        || (d.event_name && d.event_name.toLowerCase().includes(query.toLowerCase()))
    );

    return (
        <Table<Detection>
            data={filtered}
            rowKey={(d) => d.id}
            columns={[
                {
                    key: "detection_type",
                    label: "Detection Type",
                    render: (d) => (
                        <p className="font-mono">{d.detection_type.split("_").join(" ")}</p>
                    )
                },
                {
                    key: "country_code",
                    label: "Country",
                    render: (d) => (
                        d.country_code !== "UNK" ?
                        <div className="flex">
                            <CountryList countries={[d.country_code]} />
                        </div>
                        : <div className="flex gap-2">
                            <CountryList countries={[d.evidence.country_pair[0]]} />
                            <CountryList countries={[d.evidence.country_pair[1]]} />
                        </div>
                    )
                },
                {
                    key: "event_name",
                    label: "Event",
                    render: (d) => (
                        d.event_name
                    )
                },
                {
                    key: "timestamp_detected",
                    label: "Detected At",
                    render: (d) =>
                        new Date(d.timestamp_detected).toLocaleString()
                },
            ]}
            onRowClick={(d) => handleRowClick(d)}
        />
    );
}
