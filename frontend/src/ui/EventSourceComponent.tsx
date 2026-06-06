import type { EventSource } from "../types/source/eventSource";

interface EventSourceComponentProps {
    source: EventSource;
}

export default function EventSourceComponent({ source }: EventSourceComponentProps) {
  return (
    <div className="text-gray-100 p-0 rounded-md w-80 space-y-3">

      {/* Title */}
      <h3 className="font-semibold text-sm leading-tight">
        {source.title}
      </h3>

    </div>
  );
}