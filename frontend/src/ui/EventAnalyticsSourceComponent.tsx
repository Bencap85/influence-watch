import CountryList from "../components/CountryList";
import type { EventAnalyticsSource } from "../types/source/eventAnalyticsSource";


interface EventAnalyticsSourceComponentProps {
    source: EventAnalyticsSource;
}

export default function EventAnalyticsSourceComponent({ source }: EventAnalyticsSourceComponentProps) {
  return (
    <div className="text-gray-100 p-0 rounded-md shadow-lg w-80 space-y-4">

      {/* Header */}
      {/* <p className="text-sm text-gray-400">Event ID: {source.event_id}</p> */}
    <h3 className="font-semibold text-sm leading-tight">
        {source.event_id}
      </h3>

      {/* Sentiment */}
      <section>
        <h4 className="text-xs uppercase tracking-wide text-gray-400 mb-1">Sentiment</h4>
        <div className="max-h-32 overflow-y-auto custom-scroll bg-gray-800 p-2 rounded space-y-2">
          {Object.entries(source.sentiment).map(([country, sentiment]) => (
            <div key={country} className="flex justify-between items-center text-sm">
              <CountryList countries={[country]} />
              <span className="font-medium">{Number(sentiment).toPrecision(2)}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Keywords */}
      <section>
        <h4 className="text-xs uppercase tracking-wide text-gray-400 mb-1">Keywords</h4>
        <div className="max-h-32 overflow-y-auto custom-scroll bg-gray-800 p-2 rounded space-y-3">
          {Object.entries(source.keywords).map(([country, keywords]) => (
            <div key={country} className="flex gap-3">
              <CountryList countries={[country]} />
              <div className="text-gray-300 text-sm leading-snug">
                {keywords.slice(0, 5).join(",|").split("|").map((kw, i) => (
                  <div key={i}>{kw}</div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
}
