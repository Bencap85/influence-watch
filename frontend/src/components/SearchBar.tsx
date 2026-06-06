import { useSearch } from "../context/SearchContext";

interface SearchBarProps {
  placeholder: string;
}

export default function SearchBar({ placeholder }: SearchBarProps) {
  const { query, setQuery } = useSearch();

  return (
    <div className="relative w-52">
      <input
        type="text"
        placeholder={placeholder}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="
          w-full px-4 py-2 pr-8 text-sm
          rounded-md
          bg-gray-900/60 border border-gray-700
          text-gray-200 placeholder-gray-500
          focus:outline-none focus:ring-2 focus:ring-blue-500/40
          transition
        "
      />

      {query && (
        <button
          onClick={() => setQuery("")}
          className="
            absolute right-2 top-1/2 -translate-y-1/2
            text-gray-400
            hover:text-blue-400
            w-5 h-5 flex items-center justify-center
            rounded
            transition
          "
        >
          ×
        </button>
      )}
    </div>
  );
}
