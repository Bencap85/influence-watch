import CountryList from "../components/CountryList";
import type { ArticleSource } from "../types/source/articleSource";


interface ArticleSourceComponentProps {
    source: ArticleSource;
}

export default function ArticleSourceComponent({ source }: ArticleSourceComponentProps) {
  return (
    <div className="text-gray-100 p-0 rounded-md w-80 space-y-3">

      {/* Title */}
      <h3 className="font-semibold text-sm leading-tight">
        {source.title}
      </h3>

      {/* Metadata */}
      <div className="text-sm text-gray-400 border-t border-gray-700 pt-2">
        <div className="flex justify-between text-white text-sm">
          <CountryList countries={[source.country]} />
        </div>
      </div>

      {/* Description */}
      <div>
        <p className="text-xs uppercase tracking-wide text-gray-400 mb-1">Description</p>
        <div className="max-h-32 overflow-y-auto custom-scroll bg-gray-800 p-2 rounded">
          <p className="text-xs leading-snug">{source.clean_description_text || "Not found"}</p>
        </div>
      </div>

      {/* Content */}
      {/* <div>
        <p className="text-xs uppercase tracking-wide text-gray-400 mb-1">Content</p>
        <div className="max-h-32 overflow-y-auto custom-scroll bg-gray-800 p-2 rounded">
          <p className="text-sm leading-snug">{source.clean_body_text || "Not found"}</p>
        </div>
      </div> */}

    </div>
  );
}
