import CountryList from "../components/CountryList";
import type { DetectionSource } from "../types/source/detectionSource";


interface DetectionSourceComponentProps {
    source: DetectionSource;
}

export default function DetectionSourceComponent({ source }: DetectionSourceComponentProps) {
    return (
        <div className="text-gray-100 p-0 rounded-md w-80 space-y-4">

            {/* <div className="bg-black/20 p-1 rounded border border-gray-700 mt-2 mb-2">
                <div className="flex justify-between">
                    <p className="text-sm text-gray-400">Detection ID</p>
                    <span className="text-sm text-white">{source.detection_id}</span>
                </div>
                <div className="flex justify-between">
                    <p className="text-sm text-gray-400">Detected At</p>
                    <span className="text-sm text-white">{new Date(source.timestamp_detected).toLocaleString()}</span>
                </div>
            </div> */}

            {/* Title */}
      <h3 className="font-semibold text-sm leading-tight">
        {source.detection_id}
      </h3>

            {/* Evidence */}
            <section>
                <h4 className="text-xs uppercase tracking-wide text-gray-400 mb-1">Evidence</h4>
                <div className="">

                    <div className="grid grid-cols-2 gap-1">
                        {Object.entries(source.evidence).map(([key, value]) => (
                            <div
                                key={key}
                                className="
                bg-black/20 p-1 rounded 
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
            </section>

        </div>
    );
}
