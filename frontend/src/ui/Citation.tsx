import React from "react";
import Tippy from "@tippyjs/react";
import "tippy.js/dist/tippy.css";
import type { SourceItem } from "../types/source/sourceItem";
import type { EventAnalyticsSource } from "../types/source/eventAnalyticsSource";
import type { ArticleSource } from "../types/source/articleSource";
import EventSourceComponent from "./EventSourceComponent";
import EventAnalyticsSourceComponent from "./EventAnalyticsSourceComponent";
import ArticleSourceComponent from "./ArticleSourceComponent";
import DetectionSourceComponent from "./DetectionSourceComponent";

interface CitationProps {
    id: string;
    source: SourceItem;
}

export function Citation({ id, source }: CitationProps) {
    return (
        <Tippy
            interactive={true}
            className="p-0 border border-white border-1-solid rounded-md"
            content={
                <div className="p-2 text-sm text-white">
                    <div className="font-mono tracking-tight font-semibold uppercase text-gray-300">
                        [{source.type}]
                    </div>

                    {(() => {
                        switch (source.type) {
                            case "event":
                                return <EventSourceComponent source={source} />;
                            case "event_analytics":
                                return <EventAnalyticsSourceComponent source={source} />;
                            case "article":
                                return <ArticleSourceComponent source={source} />;
                            case "detection":
                                return <DetectionSourceComponent source={source} />;
                            default:
                                return null;
                        }
                    })()}

                    {source.type !== "event_analytics"&& source.type !== "detection" && (
                        <div className="mt-2">
                            <a
                                href={`../${source.type === "event" ? "event/" + source.event_id : "article/" + source.article_id}`}
                                className="text-blue-200 hover:text-blue-100 underline"
                                target="_blank"
                            >
                                View {source.type} →
                            </a>
                        </div>
                    )}

                </div>
            }
            placement="top"
            arrow={true}
        >
            <span
                className="
          text-blue-200 
          font-semibold 
          cursor-pointer 
          mx-0.1
          hover:text-blue-400
        "
            >
                [{id}]
            </span>
        </Tippy>
    );

    function renderEventSource(source: EventSource) {
        return
    }

    function renderEventAnalyticsSource(source: EventAnalyticsSource) {
        return "I am an event_analytics";
    }

    function renderArticleSource(source: ArticleSource) {
        return "I am an article";
    }
}
