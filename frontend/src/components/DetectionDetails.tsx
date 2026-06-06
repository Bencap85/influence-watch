import React, { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { fetchDetectionById } from "../api/detection";
import { useNavigate, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import type { Detection } from "../types/detection";
import type { SourceItem } from "../types/source/sourceItem";
import CountryList from "./CountryList";
import BackButton from "../ui/BackButton";
import { countryCodeToName } from "../constants/countryCodeToName";
import { BriefRenderer } from "./BriefRenderer";
import type { BriefResponse } from "../types/brief/briefResponse";


export default function DetectionDetails({ }) {

    const navigate = useNavigate();
    const { id } = useParams();
    const detectionId = id;

    const {
        data: detection,
        isLoading,
        error
    } = useQuery<Detection>({
        queryKey: ["detection", detectionId],
        queryFn: () => fetchDetectionById(detectionId),
        enabled: !!detectionId
    });

    const [briefResponse, setBriefResponse] = useState<BriefResponse>({ brief: null, sources: {} });

    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

    useEffect(() => {
        if (detection) {
            fetch(`${API_BASE_URL}/agent/brief/${detection.id}`).then(res => res.json()).then(data => {
                setBriefResponse(data.brief);
            });
        }
    }, [detection]);

    if (isLoading) return <div>Loading detection…</div>;
    if (error) return <div>Error loading detection</div>;
    if (!detection) return <div>No detection found</div>;

    const {
        event_id,
        country_code,
        detection_type,
        timestamp_detected,
        evidence
    } = detection;

    return (
        <div className="space-y-6 text-gray-200">

            <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold tracking-wide">
                    Detection Details
                </h2>
                <BackButton />
            </div>

            <div className="
        bg-tech-panel border border-tech-border rounded-lg p-6 
        shadow-[0_0_20px_rgba(0,255,255,0.05)] space-y-4
      ">
                <div className="flex justify-between items-start">
                    <div className="">
                        <h2 className="text-lg font-semibold tracking-wide">
                            {detection_type.replace(/_/g, " ").toUpperCase()} - {countryCodeToName[detection.country_code]?.toUpperCase() || detection.evidence.country_pair?.join(",")} - {detection.event_name?.toUpperCase()}
                        </h2>
                        <p className="text-gray-400 text-sm font-mono">
                            Detection ID: {id}
                        </p>
                    </div>

                </div>

                <div className="flex justify-between">
                    <span className="text-gray-400">Event</span>
                    {/* <span className="font-mono"> */}
                    <a className="font-mono underline text-blue-200 hover:text-blue-400" href={`../event/${detection.event_id}`} target="_blank">{detection.event_name}</a>
                    {/*</span>*/}
                </div>

                <div className="flex justify-between">
                    <span className="text-gray-400">Detection Type</span>
                    <span className="font-mono">
                        {detection.detection_type}
                    </span>
                </div>

                <div className="flex justify-between">
                    <span className="text-gray-400">Country</span>
                    <span className="font-mono">
                        {detection.country_code !== "UNK" ?
                            <div className="flex">
                                <CountryList countries={[detection.country_code]} />
                            </div>
                            : <div className="flex gap-2">
                                <CountryList countries={[detection.evidence.country_pair[0]]} />
                                <CountryList countries={[detection.evidence.country_pair[1]]} />
                            </div>
                        }
                    </span>
                </div>

                <div className="flex justify-between">
                    <span className="text-gray-400">Detected At</span>
                    <span className="font-mono">
                        {new Date(timestamp_detected).toLocaleString()}
                    </span>
                </div>
            </div>

            <div className="
        bg-tech-panel border border-tech-border rounded-lg p-6 
        shadow-[0_0_25px_rgba(0,255,255,0.08)] space-y-4
      ">
                <h3 className="">AI Analyst Brief</h3>

                {briefResponse.brief && briefResponse.brief !== "" ? <BriefRenderer
                    briefResponse={briefResponse}
                /> : <div className="flex space-x-1 justify-start items-center">
                    <div className="w-2 h-2 bg-stone-400 rounded-full animate-pulse"></div>
                    <div className="w-2 h-2 bg-stone-400 rounded-full animate-pulse [animation-delay:0.2s]"></div>
                    <div className="w-2 h-2 bg-stone-400 rounded-full animate-pulse [animation-delay:0.4s]"></div>
                </div>

                }

            </div>

            {/* EVIDENCE PANEL */}
            <div className="
        bg-tech-panel border border-tech-border rounded-lg p-6 
        shadow-[inset_0_0_20px_rgba(0,255,255,0.03)] space-y-4
      ">
                <h3 className="">Evidence</h3>

                <div className="grid grid-cols-2 gap-4">
                    {Object.entries(evidence).map(([key, value]) => (
                        <div
                            key={key}
                            className="
                bg-black/20 p-4 rounded 
                border border-gray-700
                space-y-1
              "
                        >
                            <p className="text-gray-400 text-sm font-mono">{key}</p>
                            <p className="text-gray-200 font-semibold">
                                {typeof value === "number" ? value.toLocaleString() : String(value)}
                            </p>
                        </div>
                    ))}
                </div>
            </div>

        </div>
    );
}
